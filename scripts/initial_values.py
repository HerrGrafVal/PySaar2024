from symbols import material_parameters as keys
import json

# Number of digits to display when passing `float` to `create_data_frame_pdf()`
FLOAT_DIGITS = 3


def build_data_frame():
    """
    Returns `pandas.DataFrame` instance with quantities defined in *symbols.py* and matching values from *../initial_values/*
    """
    import pandas as pd
    df = pd.DataFrame({"Symbol": [], "Koeffizient": [],
                       "Ordnung": [], "Einheit": []})
    for i in keys:
        df.loc[i.desc] = [i, *material_parameters["Si"][i.desc], i.unit]
    return df


def display_unit(unit_in):
    """
    Returns string in LATEX math format, after checking for missing unit prefixes
    Necessary since `cm` is defined as `100*m` in *symbols.py* to avoid unit errors during calculations.
    E.g. cm^-3 is displayed as 1/1000000*m**3 while it should be $cm^-3$

    Will not work on units with multiple missing prefixes!

    Does not need to work on units like cm^1 since conversion to base units should be done
    by lowering exponent in symbols.py accordingly instead of using prefixes.

    This is achieved by converting `sympy.core.mul.Mul` type to string,
    then splitting it at "**" and isolating unit abbreviation and power.
    Going smallest to biggest checking wether prefixes apply,
    then modifying string to desired output.

    Parameters
    : **unit_in** *(sympy.core.mul.Mul or sympy.physics.units.unit)* Unit to be rendered in LATEX
    """
    text = str(unit_in)
    try:
        unit, power = text.split("**")
        unit = unit.split("*")[-1]
        power = int(power[0])
        if "1/" in text:
            if str(1000**power) in text:
                unit = "m" + unit
            elif str(100**power) in text:
                unit = "c" + unit
            power *= -1
        return unit + "$^{" + str(power) + "}$"
    except:
        pass
    return "$" + text + "$"


def create_data_frame_pdf(df):
    """
    Creates *../initial_values/Initial Parameters.pdf* with LATEX Table containing **df** contents.

    Parameters
    : **df** *(pandas.DataFrame)* Data to be rendered
    """
    from pylatex import Document, Command
    with open("../initial_values/pandas.tex", "w", encoding="utf8") as file:
        float_format = "{:." + str(FLOAT_DIGITS) + "f}"
        file.write(df.to_latex(formatters={
            "Symbol": lambda x: "$" + x.name + "$",
            "Ordnung": lambda y: "$10^{" + str(y) + "}$" if y != 0 else 1,
            "Einheit": lambda z: display_unit(z)
        }, float_format=float_format.format
        ))
    doc = Document("basic")
    doc.preamble.append(Command("usepackage", "booktabs"))
    doc.append(Command("noindent"))
    doc.append(Command("input", "pandas.tex"))
    doc.generate_pdf("../initial_values/Initial Parameters",
                     compiler="pdfLaTeX")


with open("../initial_values/material_parameters.json", "r", encoding="utf8") as file:
    material_parameters = json.load(file)
material_parameters.pop("Hinweise")

values = build_data_frame()

if __name__ == "__main__":
    create_data_frame_pdf(values)
