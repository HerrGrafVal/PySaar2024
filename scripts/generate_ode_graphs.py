from DDM_ode import xx_p, phi_p, E_p, W_v_p, W_c_p, p_p, n_p, rho_p
from DDM_ode import xx_n, phi_n, E_n, W_v_n, W_c_n, p_n, n_n, rho_n
from DDM_ode import W_F
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

form_x = EngFormatter(unit = "$m$")
form_cc = EngFormatter(unit = "$m^{-3}$")
form_rho = EngFormatter(unit = "$C / m^{-3}$")
form_E = EngFormatter(unit = "$V / m$")
form_phi = EngFormatter(unit = "$V$")
form_W = EngFormatter(unit = "$eV$")

fig, (plt_cc, plt_rho, plt_E, plt_phi, plt_W) = plt.subplots(5,1)
fig.subplots_adjust(hspace = 1.5)

plt_cc.set_title("Ladungsträgerdichten")
plt_cc.plot(xx_p, p_p, "C0", label = "$log_{10}$ $p (x)$")
plt_cc.plot(xx_n, p_n, "C0")
plt_cc.plot(xx_p, n_p, "C1", label = "$log_{10}$ $n (x)$")
plt_cc.plot(xx_n, n_n, "C1")
plt_cc.xaxis.set_major_formatter(form_x)
plt_cc.yaxis.set_major_formatter(form_cc)
plt_cc.legend()

plt_rho.set_title("Raumladungsdichte")
plt_rho.plot(xx_p, rho_p, "C0", label = "$\\rho (x)$")
plt_rho.plot(xx_n, rho_n, "C0")
plt_rho.xaxis.set_major_formatter(form_x)
plt_rho.yaxis.set_major_formatter(form_rho)
plt_rho.legend()

plt_E.set_title("Feldstärke")
plt_E.plot(xx_p, E_p, "C0", label = "$E (x)$")
plt_E.plot(xx_n, E_n, "C0")
plt_E.xaxis.set_major_formatter(form_x)
plt_E.yaxis.set_major_formatter(form_E)
plt_E.legend()

plt_phi.set_title("Potential")
plt_phi.plot(xx_p, phi_p, "C0", label = "$\\varphi (x)$")
plt_phi.plot(xx_n, phi_n, "C0")
plt_phi.xaxis.set_major_formatter(form_x)
plt_phi.yaxis.set_major_formatter(form_phi)
plt_phi.legend()

plt_W.set_title("Bandverläufe")
plt_W.plot(xx_p, W_v_p, "C0", label = "$W_V (x)$")
plt_W.plot(xx_n, W_v_n, "C0")
plt_W.plot(xx_p, W_c_p, "C1", label = "$W_C (x)$")
plt_W.plot(xx_n, W_c_n, "C1")
plt_W.plot([xx_p[0], xx_n[-1]], [W_F, W_F], "C2", label = "$W_F$")
# plt_W.plot([xx_p[0], xx_p[-1]], [W_F, W_F], "C2", label = "$W_F$")
plt_W.xaxis.set_major_formatter(form_x)
plt_W.yaxis.set_major_formatter(form_W)
plt_W.legend()

plt.show()