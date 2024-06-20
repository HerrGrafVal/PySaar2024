import os
import json
from symbols import diode
from read_dataframe import ELEMENT
from cache import SAVE_FOLDER, pickle_read
from initial_values import JSON_PATH, PARAM_FOLDER, display_unit
from pylatex import Document, Command, NewPage, Section, Subsection, NoEscape, Figure

# ----------------------------------------------------------------------------

# Output path for generated pdf file, excluding data type suffix!
# Changes require modification of SAVE_FOLDER and PARAM_FOLDER as they need to be relative paths
PDF_PATH = "../SIMULATION RESULTS"

# Whether or not to keep .tex file
KEEP_TEX = False

# Whether to attempt to open the pdf after generating it
OPEN_PDF = True

# ----------------------------------------------------------------------------

def get_graph_path(name):
    """
    | Performs some string concatenation
    | Needs to be adjusted when PDF_PATH is changed

    :param name: Graph name, e.g. "phi"
    :type name: string
    :return: Relative path from PDF_PATH to graph .png
    :rtpye: *string*
    """

    path = SAVE_FOLDER[3:] + name + "_graph.png"
    return path

def include_img(graph, caption):
    """
    | Adds figure with image at current tex position

    :param graph: For *cc_graph.png* use ``cc``
    :type graph: string
    :param caption: Graph caption
    :type caption: string
    :return: *None*
    """

    with doc.create(Figure(position="h")) as img:
        img.add_image(get_graph_path(graph), width = NoEscape("\\textwidth"))
        img.add_caption(NoEscape(caption))

