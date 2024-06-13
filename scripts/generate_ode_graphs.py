from cache import pickle_read
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

# ----------------------------------------------------------------------------

# Whether to show results in matplotlib or generate tex
SHOW_PLOT = False
# Whether x-ticks should be numbers or just mark x_p, 0, x_n
SHOW_X_NUMBERS = False
# If not SHOW_PLOT, Whether to make seperate figure objects available outside of loop
KEEP_FIGURES = False

# ----------------------------------------------------------------------------

if __name__ == "__main__":

    """
    Retrieve simulation results
    """

    try:
        results = pickle_read("ODE_solution")
    except FileNotFoundError:
        print("No simulation results found! Execute DDM_ode.py and try again!")
        exit()

    xx = results["xx"]
    xx_rho = results["xx_rho"]
    phi = results["phi"]
    E = results["E"]
    W_v = results["W_v"]
    W_c = results["W_c"]
    W_F = results["W_F"]
    p = results["p"]
    n = results["n"]
    rho = results["rho"]

    # ----------------------------------------------------------------------------

    """
	Setup plots
	"""

    pn = ["cc", "rho", "E", "phi", "W"]

    form_x = EngFormatter(unit="$m$")
    form_cc = EngFormatter(unit="$m^{-3}$")
    form_rho = EngFormatter(unit="$C / m^{-3}$")
    form_E = EngFormatter(unit="$V / m$")
    form_phi = EngFormatter(unit="$V$")
    form_W = EngFormatter(unit="$eV$")

    fig, (ax_cc, ax_rho, ax_E, ax_phi, ax_W) = plt.subplots(5, 1)
    fig.subplots_adjust(hspace=1.5)

    ax_cc.plot(xx, p, "C0", label="$log_{10}$ $p (x)$")
    ax_cc.plot(xx, n, "C1", label="$log_{10}$ $n (x)$")
    ax_cc.yaxis.set_major_formatter(form_cc)

    ax_rho.plot(xx_rho, rho, "C0", label="$\\rho (x)$")
    ax_rho.yaxis.set_major_formatter(form_rho)

    ax_E.plot(xx, E, "C0", label="$E (x)$")
    ax_E.yaxis.set_major_formatter(form_E)

    ax_phi.plot(xx, phi, "C0", label="$\\varphi (x)$")
    ax_phi.yaxis.set_major_formatter(form_phi)

    ax_W.plot(xx, W_v, "C0", label="$W_V (x)$")
    ax_W.plot(xx, W_c, "C1", label="$W_C (x)$")
    ax_W.plot([xx[0], xx[-1]], [W_F, W_F], "C2", label="$W_F$")
    ax_W.yaxis.set_major_formatter(form_W)

    for i in pn:
        axes = eval("ax_" + i)
        axes.legend()

        if SHOW_X_NUMBERS:
            axes.xaxis.set_major_formatter(form_x)
        else:
            w_p = results["w_p"]
            x_p = results["x_p"]
            x_n = results["x_n"]
            w_n = results["w_n"]
            axes.set_xticks([w_p, x_p, 0, x_n, w_n], ["$-w_p$", "$x_p$", "$0$", "$x_n$", "$w_n$"])

    # ----------------------------------------------------------------------------

    """
	Display plots or generate tex
	"""

    if SHOW_PLOT:
        # Setting titles (calling tikzplotlib with titles causes unicode errors)
        ax_cc.set_title("Ladungsträgerdichten")
        ax_rho.set_title("Raumladungsdichte")
        ax_E.set_title("Feldstärke")
        ax_phi.set_title("Potential")
        ax_W.set_title("Bandverläufe")
        plt.show()
        # plt.savefig("../simulation_results/ODE_plot.png")

    else:
        # Additional imports
        from cache import plt_to_tex

        # Move all plots to their own figure
        for i in pn:
            if KEEP_FIGURES:
                exec("fig_" + i + " = plt.figure()", globals())
                new_fig = eval("fig_" + i)
            else:
                new_fig = plt.figure()
            ax = eval("ax_" + i)
            ax.remove()
            ax.figure = new_fig
            new_fig.axes.append(ax)
            new_fig.add_axes(ax)
            dummy_ax = new_fig.add_subplot(111)
            ax.set_position(dummy_ax.get_position())
            dummy_ax.remove()

            plt_to_tex(i + "_graph", new_fig)

        plt.close(fig)
        plt.show()
