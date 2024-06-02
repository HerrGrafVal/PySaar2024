from initial_values import values
from symbols import *

default_parameter = {
    N_a: 2.25 * (10 ** 17) * (centimeter ** -3),
    N_d: 5 * (10 ** 17) * (centimeter ** -3),
    T: 300 * kelvin,
    W_t : 0.5 * W_g,
    U_ext : 0 * volt,
    "N-Dotation" : "As",
    "P-Dotation" : "B"
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
            if W_g in func_in.free_symbols:
                func_in = fill_values(func_in, parameter = parameter, element = element)

    # Units containing prefixes have been converted to full ones in the previous steps
    # thanks to how they were defined in symbols.py - E.g. centimeter = meter/100
    for unit in full_units:
        try: func_in = func_in.subs(unit, 1)
        except: pass


    if tau_n in func_in.free_symbols:
        func_in = func_in.subs(tau_n, pick_tau(typ = "n", parameter = parameter))
    
    if tau_p in func_in.free_symbols:
        func_in = func_in.subs(tau_p, pick_tau(typ = "p", parameter = parameter))

    return func_in

def pick_tau(typ, parameter):
    from math import floor, log10
    if typ == "n":
        dot = float(parameter[N_d] * (centimeter ** 3))
        mag = floor(log10(dot))
        mu = values["Beweglichkeiten von Majoritätsträgern"].loc()[mag]
        return mu[parameter["N-Dotation"]]
    elif typ == "p":
        dot = float(parameter[N_a] * (centimeter ** 3))
        mag = floor(log10(dot))
        mu = values["Beweglichkeiten von Majoritätsträgern"].loc()[mag]
        return mu[parameter["P-Dotation"]]