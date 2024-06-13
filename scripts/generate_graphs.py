from symbols import *
from read_dataframe import fill_values
from cache import read_from_file, save_to_npy, read_from_npy
from sympy import lambdify
from numpy import linspace, interp, array
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch as Arrow
# from matplotlib.ticker import EngFormatter as Form

# ----------------------------------------------------------------------------

parameter = {
    N_a: 2.25 * (10 ** 17) * (centimeter ** -3),
    N_d: 5 * (10 ** 17) * (centimeter ** -3),
    T: 300 * kelvin,
    U_ext : 0 * volt,
    A : 19.625 * (milimeter ** 2),
    "N-Dotation" : "As",
    "P-Dotation" : "B",
    WIDTH : 3
}

USE_CACHED_PN_VALUES = True
USE_CACHED_CURRENT_VALUES = True
HIDE_CACHE_LOG = False
PLOT_PN = True
PLOT_CURRENT = True
THRESHOLD = 10000

# ----------------------------------------------------------------------------

def render(axes, x, y, title, **kwargs):
    """
    Base function to plot data. Returns line object drawn in axes

    Parameters
    : **axes** *(matplotlib.axes)* Axes to plot to
    : **x, y** *(numpy.array)* Data to plot against each other
    : **title** *(string)* Plot title to display
    : **kwargs**
    : **label** *(string)* Label to pass onto line object created from x, y
    : **center_title** *(bool)* Whether or not to center the title. Default title location is left
    : **adjust_ticks** *(bool)* Whether or not adjustment to ticks should be conducted
    : **include_zero** *(bool)* Whether or not x = 0 should be marked on x axis
    : **arrow** *(bool)* Whether or not x and y axis are drawn with arrow tips
    : **bottom** *(bool)* Whether or not the x axis should be moved down to min(y)
    : **xlabel_coord** & **ylabel_coord** *(float)* Coordinates for x, y axis label
    """

    # Setup
    args = {
    "label" : None, 
    "center_title" : False, 
    "adjust_ticks" : True, 
    "include_zero" : False, 
    "arrow" : True, 
    "bottom" : False,
    "xlabel_coord" : 1.025, 
    "ylabel_coord" : 1.1
    }

    args.update(kwargs)

    # Plot data and set axes title
    line = axes.plot(x, y, label=args["label"])
    if args["center_title"]:
        axes.set_title(title, loc="center")
    else:
        axes.set_title(title, loc="left")

    # Center x, y axis, hide additional ones
    axes.spines[["left", "bottom"]].set_position(("data", 0))
    axes.spines[["top", "right"]].set_visible(False)
    if args["bottom"]: # Move x axis down to min(y)
        axes.spines[["bottom"]].set_position(("data", min(y)))

    if args["arrow"]: # Draw arrow tips for x, y axis
        axes.plot(1, 0, ">k", transform=axes.get_yaxis_transform(), clip_on=False)
        axes.plot(0, 1, "^k", transform=axes.get_xaxis_transform(), clip_on=False)

    
    # Adjust axis length and labels
    axes.set_xlabel("$x$")
    axes.xaxis.set_label_coords(args["xlabel_coord"], 0, transform=axes.get_yaxis_transform())
    axes.yaxis.set_label_coords(0, args["ylabel_coord"], transform=axes.get_xaxis_transform())

    if args["adjust_ticks"]:
        axes.set_ylim(top=max(abs(y)) * 1.1)
        # Adjust x ticks and labels
        if args["include_zero"]:
            axes.set_xticks([x[0], x_p, 0, x_n, x[-1]], ["$-w_p$", "$x_p$", "$0$", "$x_n$", "$w_n$"])
        else:
            axes.set_xticks([x[0], x_p, x_n, x[-1]], ["$-w_p$", "$x_p$", "$x_n$", "$w_n$"])

    # Return line object drawn in axes
    return line


def render_rho(axes, x, y):
    """
    Adjust render() to plot charge density
    """

    # Set y label, call render(), change y ticks and labels
    axes.set_ylabel("$\\rho(x)$", rotation=0)
    render(axes, x, y, "Raumladungsdichte")
    axes.set_yticks([min(y), max(y)], ["$-e N_A$", "$e N_D$"])


