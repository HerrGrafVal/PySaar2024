from cache import pickle_read
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

results = pickle_read("ODE_solution")
xx = results["xx"]
xx_rho = results["xx_rho"]
phi = results["phi"]
E = results["E"]
W_v = results["W_v"]
W_c = results["W_c"]
W_F = results["W_F"]
p = results["p"]
n = results["n"]
rho = results["rho"]

"""
ToDo:
Add x_p, x_n tick labels
"""

form_x = EngFormatter(unit = "$m$")
form_cc = EngFormatter(unit = "$m^{-3}$")
form_rho = EngFormatter(unit = "$C / m^{-3}$")
form_E = EngFormatter(unit = "$V / m$")
form_phi = EngFormatter(unit = "$V$")
form_W = EngFormatter(unit = "$eV$")

fig, (plt_cc, plt_rho, plt_E, plt_phi, plt_W) = plt.subplots(5,1)
fig.subplots_adjust(hspace = 1.5)

plt_cc.set_title("Ladungsträgerdichten")
plt_cc.plot(xx, p, "C0", label = "$log_{10}$ $p (x)$")
plt_cc.plot(xx, n, "C1", label = "$log_{10}$ $n (x)$")
plt_cc.xaxis.set_major_formatter(form_x)
plt_cc.yaxis.set_major_formatter(form_cc)
plt_cc.legend()

plt_rho.set_title("Raumladungsdichte")
plt_rho.plot(xx_rho, rho, "C0", label = "$\\rho (x)$")
plt_rho.xaxis.set_major_formatter(form_x)
plt_rho.yaxis.set_major_formatter(form_rho)
plt_rho.legend()

plt_E.set_title("Feldstärke")
plt_E.plot(xx, E, "C0", label = "$E (x)$")
plt_E.xaxis.set_major_formatter(form_x)
plt_E.yaxis.set_major_formatter(form_E)
plt_E.legend()

plt_phi.set_title("Potential")
plt_phi.plot(xx, phi, "C0", label = "$\\varphi (x)$")
plt_phi.xaxis.set_major_formatter(form_x)
plt_phi.yaxis.set_major_formatter(form_phi)
plt_phi.legend()

plt_W.set_title("Bandverläufe")
plt_W.plot(xx, W_v, "C0", label = "$W_V (x)$")
plt_W.plot(xx, W_c, "C1", label = "$W_C (x)$")
plt_W.plot([xx[0], xx[-1]], [W_F, W_F], "C2", label = "$W_F$")
plt_W.xaxis.set_major_formatter(form_x)
plt_W.yaxis.set_major_formatter(form_W)
plt_W.legend()

plt.show()