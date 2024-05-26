from symbols import rho, E, phi, W_v, x, x_p, x_n
from regions import NeutralPRegion, NeutralNRegion, P_SCR, N_SCR
from cache import save_to_file
from sympy import Piecewise

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
