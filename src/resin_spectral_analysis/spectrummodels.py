import numpy as np
from scipy.optimize import curve_fit


def ha_model(z, b):
    return np.exp(-z / b)


def a_b_model(z, a, b):
    return a * np.exp(-z / b) + (1 - a)


def a_b_c_model(z, a, b, c):
    return a * np.exp(-z / b) + c


def fit_ha_model(z, dnorm):
    param_bounds = ([0.1], [np.inf])
    popt, pcov = curve_fit(ha_model, z, dnorm, bounds=param_bounds)
    return popt, pcov


def fit_a_b_model(z, dnorm):
    param_bounds = ([0.0, 0.1], [1.0, np.inf])
    popt, pcov = curve_fit(a_b_model, z, dnorm, bounds=param_bounds)
    return popt, pcov


def fit_a_b_c_model(z, dnorm):
    param_bounds = ([0.0, 0.1, 0.0], [1.0, np.inf, 1.0])
    popt, pcov = curve_fit(a_b_c_model, z, dnorm, bounds=param_bounds)
    return popt, pcov
