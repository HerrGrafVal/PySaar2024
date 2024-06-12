import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp
from functools import cache
from cache import pickle_read
from read_dataframe import fill_values
from symbols import h, q_e, k, m_e, eps, W_g, N_v, N_c, m_ec, m_hc, T, U_D, N_d, N_a, x_p0, x_n0

# ----------------------------------------------------------------------------

"""
Prepare variables of type float
"""

e = float(fill_values(q_e)) # In J
k = float(fill_values(k)) / e # In eV/K
T = float(fill_values(T)) # In K
kT = k * T # In eV
U_D = float(fill_values(U_D)) # In V
eps = float(fill_values(eps)) # In C/Vm

W_g = float(fill_values(W_g, eV=True)) # In eV

# In m^-3
N_v = float(fill_values(N_v))
N_c = float(fill_values(N_c))
N_dp = float(fill_values(N_d)) # Assume ionisation of all dotation atoms 
N_am = float(fill_values(N_a)) # Assume ionisation of all dotation atoms

x_start = float(fill_values(x_p0))
x_finish = float(fill_values(x_n0))

# ----------------------------------------------------------------------------

"""
Define band structure
"""

W_v = 0
W_c = W_g
try:
    W_F = pickle_read("Fermi_level") # In eV
except FileNotFoundError:
    print("Fermi_level.pkl not found in SAVE_FOLDER. Execute fermi_level.py and try again.")

# ----------------------------------------------------------------------------

"""
Setup for ode solver

     z0 = phi       In V
z  = z1 = E         In V/m
     
rho = DDM(z0)[4]

dz   z0. = -z1
dx = z1. = rho/eps
"""

z_start = [0, 0] # phi(x_p), E(x_p)
z_finish = [U_D, 0] # phi(x_n), E(x_n)

@cache
def DDM(phi, N_am=0, N_dp=0):
    W_v = -phi # In eV, = -e * phi / {e}
    W_c = W_v + W_g # In eV
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
    phi = z[0] # In eV
    E = z[1] # In V/m
    rho = DDM_p(phi)[4]
    dzdx = [-E, rho / eps]
    return dzdx

def fun_n(x, z):
    phi = z[0] # In eV
    E = z[1] # In V/m
    rho = DDM_n(phi)[4]
    dzdx = [-E, rho / eps]
    return dzdx

# ----------------------------------------------------------------------------

STEPS = 100

stepsize = (x_finish - x_start) / STEPS

x_span_p = np.arange(x_start, 0, stepsize)
x_span_n = np.arange(x_finish, 0, -1 * stepsize)

sol_p = solve_ivp(fun_p, [x_start, 0], z_start, t_eval = x_span_p, dense_output=True)
sol_n = solve_ivp(fun_n, [x_finish, 0], z_finish, t_eval = x_span_n, dense_output=True)


# Multiply with -1 due to ODE definition

"""
xx_p = x_span_p
zz_p = sol_p.sol(x_span_p) * -1
xx_n = np.flip(x_span_n)
zz_n = np.flip(sol_n.sol(x_span_n), 1) * -1
"""
xx_p = sol_p.t
zz_p = sol_p.y * -1
xx_n = np.flip(sol_n.t)
zz_n = np.flip(sol_n.y, 1) * -1


# ----------------------------------------------------------------------------

# p-region
phi_p = []
E_p = []
W_v_p = []
W_c_p = []
p_p = []
n_p = []
rho_p = []

for i in range(len(xx_p)):
    z = zz_p[:,i]
    phi_p.append(z[0])
    E_p.append(z[1])
    ddm = DDM_p(z[0])
    W_v_p.append(ddm[0])
    W_c_p.append(ddm[1])
    p_p.append(ddm[2])
    n_p.append(ddm[3])
    rho_p.append(ddm[4])
"""
phi_p = np.array(phi).astype(float)
E_p = np.array(E).astype(float)
W_v_p = np.array(W_v).astype(float)
W_c_p = np.array(W_c).astype(float)
p_p = np.array(p).astype(float)
n_p = np.array(n).astype(float)
rho_p = np.array(rho_p).astype(float)
"""
# ----------------------------------------------------------------------------

# n-region
phi_n = []
E_n = []
W_v_n = []
W_c_n = []
p_n = []
n_n = []
rho_n = []

for i in range(len(xx_n)):
    z = zz_n[:,i]
    z[0] += 2 * U_D # Same as the *-1 above
    phi_n.append(z[0])
    E_n.append(z[1])
    ddm = DDM_n(z[0])
    W_v_n.append(ddm[0])
    W_c_n.append(ddm[1])
    p_n.append(ddm[2])
    n_n.append(ddm[3])
    rho_n.append(ddm[4])

"""
phi_n = np.array(phi).astype(float)
E_n = np.array(E).astype(float)
W_v_n = np.array(W_v).astype(float)
W_c_n = np.array(W_c).astype(float)
p_n = np.array(p).astype(float)
n_n = np.array(n).astype(float)
rho_n = np.array(rho_n).astype(float)
"""
# ----------------------------------------------------------------------------



"""
ToDo:
Try mpmath odefun() to solve ode
Scipy solve_ivp: Add interpolation for p-r gap
"""