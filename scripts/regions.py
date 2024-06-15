from symbols import *
from sympy import Eq, exp, sqrt, sinh, simplify
from sympy.solvers.ode.systems import dsolve_system

# ----------------------------------------------------------------------------

class Region():
    """
    | Parent class for all region classes. (This excludes Dotation classes)

    +---------------+-------------------+------------------------+
    | Attribute     | Type              | Explanation            |
    +===============+===================+========================+
    | ``self.rho``  | *sympy.Function*  | Raumladungsdichte      |
    +---------------+-------------------+------------------------+
    | ``self.U_RLZ``| *sympy.expression*| Spannung über RLZ      |
    +---------------+-------------------+------------------------+
    | ``self.E``    | *sympy.expression*| Feldstärke             |
    +---------------+-------------------+------------------------+
    | ``self.phi``  | *sympy.expression*| Potential              |
    +---------------+-------------------+------------------------+
    | ``self.W_v``  | *sympy.expression*| Valenzbandkante        |
    +---------------+-------------------+------------------------+
    | ``self.funcs``| *dict*            | Keys: rho, E, phi, W_v |
    +---------------+-------------------+------------------------+

    :methods: ``Region.simulate()``
    """

    def __init__(self):
        """
        | Define ``self.rho`` and ``self.U_RLZ``
        | Other attributes of this class are initiated when calling ``Region.simulate()``

        :return: *self*
        """

        # Setup functions
        self.rho = Function("\\rho")(x)

        # Setup voltage
        self.U_RLZ = U_D

    def simulate(self, a, b):
        """
        | Define derived DDM functions
        | Save results in ``self.funcs`` dict

        :param a: Left integration border
        :type a: float
        :param b: Right integration border
        :type b: float
        :return: *None*
        """
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
    | Parent class for all p-dotated areas
    | Includes dotation and charge carrier density
    """

    def __init__(self):
        """
        | Defines variables for dotation and charge carrier density
        | See source code

        :return: *self*
        """

        self.pp0 = N_a
        self.np0 = (n_i**2) / self.pp0
        self.N_am = N_a
        self.N_dp = 0
        self.n = Function("n_p")(x)
        self.p = Function("p_p")(x)
      
class NDotation():
    """
    | Parent class for all n-dotated areas
    | Includes dotation and charge carrier density

    :methods: ``NDotation.adjust_for_integration_constants()``
    """

    def __init__(self):
        """
        | Defines variables for dotation and charge carrier density
        | See source code

        :return: *self*
        """

        self.nn0 = N_d
        self.pn0 = (n_i**2) / self.nn0
        self.N_dp = N_d
        self.N_am = 0
        self.n = Function("n_n")(x)
        self.p = Function("p_n")(x)

    def adjust_for_integration_constants(self):
        """
        | Adjusts ``self.funcs[phi]`` and ``self.funcs[W_v]``
        | Necessary since n-regions are set at greater x values than p-regions

        :return: *None*
        """

        self.funcs[phi] += self.U_RLZ
        self.funcs[W_v] -= q_e * self.U_RLZ

class NeutralRegion(Region):
    """
    | Subclass of ``regions.Region()``
    | Parent class for neutral regions (in contrast to areas within the space charge region)
    | Has all ``self.funcs`` values at zero
    """

    def __init__(self):
        """
        | Initialize parent class
        | Set all ``self.funcs`` values to zero

        :return: *self*
        """

        Region.__init__(self)
        self.funcs = {
            rho: 0,
            E: 0,
            phi: 0,
            W_v: 0
        }

class SpaceChargeRegion(Region):
    """
    | Subclass of ``regions.Region()``
    | Parent class for areas within the space charge region

    :attributes: ``self.n`` , ``self.p``

    :methods: ``SpaceChargeRegion.charge_carriers()``
              ``SpaceChargeRegion.apply_voltage()``
    """

    def __init__(self):
        """
        | Initialize parent class

        :return: *self*
        """

        Region.__init__(self)

    def charge_carriers(self):
        """
        | Defines variables for charge carrier density ``self.n`` , ``self.p``

        :return: *None*
        """

        self.n = N_d * exp((self.funcs[phi] - self.U_RLZ) / U_T)
        self.p = N_a * exp(-1 * self.funcs[phi] / U_T)

    def apply_voltage(self, U):
        """
        | Adjusts ``self.U_RLZ`` according to external voltage

        :param U: External voltage
        :type U: float
        :return: *None*
        """
        # U_RLZ = U_D - U_ext
        self.U_RLZ -= U

# ----------------------------------------------------------------------------

class NeutralPRegion(NeutralRegion, PDotation):
    """
    | Subclass of ``regions.NeutralRegion()`` and ``regions.PDotation()``

    :methods: ``NeutralPRegion.apply_voltage()``
    """

    def __init__(self):
        """
        | Initialize parent classes and set charge carrier density

        :return: *self*
        """

        # Parent class initialisation
        NeutralRegion.__init__(self)
        PDotation.__init__(self)

        # Charge carrier density (thermodynamic equilibrium)
        self.p = self.pp0
        self.n = self.np0

    def apply_voltage(self, U):
        """
        | Adjust charge minority carrier density according to external voltage

        :param U: External voltage
        :type U: float
        :return: *None*
        """

        # Minority changes with external voltage
        self.n = self.np0 + self.np0 * (exp(U/U_T) - 1) * sinh((w_p + x)/L_n) / sinh((w_p + x_p)/L_n)


class NeutralNRegion(NeutralRegion, NDotation):
    """
    | Subclass of ``regions.NeutralRegion()`` and ``regions.NDotation()``

    :methods: ``NeutralNRegion.apply_voltage()``
    """

    def __init__(self):
        """
        | Initialize parent classes and set charge carrier density
        | Call ``NDotation.adjust_for_integration_constants()``

        :return: *self*
        """

        # Parent class initialisation
        NeutralRegion.__init__(self)
        NDotation.__init__(self)
        
        self.adjust_for_integration_constants()

        # Charge carrier density (thermodynamic equilibrium)
        self.n = self.nn0
        self.p = self.pn0

    def apply_voltage(self, U):
        """
        | Adjust charge minority carrier density according to external voltage

        :param U: External voltage
        :type U: float
        :return: *None*
        """

        # Minority changes with external voltage
        self.p = self.pn0 + self.pn0 * (exp(U/U_T) - 1) * sinh((w_n - x)/L_p) / sinh((w_n - x_n)/L_p)

# ----------------------------------------------------------------------------

class P_SCR(SpaceChargeRegion, PDotation):
    """
    | Subclass of ``regions.SpaceChargeRegion()`` and ``regions.PDotation()``
    """

    def __init__(self):
        """
        | Initialize parent classes and set ``self.rho``
        | Call ``Region.simulate()`` to create and populate ``self.funcs``
        | Call ``SpaceChargeRegion.charge_carriers()``

        :return: *self*
        """

        # Parent class initialisation
        SpaceChargeRegion.__init__(self)
        PDotation.__init__(self)
        self.rho = -1 * q_e * N_a

        self.simulate(x_p, x)
        self.charge_carriers()

class N_SCR(SpaceChargeRegion, NDotation):
    """
    | Subclass of ``regions.SpaceChargeRegion()`` and ``regions.NDotation()``
    """

    def __init__(self):
        """
        | Initialize parent classes and set ``self.rho``
        | Call ``Region.simulate()`` to create and populate ``self.funcs``
        | Call ``SpaceChargeRegion.charge_carriers()``
        | Call ``NDotation.adjust_for_integration_constants()``

        :return: *self*
        """

        # Parent class initialisation
        SpaceChargeRegion.__init__(self)
        NDotation.__init__(self)
        self.rho = q_e * N_d

        self.simulate(x_n, x)
        self.charge_carriers()
        self.adjust_for_integration_constants()
