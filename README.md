# PySaar2024
Simulation und Visualisierung eines p-n-Übergang in einer Diode nach vereinfachtem Drift-Diffusions-Modell (DDM).

## ToDo:
- [x] [Markdown](https://www.markdownguide.org/cheat-sheet/) für README & Docstrings nutzen
- [x] In Git Branch `dev` arbeiten
- [x] Literaturgrundlage[^1] in Repository speichern
- [x] DDM Konstanten mit [Pandas](https://pandas.pydata.org/docs/) darstellen
- [x] DDM Bestimmungsgleichungen[^2] mit [SymPy](https://docs.sympy.org/latest/index.html) implementieren
- [x] [PyLaTeX](https://jeltef.github.io/PyLaTeX/current/index.html) implementieren um DataFrames und später Tabellen in pdf Form auszugeben
### p-n-Übergang im thermodynamischen Gleichgewicht
- [x] Verläufe *wichtiger Größen* mit [Matplotlib](https://matplotlib.org/stable/index.html) darstellen:
    1. [x] *Wichtige Größen* als solche bestimmen
    2. [x] Darstellung in Achsendiagrammen, Bändermodell
- [x] [Visualisierungsmöglichkeiten](https://matplotlib.org/stable/gallery/index.html) des p-n-Übergangs recherchieren
- [x] Visualisierung des p-n-Übergangs implementieren
- [ ] [tikzplotlib](https://pypi.org/project/tikzplotlib/) implementieren und plots zu .tex -> zu .pdf umwandeln
- [ ] pn-Übergang mit Heatmaps *wichtier Größen*
### p-n-Übergang außerhalb des thermodynamischen Gleichgewichts
- [ ] Externe Spannung und Stromfluss durch Diode implementieren
- [ ] Kennlinie visualiseren
- [ ] Kennlinie mit stückweiser linearer Regression approximieren
- [ ] Flussspannung aus Regressionsergebnis ermitteln
### Präsentation
- [ ] Folien vorbereiten
- [ ] Präsentation in vorgegebener Zeit proben

[^1]: Skriptum zur Vorlesung **Physikalische Grundlagen elektronischer Bauelemente** WS 2022/23, Prof. Dr.-Ing. Michael Möller
[^2]: Verzicht auf Rechteck Näherung intensiv erprobt. Bisher mit sympy nicht realisierbar.
