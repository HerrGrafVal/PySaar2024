from sympy import Symbol, Function, log, root


class Sym(Symbol):

    """
    Returns `sympy.Symbol` instance with added properties.

    Parameters
    : **name** *(string)* Symbol name (should be LATEX) e.g. "\\epsilon_r"
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
nanometer = 10**9 * meter
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
eps_0 = Sym("\\epsilon_0", "Dielektrizitätskonstante des Vakuums",
            ampere * second / (volt * meter))
h = Sym("h", "Plank'sches Wirkungsquantum", joule * second)
k = Sym("k", "Boltzmann-Konstante", joule / kelvin)

constants = [m_e, q_e, eps_0, h, k]

n_i = Sym("n_i", "Eigenleitungsdichte", centimeter**(-3))
eps_r = Sym("\\epsilon_r", "Relative Permittivität", 1)
W_g = Sym("W_g", "Bandlücke", electron_volt)

N_c = Sym("N_C", "Effektive Ladungsträgerdichte im Leitungsband", centimeter**(-3))
N_v = Sym("N_V", "Effektive Ladungsträgerdichte im Valenzband", centimeter**(-3))

m_ed = Sym("m_{ed}^*/m_e", "Effektive Zustandsdichte-Massen für Elektronen", 1)
m_hd = Sym("m_{hd}^*/m_e", "Effektive Zustandsdichte-Massen für Löcher", 1)

m_ec = Sym("m_{ec}^*/m_e", "Effektive Leitfähigkeits-Massen für Elektronen", 1)
m_hc = Sym("m_{hc}^*/m_e", "Effektive Leitfähigkeits-Massen für Löcher", 1)

material_parameters = [n_i, eps_r, W_g, N_c, N_v, m_ed, m_hd, m_ec, m_hc]

N_a = Sym("N_A", "Akzeptor Dotierungsdichte", centimeter**(-3))
N_am = Sym("N_A^-", "Dichte ionisierter Akzeptorniveaus", centimeter**(-3))
N_d = Sym("N_D", "Donator Dotierungsdichte", centimeter**(-3))
N_dp = Sym("N_D^+", "Dichte ionisierter Donatorniveaus", centimeter**(-3))

"""
Create `Sym()` instances for variables needed during calculations
"""

x = Sym("x", "Ortskoordinate, Nullpunkt im p-n-Übergang", nanometer)
T = Sym("T", "Temperatur", kelvin)
w_p = Sym("w_p", "Weite p-Bahngebiet", nanometer)
x_p = Sym("x_p", "Grenze p-Raumladungszone", nanometer)
w_n = Sym("w_n", "Weite n-Bahngebiet", nanometer)
x_n = Sym("x_n", "Grenze n-Raumladungszone", nanometer)

rho = Function("\\rho")(x)
n0 = Function("n_0")(x)
n = Function("n")(x)
del_n = Function("\\Delta n")(x)
p0 = Function("p_0")(x)
p = Function("p")(x)
del_p = Function("\\Delta p")(x)
E = Function("E")(x)
phi = Function("\\varphi")(x)
W_c = Function("W_c")(x)
W_v = Function("W_v")(x)
W_F = Function("W_F")(x)
W_Fn = Function("W_{Fn}")(x)
W_Fp = Function("W_{Fp}")(x)
J_n = Function("J_n")(x)
J_p = Function("J_n")(x)
R = Function("R")(x)
mu_n = Sym("\\mu_n", "Beweglichkeit der Elektronen im p-Bereich", centimeter**2 / (volt*second))
mu_p = Sym("\\mu_p", "Beweglichkeit der Löcher im n-Bereich", centimeter**2 / (volt*second))
tau_n = Function("\\tau_n")(x)
tau_p = Function("\\tau_p")(x)

eps = eps_0 * eps_r
U_T = k * T / q_e
U_D = U_T * log((N_a * N_d) / (n_i ** 2))
x_n = root((2*eps*U_D*N_a)/(q_e * N_d * (N_d + N_a)), 2)
x_p = -1 * x_n * N_d / N_a
D_n = U_T * mu_n
D_p = U_T * mu_p

U_ext = Sym("U_{ext}", "Extern angelegte Spannung", volt)

ddx_E = E.diff(x)
ddx_phi = phi.diff(x)

ddx_J_n = J_n.diff(x)
ddx_J_p = J_p.diff(x)

namespace = dir()