def render_E(axes, x, y):
    """
    Adjust render() to plot field strength
    """

    # Set y label, call render(), change y axis length, change y ticks and labels
    axes.set_ylabel("$E(x)$", rotation=0)
    render(axes, x, y, "Feldstärke")
    axes.set_ylim(top=max(abs(y)) / 2)
    axes.set_yticks([-max(abs(y))], ["$\\dfrac{e}{ \\epsilon } N_A x_p$"])


def render_phi(axes, x, y):
    """
    Adjust render() to plot potential
    """

    # Set y label, call render(), change y ticks and labels
    axes.set_ylabel("$\\varphi(x)$", rotation=0)
    render(axes, x, y, "Potential", include_zero=True)
    axes.set_yticks([max(abs(y))], ["$U_D$"])


def render_W(axes, x, y):
    """
    Adjust render() to plot band structure
    """

    # Call render() for W_V, plot W_C, remove y ticks
    render(axes, x, y, "Bandverläufe", label="$W_V$", arrow=False, bottom=True)[0]
    axes.plot(x, y + fill_values(W_g), "C1", label="$W_C$")
    axes.set_yticks([], [])
    # Change y axis length, plot arrow tip for y axis in bottom position
    axes.set_ylim(auto=True)
    axes.plot(1, y[-1], ">k", transform=axes.get_yaxis_transform(), clip_on=False)
    # Readjust x axis label position
    axes.xaxis.set_label_coords(1.025, y[-1], transform=axes.get_yaxis_transform())
    # Hide y axis
    axes.spines[["left"]].set_visible(False)

    # Add legend
    h, l = axes.get_legend_handles_labels()
    axes.legend(h[::-1], l[::-1], loc="lower left")

    # Draw indicator for band change
    YSCALE = 0.1 * y[-1]
    arrow = Arrow((1.5 * x_n, -1 * YSCALE), (1.5 * x_n, YSCALE + y[-1]), arrowstyle="<->", mutation_scale=6)
    axes.add_patch(arrow)
    axes.plot([x[0], x[-1]], [0, 0], color="black", linestyle="--", linewidth=1)
    axes.annotate("$e U_D$", (1.55 * x_n, 0.75 * y[-1]))


