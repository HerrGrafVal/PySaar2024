# PySaar2024
Simulation und Visualisierung eines p-n-Übergang in einer Diode nach vereinfachtem Drift-Diffusions-Modell (DDM).
Präsentiert Ergebnisse in Form einer pdf-Datei, nützlich als Grundlage für Datenblätter (Wirtschaft) oder Lehre.

## Setup & Requirements:
- Install all the python modules linked above, try executing:
    `pip install pandas sympy numpy scipy mpmath pylatex matplotlib sphinx`
- Make sure previously installed packages are up-to-date:
    `pip install *package-name* --upgrade`
- A working latex installation is required to use this project (pdfLaTeX **and** latexmk).
- Generate documentation HTML:
    1. Navigate to */PySaar2024/docs/*
    2. Execute `make.bat html`, on Windows do `.\make.bat html` instead
    3. Ignore one occurence of the sphinx warning: `Inline strong start-string without end-string`
- The HTML documentation contains additional information not present in source code docstrings
- **The HTML documentation of *main.py* contains a step by step on how to perform your own simulation**
- Steps 4 and 8 of this "step by step" can be skipped **for a fresh git clone** as they resemble default values.
- Access documentation HTML:
    1. Navigate to */PySaar2024/docs/build/html*
    2. Open *index.html* in browser
- Additional information and explanation can be found in [these presentation slides](https://unisaarlandde-my.sharepoint.com/:b:/g/personal/viki00002_uni-saarland_de/EU1d6F0i71NJjNuTuZtmStABZqZKjob51OWYPApswxmV6Q?e=poxLCC)[^1]

## ToDo:
- [x] [Markdown](https://www.markdownguide.org/cheat-sheet/) für README nutzen
- [x] [reStructuredText](https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst) für Docstrings nutzen
- [x] In Git Branch `dev` arbeiten
- [x] Literaturgrundlage[^2] aus Repository History entfernen
- [x] DDM Konstanten mit [Pandas](https://pandas.pydata.org/docs/) darstellen
- [x] DDM Bestimmungsgleichungen[^3] mit [SymPy](https://docs.sympy.org/latest/index.html) implementieren
- [x] DDM[^4] Numerisch lösen. [NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [mpmath](https://mpmath.org/) verwenden
- [x] [PyLaTeX](https://jeltef.github.io/PyLaTeX/current/index.html) implementieren um Tabellen und plots in pdf auszugeben
### p-n-Übergang im thermodynamischen Gleichgewicht - Symbolisch
- [x] Verläufe *wichtiger Größen* mit [Matplotlib](https://matplotlib.org/stable/index.html) darstellen:
    1. [x] *Wichtige Größen* als solche bestimmen
    2. [x] Darstellung in Achsendiagrammen, Bändermodell
- [x] [Visualisierungsmöglichkeiten](https://matplotlib.org/stable/gallery/index.html) des p-n-Übergangs recherchieren
- [x] Visualisierung des p-n-Übergangs implementieren
- [x] Option zum rendern der Label in LaTeX hinzufügen, Ausführung der Skripte dauert damit signifikant länger!
- [x] Graphiken speichern
### p-n-Übergang im thermodynamischen Gleichgewicht - Numerisch
- [x] Verläufe *wichtiger Größen* mit [Matplotlib](https://matplotlib.org/stable/index.html) darstellen:
    1. [x] *Wichtige Größen* als solche bestimmen
    2. [x] Darstellung in Achsendiagrammen, Bändermodell
- [x] [Visualisierungsmöglichkeiten](https://matplotlib.org/stable/gallery/index.html) des p-n-Übergangs recherchieren
- [x] Visualisierung des p-n-Übergangs implementieren
- [x] Option zum rendern der Label in LaTeX hinzufügen, Ausführung der Skripte dauert damit signifikant länger!
- [x] Graphiken speichern
### p-n-Übergang außerhalb des thermodynamischen Gleichgewichts
- [x] Externe Spannung und Stromfluss durch Diode implementieren
- [x] Kennlinie visualiseren
- [x] Kennlinie mit stückweiser linearer Regression approximieren
- [x] Flussspannung aus Regressionsergebnis ermitteln
### Output
- [x] pdf Struktur erarbeiten
- [x] `main.py` anlegen:
    1. [x] Frage nach Parametern
    2. [x] Gesamt pdf generieren
    3. [x] pdf öffnen
### Dokumentation
- [x] [Sphinx](https://www.sphinx-doc.org/en/master/index.html) implementieren
- [x] Docstrings korrigieren
- [x] .rst zu scripts ohne Docstrings schreiben
- [x] Docs erweitern:
    1. [x] Anleitung zu parameter.json (Farbkodierung)
    2. [x] Step-by-Step Anleitung zu Simulation in *main.py* documentation
- [x] OneDrive Präsentation verlinken
### Präsentation
- [x] Folien vorbereiten
- [x] Präsentation in vorgegebener Zeit proben

[^1]: Link expires July 20th 2024. Contact project author for later access.
[^2]: Skriptum zur Vorlesung **Physikalische Grundlagen elektronischer Bauelemente** WS 2022/23, Prof. Dr.-Ing. Michael Möller
[^3]: Verzicht auf Rechteck Näherung auch hier intensiv erprobt. Mit sympy nicht realisierbar. 
[^4]: Ohne Rechteck Näherung der Raumladungsdichte