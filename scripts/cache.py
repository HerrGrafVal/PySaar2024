import pickle
from symbols import *
from sympy import sympify
from numpy import array, save, load
# from tikzplotlib import save as fig_to_tex

# ----------------------------------------------------------------------------

# Relative path to save folder. Must end with "/"!
SAVE_FOLDER = "../simulation_results/"

# ----------------------------------------------------------------------------

def read_from_file(filename, namespace):
    """
    | Returns sympy expression instance from *SAVE_FOLDER/filename*
    | Returned expression uses working symbols from provided namespace
    | Useful to retrieve expressions saved with ``save_to_file()``

    :param filename: Filename (excluding data type suffix) to read. Must be .txt
    :type filename: string
    :param namespace: See *symbols.py* where ``namespace = dir()``
    :type namespace: list[str]
    :return: Sympy expression
    :rtype: sympy.expression
    """

    filename += ".txt"
    ns = {}
    for var in namespace:
        if "__" not in var:
            temp = eval(var)
            name = str(temp)
            name = name.replace("\\", "")
            if type(temp) in [type(x), type(rho)]:
                ns[name] = temp
    with open(SAVE_FOLDER + filename, "r") as file:
        expr_str = file.read()
    expr_str = expr_str.replace("\\", "")
    expr_str = expr_str.replace("U_{ext}", "VOLTAGE")
    ns["VOLTAGE"] = U_ext
    expr = sympify(expr_str, locals=ns)
    return expr


def save_to_file(filename, expr):
    """
    | Saves *expr* to *SAVE_FOLDER/filename*
    | Retrieve saved expression with ``read_from_file()``

    :param filename: Filename (excluding data type suffix .txt) to write
    :type filename: string
    :param expr: Sympy expression to save
    :type expr: sympy.expression
    :return: *None*
    """

    filename += ".txt"
    with open(SAVE_FOLDER + filename, "w") as file:
        file.write(str(expr))


def save_to_npy(filename, x, y):
    """
    | Saves 2d ``numpy.array([x, y])`` to *SAVE_FOLDER/filename*
    | Useful to save data ready to be plotted
    | Retrieve saved data with ``read_from_npy()``

    :param filename: Filename (excluding data type suffix) to write
    :type filename: string
    :param x: First array to save
    :type x: numpy.array
    :param y: Second array to save
    :type y: numpy.array
    :return: *None*
    """

    values = array([x, y])
    save(SAVE_FOLDER + filename + ".npy", values)


def read_from_npy(filename):
    """
    | Returns *list[numpy.array]* from *SAVE_FOLDER/filename*
    | Useful to retrieve data saved with ``save_to_npy()``

    :param filename: Filename (excluding data type suffix) to read. Must be *.npy* file
    :type filename: string
    :return: ``[x, y]`` 2d Array
    :rtype: *numpy.array*
    """

    values = load(SAVE_FOLDER + filename + ".npy", allow_pickle=True)
    x = values[0]
    y = values[1]
    return [x, y]


def check_savefoler():
    """
    | Checks for directory at SAVE_FOLDER and creates one if necessary
    | Executed upon import of *scripts/cache.py*

    :return: *None*
    """

    import os
    if os.path.isdir(SAVE_FOLDER):
        return
    else:
        os.mkdir(SAVE_FOLDER)


def pickle_save(obj, filename):
    """
    | Saves *obj* to *SAVE_FOLDER/filename*
    | Retrieve saved object with ``pickle_read()``

    :param obj: Object to pickle
    :type obj: object
    :param filename: Filename (excluding data type suffix) to write
    :type filename: string
    :return: *None*
    """

    with open(SAVE_FOLDER + filename + ".pkl", "wb") as file:
        pickle.dump(obj, file)


def pickle_read(filename):
    """
    | Returns object saved at *SAVE_FOLDER/filename*
    | Useful to retrieve data saved with ``pickle_save()``

    :param filename: Filename (excluding data type suffix) to read. Must be *.pkl* file
    :type filename: string
    :return: Object
    :rtype: *object*
    """

    with open(SAVE_FOLDER + filename + ".pkl", "rb") as file:
        obj = pickle.load(file)
    return obj


def plt_to_tex(filename, fig):
    """
    | This functions **remains unused** . While TikZ figures are preferred over *.png*
    | tikzplotlib messes with figure labels and layout. Reverting those changes is doable,
    | but not feasable after going through the effort to create them in matplotlib.
    | See *pdf_plot_test.py* in previous git commits (branch: dev)
    | See README in said commit on how to hotfix tikzplotlib
    | 
    | Reenable import in line 4 to make this functional
    | 
    | **plt_to_tex** ( *filename, fig* )
    | Generates TikZ figure and saves tex at `SAVE_FOLDER/filename`

    :param filename: Filename (without data type suffix) to write
    :type filename: string
    :param fig: Figure to tex with ``tikzplotlib.save()``
    :type fig: matplotlib.Figure
    :return: *None*
    """

    fig_to_tex(SAVE_FOLDER + filename + ".tex", figure=fig, strict=True)

# ----------------------------------------------------------------------------
# Execute upon import

check_savefoler()
