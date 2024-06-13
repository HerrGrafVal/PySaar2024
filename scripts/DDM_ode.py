import numpy as np
import mpmath as mp
from functools import cache
from cache import pickle_read, pickle_save
from read_dataframe import fill_values
from symbols import h, q_e, k, m_e, eps, W_g, N_v, N_c, m_ec, m_hc, T, U_D, N_d, N_a, x_p0, x_n0, WIDTH

# ----------------------------------------------------------------------------

@cache
def DDM(phi, N_am=0, N_dp=0):
    W_v = -phi  # In eV, = -e * phi / {e}
    W_c = W_v + W_g  # In eV
    p = N_v * mp.exp((- (W_F - W_v) / (kT)))
    n = N_c * mp.exp((- (W_c - W_F) / (kT)))
    rho = e * (p + N_dp - n - N_am)
    out = [W_v, W_c, float(p), float(n), float(rho)]
    return out

@cache
def DDM_p(phi):
    return DDM(phi, N_am=N_am)

@cache
def DDM_n(phi):
    return DDM(phi, N_dp=N_dp)

def fun_p(x, z):
    phi = z[0]  # In eV
    E = z[1]  # In V/m
    rho = DDM_p(phi)[4]
    dzdx = [-E, rho / eps]
    return dzdx

def fun_n(x, z):
    phi = z[0]  # In eV
    E = z[1]  # In V/m
    rho = DDM_n(phi)[4]
    dzdx = [-E, rho / eps]
    return dzdx

# ----------------------------------------------------------------------------

