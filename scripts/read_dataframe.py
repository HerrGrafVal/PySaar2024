from initial_values import values
from functools import cache
from symbols import *

# ----------------------------------------------------------------------------

ELEMENT = "Si"

default_parameter = {
    U_ext : 0 * volt,
    WIDTH : 3
}

# ----------------------------------------------------------------------------

def populate_dict(element=ELEMENT):
    global json_parameter
    for df in ["Naturkonstanten", "Materialparameter " + element, "Diode"]:
        for index, konst in values[df].iterrows():
            # Read Dataframe entry
            s = konst.Symbol
            v = konst.Koeffizient * (10 ** konst.Ordnung)
            u = konst.Einheit
            json_parameter[s] = [v, u]

def fill_values(func_in, parameter = default_parameter, element=ELEMENT, recursive_call=False, eV = False):
    """
    Returns `sympy.expression` instance with all possible parameters substituted for their values

    Parameters
    : **func_in** *(sympy.expression)* Expression to fill with values
    : **element** *(string)* Optional, which element's values to choose from. Default set in ELEMENT
    """

    # Update default_parameter with those from function argument without modifying orginial dict
    parameter = {**default_parameter, **parameter}

    names = func_in.free_symbols

    # Check parameter dict for matching symbols
    for s in names:
        # Check for matching symbols
        if s in parameter.keys():
            # Substitute symbol for value * unit
            func_in = func_in.subs(s, parameter[s])

            # W_t would be defined as something like 0.5 * W_g
            if W_g in func_in.free_symbols:
                # Substitute W_g value too
                func_in = fill_values(func_in, parameter = parameter, element = element)

    # Reset names before checking json parameters for additional matches
    names = func_in.free_symbols

    # Check json_parameters for matching symbols 
    for s in names:
        if s in json_parameter.keys():
            v, u = json_parameter[s]

            # Keep output unit in eV if desired
            if eV: u = 1

            # Go from eV to J
            if u == electron_volt and not recursive_call:
                v = v * fill_values(q_e, recursive_call = True)

            func_in = func_in.subs(s, v * u)

    if tau_n in func_in.free_symbols:
        func_in = func_in.subs(tau_n, pick_tau()) 
    if tau_p in func_in.free_symbols:
        func_in = func_in.subs(tau_p, pick_tau())

    if mu_n in func_in.free_symbols:
        func_in = func_in.subs(mu_n, pick_mu("n"))
    if mu_p in func_in.free_symbols:
        func_in = func_in.subs(mu_p, pick_mu("p"))

    # Units containing prefixes have been converted to full ones in the previous steps
    # thanks to how they were defined in symbols.py - E.g. centimeter = meter/100
    for unit in full_units:
        try: func_in = func_in.subs(unit, 1)
        except: pass

    # Check if all symbols were substituted, convert to float if possible
    if func_in.free_symbols == set():
        func_in = float(func_in)

    return func_in

@cache
def pick_tau():
    df = values["Lebensdauer-Zeitkonstanten der Minoritäten"]
    tau_range = list(df.loc()[ELEMENT])
    # tau_range = [From, To, Unit]
    tau_mag = (tau_range[0] + tau_range[1])/2
    return (10 ** tau_mag) * tau_range[2]

@cache
def pick_mu(typ):
    # **typ** *(string)* Which charge is the current majority. Must be either "n" or "p"
    from math import floor, log10
    content = values["Diode"]
    if typ == "n":
        dot = float(fill_values(N_d * centimeter ** 3))
        mag = floor(log10(dot))
        mu = values["Beweglichkeiten von Majoritätsträgern"].loc()[mag]
        kind = content.loc()["Donator Atomsorte"].Symbol
        return mu[kind]
    elif typ == "p":
        dot = float(fill_values(N_a * centimeter ** 3))
        mag = floor(log10(dot))
        mu = values["Beweglichkeiten von Majoritätsträgern"].loc()[mag]
        kind = content.loc()["Akzeptor Atomsorte"].Symbol
        return mu[kind]

# ----------------------------------------------------------------------------

json_parameter = {}
populate_dict()
