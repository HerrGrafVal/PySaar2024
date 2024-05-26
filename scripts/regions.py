from sympy import Eq, exp, sqrt, sinh, simplify
from sympy.solvers.ode.systems import dsolve_system
from symbols import *

# ----------------------------------------------------------------------------

class Region():
    def __init__(self):
        # Setup functions
        self.rho = Function("\\rho")(x)

    def simulate(self, a, b):
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
    def __init__(self):
        # Dotation and charge carrier density
        self.pp0 = N_a
        self.np0 = (n_i**2) / self.pp0
        self.N_am = N_a
        self.N_dp = 0
        self.n = Function("n_p")(x)
        self.p = Function("p_p")(x)
      
class NDotation():
    def __init__(self):
        # Dotation and charge carrier density
        self.nn0 = N_d
        self.pn0 = (n_i**2) / self.nn0
        self.N_dp = N_d
        self.N_am = 0
        self.n = Function("n_n")(x)
        self.p = Function("p_n")(x)

    def adjust_for_integration_constants(self):
        self.funcs[phi] += U_D
        self.funcs[W_v] -= q_e * U_D

class NeutralRegion(Region):
    def __init__(self):
        Region.__init__(self)
        self.funcs = {
            rho: 0,
            E: 0,
            phi: 0,
            W_v: 0
        }

class SpaceChargeRegion(Region):
    def __init__(self):
        Region.__init__(self)

# ----------------------------------------------------------------------------

class NeutralPRegion(NeutralRegion, NDotation):
    def __init__(self):
        # Parent class initialisation
        NeutralRegion.__init__(self)
        PDotation.__init__(self)

        # Majority
        self.p = self.pp0
        # Minority changes with external voltage! Yet to be implemented
        self.n = self.np0


class NeutralNRegion(NeutralRegion, NDotation):
    def __init__(self):
        # Parent class initialisation
        NeutralRegion.__init__(self)
        NDotation.__init__(self)

        self.adjust_for_integration_constants()

        # Majority
        self.n = self.nn0
        # Minority changes with external voltage! Yet to be implemented
        self.p = self.pn0

# ----------------------------------------------------------------------------

class P_SCR(SpaceChargeRegion, PDotation):

    def __init__(self):
        # Parent class initialisation
        SpaceChargeRegion.__init__(self)
        PDotation.__init__(self)
        self.rho = -1 * q_e * N_a

        self.simulate(x_p, x)

class N_SCR(SpaceChargeRegion, NDotation):

    def __init__(self):
        # Parent class initialisation
        SpaceChargeRegion.__init__(self)
        NDotation.__init__(self)
        self.rho = q_e * N_d

        self.simulate(x_n, x)
        self.adjust_for_integration_constants()
