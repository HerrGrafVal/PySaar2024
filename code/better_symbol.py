from sympy import Symbol

class Sym(Symbol):

	"""
	Returns sympy.Symbol instance with added properties.

	Parameters
	: **name** *(string)* Symbol name (can be LATEX) e.g. "epsilon_r"
	: **desc** *(string)* Symbol description e.g. "Relative Permittivität"
	: **\*kwargs** Passed along to `sympy.Symbol()`
	"""

	def __init__(self, name, desc, unit = None, **kwargs):
		self.desc = desc
		self.unit = unit

	def __new__(cls, name, desc, unit = None, **kwargs):
		return super().__new__(cls, name, **kwargs)
