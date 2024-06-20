main
====

*main.py* also sits inside the *scripts/* folder. Making that folder into a valid python module and moving *main.py* outside changes ``sphinx-apidoc`` behaviour and therefore hasn't been done at this point in development.

Upon execution *main.py* prompts the user with the question *Have all over scripts been executed properly with current parameters?* Only after choosing yes will the script attempt to create a pdf file with complete simulation results.

If ``OPEN_PDF`` is set to True the pdf file will attempt to open in your default application when ready.

Executing all over scripts properly means:
   1. Adjusting json parameters and ``read_dataframe.ELEMENT`` to the user's content [1]_ [2]_
   2. Execute *scripts/initial_values.py* to create tex tables from json content.
   3. Executing *scripts/modell.py*
   4. In *scripts/generate_graphs.py* disable use of cached values and set ``SHOW_PLOT`` to False in lines 13, 14 and 24. Enable both pn-value and current plots in lines 20 and 21. **These resemble the default values after a fresh git clone**
   5. Execute *scripts/generate_graphs.py* the symbolic and current simulation is done and the graphs are saved!
   6. Execute *scripts/fermi_level.py*
   7. Execute *scripts/DDM_ode.py*
   8. In *scripts/generate_ode_graphs.py* disable ``SHOW_PLOT`` in line 8. **These resemble the default values after a fresh git clone**
   9. Execute *scripts/generate_ode_graphs.py* the numeric simulation is done and the graphs are saved!
   10. Execute *scripts/main.py* and reply ``y`` to create pdf

| 
| 

.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:

| 
| 

.. [1] Note that some adjustments invalidate the modell, e.g. a change solely in Temperature value changes simulation results. Since however all substrate specific material parameters are temperature dependent not changing those invalidates results.

.. [2] See HTML documentation on *parameters*