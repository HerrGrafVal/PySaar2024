from sympy import Symbol


class Sym(Symbol):

    """
    Returns `sympy.Symbol` instance with added properties.

    Parameters
    : **name** *(string)* Symbol name (should be LATEX) e.g. "\epsilon_r"
    : **desc** *(string)* Symbol description e.g. "Relative Permittivität"
    : ***kwargs** Passed along to `sympy.Symbol()`
    """

    def __init__(self, name, desc, unit, **kwargs):
        self.desc = desc
        self.unit = unit

    def __new__(cls, name, desc, unit, **kwargs):
        return super().__new__(cls, name, **kwargs)


"""
Create `sympy.Symbol()` instances for required units of measurement
Decision not to use `sympy.physics.units` was made for lack of good documentation on `sympy.physics.units`
"""

meter = Symbol("m")
centimeter = 100 * meter
kilogram = Symbol("kg")
second = Symbol("s")
ampere = Symbol("A")
volt = Symbol("V")
electron_volt = Symbol("eV")
joule = Symbol("J")
kelvin = Symbol("K")


"""
Create `Sym()` instances for universal constants and material parameters in seperate namespace
"""

m_e = Sym("m_e", "Ruhemasse eines Elektrons", kilogram)
q_e = Sym("e", "Elementarladung", ampere * second)
eps_0 = Sym("\epsilon_0", "Dielektrizitätskonstante des Vakuums", ampere * second / (volt * meter))
h = Sym("h", "Plank'sches Wirkungsquantum", joule * second)
k = Sym("k", "Boltzmann-Konstante", joule / kelvin)

constants = [m_e, q_e, eps_0, h, k]

n_i = Sym("n_i", "Eigenleitungsdichte", centimeter**(-3))
eps_r = Sym("\epsilon_r", "Relative Permittivität", 1)
W_g = Sym("W_g", "Bandlücke", electron_volt)

N_c = Sym("N_C", "Effektive Ladungsträgerdichte im Leitungsband", centimeter**(-3))
N_v = Sym("N_V", "Effektive Ladungsträgerdichte im Valenzband", centimeter**(-3))

m_ed = Sym("m_{ed}^*/m_e", "Effektive Zustandsdichte-Massen für Elektronen", 1)
m_hd = Sym("m_{hd}^*/m_e", "Effektive Zustandsdichte-Massen für Löcher", 1)

m_ec = Sym("m_{ec}^*/m_e", "Effektive Leitfähigkeits-Massen für Elektronen", 1)
m_hc = Sym("m_{hc}^*/m_e", "Effektive Leitfähigkeits-Massen für Löcher", 1)

material_parameters = [n_i, eps_r, W_g, N_c, N_v, m_ed, m_hd, m_ec, m_hc]