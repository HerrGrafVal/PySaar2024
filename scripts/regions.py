from sympy import Eq, exp, simplify
from sympy.solvers.ode.systems import dsolve_system
from symbols import *

# Drift Diffusion Modell (DDM) equations
bandgap = Eq(W_c, W_v + W_g)
charge_density = Eq(rho, q_e * (p + N_dp - n - N_am))
field_strength = Eq(E.diff(x), rho / eps)
potential = Eq(phi.diff(x), -1 * E)
field_energy = Eq(W_v.diff(x), q_e * E)
electron_density = Eq(n, N_c * exp(-1 * (W_c - W_Fn) / (k * T)))
hole_density = Eq(p, N_v * exp(-1 * (W_Fp - W_v) / (k * T)))

# ----------------------------------------------------------------------------

class PDotation():
    def __init__(self):
        # Dotation and charge carrier density
        self.p0 = N_a
        self.n0 = (n_i**2) / self.p0
        self.N_am = N_a
        self.N_dp = 0

class NDotation():
    def __init__(self):
        # Dotation and charge carrier density
        self.n0 = N_d
        self.p0 = (n_i**2) / self.n0
        self.N_dp = N_d
        self.N_am = 0

class NeutralRegion():
    def __init__(self):
        # Adjust DDM equations
        self.charge_density = Eq(rho, 0)
        self.field_strength = Eq(E, 0)

class SpaceChargeRegion():
    def __init__(self):
        # Select relevant DDM equations
        # self.EQS = [bandgap, charge_density, field_strength, potential, field_energy, electron_density, hole_density]
        self.EQS = [bandgap, charge_density, field_strength, potential, field_energy]
        # self.funcs = [rho, E, phi, W_v, W_c, p, n]
        self.funcs = [rho, E, phi, W_v, W_c]

    def use_self(self):
        new_EQS = []
        for EQ in self.EQS:
            EQ = EQ.subs(N_dp, self.N_dp)
            EQ = EQ.subs(N_am, self.N_am)
            EQ = EQ.subs(n, self.n0)
            EQ = EQ.subs(p, self.p0)
            new_EQS.append(EQ)
        self.EQS = new_EQS


    def get_sol_dict(self):
        # Solve DDM and return result as Dictionary rather than list of EQs
        # EQS_SOLVED = dsolve_system(self.EQS, self.funcs, x, self.ics)[0]
        EQS_SOLVED = dsolve_system(self.EQS, self.funcs, x)[0]
        sol_dict = {}
        for EQ in EQS_SOLVED:
            sol_dict[EQ.lhs] = simplify(EQ.rhs)
        return sol_dict


# ----------------------------------------------------------------------------

class NeutralPRegion(NeutralRegion, NDotation):
    def __init__(self):
        # Parent class initialisation
        NeutralRegion.__init__(self)
        PDotation.__init__(self)

        # Adjust DDM equations
        self.potential = Eq(phi, 0)
        self.valence = Eq(W_v, 0)

        # Minority changes with external voltage!
        # Yet to be implemented, see page 209
        self.n = self.n0
        self.p = self.p0

class NeutralNRegion(NeutralRegion, NDotation):
    def __init__(self):
        # Parent class initialisation
        NeutralRegion.__init__(self)
        NDotation.__init__(self)

        # Adjust DDM equations
        self.potential = Eq(phi, U_D)
        self.valence = Eq(W_v, q_e * U_D)

        # Minority changes with external voltage!
        # Yet to be implemented, see page 209
        self.n = self.n0
        self.p = self.p0

# ----------------------------------------------------------------------------

class P_SCR(SpaceChargeRegion, PDotation):

    def __init__(self, x_p):
        # Parent class initialisation
        SpaceChargeRegion.__init__(self)
        PDotation.__init__(self)

        # Boltzmann boundary conditions, see page 205f
        self.ics = {
            n.subs(x, x_p) : N_d * exp(-U_D/U_T),
            p.subs(x, x_p) : N_a
            }

class N_SCR(SpaceChargeRegion, NDotation):

    def __init__(self, x_n):
        # Parent class initialisation
        SpaceChargeRegion.__init__(self)
        NDotation.__init__(self)

        # Boltzmann boundary conditions, see page 205f
        self.ics = {
            n.subs(x, x_n) : N_d,
            p.subs(x, x_n) : N_a * exp(-U_D/U_T),
            }
