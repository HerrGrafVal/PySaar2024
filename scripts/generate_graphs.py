from symbols import *
from cache import read_from_file, save_to_npy, read_from_npy
from read_dataframe import fill_values
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch as Arrow
# from matplotlib.ticker import EngFormatter as Form
from sympy import lambdify
from numpy import linspace

# ----------------------------------------------------------------------------

# Change USE_CACHED_VALUES to False after changing WIDTH
WIDTH = 3

parameter = {
    N_a: 2.25 * (10 ** 17) * (centimeter ** -3),
    N_d: 5 * (10 ** 17) * (centimeter ** -3),
    T: 300 * kelvin
}

USE_CACHED_VALUES = True

# ----------------------------------------------------------------------------

def render(axes, x, y, title, xlabel_coord=1.025, ylabel_coord=1.1, label=None, include_zero=False, arrow = True, bottom = False):

    line = axes.plot(x, y, label=label)
    axes.set_title(title, loc = "left")

    axes.spines[["left", "bottom"]].set_position(("data", 0))
    axes.spines[["top", "right"]].set_visible(False)
    if bottom: axes.spines[["bottom"]].set_position(("data", min(y)))

    if arrow: 
        axes.plot(1, 0, ">k", transform=axes.get_yaxis_transform(), clip_on=False)
        axes.plot(0, 1, "^k", transform=axes.get_xaxis_transform(), clip_on=False)

    axes.set_xlabel("$x$")

    axes.set_ylim(top=max(abs(y)) * 1.1)

    axes.xaxis.set_label_coords(xlabel_coord, 0, transform=axes.get_yaxis_transform())
    axes.yaxis.set_label_coords(0, ylabel_coord, transform=axes.get_xaxis_transform())

    if include_zero:
        axes.set_xticks([x[0], x_p, 0, x_n, x[-1]], ["$-w_p$", "$x_p$", "$0$", "$x_n$", "$w_n$"])
    else:
        axes.set_xticks([x[0], x_p, x_n, x[-1]], ["$-w_p$", "$x_p$", "$x_n$", "$w_n$"])

    return line


def render_rho(axes, x, y):

    axes.set_ylabel("$\\rho(x)$", rotation=0)

    render(axes, x, y, "Raumladungsdichte")

    axes.set_yticks([min(y), max(y)], ["$-e N_A$", "$e N_D$"])


def render_E(axes, x, y):

    axes.set_ylabel("$E(x)$", rotation=0)

    render(axes, x, y, "Feldstärke")

    axes.set_ylim(top=max(abs(y)) / 2)
    axes.set_yticks([-max(abs(y))], ["$\\dfrac{e}{ \\epsilon } N_A x_p$"])


def render_phi(axes, x, y):

    axes.set_ylabel("$\\varphi(x)$", rotation=0)

    render(axes, x, y, "Potential", include_zero=True)

    axes.set_yticks([max(abs(y))], ["$U_D$"])


def render_W(axes, x, y):

    # axes.set_ylabel("$W_V(x)$", rotation = 0)

    render(axes, x, y, "Bandverläufe", label="$W_V$", arrow = False, bottom = True)[0]
    axes.plot(x,y + fill_values(W_g), color = "blue", label="$W_C$")
    axes.set_ylim(auto = True)
    axes.plot(1, y[-1], ">k", transform=axes.get_yaxis_transform(), clip_on=False)
    axes.xaxis.set_label_coords(1.025, y[-1], transform=axes.get_yaxis_transform())
    axes.spines[["left"]].set_visible(False)

    h, l = axes.get_legend_handles_labels()
    axes.legend(h[::-1], l[::-1], loc="lower left")

    YSCALE = 0.1 * y[-1]
    arrow = Arrow((1.5 * x_n, -1 * YSCALE), (1.5 * x_n, YSCALE + y[-1]), arrowstyle = "<->", mutation_scale = 6)
    axes.add_patch(arrow)
    axes.plot([x[0], x[-1]], [0, 0], color = "black", linestyle = "--", linewidth = 1)
    axes.annotate("$e U_D$", (1.55 * x_n, 0.75 * y[-1]))

    axes.set_yticks([], [])

# ----------------------------------------------------------------------------

"""
Calculate relevant x vector
"""

x_p = float(fill_values(x_p, parameter=parameter))
x_n = float(fill_values(x_n, parameter=parameter))
w_p = abs(x_p * WIDTH)
w_n = x_n * WIDTH
xx = linspace(-1 * w_p, w_n, 1000)

# ----------------------------------------------------------------------------

if __name__ == "__main__":

    if USE_CACHED_VALUES:
        try:
            xx, rho_values = read_from_npy("rho_values")
            xx, E_values = read_from_npy("E_values")
            xx, phi_values = read_from_npy("phi_values")
            xx, W_v_values = read_from_npy("W_v_values")
            print("Using previously saved values. Change USE_CACHED_VALUES in generate_graphs.py line 20 to False to calculate new ones instead.")

        except FileNotFoundError:
            print("Saved values missing. Please change USE_CACHED_VALUES in generate_graphs.py line 20 to False and try again.")
            exit()

    # ----------------------------------------------------------------------------

    else:

        """
        Read functions from save
        """
        func_names = ["rho", "E", "phi", "W_v"]
        try:
            for i in func_names:
                exec(i + " = read_from_file('" + i + "_results.txt', namespace)")
        except FileNotFoundError:
            print("Saved function(s) missing. Please execute modell.py and try again.")
            exit()

        """
        Lambdify all functions in func_names
        """

        for i in func_names:
            exec(i + "_func = lambdify(x, fill_values(" + i + ", parameter = parameter))", globals())

        """
        Call lambdified function and save results to .npy file
        """

        rho_values = rho_func(xx)
        E_values = E_func(xx)
        phi_values = phi_func(xx)
        W_v_values = W_v_func(xx)

        save_to_npy("rho_values", xx, rho_values)
        save_to_npy("E_values", xx, E_values)
        save_to_npy("phi_values", xx, phi_values)
        save_to_npy("W_v_values", xx, W_v_values)

        print("Values saved. You may now change USE_CACHED_VALUES in generate_graphs.py to True to speed up future calls to this script")

    # ----------------------------------------------------------------------------

    """
    Generate subplots and pass them to render functions
    """

    fig, (plt_rho, plt_E, plt_phi, plt_W) = plt.subplots(4, 1)
    fig.subplots_adjust(hspace=1.5)

    render_rho(plt_rho, xx, rho_values)
    render_E(plt_E, xx, E_values)
    render_phi(plt_phi, xx, phi_values)
    render_W(plt_W, xx, W_v_values)

    # ----------------------------------------------------------------------------

    plt.show()
