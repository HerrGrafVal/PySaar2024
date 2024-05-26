from initial_values import values
from symbols import *
from regions import NeutralPRegion, NeutralNRegion, P_SCR, N_SCR
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np

WIDTH = 7

parameter = {
    N_a: 2.25 * (10 ** 17),
    N_d: 5 * (10 ** 17),
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

    # neutral-p-region -w_p <= x < x_p
    ONE = NeutralPRegion()

    # p-SCR x_p <= x < 0
    TWO = P_SCR()

    # n-SCR 0 < x <= x_n
    THREE = N_SCR()

    # neutral-n-region x_n < x <= w_n
    FOUR = NeutralNRegion()

    # Create Piecewise functions from ONE, TWO, THREE, FOUR
    index = 0
    funcs = [rho, E, phi, W_v]
    func_names = ["rho", "E", "phi", "W_v"]
    for sym in funcs:
        exec(func_names[index] + " = sp.Piecewise("
             + "(ONE.funcs[sym], x < x_p),"
             + "(TWO.funcs[sym], (x_p <= x) & (x < 0)),"
             + "(THREE.funcs[sym], (0 < x) & (x <= x_n)),"
             + "(FOUR.funcs[sym], x_n < x))", globals()
             )
        index += 1

    # Lambdify all functions in func_names
    for i in func_names:
        exec(i + " = sp.lambdify(x, fill_values(" + i + "))", globals())

    x_p = float(fill_values(x_p))
    x_n = float(fill_values(x_n))
    w_p = abs(x_p * WIDTH)
    w_n = x_n * WIDTH

    xx = np.linspace(-1 * w_p, w_n, 1000)

    fig, (plt_rho, plt_E, plt_phi, plt_W) = plt.subplots(4, 1)
    plt_rho.plot(xx, rho(xx))
    plt_E.plot(xx, E(xx))
    plt_phi.plot(xx, phi(xx))
    plt_W.plot(xx, W_v(xx))
    plt.show()
