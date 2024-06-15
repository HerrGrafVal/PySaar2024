import json
from symbols import second
from pandas import DataFrame
from symbols import diode as d_keys
from symbols import constants as c_keys
from symbols import material_parameters as m_keys

# ----------------------------------------------------------------------------

# Number of digits to display when passing `float` to `create_data_frame_pdf()`
FLOAT_DIGITS = 3

# Relative path to the folder containing json with parameters. Corresponding pdf will be saved here. 
# Must end in "/"
PARAM_FOLDER = "../initial_values/"

# File name for parameters. Must end in ".json"
# Physically acurate values can be found in *../initial_values/default_parameters.json*
JSON_FILE_NAME = "parameters.json"

# File name for parameter pdf. Must end in ".pdf"
PDF_FILE_NAME = "Initial Parameters.pdf"

# Don't change anything here
JSON_PATH = PARAM_FOLDER + JSON_FILE_NAME
PDF_PATH = PARAM_FOLDER + PDF_FILE_NAME
PDF_PATH = PDF_PATH[:-4]

# ----------------------------------------------------------------------------

def build_data_frame(name, var=0):
    """
    | Returns pandas DataFrame instance with quantities defined in *scripts/symbols.py*
    | and corresponding values from *JSON_PATH*

    :param name: Json dict key, used as DataFrame name
    :type name: string
    :param var: 0 for material parameters, 
                1 for universal constants, 
                2 for tau, 
                3 for mu, 
                4 for diode parameters
    :type var: int
    :return: Data Frame
    :rtype: *pandas.DataFrame*
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

    elif var == 4:
        # Diode
        content = parameters[name]
        df = DataFrame({"Symbol": [], "Koeffizient": [],
                        "Ordnung": [], "Einheit": []})
        for i in d_keys:
            df.loc[i.desc] = [i, *content[i.desc], i.unit]
        df.loc["Donator Atomsorte"] = [content["Donator Atomsorte"], 0,0,0]
        df.loc["Akzeptor Atomsorte"] = [content["Akzeptor Atomsorte"], 0,0,0]
        df.columns.name = name

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
    | Returns string in LATEX math format, after checking for missing unit prefixes
    | Necessary since ``cm`` is defined as ``m/100`` in *scripts/symbols.py* to avoid unit errors during calculations.
    | Example: ``cm^-3`` is displayed as ``1000000/m**3`` while it should be ``$cm^-3$``
    | 
    | Renders units such as ``A * s / (V * m)`` in LaTeX fractions
    | 
    | Will not work on units with multiple missing prefixes!
    | 
    | Does not need to work on units like cm^1 since conversion to base units should be done
    | by lowering exponent in *scripts/symbols.py* accordingly instead of using prefixes.
    | 
    | This is achieved by converting ``sympy.core.mul.Mul`` type to string,
    | then splitting it at \\"\\*\\*\\" and isolating unit abbreviation and power.
    | Going smallest to largest checking wether prefixes apply, then modifying string to desired output.

    :param unit_in: Unit to be rendered in LaTeX
    :type unit_in: sympy.core.mul.Mul or sympy.Symbol
    :return: LaTeX ready unit
    :rtype: *string*
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
    | Creates *PARAM_FOLDER/name.tex* with LaTeX Table containing DataFrame contents

    :param df: Data to be rendered
    :type df: pandas.DataFrame
    :param name: Desired file name (without data type suffix) 
    :type name: string
    :param typ: 0 for material parameters or universal constants, 2 for tau, 3 for mu
    :type typ: int
    :return: *None*
    """

    name = name.replace("-", " ")

    with open(PARAM_FOLDER + name + ".tex", "w", encoding="utf8") as file:
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
    | Creates pdf at *PDF_PATH* with LaTeX tables
    | Executed if __name__ == "__main__"

    :param name_list: .tex files to include. List entries without data type suffix!
    :type name_list: list[string]
    """

    from pylatex import Document, Command, Section, NoEscape
    doc = Document("basic")
    doc.preamble.append(Command("usepackage", "booktabs"))
    doc.append(Command("noindent"))
    for name in name_list:
        name = name.replace("-", " ")
        with doc.create(Section(name)):
            doc.append(Command("input", name + ".tex"))
            if name == "Beweglichkeiten von Majoritätsträgern":
                doc.append(NoEscape("$[\\mu]$ $=$ $\\frac{cm^{2}}{Vs}$"))
    doc.generate_pdf(PDF_PATH,
                     compiler="pdfLaTeX")

# ----------------------------------------------------------------------------
# Create **values** dictionary with key : DataFrame pairs
# for material parameters and universal constants as defined
# in `symbols.py` and `JSON_PATH`

try:
    with open(JSON_PATH, "r", encoding="utf8") as file:
        parameters = json.load(file)
    parameters.pop("Materialparameter & Naturkonstanten")
except FileNotFoundError:
    print("No proper file found at", JSON_PATH)
    print("Take a look at default_parameters.json")
    exit()

values = {}

for key in parameters.keys():
    typ = 0
    if key == "Naturkonstanten":
        typ = 1
    elif key == "Lebensdauer-Zeitkonstanten der Minoritäten":
        typ = 2
    elif key == "Beweglichkeiten von Majoritätsträgern":
        typ = 3
    elif key == "Diode":
        typ = 4
    values[key] = build_data_frame(key, typ)

# ----------------------------------------------------------------------------

if __name__ == "__main__":

    # Execute create_pdf()
    name_list = []
    for key in values.keys():
        typ = 0
        if key == "Lebensdauer-Zeitkonstanten der Minoritäten":
            typ = 2
        elif key == "Beweglichkeiten von Majoritätsträgern":
            typ = 3
        if key != "Diode": 
            name_list.append(key)
        create_data_frame_tex(values[key], key, typ)
    create_pdf(name_list)

    try:
        # Open generated pdf file in default application.
        # Tested on Windows 10 only
        import os
        cmd = '"' + PDF_PATH + '.pdf"'
        os.system(cmd)
    except:
        pass
    print(PDF_FILE_NAME, "generated at", PARAM_FOLDER)
