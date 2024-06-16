scripts.read\_dataframe
=======================

*read_dataframe.py* provides functions to substitute *sympy.Symbols* for their numeric values as defined in ``initial_values.values`` *dict*, originating from *PARAM_FOLDER/JSON_FILE_NAME*

Relevant Variables include ``ELEMENT`` which **sets the active semicondutor substrate for all simulation**.

Creates and populates ``json_parameter`` *dict* from *DataFrame* values upon import to accelerate simulation speed, see ``read_dataframe.populate_dict()`` documentation.

| 
| 

.. automodule:: read_dataframe
   :members:
   :undoc-members:
   :show-inheritance:
