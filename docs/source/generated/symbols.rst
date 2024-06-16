scripts.symbols
===============

*symbols.py* creates *sympy.Symbol* / *symbols.Sym* and *sympy.Function* instances for use in all other scripts. Alongside individual symbols first derived quantities are defined, such as ``eps = eps_0 + eps_r``.

Three lists of symbols ``constants``, ``material_parameters``, ``diode`` are defined for later use in different scripts.

Contains ``namespace = dir()`` to pass onto ``cache.read_from_file()``

Will be imported by almost all other scripts.

| 
| 

.. autoclass:: symbols.Sym
   :special-members: __init__
   :undoc-members:
   :show-inheritance:
