from sympy import Eq, exp, sqrt, sinh, simplify
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
electron_transport = Eq(J_n, q_e * (n * mu_n * E + D_n * n.diff(x)))
hole_transport = Eq(J_p, q_e * (p * mu_p * E + D_p * p.diff(x)))
electron_continuity = Eq(J_n.diff(x), q_e * (n - n0)/tau_n)
hole_continuity = Eq(J_p.diff(x), q_e * (p - p0)/tau_p)

# ----------------------------------------------------------------------------

class PDotation():
    def __init__(self):
        # Dotation and charge carrier density
        self.pp0 = N_a
        self.np0 = (n_i**2) / self.pp0
        self.N_am = N_a
        self.N_dp = 0
      
class NDotation():
    def __init__(self):
        # Dotation and charge carrier density
        self.nn0 = N_d
        self.pn0 = (n_i**2) / self.nn0
        self.N_dp = N_d
        self.N_am = 0

class NeutralRegion():
    def __init__(self):
        # Adjust DDM equations
        self.charge_density = Eq(rho, 0)
        self.field_strength = Eq(E, 0)
        # Diffusionlength for charge minority
        self.L_n = sqrt(tau_n * D_n)
        self.L_p = sqrt(tau_p * D_p)

    def use_self(self, EQS):
        new_EQS = []
        for EQ in EQS:
            EQ = EQ.subs(N_dp, self.N_dp)
            EQ = EQ.subs(N_am, self.N_am)
            EQ = EQ.subs(n, self.n)
            EQ = EQ.subs(n0, self.n0)
            EQ = EQ.subs(p, self.p)
            EQ = EQ.subs(p0, self.p0)
            new_EQS.append(EQ)
        return new_EQS

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
        self.use_self()
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

        # See page 209, 220f
        # Charge Majority
        self.p = self.pp0
        self.p0 = self.pp0
        # Charge Minority
        self.n = Function("n_p")(x)
        self.n0 = self.np0
        self.minority_density = Eq(n, n0 + n0 * (exp(U_ext/U_T) - 1) * sinh((w_p + x)/self.L_n) / sinh((w_p + x_p)/self.L_n))
    
    def solve_minority(self, U):
        # P-Region, electron minority
        if U == 0:
            self.n = self.n0
            return self.n
        else:
            EQS = [electron_transport.subs(E, 0), electron_continuity, self.minority_density.subs(U_ext, U)]
            self.EQS = self.use_self(EQS)
            self.funcs = [J_n, self.n, tau_n]
            sol = dsolve_system(self.EQS, self.funcs, x)
            return sol

class NeutralNRegion(NeutralRegion, NDotation):
    def __init__(self):
        # Parent class initialisation
        NeutralRegion.__init__(self)
        NDotation.__init__(self)

        # Adjust DDM equations
        self.potential = Eq(phi, U_D)
        self.valence = Eq(W_v, q_e * U_D)

        # See page 209, 220f
        # Charge Majority
        self.n = self.nn0
        self.p = self.pn0
        # Charge Minority
        minority_density = Eq(self.p, self.pn0 + self.pn0 * (exp(U_ext/U_T) - 1) * sinh((w_n - x)/self.L_p) / sinh((w_n - x_n)/self.L_p))
        


# ----------------------------------------------------------------------------

class P_SCR(SpaceChargeRegion, PDotation):

    def __init__(self, x_p):
        # Parent class initialisation
        SpaceChargeRegion.__init__(self)
        PDotation.__init__(self)

        self.p = self.pp0
        self.p0 = self.pp0
        self.n = self.np0
        self.n0 = self.np0

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

        self.p = self.pn0
        self.p0 = self.pn0
        self.n = self.nn0
        self.n0 = self.nn0

        # Boltzmann boundary conditions, see page 205f
        self.ics = {
            n.subs(x, x_n) : N_d,
            p.subs(x, x_n) : N_a * exp(-U_D/U_T),
            }
