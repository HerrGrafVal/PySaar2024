from sympy import sympify
from symbols import *
from numpy import array, save, load

SAVE_FOLDER = "../simulation_results/"

def read_from_file(filename, namespace):
    """
    Returns `sympy.expression` instance with working symbols

    Parameters
    : **filename** *(string)* Filename (including data type suffix .txt) to read
    : **namespace** *(list)* dir() from symbols.py
    """

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
    expr = sympify(expr_str, locals = ns)
    return expr

def save_to_file(filename, expr):
    """
    Saves `expr` to `simulation_results/filename`

    Parameters
    : **filename** *(string)* Filename (including data type suffix .txt) to write to
    : **expr** *(sympy expression)* to save
    """

    with open(SAVE_FOLDER + filename, "w") as file:
        file.write(str(expr))

def save_to_npy(filename, x, y):
    """
    Saves `numpy array from x, y` to `simulation_results/filename`

    Parameters
    : **filename** *(string)* Filename (without data type suffix) to write to
    : **[x, y]** *(numpy.arrays)* to save
    """

    values = array([x, y])
    save(SAVE_FOLDER + filename + ".npy", values)

def read_from_npy(filename):
    """
    Returns `list` of `numpy.arrays` from `simulation_results/filename`

    Parameters
    : **filename** *(string)* Filename (without data type suffix) to read from, must be .npy
    """

    values = load(SAVE_FOLDER + filename + ".npy", allow_pickle = True)
    x = values[0]
    y = values[1]
    return [x, y]

def check_savefoler():
    """
    Checks for directory at SAVE_FOLDER and creates one if required
    """

    import os
    if os.path.isdir(SAVE_FOLDER):
        return
    else:
        os.mkdir(SAVE_FOLDER)

check_savefoler()