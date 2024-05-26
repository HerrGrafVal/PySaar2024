from initial_values import values
from sympy import Eq, exp, simplify, lambdify
from sympy.solvers.ode.systems import dsolve_system
from symbols import *
import matplotlib.pyplot as plt
import numpy as np

p = N_a
n = (n_i**2) / p
N_am = 0
N_dp = N_d
W_Fn = W_F
W_Fp = W_F

parameter = {
    N_a: 2.25 * (10 ** 17),
    N_d: 5 * (10 ** 17),
    w_p: 10,
    T: 300
}

ELEMENT = "Si"



def fill_values(func_in, element=ELEMENT):
    """
    Returns `sympy.expression` instance with all possible parameters substituted for their values

    Parameters
    : **func_in** *(sympy.expression)* Expression to fill with values
    : **element** *(string)* Optional, which element's values to choose from. Default set in ELEMENT
    """

    names = func_in.free_symbols
    for df in ["Naturkonstanten", "Materialparameter " + element]:
        for index, konst in values[df].iterrows():
            s = konst.Symbol
            v = konst.Koeffizient * (10 ** konst.Ordnung)
            u = konst.Einheit
            if s in names:
                func_in = func_in.subs(s, v)
    for s in parameter.keys():
        if s in names:
            func_in = func_in.subs(s, parameter[s])
    return func_in




if __name__ == "__main__":

    # Define Drift Diffusion Modell Equations
    bandgap = Eq(W_c, W_v + W_g)
    charge_density = Eq(q_e * (p + N_dp - n - N_am), rho)
    field_strength = Eq(E.diff(x), rho / eps)
    potential = Eq(phi.diff(x), -1 * E)
    field_energy = Eq(W_v.diff(x), q_e * E)
    # electron_density = Eq(n, N_c * exp(-1 * (W_c - W_Fn) / (k * T)))
    # hole_density = Eq(p, N_v * exp(-1 * (W_Fp - W_v) / (k * T)))

    # Prepare to solve DDM
    EQS = [bandgap, charge_density, field_strength, potential, field_energy]
    funcs = [rho, E, phi, W_v, W_c]
    # Simulation result useful as soon as missing ics are implemented
    ics = {
        W_v.subs(x, -1 * w_p): 0,
        W_v.diff(x).subs(x, -1 * w_p) : 0
    }

    # Solve DDM
    EQS_SOLVED = dsolve_system(EQS, funcs, x, ics)[0]

    # Create dictionary from solutions
    sol_sym = {}
    sol_num = {}
    index = 0
    for EQ in EQS_SOLVED:
        sol_sym[EQ.lhs] = simplify(EQ.rhs)
        sol_num[EQ.lhs] = fill_values(sol_sym[EQ.lhs])
        index += 1

    print(sol_num)
