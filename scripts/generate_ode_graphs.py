from cache import pickle_read
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

# ----------------------------------------------------------------------------

# Whether to show results in matplotlib or generate tex
SHOW_PLOT = True
# Whether x-ticks should be numbers or just mark x_p, 0, x_n
SHOW_X_NUMBERS = False

# ----------------------------------------------------------------------------
# Retrieve simulation results

if __name__ == "__main__":

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

    w_p = results["w_p"]
    x_p = results["x_p"]
    x_n = results["x_n"]
    w_n = results["w_n"]

    # ----------------------------------------------------------------------------
    # Setup for plots

    form_x = EngFormatter(unit="$m$")
    form_cc = EngFormatter()
    form_rho = EngFormatter(unit="$C / m^{-3}$")
    form_E = EngFormatter(unit="$V / m$")
    form_phi = EngFormatter(unit="$V$")
    form_W = EngFormatter(unit="$eV$")

    pn = ["cc", "rho", "E", "phi", "W"]

    label = {
        "rho": ["$\\rho (x)$", "Raumladungsdichte"],
        "E": ["$E (x)$", "Feldstärke"],
        "phi": ["$\\varphi (x)$", "Potential"]
    }

    # ----------------------------------------------------------------------------
    # Generate single figure with subplot for each graph

    fig, (ax_cc, ax_rho, ax_E, ax_phi, ax_W) = plt.subplots(5, 1, layout="constrained")

    # Adjust subplot spacing
    size = fig.get_size_inches()
    w_pad, h_pad, wspace, hspace = fig.get_constrained_layout_pads()
    fig.set_size_inches((size[0] * 1.25, size[1] * 1.5))
    fig.set_constrained_layout_pads(w_pad=w_pad, h_pad=h_pad * 7.5, wspace=wspace, hspace=hspace * 7.5)

    # ----------------------------------------------------------------------------    
    # Populate subplots

    for i in pn:
        ax = eval("ax_" + i)

        # Plot data, set title
        if i == "cc":
            ax.plot(xx, p, "C0", label="$log_{10}($ $p (x) \\cdot m^3)$")
            ax.plot(xx, n, "C1", label="$log_{10}($ $n (x) \\cdot m^3)$")
            ax.set_title("Ladungsträgerdichten")
        elif i == "W":
            ax.plot(xx, W_v, "C0", label="$W_V (x)$")
            ax.plot(xx, W_c, "C1", label="$W_C (x)$")
            ax.plot([xx[0], xx[-1]], [W_F, W_F], "C2", label="$W_F$")
            ax.set_title("Bandverläufe")
        else:
            if i == "rho":
                ax.plot(xx_rho, eval(i), "C0", label=label[i][0])
            else:
                ax.plot(xx, eval(i), "C0", label=label[i][0])
            ax.set_title(label[i][1])

        # Show legend
        exec("legend_" + i + " = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))", globals())

        # Adjust visible x, y axis
        ax.spines[["bottom"]].set_position(("data", 0))
        ax.spines[["top", "right"]].set_visible(False)
        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False)

        # Adjust x, y ticks
        ax.yaxis.set_major_formatter(eval("form_" + i))
        if SHOW_X_NUMBERS:
            ax.xaxis.set_major_formatter(form_x)
        else:
            ax.set_xticks([w_p, x_p, 0, x_n, w_n], ["$-w_p$", "$x_p$", "$0$", "$x_n$", "$w_n$"])

    # ----------------------------------------------------------------------------
    # Display plots or save png

    if SHOW_PLOT:
        plt.show()

    else:
        # Additional imports
        from cache import SAVE_FOLDER

        # Save full figure
        plt.savefig(SAVE_FOLDER + "DDM_graph.png")
        plt.close(fig)

        # ----------------------------------------------------------------------------
        # Create new figures for each graph
        
        for i in pn:
            exec("fig_" + i + ", ax_" + i + " = plt.subplots(1, 1, layout = 'constrained')", globals())

            new_fig = eval("fig_" + i)
            ax = eval("ax_" + i)

            # Plot data, set title
            if i == "cc":
                ax.plot(xx, p, "C0", label="$log_{10}($ $p (x) \\cdot m^3)$")
                ax.plot(xx, n, "C1", label="$log_{10}($ $n (x) \\cdot m^3)$")
                ax.set_title("Ladungsträgerdichten")
            elif i == "W":
                ax.plot(xx, W_v, "C0", label="$W_V (x)$")
                ax.plot(xx, W_c, "C1", label="$W_C (x)$")
                ax.plot([xx[0], xx[-1]], [W_F, W_F], "C2", label="$W_F$")
                ax.set_title("Bandverläufe")
            else:
                if i == "rho":
                    ax.plot(xx_rho, eval(i), "C0", label=label[i][0])
                else:
                    ax.plot(xx, eval(i), "C0", label=label[i][0])
                ax.set_title(label[i][1])

            # Show legend
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            # Adjust visible x, y axis
            ax.spines[["bottom"]].set_position(("data", 0))
            ax.spines[["top", "right"]].set_visible(False)
            ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
            ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False)

            # Adjust x, y ticks
            ax.yaxis.set_major_formatter(eval("form_" + i))
            if SHOW_X_NUMBERS:
                ax.xaxis.set_major_formatter(form_x)
            else:
                ax.set_xticks([w_p, x_p, 0, x_n, w_n], ["$-w_p$", "$x_p$", "$0$", "$x_n$", "$w_n$"])

            # Adjust figure aspect ratio
            size = new_fig.get_size_inches()
            size[0] *= 1.75  # Width
            size[1] *= 0.4  # Height
            new_fig.set_size_inches(size)

            # Save single graph figure
            plt.savefig(SAVE_FOLDER + i + "_graph.png", bbox_inches="tight")

            # Close figure
            plt.close(new_fig)

"""
Attempt to save individual subplots from single figure
Problem: Title from adjacent graphs clips into saved images

from matplotlib.transforms import Bbox

for i in pn:
    axes = eval("ax_" + i)
    items = axes.get_xticklabels() + axes.get_yticklabels()
    items += [axes, axes.title, eval("legend_" + i)]
    bbox = Bbox.union([item.get_window_extent() for item in items])
    extent = bbox.expanded(1.05, 1.1).transformed(fig.dpi_scale_trans.inverted())
    plt.savefig("../simulation_results/" + i + "_graph.png", bbox_inches=extent)
"""

"""
Attempt to move existing axes to seperate figures
Problem: Cannot control aspect ratio in new figure

# If not SHOW_PLOT, Whether to make seperate figure objects available outside of loop
KEEP_FIGURES = False

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
plt.close(fig)
plt.show()
"""
