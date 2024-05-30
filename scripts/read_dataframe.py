from initial_values import values
from symbols import *

default_parameter = {
    N_a: 2.25 * (10 ** 17) * (centimeter ** -3),
    N_d: 5 * (10 ** 17) * (centimeter ** -3),
    T: 300 * kelvin,
    U_ext : 0 * volt
}

ELEMENT = "Si"

def fill_values(func_in, parameter = default_parameter, element=ELEMENT, recursive_call=False):
    """
    Returns `sympy.expression` instance with all possible parameters substituted for their values

    Parameters
    : **func_in** *(sympy.expression)* Expression to fill with values
    : **element** *(string)* Optional, which element's values to choose from. Default set in ELEMENT
    """

    names = func_in.free_symbols

    # Check dataframe for elements of names
    for df in ["Naturkonstanten", "Materialparameter " + element]:
        for index, konst in values[df].iterrows():
            # Read Dataframe entry
            s = konst.Symbol
            v = konst.Koeffizient * (10 ** konst.Ordnung)
            u = konst.Einheit

            if u == electron_volt and not recursive_call:
                v = v * fill_values(q_e, recursive_call = True)
            # Check for matching symbols
            if s in names:
                # Substitute symbol for value * unit
                func_in = func_in.subs(s, v * u)

    # Check parameter dict for elements of names
    for s in parameter.keys():
        # Check for matching symbols
        if s in names:
            # Substitute symbol for value * unit
            func_in = func_in.subs(s, parameter[s])

    # Units containing prefixes have been converted to full ones in the previous steps
    # thanks to how they were defined in symbols.py - E.g. centimeter = meter/100
    for unit in full_units:
        try: func_in = func_in.subs(unit, 1)
        except: pass

    return func_in