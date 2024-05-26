from sympy import sympify
from symbols import *

SAVE_FOLDER = "../simulation_results/"

def read_from_file(filename, namespace):
    """
    Returns `sympy.expression` instance with working symbols

    Parameters
    : **filename** *(string)* Filename (including data type suffix) to read
    : **namespace** *(list)* dir() from symbols.py
    """

    ns = {"e" : q_e}
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
    expr = sympify(expr_str, locals = ns)
    return expr

def save_to_file(filename, expr):
    """
    Saves `expr` to `simulation_results/filename`

    Parameters
    : **filename** *(string)* Filename (including data type suffix) to write to
    : **expr** *(sympy expression)* to save
    """

    with open(SAVE_FOLDER + filename, "w") as file:
        file.write(str(expr))