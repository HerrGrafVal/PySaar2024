scripts.DDM\_ode
================

| *DDM\_ode* solves DDM equations numerically using the mpmath module.
| For solving ODEs please see ``mpmath.odefun()`` documentation.

Since x values for initial conditions are unknown and we need to move in -x direction  for n-area integration (which is not supported by mpmath ode solutions) a few tricks are employed when this script is executed. By using ``0, (0, 0)`` as start value for both areas we can approximate how they behave over x. Raising n-area potential values by ``U_D`` [1]_ we can look at the amount of steps required in the p / n-area each until both their potential and field strength values meet. Once we know how many x-steps per area are needed we can flip the x or (phi, E) values (and adjust signs) to gain proper results across all the Space-Charge-Region.

| See project presentation slides (Link in git README) for more.
| 
| Solutions are saved in a dictionary and pickled to *SAVE_FOLDER/ODE_solution.pkl*
| 
| 

.. automodule:: DDM_ode
   :members:
   :undoc-members:
   :show-inheritance:

| 
| 

.. [1] At this point in development it is unclear whether the calculation used for ``U_D`` is correct outside of rectangular charge-carrier-density. The resulting error would be minimal, barely affecting model output.