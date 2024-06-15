from sympy import Symbol, Function, log, root

# ----------------------------------------------------------------------------

class Sym(Symbol):
    """
    | Adds 2 additional attributes to `sympy.Symbol` instances during initialisation
    | The description is used to match the Sym instance with their value from json files
    | The unit is later multiplied onto the numeric value when Sym is substituted

    :attributes: ``self.desc`` , ``self.unit``
    """

    def __init__(self, name, desc, unit, **kwargs):
        """
        | Returns `sympy.Symbol` instance with additional attributes.

        :param name: Symbol name, passed along to ``sympy.Symbol()``
        :type name: string
        :param desc: Additional symbol description
        :type desc: string
        :param unit: Symbol's unit
        :type unit: sympy.Symbol
        :return: self
        """

        self.desc = desc
        self.unit = unit

    def __new__(cls, name, desc, unit, **kwargs):
        return super().__new__(cls, name, **kwargs)

# ----------------------------------------------------------------------------
# Create `sympy.Symbol()` instances for required units of measurement
# Decision not to use `sympy.physics.units` was made for lack of good documentation on `sympy.physics.units`

meter = Symbol("m")
centimeter = meter / 100
milimeter = meter / 1000
nanometer = meter / (10**9)
kilogram = Symbol("kg")
second = Symbol("s")
ampere = Symbol("A")
volt = Symbol("V")
electron_volt = Symbol("eV")
joule = Symbol("J")
kelvin = Symbol("K")

full_units = [meter, kilogram, second, ampere, volt, joule, kelvin, electron_volt]

# ----------------------------------------------------------------------------
# Create `Sym()` instances and list of such for universal constants in this namespace

m_e = Sym("m_e", "Ruhemasse eines Elektrons", kilogram)
q_e = Sym("e", "Elementarladung", ampere * second)
eps_0 = Sym("\\epsilon_0", "Dielektrizitätskonstante des Vakuums",
            ampere * second / (volt * meter))
h = Sym("h", "Plank'sches Wirkungsquantum", joule * second)
k = Sym("k", "Boltzmann-Konstante", joule / kelvin)

constants = [m_e, q_e, eps_0, h, k]

# ----------------------------------------------------------------------------
# Create `Sym()` instances and list of such for material parameters in this namespace

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

mu_n = Sym("\\mu_n", "Beweglichkeit der Elektronen als Minoritätsträger", centimeter**2 / (volt * second))
mu_p = Sym("\\mu_p", "Beweglichkeit der Löcher als Minoritätsträger", centimeter**2 / (volt * second))

# ----------------------------------------------------------------------------
# Create additional `Sym()` instances for use in later calculations

x = Sym("x", "Ortskoordinate, Nullpunkt im p-n-Übergang", nanometer)
A = Sym("A", "Querschnittsfläche der Diode", milimeter**2)
T = Sym("T", "Temperatur", kelvin)

w_p = Sym("w_p", "Weite p-Bahngebiet", nanometer)
x_p = Sym("x_p", "Grenze p-Raumladungszone", nanometer)

w_n = Sym("w_n", "Weite n-Bahngebiet", nanometer)
x_n = Sym("x_n", "Grenze n-Raumladungszone", nanometer)

WIDTH = Sym("w_n / x_n", "Verhältnis: (Weite der Bahngebiete) / (Ausdehnung der RLZ ohne externe Spannung)", 1)

U_ext = Sym("U_{ext}", "Extern angelegte Spannung", volt)

W_t = Sym("W_t", "Trap Energieniveaus (Halbleiter Verunreinigung)", W_g)

tau_n = Sym("\\tau_n", "Mittlere Lebensdauer der Elektronen als Minoritätsträger", second)
tau_p = Sym("\\tau_p", "Mittlere Lebensdauer der Löcher als Minoritätsträger", second)

I_s = Sym("I_S", "Sättigungsstrom", ampere)
I_rg = Sym("I_{rg}", "Rekombinationsstrom", ampere)

# ----------------------------------------------------------------------------
# Create `Sym()` instances for charge carrier densities, needed during calculations

N_a = Sym("N_A", "Akzeptor Dotierungsdichte", centimeter**(-3))
N_am = Sym("N_A^-", "Dichte ionisierter Akzeptorniveaus", centimeter**(-3))
N_d = Sym("N_D", "Donator Dotierungsdichte", centimeter**(-3))
N_dp = Sym("N_D^+", "Dichte ionisierter Donatorniveaus", centimeter**(-3))

diode = [N_d, N_a, W_t, A, T]

n0 = Function("n_0")(x)
del_n = Function("\\Delta n")(x)
n = Function("n")(x)

p0 = Function("p_0")(x)
del_p = Function("\\Delta p")(x)
p = Function("p")(x)

# ----------------------------------------------------------------------------
# Create `sympy.Function()` instances for use in later calculations
# Some of the following might be redundand!

rho = Function("\\rho")(x)
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

# ----------------------------------------------------------------------------
# Define derived quantities for use in later calculations

eps = eps_0 * eps_r
U_T = k * T / q_e
U_D = U_T * log((N_a * N_d) / (n_i ** 2))
x_n = root((2 * eps * (U_D-U_ext) * N_a) / (q_e * N_d * (N_d + N_a)), 2)
x_p = -1 * x_n * N_d / N_a


x_n0 = root((2 * eps * U_D * N_a) / (q_e * N_d * (N_d + N_a)), 2)
w_n = x_n0 * WIDTH
x_p0 = -1 * x_n0 * N_d / N_a
w_p = abs(x_p0 * WIDTH)

w_RLZ = x_n - x_p
D_n = U_T * mu_n
D_p = U_T * mu_p
L_n = root(tau_n * D_n, 2)
L_p = root(tau_p * D_p, 2)

# ----------------------------------------------------------------------------
# Save namespace to later pass it onto `cache.read_from_file()`

namespace = dir()
