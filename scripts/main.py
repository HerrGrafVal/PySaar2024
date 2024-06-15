import json
from read_dataframe import ELEMENT
from cache import SAVE_FOLDER, pickle_read
from initial_values import JSON_PATH, PARAM_FOLDER
from pylatex import Document, Command, Section, NoEscape

# ----------------------------------------------------------------------------

# Output path for generated pdf file, excluding data type suffix!
PDF_PATH = "../SIMULATION RESULTS"

# ----------------------------------------------------------------------------
# Setup
# Get all simulation results ready

def get_graph_path(name):
    """
    | Performs some string concatenation

    :param name: Graph name, e.g. "phi"
    :type name: string
    :return: Full file path to graph .png
    :rtpye: *string*
    """
    path = SAVE_FOLDER + name + "_graph.png"
    return path

with open(JSON_PATH, "r", encoding="utf8") as file:
    values = json.load(file)
diode_dict = values["Diode"]

U_F = pickle_read("V_min")

tex_paths = {
    "mu": PARAM_FOLDER + "Beweglichkeiten von Majoritätsträgern.tex",
    "tau": PARAM_FOLDER + "Lebensdauer Zeitkonstanten der Minoritäten.tex",
    "constants": PARAM_FOLDER + "Naturkonstanten.tex",
    "parameters": PARAM_FOLDER + "Materialparameter " + ELEMENT + ".tex"
    }

# ----------------------------------------------------------------------------
# Create tex

doc = Document("basic")
doc.preamble.append(Command("usepackage", "booktabs"))











# ----------------------------------------------------------------------------
# Create pdf
doc.generate_pdf(PDF_PATH, compiler = "pdfLaTeX")