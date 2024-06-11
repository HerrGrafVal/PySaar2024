from functools import cache
from mpmath import mp, exp, log, findroot
from scipy.integrate import solve_ivp
from read_dataframe import fill_values
from symbols import h, q_e, k, m_e, eps, W_g, N_v, N_c, m_ec, m_hc, T, U_D, N_d, N_a, x_p0, x_n0

# ----------------------------------------------------------------------------

def Fermi_Dirac_Distribution(W, W_F):
    """
    Returns the probability P to find an electron at energy level W if W_F is the Fermi level
    Note that 1 - P is the probability not to find and electron = to find a hole at W

    Parameters
    : **W** *(mpf)* Energy level of electron
    : **W_F** *(mpf)* Fermi level
    """

    P = 1 / (1 + exp((W - W_F) / kT))
    return P


@cache
def Fermi(W_F, N_a=0, N_d=0):
    """
    Charge neutrality in thermodynamic equilibrium requires pos = neg, see page 114
    By calculating pos and neg for a given W_F this function checks if above requirement is satisfied.
    Returns pos - neg (Usually around +- e 24) Therefore findroot later has a tolerance of only 0.1
    If pos - neg == 0 then W_F is the Fermi level

    Parameters
    : **W_F** *(mpf)* Energy level to check
    : **N_a** *(float)* level of p-dotation
    : **N_d** *(float)* level of n-dotation
    """

    pos = N_c * Fermi_Dirac_Distribution(W_c, W_F) + N_a * Fermi_Dirac_Distribution(W_a, W_F)
    neg = N_v * (1 - Fermi_Dirac_Distribution(W_v, W_F)) + N_d * (1 - Fermi_Dirac_Distribution(W_d, W_F))
    return pos - neg


def Fermi_p(W_F):
    """
    Calls Fermi() for W_F and dotation matching the p-region of the diode.
    Passes along return value of Fermi()

    Parameters:
    **W_F** *(mpf)* Energy level to check
    """

    return(Fermi(W_F, N_a=N_a))


def Fermi_n(W_F):
    """
    Calls Fermi() for W_F and dotation matching the n-region of the diode.
    Passes along return value of Fermi()

    Parameters:
    **W_F** *(mpf)* Energy level to check
    """

    return(Fermi(W_F, N_d=N_d))


def approximate_Fermi_level():
    """
    Returns approximated Fermi level height over the valence band (divided by 1 electron volt)
    In thermodynamic equilibrium the Fermi level is constant over space.
    The Fermi level for the n-dotated and p-dotated must therefore equal one another.
    To validate results we approximate both areas seperately, compare them and take the average.

    mpmath dps must be set high enough before a call to this function!
    Tested only with mp.dps >= 22
    """

    # Find starting point for p-region
    i = 1
    for h in range(15):
        step = 10 ** -h
        while Fermi_p(W_A * i) <= 0:
            i += step
        i -= step
    W_start = W_A * i

    # Improve approximation numerically
    W_F1 = findroot(Fermi_p, W_start, tol=0.1)

    # Find starting point for n-region
    i = 1
    for h in range(15):
        step = 10 ** -h
        while Fermi_n(W_A * i) <= 0:
            i += step
        i -= step
    W_start = W_A * i

    # Improve approximation numerically
    W_F2 = findroot(Fermi_n, W_start, tol=0.1)

    # Adjust for lower valence band in n-region
    W_F2 -= U_D

    # Validate results
    if abs(W_F1 - W_F2) > 0.05:
        raise ValueError("Calculated Fermi levels for left and right diode half don't match! Check input parameters and try again.")

    # Average results
    W_F = (W_F1 + W_F2) / 2

    return(W_F)

# ----------------------------------------------------------------------------

"""
Prepare variables of type float/mpf
"""

h = fill_values(h).evalf()
e = fill_values(q_e).evalf()
k = fill_values(k).evalf() / e
m_e = fill_values(m_e).evalf()
eps = fill_values(eps).evalf()
W_g = fill_values(W_g, eV=True).evalf()
N_v = fill_values(N_v).evalf()
N_c = fill_values(N_c).evalf()
m_ec = fill_values(m_ec).evalf()
m_hc = fill_values(m_hc).evalf()
T = fill_values(T).evalf()
U_D = fill_values(U_D).evalf()
N_d = fill_values(N_d).evalf()
N_a = fill_values(N_a).evalf()
N_dp = N_d
N_am = N_a
kT = k * T
x_start = fill_values(x_p0).evalf()
x_finish = fill_values(x_n0).evalf()

# ----------------------------------------------------------------------------

"""
Define band structure
"""

W_v = 0
W_c = W_g

# page 106 - 107, W in electron volts
W_ion_D = ((m_ec * m_e) * (e ** 3)) / (8 * ((eps * h) ** 2))
W_ion_A = ((m_hc * m_e) * (e ** 3)) / (8 * ((eps * h) ** 2))
W_D = W_c - W_ion_D
W_A = W_v + W_ion_A
W_d = W_D - kT * log(2)
W_a = W_A + kT * log(2)

# Allow for higher numeric precision
mp.dps = 22
W_F = approximate_Fermi_level()

print(W_F)

# ----------------------------------------------------------------------------

"""
Setup for ode solver

     z0 = phi
z  = z1 = E
     
rho = DDM(z0)[4]

dz     z0. = -z1
dx = z1. = 1/eps * rho
"""

z0 = [0, 0]

@cache
def DDM(phi, N_am=0, N_dp=0):
    W_v = -e * phi
    W_c = W_v + W_g
    p = N_v * exp(- (W_F - W_v) / (kT))
    n = N_c * exp(- (W_c - W_F) / (kT))
    rho = e * (p + N_dp - n - N_am)
    out = [W_v, W_c, p, n, rho]
    return out

@cache
def DDM_p(phi):
    return DDM(phi, N_am=N_am)

@cache
def DDM_n(phi):
    return DDM(phi, N_dp=N_dp)

def fun_p(x, z):
    rho = DDM_p(z[0])[4]
    dzdx = [-z[1], 1 / eps * rho]
    return dzdx

def fun_n(x, z):
    rho = DDM_n(z[0])[4]
    dzdx = [-z[1], 1 / eps * rho]
    return dzdx

# ToDo solve ivp
