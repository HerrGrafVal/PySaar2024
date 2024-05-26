from symbols import *
from cache import read_from_file
from read_dataframe import fill_values
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np

WIDTH = 8


func_names = ["rho", "E", "phi", "W_v"]

try:
	for i in func_names:
		exec(i + " = read_from_file('" + i + "_results.txt', namespace)")
except FileNotFoundError:
	print("Saved function(s) missing. Please execute modell.py and try again.")
	exit()

# Lambdify all functions in func_names
for i in func_names:
    exec(i + "_num = sp.lambdify(x, fill_values(" + i + "))", globals())

x_p = float(fill_values(x_p))
x_n = float(fill_values(x_n))
w_p = abs(x_p * WIDTH)
w_n = x_n * WIDTH

xx = np.linspace(-1 * w_p, w_n, 1000)

fig, (plt_rho, plt_E, plt_phi, plt_W) = plt.subplots(4, 1)
plt_rho.plot(xx, rho_num(xx))
plt_E.plot(xx, E_num(xx))
plt_phi.plot(xx, phi_num(xx))
plt_W.plot(xx, W_v_num(xx))
plt_W.plot(xx, W_v_num(xx) + fill_values(W_g))
plt.show()