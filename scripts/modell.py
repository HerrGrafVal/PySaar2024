from symbols import *
from regions import NeutralPRegion, NeutralNRegion, P_SCR, N_SCR
from cache import save_to_file
from sympy import Piecewise, exp, coth
from read_dataframe import fill_values

# ----------------------------------------------------------------------------

"""
Define areas ONE-FOUR as follows
"""

# neutral-p-region -w_p <= x < x_p
ONE = NeutralPRegion()

# p-SCR x_p <= x < 0
TWO = P_SCR()

# n-SCR 0 < x <= x_n
THREE = N_SCR()

# neutral-n-region x_n < x <= w_n
FOUR = NeutralNRegion()

PN = [ONE, TWO, THREE, FOUR]

# ----------------------------------------------------------------------------

def calculate_current(parameter, U):
    """
    Returns current/ampere (float) based on parameter

    Parameter
    : **parameter** *(dict)* Must be in form of read_dataframe.default_parameter
    : **U** *(float)* External voltage
    """

    if U in [0, 0 * volt]:
        return 0

    I_s = calculate_I_s(parameter, U)
    I = I_s * (exp(U / U_T) - 1)
    current = fill_values(I, parameter = parameter).evalf()

    return current

def calculate_I_s(parameter, U):
    """
    Returns saturation current/ampere (float) based on parameter

    Parameter
    : **parameter** *(dict)* Must be in form of read_dataframe.default_parameter
    : **U** *(float)* External voltage, needed for calculation of SCR width
    """

    if U in [0, 0 * volt]:
        return 0

    parameter[U_ext] = U

    # Prevent SCR width errors after sufficient external voltage
    if fill_values(U * volt) >= fill_values(U_D, parameter = parameter): 
        # x_n = 0 * meter
        # x_p = 0 * meter
        I_s = q_e * A * (ONE.np0 * D_n / L_n * coth((w_p) / L_n) + FOUR.pn0 * D_p / L_p * coth((w_n) / L_p))
    else:
        # Diode current
        I_s = q_e * A * (ONE.np0 * D_n / L_n * coth((w_p + x_p) / L_n) + FOUR.pn0 * D_p / L_p * coth((w_n - x_n) / L_p))

    return fill_values(I_s, parameter = parameter).evalf()

# ----------------------------------------------------------------------------

if __name__ == "__main__":

    # Create Piecewise functions from ONE, TWO, THREE, FOUR
    index = 0
    funcs = [rho, E, phi, W_v]
    func_names = ["rho", "E", "phi", "W_v"]
    for sym in funcs:
        exec(func_names[index] + " = Piecewise("
             + "(ONE.funcs[sym], x < x_p),"
             + "(TWO.funcs[sym], (x_p <= x) & (x < 0)),"
             + "(THREE.funcs[sym], (0 < x) & (x <= x_n)),"
             + "(FOUR.funcs[sym], x_n < x))", globals()
             )
        index += 1

    # Save simulation results to .txt files
    for i in func_names:
        save_to_file(i + "_results.txt", eval(i))


