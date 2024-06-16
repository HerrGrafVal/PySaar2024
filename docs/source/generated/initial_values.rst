scripts.initial\_values
=======================

*initial_values.py* reads *PARAM_FOLDER/JSON_FILE_NAME* to fetch parameter values from the supplied json. Creates *dict* of *pandas.DataFrame* called ``values`` upon import that is later imported by *read_dataframe.py*.

Upon execution leads up to call of ``initial_values.create_pdf()``

Notable variables (see source code) include ``FLOAT_DIGITS``, ``PARAM_FOLDER``, ``JSON_FILE_NAME``, ``PDF_FILE_NAME`` and ``OPEN_PDF``

Must be executed at least once before *main.py* can be executed.

| 
| 

.. automodule:: initial_values
   :members:
   :undoc-members:
   :show-inheritance:
