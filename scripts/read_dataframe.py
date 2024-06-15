from initial_values import values
from functools import cache
from symbols import *

# ----------------------------------------------------------------------------

# Semiconductor substrate to use for simulations
ELEMENT = "Si"

# See WIDTH.desc in scripts/symbols.py
default_parameter = {
    U_ext : 0 * volt,
    WIDTH : 3
}

# ----------------------------------------------------------------------------

def populate_dict(element=ELEMENT):
    """
    | Popultates json_parameter dict with values from pandas DataFrames
    | Implemented after realising that accessing a dictionary is a lot faster than a DataFrame
    | Executed upon import of *scripts/read_dataframe.py*
    |
    | This makes creation of the DataFrames unnecessary outside of pdf creation.
    | **ToDo:** Adjust *scripts/initial_values.py* accordingly

    :param element: Semiconductor substrate to fetch values from
    :type element: string
    :returns: *None*
    """

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
    | Returns sympy.expression instance where all possible symbols are substituted for their numeric values
    | Returns float if all symbols can be substituted
    | Returns unchanged input if said input contains no symbols
    | All substituted values are in full base units [1]_

    :param func_in: Expression to fill with values
    :type func_in: sympy.expression
    :param parameter: Parameters to use instead of default (json) ones, 
                      see *scripts/read_dataframe.py* line 11 ``default_parameter`` for syntax
    :type parameter: dict
    :param element: Semiconductor substrate to fetch values from
    :type element: string
    :param recursive_call: For internal use only!
    :type recursive_call: bool
    :param eV: Whether output should be in eV instead of J,
               Only use this if you know what you're doing!
    :type eV: bool
    :returns: func_in, with as little symbols left as possible
    :rtype: *float* when possible, *sympy.expression* otherwise

    .. [1] Unless eV = True 
    """

    try:
        names = func_in.free_symbols
    except AttributeError:
        print("fill_values() received non sympy input. Returns input unchanged.")
        return func_in

    # Update default_parameter with those from function argument without modifying orginial dict
    parameter = {**default_parameter, **parameter}

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
    """
    | Returns appropriate tau value depending on semiconductor substrate
    | Called from ``read_dataframe.fill_values()`` during ``modell.calculate_I_rg()``
    | 
    | This function uses ``@functools.cache`` decorator

    :return: \\{tau\\} \\* 1 second
    :rtype: *sympy.expression*
    """

    df = values["Lebensdauer-Zeitkonstanten der Minoritäten"]
    if ELEMENT not in df.index:
        from initial_values import JSON_PATH
        raise NotImplementedError("No \\tau values for the current substrate available in " + JSON_PATH[3:])
    tau_range = list(df.loc()[ELEMENT])
    # tau_range = [From, To, Unit]
    tau_mag = (tau_range[0] + tau_range[1])/2
    return (10 ** tau_mag) * tau_range[2]

@cache
def pick_mu(typ):
    """
    | Returns appropriate mu value depending on dotation element and magnitude
    | Only has access to Si substrate values, see *scripts/initial_values.py* line 61
    | Called from ``read_dataframe.fill_values()`` during ``modell.calculate_I_s()``
    | 
    | This function uses ``@functools.cache`` decorator

    :param typ: Must be "n" or "p". Set's current charge majority
    :type typ: string
    :return: mu_n or mu_p
    :rtype: int
    """

    from math import floor, log10
    content = values["Diode"]
    if typ == "n":
        dot = float(fill_values(N_d * centimeter ** 3))
        mag = floor(log10(dot))
        mu = values["Beweglichkeiten von Majoritätsträgern"].loc()[mag]
        kind = content.loc()["Donator Atomsorte"].Symbol
    elif typ == "p":
        dot = float(fill_values(N_a * centimeter ** 3))
        mag = floor(log10(dot))
        mu = values["Beweglichkeiten von Majoritätsträgern"].loc()[mag]
        kind = content.loc()["Akzeptor Atomsorte"].Symbol
    if kind in mu.keys():
        return mu[kind]
    else:
        from initial_values import JSON_PATH
        raise NotImplementedError("No \\mu values for the current dotation available in " + JSON_PATH[3:])

# ----------------------------------------------------------------------------

json_parameter = {}
populate_dict()
