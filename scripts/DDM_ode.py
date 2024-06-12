import numpy as np
import mpmath as mp
from functools import cache
from cache import pickle_read
from read_dataframe import fill_values
from symbols import h, q_e, k, m_e, eps, W_g, N_v, N_c, m_ec, m_hc, T, U_D, N_d, N_a, x_p0, x_n0

# ----------------------------------------------------------------------------

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

x_p0 = float(fill_values(x_p0))
x_n0 = float(fill_values(x_n0))

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
SciPy sole_ivp (method = RK45) yielded unsatisfactory results, other methods fail to work see previous commit
mpmath odefun (method = taylor) produces satisfactory results, but can't iterate backwards

x_p, x_n are defined by fieldstrength reaching zero and continuity in x = 0
x_p0, x_n0 correspond to approximating rho with rect functions


The following ignores that the fieldstrength should be continous in x = 0, see bottom of file for solution

The following results use x_p0 and x_n! To resemble reality it needs to use x_p and x_n instead.
To calculate x_p the following formula can be used x_p * N_a = -x_n * N_d
Since our x_n depends on x_p0 these steps would need repetition until a satisfactory result is achieved.
This could be achieved by packing the following code into functions and running them recursively


     z0 = phi
z  = z1 = E
     
rho = DDM(z0)[4]

dz   z0. = -z1
dx = z1. = rho/eps
"""

x_start = x_p0 # x_p < 0
x_finish = x_n0 # x_n > 0
z_start = [0, 0] # phi(x_p), E(x_p)
z_finish = [U_D, 0] # phi(x_n), E(x_n)

HIDE_LOG = False

STEPS = 100
stepsize = (x_finish - x_start) / STEPS

# ----------------------------------------------------------------------------

"""
P-region, where we can move in +x direction from known initial conditions
x_p0 <= x < 0
"""

x_span_p = np.arange(x_start, -stepsize/2, stepsize).astype(mp.mpf)

sol_p = mp.odefun(fun_p, x_start, z_start)
if not HIDE_LOG: print("P-area solved")

xx_p = x_span_p
zz_p = []
for x in xx_p:
    zz_p.append(sol_p(x))
if not HIDE_LOG: print("P-area computed")

phi_p = []
E_p = []
W_v_p = []
W_c_p = []
p_p = []
n_p = []
rho_p = []

for z in zz_p:
    z[0] *= -1
    z[1] *= -1
    phi_p.append(z[0])
    E_p.append(z[1])
    ddm = DDM_p(z[0])
    W_v_p.append(ddm[0])
    W_c_p.append(ddm[1])
    p_p.append(mp.log10(ddm[2]))
    n_p.append(mp.log10(ddm[3]))
    rho_p.append(ddm[4])

# ----------------------------------------------------------------------------

"""
N-region, where we need to move in -x directin to include initial conditions
0 < x <= x_n

We solve in +x, calculate how far we need to go to match p-region x=0 and then flip vertically
"""

sol_n = mp.odefun(fun_n, 0, [0,0])
print("N-area solved")

mp.mp.dps = 30

# n-region
phi_n = []
E_n = []
W_v_n = []
W_c_n = []
p_n = []
n_n = []
rho_n = []

phi0 = phi_p[-1]
phi = U_D
xx_n = []

i = 0
while phi >= phi0:
    x = i * stepsize
    i += 1
    z = sol_n(x)
    phi = U_D + z[0]
    E = -z[1]
    xx_n.append(x)
    phi_n.append(phi)
    E_n.append(E)

phi_n.pop()
E_n.pop()
xx_n.pop() # xx_temp now contains values from 0 to x_n Mind that x_n != x_n0

phi_n.reverse()
E_n.reverse()
# xx_n doesn't need to be flipped

for phi in phi_n:
    ddm = DDM_n(phi)
    W_v_n.append(ddm[0])
    W_c_n.append(ddm[1])
    p_n.append(mp.log10(ddm[2]))
    n_n.append(mp.log10(ddm[3]))
    rho_n.append(ddm[4])

# ----------------------------------------------------------------------------

"""
To ensure continuity of E the above approach has to be used for both phi and E,
in order to do so the p-area needs to be increased in size to a (randomly chosen) point,
so that phi and E levels from p and n are likely to match before reaching said point.
This can be achieved by using the n-area approach for calculating x
"""