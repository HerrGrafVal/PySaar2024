from pylatex import Document, Command

"""
Even with `strict = True` in `cache.plt_to_tex()` tikzplotlib changes plot visuals.
Labels and units are lost, execute this script to see for yourself.
Moving forward `matplotlib.pyplot.savefig()` will be used to save plots as png
"""

doc = Document("basic")
doc.preamble.append(Command("usepackage[utf8]", "inputenc"))
doc.preamble.append(Command("usepackage", "pgfplots"))
doc.preamble.append(Command("usepgfplotslibrary", "groupplots,dateplot"))
doc.preamble.append(Command("usetikzlibrary", "patterns,shapes.arrows"))
doc.preamble.append(Command("pgfplotsset", "compat=newest"))

# Note that file paths need to be relative to the pdf output path!
doc.append(Command("input", "simulation_results/cc_graph.tex"))

doc.generate_pdf("../pdf_plot", compiler = "pdfLaTeX")