if __name__ == "__main__":

    """
    Prepare variables of type float
    """

    e = float(fill_values(q_e))  # In J
    k = float(fill_values(k)) / e  # In eV/K
    T = float(fill_values(T))  # In K
    kT = k * T  # In eV
    U_D = float(fill_values(U_D))  # In V
    eps = float(fill_values(eps))  # In C/Vm

    W_g = float(fill_values(W_g, eV=True))  # In eV

    # In m^-3
    N_v = float(fill_values(N_v))
    N_c = float(fill_values(N_c))
    N_dp = float(fill_values(N_d))  # Assume ionisation of all dotation atoms
    N_am = float(fill_values(N_a))  # Assume ionisation of all dotation atoms

    x_p0 = float(fill_values(x_p0))
    x_n0 = float(fill_values(x_n0))

    WIDTH = float(fill_values(WIDTH))

    # ----------------------------------------------------------------------------

    """
    Define band structure
    """

    W_v = 0
    W_c = W_g
    try:
        W_F = pickle_read("Fermi_level")  # In eV
    except FileNotFoundError:
        print("Fermi_level.pkl not found in SAVE_FOLDER. Execute fermi_level.py and try again.")
        exit()

    # ----------------------------------------------------------------------------

    """
    SciPy sole_ivp (method = RK45) yielded unsatisfactory results, other methods fail to work see previous commit
    mpmath odefun (method = taylor) produces satisfactory results, but can't iterate backwards

    x_p, x_n are defined by fieldstrength reaching zero and continuity in x = 0
    We assume they can be found in [2*x_p0 ; 2*x_n0]

         z0 = phi
    z  = z1 = E
         
    rho = DDM(z0)[4]

    dz   z0. = -z1
    dx = z1. = rho/eps
    """

    STEPS = 100

    # p-region
    phi_p = []
    E_p = []
    W_v_p = []
    W_c_p = []
    p_p = []
    n_p = []
    rho_p = []
    # n-region
    phi_n = []
    E_n = []
    W_v_n = []
    W_c_n = []
    p_n = []
    n_n = []
    rho_n = []

    # ----------------------------------------------------------------------------

    """
    Generate phi, E values for STEPS amount of x values per area
    """

    stepsize_p = -x_p0*2/STEPS
    stepsize_n = x_n0*2/STEPS

    x_span_p = np.arange(0, -x_p0 * 2, stepsize_p).astype(mp.mpf)
    x_span_n = np.arange(0, x_n0 * 2, stepsize_n).astype(mp.mpf)

    sol_p = mp.odefun(fun_p, 0, [0, 0])
    sol_n = mp.odefun(fun_n, 0, [0, 0])

    for x in x_span_p:
        z = sol_p(x)
        phi = -z[0]
        E = -z[1]
        phi_p.append(phi)
        E_p.append(E)

    zz_p = np.array([phi_p, E_p])

    for x in x_span_n:
        z = sol_n(x)
        phi = U_D + z[0]
        E = -z[1]
        phi_n.append(phi)
        E_n.append(E)

    zz_n = np.array([phi_n, E_n])

    # ----------------------------------------------------------------------------

    """
    Check where zz_p best meets zz_n in terms of phi AND E
    """

    DELTA = []
    for k, zz_P in enumerate(zz_p.T[1:,:]):
        for j, zz_N in enumerate(zz_n.T[1:,:]):
            delta = abs([1, 1] - np.divide(zz_P, zz_N))
            DELTA.append([k + 1, j + 1, delta])
    best_total = min(DELTA, key = lambda x: x[2][0] + x[2][1])

    index_p = best_total[0]
    index_n = best_total[1]

    # p-area
    # crop all lists to end at approximated continuity
    # xx_p needs to be reversed
    xx_p = -1 * x_span_p[:index_p + 1]
    xx_p = np.flip(xx_p)
    #xx_p -= stepsize_p # Only for improved visualisation
    phi_p = phi_p[:index_p + 1]
    E_p = E_p[:index_p + 1]

    # n-area
    # crop all lists to end at approximated continuity
    # phi and E need to be reversed
    xx_n = x_span_n[:index_n + 1]
    xx_n += stepsize_n # Prevent overlap at x = 0
    phi_n = phi_n[:index_n + 1]
    phi_n.reverse()
    E_n = E_n[:index_n + 1]
    E_n.reverse()

    # ----------------------------------------------------------------------------

    """
    Evaluate DDM for all relevant potentials
    """

    for phi in phi_p:
        ddm = DDM_p(phi)
        W_v_p.append(ddm[0])
        W_c_p.append(ddm[1])
        p_p.append(mp.log10(ddm[2]))
        n_p.append(mp.log10(ddm[3]))
        rho_p.append(ddm[4])

    for phi in phi_n:
        ddm = DDM_n(phi)
        W_v_n.append(ddm[0])
        W_c_n.append(ddm[1])
        p_n.append(mp.log10(ddm[2]))
        n_n.append(mp.log10(ddm[3]))
        rho_n.append(ddm[4])

    # ----------------------------------------------------------------------------

    """
    Join p and n values together
    """

    xx = list(xx_p) + list(xx_n)
    phi = phi_p + phi_n
    E = E_p + E_n
    W_v = W_v_p + W_v_n
    W_c = W_c_p + W_c_n
    p = p_p + p_n
    n = n_p + n_n

    # Charge density jumps at x=0 -> better visualisation with two values at x = 0
    xx_rho = list(xx_p) + list(xx_n - stepsize_n)
    rho = rho_p + rho_n

    # ----------------------------------------------------------------------------

    """
    Include neutral areas
    """

    x_p = xx[0]
    x_n = xx[-1]
    w_p = WIDTH * x_p
    w_n = WIDTH * x_n

    xx = [w_p] + xx + [w_n]
    xx_rho = [w_p] + xx_rho + [w_n]

    results = {
        "W_F" : W_F,
        "x_p" : x_p,
        "x_n" : x_n,
        "w_p" : w_p,
        "w_n" : w_n,
        "xx" : xx,
        "xx_rho" : xx_rho
        }

    for name in ["phi", "E", "W_v", "W_c", "p", "n", "rho"]:
        values = eval(name)
        results[name] = [values[0]] + values + [values[-1]]

    pickle_save(results, "ODE_solution")
    print("Results saved successfully!")