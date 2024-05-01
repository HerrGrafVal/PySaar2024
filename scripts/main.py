from initial_values import values
from symbols import *
from sympy import Function, solve, exp, Piecewise, plot, lambdify, simplify
import matplotlib.pyplot as plt
import numpy as np


parameter = {
    N_a : 2.25 * (10 ** 17),
    N_d : 5 * (10 ** 17),
    T : 300
}

ELEMENT = "Si"


def fill_values(func_in, element = ELEMENT):

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
                func_in = func_in.subs(s,v)
    for s in parameter.keys():
        if s in names:
            func_in = func_in.subs(s, parameter[s])
    return func_in


if __name__ == "__main__":

    """
    ## Ladungsträgerdichten
    Annahmen: Störstellenerschöpfung, thermodynamisches Gleichgewicht
    """

    # p-Bahnbereich
    p_p0 = N_a
    n_p0 = (n_i**2)/p_p0

    # n-Bahnbereich
    n_n0 = N_d
    p_n0 = (n_i**2)/n_n0

    # RLZ
    n0 = N_c * exp(-(W_c-W_F)/(k*T))
    p0 = N_v * exp(-(W_F-W_v)/(k*T))

    # Ortsabhängig
    p = Piecewise(
        (p_p0, x <= x_p),
        (p0, (x_p < x) & (x <= x_n)),
        (p_n0, x_n < x)
        )

    n = Piecewise(
        (n_p0, x <= x_p),
        (n0, (x_p < x) & (x <= x_n)),
        (n_n0, x_n < x)
        )

    N_dp = Piecewise(
        (N_d, x <= 0),
        (0, 0 < x)
        )

    N_am = Piecewise(
        (0, x <= 0),
        (N_a, 0 < x)
        )

    rho = q_e * (p + N_dp - n - N_am)

    rho_ = Piecewise(
        (0, x <= x_p),
        (-1 * q_e * N_a, (x_p < x) & (x <= 0)),
        (q_e * N_d, (0 < x) & (x <= x_n)),
        (0, x_n < x)
        )

    func = lambdify(x, fill_values(rho_))

    SCALE = 0

    x_p = float(fill_values(x_p)) * 10**SCALE
    x_n = float(fill_values(x_n)) * 10**SCALE


    xx = np.linspace(x_p, x_n, 1000)
    plt.plot(xx, func(xx))
    plt.show()

    # E = (rho/eps).integrate(x)



# BANDVERLÄUFE IMPLEMENTIEREN