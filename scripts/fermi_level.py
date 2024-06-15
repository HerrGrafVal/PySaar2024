from functools import cache
from cache import pickle_save
from read_dataframe import fill_values
from mpmath import mp, exp, log, findroot, mpf
from symbols import h, q_e, k, m_e, eps, W_g, N_v, N_c, m_ec, m_hc, T, U_D, N_d, N_a, x_p0, x_n0

# ----------------------------------------------------------------------------

# Whether or not to hide script Feedback
HIDE_LOG = False

# ----------------------------------------------------------------------------

def Fermi_Dirac_Distribution(W, W_F):
    """
    | Returns the probability P to find an electron at energy level W if W_F is the Fermi level
    | Note that 1 - P is the probability not to find and electron = to find a hole at W
    | See page 90ff, 108ff

    :param W: Energy level of electron
    :type W: mpmath.mpf
    :param W_F: Fermi level
    :type W_F: mpmath.mpf
    :return: Probability
    :rtype: mpmath.mpf
    """

    P = 1 / (1 + exp((W - W_F) / kT))
    return P


@cache
def Fermi(W_F, N_a=0, N_d=0):
    """
    | Charge neutrality in thermodynamic equilibrium requires pos = neg, see page 114
    | By calculating pos and neg for a given W_F this function checks if above requirement is satisfied.
    | If pos - neg == 0 then W_F is the Fermi level
    | Returns pos - neg (Usually around +- e 24)

    | This function uses ``@functools.cache`` decorator

    :param W_F: Energy level to check
    :type W_F: mpmath.mpf
    :param N_a: Level of p-dotation
    :type N_a: float
    :param N_d: Level of n-dotation
    :type N_d: float
    :return: Deviation from equilibrium
    :rtype: mpmath.mpf
    """

    pos = N_c * Fermi_Dirac_Distribution(W_c, W_F) + N_a * Fermi_Dirac_Distribution(W_a, W_F)
    neg = N_v * (1 - Fermi_Dirac_Distribution(W_v, W_F)) + N_d * (1 - Fermi_Dirac_Distribution(W_d, W_F))
    return pos - neg

@cache
def Fermi_p(W_F):
    """
    | Calls ``fermi_level.Fermi(W_F, N_a = N_a)`` and passes return value along
    | Use this function to evaluate Fermi in p-dotated areas

    | This function uses ``@functools.cache`` decorator

    :param W_F: Energy level to check
    :type W_F: mpmath.mpf
    :return: Deviation from equilibrium
    :rtype: mpmath.mpf
    """

    return(Fermi(W_F, N_a=N_a))

@cache
def Fermi_n(W_F):
    """
    | Calls ``fermi_level.Fermi(W_F, N_d = N_d)`` and passes return value along
    | Use this function to evaluate Fermi in n-dotated areas

    | This function uses ``@functools.cache`` decorator

    :param W_F: Energy level to check
    :type W_F: mpmath.mpf
    :return: Deviation from equilibrium
    :rtype: mpmath.mpf
    """

    return(Fermi(W_F, N_d=N_d))


def approximate_Fermi_level():
    """
    | Returns approximated Fermi level height over the valence band (divided by 1 electron volt)
    | In thermodynamic equilibrium the Fermi level is constant over space.
    | The Fermi level for the n-dotated and p-dotated must therefore equal one another.
    | To validate results we approximate both areas seperately, compare them and take the average.

    | mpmath.mp.dps must be set high enough before a call to this function!
    | Tested only with mp.dps >= 22

    | Approximation is performed by finding roots of ``fermi_level.Fermi()`` function

    :return: Fermi level / 1eV
    :rtype: mpmath.mpf
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
    # "Bad" tolerance of 0.1 due to high magnitude of Fermi() output
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
    # "Bad" tolerance of 0.1 due to high magnitude of Fermi() output
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

if __name__ == "__main__":

    """
    Prepare variables
    """

    h = mpf(fill_values(h)) # In Js
    e = mpf(fill_values(q_e)) # In J
    k = mpf(fill_values(k) / e) # In eV/K
    m_e = mpf(fill_values(m_e))
    eps = mpf(fill_values(eps))
    W_g = mpf(fill_values(W_g, eV=True))
    N_v = mpf(fill_values(N_v))
    N_c = mpf(fill_values(N_c))
    m_ec = mpf(fill_values(m_ec))
    m_hc = mpf(fill_values(m_hc))
    T = mpf(fill_values(T))
    U_D = mpf(fill_values(U_D))
    N_d = mpf(fill_values(N_d))
    N_a = mpf(fill_values(N_a))
    N_dp = N_d
    N_am = N_a
    kT = k * T # In eV

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
    W_F = approximate_Fermi_level() # In eV

    pickle_save(float(W_F), "Fermi_level")

    if not HIDE_LOG: print("Fermi level approximated! Results saved!")