from initial_values import values
from sympy import lambdify
from symbols import *
from regions import NeutralPRegion, NeutralNRegion, P_SCR, N_SCR
import matplotlib.pyplot as plt
import numpy as np

W_Fn = W_F
W_Fp = W_F
W_F = 0.5 * W_g

parameter = {
    N_a: 2.25 * (10 ** 17),
    N_d: 5 * (10 ** 17),
    w_p: 10,
    w_n: 10,
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

    x_p = float(fill_values(x_p))
    x_n = float(fill_values(x_n))

    # neutral-p-region -w_p <= x < x_p
    ONE = NeutralPRegion()

    # p-SCR x_p <= x < 0
    TWO = P_SCR(x_p)

    # n-SCR 0 < x <= x_n
    THREE = N_SCR(x_n)

    # neutral-n-region x_n < x <= w_n
    FOUR = NeutralNRegion()