if __name__ == "__main__":

    # ----------------------------------------------------------------------------
    # User validation
    inp = str(input("Have all over scripts been executed properly with current parameters? (y|n) [n]: "))

    if inp != "y":
        print("Please consult project documentation on How-To and come back here later")
        exit()

    # ----------------------------------------------------------------------------
    # Setup
    # Get all simulation results ready

    # Order of assignments must match `diode` definition in scripts/symbols.py
    N_d, N_a, W_t, A, T = diode

    diode_units = {}
    for sym in diode:
        diode_units[sym.desc] = sym.unit

    with open(JSON_PATH, "r", encoding="utf8") as file:
        values = json.load(file)
    diode_dict = values["Diode"]

    tex_paths = {
        "mu": PARAM_FOLDER[3:] + "Beweglichkeiten von Majoritätsträgern.tex",
        "tau": PARAM_FOLDER[3:] + "Lebensdauer Zeitkonstanten der Minoritäten.tex",
        "constants": PARAM_FOLDER[3:] + "Naturkonstanten.tex",
        "parameters": PARAM_FOLDER[3:] + "Materialparameter " + ELEMENT + ".tex"
        }

    U_F = pickle_read("V_min")

    numeric_results = pickle_read("ODE_solution")
    x_p = round(numeric_results["x_p"] * (10 ** 9), 1)
    x_n = round(numeric_results["x_n"] * (10 ** 9), 1)
    W_F = round(numeric_results["W_F"], 4)
    w_scr = x_n - x_p
    x_p = str(x_p) + " nm"
    x_n = str(x_n) + " nm"
    W_F = "$W_{V} (-w_{p})$ + " + str(W_F) + " eV"
    w_scr = str(w_scr) + " nm"

    diameter = round(((diode_dict[A.desc][0] * (10 ** diode_dict[A.desc][1])) / 3.14) ** 0.5, 1)

    # ----------------------------------------------------------------------------
    # Create tex

    # ----------------------------------------------------------------------------
    # Preamble and some lambda functions

    doc = Document("article")
    doc.preamble.append(Command("usepackage", "booktabs"))
    doc.preamble.append(Command("usepackage", "hyperref"))
    doc.preamble.append(Command("hypersetup", "colorlinks=true, linkcolor=blue, urlcolor=blue"))
    doc.preamble.append(NoEscape("\\renewcommand*\\contentsname{Inhalt}"))

    doc.preamble.append(Command("author", "Vincent Kiefer"))
    doc.preamble.append(Command("title", "Simulationsergebnisse P-N-Übergang"))

    write = lambda text: doc.append(NoEscape(text))
    nl = lambda : doc.append(NoEscape("\\\\"))
    np = lambda : doc.append(NewPage())

    # ----------------------------------------------------------------------------
    # Title page, including table of contents

    doc.append(Command("maketitle"))
    doc.append(Command("tableofcontents"))
    doc.append(Command("vspace","5mm"))
    doc.append(Command("noindent"))
    write("Entstanden im Rahmen des Projekts \\href{https://python-fuer-ingenieure.de/pysaar2024}{PySaar2024}")
    nl()
    write("Generiert durch Code von Vincent Kiefer, 7031439. Siehe \\href{https://github.com/HerrGrafVal/PySaar2024}{GitHub Repository}")
    np()

    # ----------------------------------------------------------------------------

    # Diode parameters
    with doc.create(Section("Dioden-Parameter")):
        write("Die folgenden Parameter wurden zur Simulation verwendet:")
        nl()
        nl()
        write("Halbleiter Substrat: " + ELEMENT)
        nl()
        write("Durchmesser der Diode: " + str(diameter) + " " + display_unit(A.unit ** 0.5))

        # 'Newer' python versions keep the order of dict entries
        for i in diode_dict.items():
            nl()
            # Numeric values
            if type(i[1]) == list:
                unit = display_unit(diode_units[i[0]])
                if i[0] == W_t.desc:
                    text = i[0] + ": $" + str(i[1][0] * 10**i[1][1]) + " \\cdot W_g$"
                elif i[1][1] == 0:
                    text = i[0] + ": $" + str(i[1][0] * 10**i[1][1]) + "$ " + unit
                else:
                    text = i[0] + ": $" + str(i[1][0]) + " \\cdot 10^{" + str(i[1][1]) + "}$ " + unit
                write(text)
            
            # String values
            else:
                write(i[0] + ": " + i[1])

    np()

    # pn-values
    with doc.create(Section("Verläufe von Kenngrößen")):
        write("Die hier dargestellten Kenngrößen beinhalten die Ortsverläufe der Raumladungsdichte, \
            Feldstärke, des elektr. Potentials und Bandkanten. Im Falle der numerischen Simulation \
            außerdem die (logarithmierten) Ladungsträgerdichten.")
        nl()
        write("Die hier dargestellten Verläufe (symbolisch und numerisch) gelten nur im thermodynamischen Gleichgewicht, also ohne externer Spannung!")
     
        # Symbolic
        with doc.create(Subsection("Symbolisch")):
            write("Nach Rechtecknäherung der Raumladungsdichte ergeben sich folgende Verläufe")
            include_img("pn", 'Kenngrößen des pn-Übergangs, symbolisch')

        np()
        
        # Numeric
        with doc.create(Subsection("Numerisch")):
            write('Durch numerisches lösen der Bestimmungsgleichungen des Drift-Diffusions-Modells (DDM) ergeben sich folgende Verläufe')
            include_img("DDM", 'Kenngrößen des pn-Übergangs, numerisch')
            
            doc.append(Command("noindent"))
            write("Mit folgenden (berechneten) Parametern:")
            nl()
            write("$x_{p}$ = " + x_p)
            nl()
            write("$x_{n}$ = " + x_n)
            nl()
            write("$w_{RLZ}$ = " + w_scr)
            nl()
            write("$W_{F}$ = " + W_F)

            """
            # Use individual graphs instead
            include_img("cc", "Logarithmischer Verlauf der Ladungsträgerdichten $n(x)$ \\& $p(x)$, numerisch")
            include_img("rho", "Verlauf der Raumladungsdichte $\\rho (x)$, numerisch")
            include_img("E", "Verlauf der Feldstärke $E(x)$, numerisch")
            include_img("phi", "Verlauf des Potentials $\\varphi (x)$, numerisch")
            include_img("W", "Verlauf der Bandkanten $W_{V} (x)$, $W_{C} (x)$ und des Fermi-Niveaus $W_{F}$, numerisch")
            """
    np()

    # current over voltage
    with doc.create(Section("Strom-Spannungs-Kennlinie")):
        write("Die gegebenen Parameter erzeugen die folgende Kennlinie,")
        nl()
        write("mit einer Flussspannung von $U_{F}$ $=$ $" + str(U_F) + "$ $V$")
        include_img("I(U)", "Strom-Spannungs-Kennlinie der Diode")

    np()

    # material parameter and universal constants
    with doc.create(Section("Anhang")):
        with doc.create(Subsection("Naturkonstanten")):
            write("Die folgenden Werte wurden für Naturkonstanten substituiert")
            doc.append(Command("input", tex_paths["constants"]))
            nl()
        with doc.create(Subsection("Materialparameter")):
            write("Die folgenden Werte wurden für Materialparameter substituiert")
            doc.append(Command("input", tex_paths["parameters"]))
            np()
            doc.append(Command("noindent"))
            write("Die folgenden Werte wurden, je nach Dotierung, \
                für die Beweglichkeit $\\mu_{p}$ bzw. $\\mu_{n}$ substituiert, für " + ELEMENT + "-Halbleiter:")
            doc.append(Command("input", tex_paths["mu"]))
            nl()
            write("Der Mittelwert folgender Intervalle wurde, je nach Halbleiter Substrat, \
                als Lebensdauer $\\tau_{n}$ bzw. $\\tau_{p}$ substituiert")
            doc.append(Command("input", tex_paths["tau"]))

    # ----------------------------------------------------------------------------
    # Render pdf

    # Attempt compiling with latexmk, in order to set up Table of Contents
    try:
        doc.generate_pdf(PDF_PATH, compiler = "latexmk")
    except UnicodeDecodeError:
        # latexmk handles unicode different to pdfLaTex, but the Toc is setup now
        os.remove(PDF_PATH + ".dvi")
    # Create pdf
    doc.generate_pdf(PDF_PATH, compiler = "pdfLaTeX")

    if KEEP_TEX:
        doc.generate_tex(PDF_PATH)

    # ----------------------------------------------------------------------------
    # Open generated pdf file in default application.

    if OPEN_PDF:
        try:
            # Tested on Windows 10 only
            cmd = '"' + PDF_PATH + '.pdf"'
            os.system(cmd)
        except:
            pass
        print(PDF_PATH + ".pdf generated successfully!")