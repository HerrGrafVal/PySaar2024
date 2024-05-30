from sympy import Eq, exp, sqrt, sinh, simplify
from sympy.solvers.ode.systems import dsolve_system
from symbols import *

# ----------------------------------------------------------------------------

class Region():
    """
    Parent class for all area classes
    """

    def __init__(self):
        # Setup functions
        self.rho = Function("\\rho")(x)

        # Setup voltage
        self.U_RLZ = U_D

    def simulate(self, a, b):
        # Calculate derived functions
        self.E = self.rho.integrate((x, a, b)) / eps
        self.phi = -1 * self.E.integrate((x, a, b))
        self.W_v = -1 * q_e * self.phi
        self.funcs = {
            rho: simplify(self.rho),
            E: simplify(self.E),
            phi: simplify(self.phi),
            W_v: simplify(self.W_v)
        }

class PDotation():
    """
    Parent class for all p-dotated areas
    """

    def __init__(self):
        # Dotation and charge carrier density
        self.pp0 = N_a
        self.np0 = (n_i**2) / self.pp0
        self.N_am = N_a
        self.N_dp = 0
        self.n = Function("n_p")(x)
        self.p = Function("p_p")(x)
      
class NDotation():
    """
    Parent class for all n-dotated areas
    """

    def __init__(self):
        # Dotation and charge carrier density
        self.nn0 = N_d
        self.pn0 = (n_i**2) / self.nn0
        self.N_dp = N_d
        self.N_am = 0
        self.n = Function("n_n")(x)
        self.p = Function("p_n")(x)

    def adjust_for_integration_constants(self):
        self.funcs[phi] += self.U_RLZ
        self.funcs[W_v] -= q_e * self.U_RLZ

class NeutralRegion(Region):
    """
    Parent class for neutral regions (in contrast to areas within the space charge region)
    """

    def __init__(self):
        Region.__init__(self)
        self.funcs = {
            rho: 0,
            E: 0,
            phi: 0,
            W_v: 0
        }

class SpaceChargeRegion(Region):
    """
    Parent class for areas within the space charge region
    """

    def __init__(self):
        Region.__init__(self)

    def charge_carriers(self):
        self.n = N_d * exp((self.funcs[phi] - self.U_RLZ) / U_T)
        self.p = N_a * exp(-1 * self.funcs[phi] / U_T)

    def apply_voltage(self, U):
        # U_RLZ = U_D - U_ext
        self.U_RLZ -= U

# ----------------------------------------------------------------------------

class NeutralPRegion(NeutralRegion, NDotation):
    def __init__(self):
        # Parent class initialisation
        NeutralRegion.__init__(self)
        PDotation.__init__(self)

        # Charge carrier density (thermodynamic equilibrium)
        self.p = self.pp0
        self.n = self.np0

    def apply_voltage(self, U):
        # Minority changes with external voltage
        self.n = self.np0 + self.np0 * (exp(U/U_T) - 1) * sinh((w_p + x)/L_n) / sinh((w_p + x_p)/L_n)


class NeutralNRegion(NeutralRegion, NDotation):
    def __init__(self):
        # Parent class initialisation
        NeutralRegion.__init__(self)
        NDotation.__init__(self)
        
        self.adjust_for_integration_constants()

        # Charge carrier density (thermodynamic equilibrium)
        self.n = self.nn0
        self.p = self.pn0

    def apply_voltage(self, U):
        # Minority changes with external voltage
        self.p = self.pn0 + self.pn0 * (exp(U/U_T) - 1) * sinh((w_n - x)/L_p) / sinh((w_n - x_n)/L_p)

# ----------------------------------------------------------------------------

class P_SCR(SpaceChargeRegion, PDotation):

    def __init__(self):
        # Parent class initialisation
        SpaceChargeRegion.__init__(self)
        PDotation.__init__(self)
        self.rho = -1 * q_e * N_a

        self.simulate(x_p, x)
        self.charge_carriers()

class N_SCR(SpaceChargeRegion, NDotation):

    def __init__(self):
        # Parent class initialisation
        SpaceChargeRegion.__init__(self)
        NDotation.__init__(self)
        self.rho = q_e * N_d

        self.simulate(x_n, x)
        self.charge_carriers()
        self.adjust_for_integration_constants()
