# PySaar2024
Simulation und Visualisierung eines p-n-Übergang in einer Diode nach vereinfachtem Drift-Diffusions-Modell (DDM).

## ToDo:
- [x] [Markdown](https://www.markdownguide.org/cheat-sheet/) für README & Docstrings nutzen
- [x] In Git Branch `dev` arbeiten
- [x] Literaturgrundlage[^1] in Repository speichern
- [x] DDM Konstanten mit [Pandas](https://pandas.pydata.org/docs/) darstellen
- [x] DDM Bestimmungsgleichungen[^2] mit [SymPy](https://docs.sympy.org/latest/index.html) implementieren
- [x] DDM Numerisch lösen. Eventuell [mpmath](https://mpmath.org/) verwenden
- [x] [PyLaTeX](https://jeltef.github.io/PyLaTeX/current/index.html) implementieren um DataFrames und später Tabellen in pdf Form auszugeben
### p-n-Übergang im thermodynamischen Gleichgewicht - Symbolisch
- [x] Verläufe *wichtiger Größen* mit [Matplotlib](https://matplotlib.org/stable/index.html) darstellen:
    1. [x] *Wichtige Größen* als solche bestimmen
    2. [x] Darstellung in Achsendiagrammen, Bändermodell
- [x] [Visualisierungsmöglichkeiten](https://matplotlib.org/stable/gallery/index.html) des p-n-Übergangs recherchieren
- [x] Visualisierung des p-n-Übergangs implementieren
- [ ] [tikzplotlib](https://pypi.org/project/tikzplotlib/) implementieren und plots zu .tex -> zu .pdf umwandeln
### p-n-Übergang im thermodynamischen Gleichgewicht - Numerisch
- [ ] Verläufe *wichtiger Größen* mit [Matplotlib](https://matplotlib.org/stable/index.html) darstellen:
    1. [x] *Wichtige Größen* als solche bestimmen
    2. [ ] Darstellung in Achsendiagrammen, Bändermodell
- [ ] [Visualisierungsmöglichkeiten](https://matplotlib.org/stable/gallery/index.html) des p-n-Übergangs recherchieren
- [ ] Visualisierung des p-n-Übergangs implementieren
- [ ] [tikzplotlib](https://pypi.org/project/tikzplotlib/) implementieren und plots zu .tex -> zu .pdf umwandeln
### p-n-Übergang außerhalb des thermodynamischen Gleichgewichts
- [x] Externe Spannung und Stromfluss durch Diode implementieren
- [x] Kennlinie visualiseren
- [x] Kennlinie mit stückweiser linearer Regression approximieren
- [x] Flussspannung aus Regressionsergebnis ermitteln
### Dokumentation
- [x] [Sphinx](https://www.sphinx-doc.org/en/master/index.html) implementieren
- [ ] Docs korrigieren
### Präsentation
- [ ] Folien vorbereiten
- [ ] Präsentation in vorgegebener Zeit proben

[^1]: Skriptum zur Vorlesung **Physikalische Grundlagen elektronischer Bauelemente** WS 2022/23, Prof. Dr.-Ing. Michael Möller
[^2]: Verzicht auf Rechteck Näherung intensiv erprobt. Bisher mit sympy nicht realisierbar.
