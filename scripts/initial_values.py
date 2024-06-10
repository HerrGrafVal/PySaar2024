from symbols import material_parameters as m_keys
from symbols import constants as c_keys
from symbols import second
from pandas import DataFrame
import json

# ----------------------------------------------------------------------------

# Number of digits to display when passing `float` to `create_data_frame_pdf()`
FLOAT_DIGITS = 3

# Path to find parameters.json - Physically acurate values can be found in *../initial_values/default_parameters.json*
JSON_PATH = "../initial_values/parameters.json"

# Path to create Initial Parameters.pdf
PDF_PATH = "../initial_values/Initial Parameters.pdf"
PDF_PATH = PDF_PATH[:-4]

# ----------------------------------------------------------------------------

def build_data_frame(name, var=0):
    """
    Returns `pandas.DataFrame` instance with quantities defined in *symbols.py* and corresponding values from *JSON_PATH*

    Parameters
    : **name** *(string)* Key to dictionary from *JSON_PATH*
    : **var** *(int)* 0 to define material parameters, 1 to define universal constants, 2 for tau, 3 for mu
    """

    if var == 2:
        # Lebensdauer-Zeitkonstanten der Minoritäten
        content = parameters[name]
        content.pop("Halbleiter Element")
        df = DataFrame({"Von": [], "Bis": [], "Einheit": []})
        for element in content.keys():
            df.loc[element] = [*content[element], second]
        df.columns.name = "Halbleiter"

    elif var == 3:
        # Beweglichkeit von Majoritätsträgern
        parameters[name].pop("Halbleiter Element")

        # Currently only returning last substrat values, "Si" in default_parameters.json
        substrat = list(parameters[name].keys())
        for sub in substrat:
            content = parameters[name][sub]
            magnitudes = content.pop("N/cm^3")
            df = DataFrame(content)
            df.columns.name = "$N/cm^3$"
            shift = {}
            for i in range(len(magnitudes)):
                shift[i] = magnitudes[i]
            df.rename(index = shift, inplace = True)

    else:
        # Materialparameter & Naturkonstanten
        df = DataFrame({"Symbol": [], "Koeffizient": [],
                        "Ordnung": [], "Einheit": []})
        keys = m_keys
        if var:
            keys = c_keys
        for i in keys:
            df.loc[i.desc] = [i, *parameters[name][i.desc], i.unit]
        df.columns.name = name

    return df


def display_unit(unit_in):
    """
    Returns string in LATEX math format, after checking for missing unit prefixes
    Necessary since `cm` is defined as `m/100` in *symbols.py* to avoid unit errors during calculations.
    E.g. cm^-3 is displayed as 1000000/m**3 while it should be $cm^-3$

    Also renders units such as A * s / (V * m) to Latex Fraction

    Will not work on units with multiple missing prefixes!

    Does not need to work on units like cm^1 since conversion to base units should be done
    by lowering exponent in symbols.py accordingly instead of using prefixes.

    This is achieved by converting `sympy.core.mul.Mul` type to string,
    then splitting it at "**" and isolating unit abbreviation and power.
    Going smallest to largest checking wether prefixes apply,
    then modifying string to desired output.

    Parameters
    : **unit_in** *(sympy.core.mul.Mul or sympy.Symbol)* Unit to be rendered in LATEX
    """
    text = str(unit_in)
    try:
        unit, power = text.split("**")
        unit = unit.split("/")[-1]
        power = int(power[0])
        if "/m" in text:
            if str(1000**power) in text:
                unit = "m" + unit
            elif str(100**power) in text:
                unit = "c" + unit
            power *= -1
        return "$" + unit + "^{" + str(power) + "}$"

    # Remove unnecessary arithmetic symbols before rendering
    except:
        if "*" in text:
            text = text.replace("*", "")
        if "/" in text:
            numerator, denominator = text.split("/")
            text = "\\frac{" + numerator + "}{" + denominator + "}"
        if "(" in text:
            text = text.replace("(", "")
        if ")" in text:
            text = text.replace(")", "")
    return "$" + text + "$"


def create_data_frame_tex(df, name, typ):
    """
    Creates *../initial_values/**name**.tex* with LATEX Table containing **df** contents.

    Parameters
    : **df** *(pandas.DataFrame)* Data to be rendered
    : **name** *(string)* Desired file name
    : **typ** *(int)* 0 for material parameters or universal constants, 2 for tau, 2 for mu
    """
    name = name.replace("-", "")

    with open("../initial_values/" + name + ".tex", "w", encoding="utf8") as file:
        float_format = "{:." + str(FLOAT_DIGITS) + "f}"

        if typ == 0: # Materialparameter & Naturkonstanten
            file.write(df.to_latex(formatters={
                "Symbol": lambda x: "$" + x.name + "$",
                "Ordnung": lambda y: "$10^{" + str(y) + "}$" if y != 0 else 1,
                "Einheit": lambda z: display_unit(z)
            }, float_format=float_format.format
            ))
        elif typ == 2: # Lebensdauer-Zeitkonstanten der Minoritäten
            file.write(df.to_latex(formatters={
                    "Von": lambda x: "$10^{" + str(x) + "}$",
                    "Bis": lambda y: "$10^{" + str(y) + "}$",
                }))
        elif typ == 3: # Beweglichkeit von Majoritätsträgern
            df.rename(index = {(x):("$10^{" + str(x) + "}$") for x in list(df.index)}, inplace = True)
            file.write(df.to_latex())


def create_pdf(name_list):
    """
    Creates pdf at *PDF_PATH* with LATEX Table containing **name_list** contents.

    Parameters
    : **name_list** *(list of strings)* .tex files to be included
    """
    from pylatex import Document, Command, Section, NoEscape
    doc = Document("basic")
    doc.preamble.append(Command("usepackage", "booktabs"))
    doc.append(Command("noindent"))
    for name in name_list:
        name = name.replace("-", "")
        with doc.create(Section(name)):
            doc.append(Command("input", name + ".tex"))
            if name == "Beweglichkeiten von Majoritätsträgern":
                doc.append(NoEscape("$[\\mu]$ $=$ $\\frac{cm^{2}}{Vs}$"))
    doc.generate_pdf(PDF_PATH,
                     compiler="pdfLaTeX")

# ----------------------------------------------------------------------------

"""
Create **values** dictionary with key : DataFrame pairs
for material parameters and universal constants as defined
in `symbols.py` and `JSON_PATH`
"""

with open(JSON_PATH, "r", encoding="utf8") as file:
    parameters = json.load(file)
parameters.pop("Materialparameter & Naturkonstanten")

values = {}

for key in parameters.keys():
    typ = 0
    if key == "Naturkonstanten":
        typ = 1
    elif key == "Lebensdauer-Zeitkonstanten der Minoritäten":
        typ = 2
    elif key == "Beweglichkeiten von Majoritätsträgern":
        typ = 3
    values[key] = build_data_frame(key, typ)

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Execute create_pdf()
    """
    name_list = []
    for key in values.keys():
        typ = 0
        if key == "Lebensdauer-Zeitkonstanten der Minoritäten":
            typ = 2
        elif key == "Beweglichkeiten von Majoritätsträgern":
            typ = 3
        name_list.append(key)
        create_data_frame_tex(values[key], key, typ)
    create_pdf(name_list)
