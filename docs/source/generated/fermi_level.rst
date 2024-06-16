scripts.fermi\_level
====================

| Upon execution *fermi_level.py* approximates the fermi-level (in eV above W_v)
| Notable variables (see source code) include ``HIDE_LOG``

Approximation is conducted by setting up a function that takes possible W\_F values and returns an amount of error (of charge neutrality conditions) resulting from the hypothesis.
Roots of that function (output close to 0) provide the fermi level.

| Results are of type *float* and are pickled to *SAVE_FOLDER/Fermi_level.pkl*
| 
| 

.. automodule:: fermi_level
   :members:
   :undoc-members:
   :show-inheritance:
