scripts.generate\_graphs
========================

*generate_graphs.py* requires sympy expressions for pn-functions saved in *SAVE_FOLDER*. These can be provided by executing *modell.py* Plots results of symbolic diode approximation.

Notable variables (see source code) include ``USE_CACHED_PN_VALUES``, ``USE_CACHED_CURRENT_VALUES``, ``HIDE_CACHE_LOG``, ``PLOT_PN``, ``PLOT_CURRENT``, ``SHOW_PLOT`` and ``THRESHOLD``.

| Execution behaviour depends on above mentioned variables. See source code.
| Does nothing upon import.

Executing this function with ``PLOT_PN = True`` and ``PLOT_CURRENT = True`` and ``SHOW_PLOT = False`` at least once is mandatory before *main.py* can be executed.

| 
| 

.. automodule:: generate_graphs
   :members:
   :undoc-members:
   :show-inheritance:
