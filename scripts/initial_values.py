from symbols import material_parameters as m_keys
from symbols import constants as c_keys
from pandas import DataFrame
import json

# Number of digits to display when passing `float` to `create_data_frame_pdf()`
FLOAT_DIGITS = 3

# Path to find parameters.json - Physically acurate values can be found in *../initial_values/default_parameters.json*
JSON_PATH = "../initial_values/parameters.json"

# Path to create Initial Parameters.pdf
PDF_PATH = "../initial_values/Initial Parameters.pdf"
PDF_PATH = PDF_PATH[:-4]


def build_data_frame(name, var=0):
    """
    Returns `pandas.DataFrame` instance with quantities defined in *symbols.py* and corresponding values from *JSON_PATH*

    Parameters
    : **name** *(string)* Key to dictionary from *JSON_PATH*
    : **var** *(bool)* 0 to define material parameters, 1 to define universal constants
    """
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


def create_data_frame_tex(df, name):
    """
    Creates *../initial_values/**name**.tex* with LATEX Table containing **df** contents.

    Parameters
    : **df** *(pandas.DataFrame)* Data to be rendered
    : **name** *(string)* Desired file name
    """
    with open("../initial_values/" + name + ".tex", "w", encoding="utf8") as file:
        float_format = "{:." + str(FLOAT_DIGITS) + "f}"
        file.write(df.to_latex(formatters={
            "Symbol": lambda x: "$" + x.name + "$",
            "Ordnung": lambda y: "$10^{" + str(y) + "}$" if y != 0 else 1,
            "Einheit": lambda z: display_unit(z)
        }, float_format=float_format.format
        ))


def create_pdf(name_list):
    """
    Creates pdf at *PDF_PATH* with LATEX Table containing **name_list** contents.

    Parameters
    : **name_list** *(list of strings)* .tex files to be included
    """
    from pylatex import Document, Command, Section
    doc = Document("basic")
    doc.preamble.append(Command("usepackage", "booktabs"))
    doc.append(Command("noindent"))
    for name in name_list:
        with doc.create(Section(name)):
            doc.append(Command("input", name + ".tex"))
    doc.generate_pdf(PDF_PATH,
                     compiler="pdfLaTeX")


"""
Create **values** dictionary with key : DataFrame pairs
for material parameters and universal constants as defined
in `symbols.py` and `JSON_PATH`
"""

with open(JSON_PATH, "r", encoding="utf8") as file:
    parameters = json.load(file)
parameters.pop("Hinweise")

values = {}

for key in parameters.keys():
    typ = 0
    if key == "Naturkonstanten":
        typ = 1
    values[key] = build_data_frame(key, typ)


if __name__ == "__main__":
    """
    Execute create_pdf()
    """
    name_list = []
    for key in values.keys():
        name_list.append(key)
        create_data_frame_tex(values[key], key)
    create_pdf(name_list)