def render_current(axes, uu, ii):
    """
    Adjust render() to plot current over voltage
    """

    # Call render() for I(U)
    render(axes, uu, ii, "Strom-Spannungs-Kennlinie", label = "Simulation", center_title = True, adjust_ticks = False)
    
    # Adjust axis labels
    axes.set_xlabel("$U\\ in\\ V$")
    axes.set_ylabel("$I\\ in\\ A$", rotation=0)
    axes.xaxis.set_label_coords(1.07, 0, transform=axes.get_yaxis_transform())
    axes.yaxis.set_label_coords(0, 1.025, transform=axes.get_xaxis_transform())

    # Piecewise linear interpolation of I(U) results
    first_above = uu[-1]
    last_below = round(0.05 * (first_above//0.05), 2)
    UU = interp(first_above, uu.astype(float), ii.astype(float))
    
    # Plot linear approximation
    axes.plot([VOLTAGE_START, last_below, first_above], [0, 0, UU], label="Interpolation")
    
    # Show legend
    axes.legend(loc="lower left")

    # Adjust xticks
    xticks = [round(tick, 2) for tick in axes.get_xticks()]
    xticklabels = [str(tick) for tick in xticks]
    if last_below not in xticks:
        xticks.append(last_below)
        xticklabels.append("$U_F$")
    else:
        index = xticks.index(last_below)
        xticklabels[index] = f"$U_F$ = {last_below}V"
    axes.set_xticks(xticks, xticklabels)

# ----------------------------------------------------------------------------

if __name__ == "__main__":

    if PLOT_PN: # Plot rho(x), E(x), phi(x), W(x)

        if USE_CACHED_PN_VALUES: # Read numpy arrays from save
            try:
                xx, rho_values = read_from_npy("rho_values")
                xx, E_values = read_from_npy("E_values")
                xx, phi_values = read_from_npy("phi_values")
                xx, W_v_values = read_from_npy("W_v_values")
                
                if not HIDE_CACHE_LOG:
                    print("Using previously saved pn-values. Change USE_CACHED_PN_VALUES in generate_graphs.py line 23 to False to calculate new ones instead.")

                x_p = float(fill_values(x_p, parameter=parameter))
                x_n = float(fill_values(x_n, parameter=parameter))

            except FileNotFoundError:
                print("Saved pn-values missing. Please change USE_CACHED_PN_VALUES in generate_graphs.py line 23 to False and try again.")
                exit()

        else: # Calculate numpy arrays to plot

            # Read sympy functions from save
            func_names = ["rho", "E", "phi", "W_v"]
            try:
                for i in func_names:
                    exec(i + " = read_from_file('" + i + "_results.txt', namespace)")
            except FileNotFoundError:
                print("Saved pn-function(s) missing. Please execute modell.py and try again.")
                exit()

            # Calculate relevant x vector
            x_p = float(fill_values(x_p, parameter=parameter))
            x_n = float(fill_values(x_n, parameter=parameter))
            w_p = float(fill_values(w_p, parameter = parameter))
            w_n = float(fill_values(w_n, parameter = parameter))
            xx = linspace(-1 * w_p, w_n, 1000)

            # Lambdify all functions in func_names
            for i in func_names:
                exec(i + "_func = lambdify(x, fill_values(" + i + ", parameter = parameter))", globals())

            # Call lambdified function to create numpy arrays
            rho_values = rho_func(xx)
            E_values = E_func(xx)
            phi_values = phi_func(xx)
            W_v_values = W_v_func(xx)

            # Save numpy arrays to files
            save_to_npy("rho_values", xx, rho_values)
            save_to_npy("E_values", xx, E_values)
            save_to_npy("phi_values", xx, phi_values)
            save_to_npy("W_v_values", xx, W_v_values)

            if not HIDE_CACHE_LOG:
                print("pn-Values saved. You may now change USE_CACHED_PN_VALUES in generate_graphs.py line 23 to True to speed up future calls to this script")

# ----------------------------------------------------------------------------

        # Generate subplots and pass them to render functions
        no_ext_volt_fig, (plt_rho, plt_E, plt_phi, plt_W) = plt.subplots(4, 1)
        no_ext_volt_fig.subplots_adjust(hspace=1.5)

        render_rho(plt_rho, xx, rho_values)
        render_E(plt_E, xx, E_values)
        render_phi(plt_phi, xx, phi_values)
        render_W(plt_W, xx, W_v_values)

# ----------------------------------------------------------------------------

    if PLOT_CURRENT: # Plot current over voltage

        if USE_CACHED_CURRENT_VALUES: # Read numpy arrays from save
            try:
                uu, ii = read_from_npy("I_of_U_results")
                VOLTAGE_START = uu[0]

                if not HIDE_CACHE_LOG:
                    print("Using previously saved I(U)-values. Change USE_CACHED_CURRENT_VALUES in generate_graphs.py line 24 to False to calculate new ones instead.")

            except FileNotFoundError:
                print("Saved current-values missing. Please change USE_CACHED_CURRENT_VALUES in generate_graphs.py line 24 to False and try again.")
                exit()

        else: # Calculate numpy arrays to plot
            
            # Additional imports
            from modell import calculate_current as cc

            # Setup
            VOLTAGE_START = 0
            uu_list = [VOLTAGE_START]
            ii_list = [0]

            # Calculate new values until |ii|*ampere >= |THRESHOLD|*ampere
            while ii_list[-1] < THRESHOLD:
                ii_list.append(cc(parameter, uu_list[-1]))
                uu_list.append(uu_list[-1]+0.01)

            # Fix value shift
            uu_list.pop(-1)
            ii_list.pop(0)

            # Generate numpy arrays
            uu = array(uu_list)
            ii = array(ii_list)

            # Save numpy arrays to file
            save_to_npy("I_of_U_results", uu, ii)
            
            if not HIDE_CACHE_LOG:
                print("I(U) Values saved. You may now change USE_CACHED_CURRENT_VALUES in generate_graphs.py line 24 to True to speed up future calls to this script")

        # Generate new axes in seperate figure and call render_current()
        plt.figure()
        axes = plt.gca()

        render_current(axes, uu, ii)

# ----------------------------------------------------------------------------

    # Show figure(s)
    plt.show()
