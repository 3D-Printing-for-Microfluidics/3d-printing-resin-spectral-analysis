import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

from spectra.irradiance import Irradiance
from spectra.utilities import ArrayParams
from spectra.spectrummodels import (
    ha_model,
    a_b_model,
    a_b_c_model,
    fit_ha_model,
    fit_a_b_model,
    fit_a_b_c_model,
)


class NormalizedDose:
    def __init__(self, *, irradiance, z_array_params):

        assert isinstance(irradiance, Irradiance)
        assert isinstance(z_array_params, ArrayParams)

        # Store inputs
        self.irradiance = irradiance
        self.z_array_params = z_array_params

        # Create array of z values in microns
        self.z_um = np.linspace(*z_array_params)

        # Pre-calculate source integral over wavelengths
        self.source_integral = integrate.simps(
            self.irradiance(0), self.irradiance.wavelengths
        )

        # Calculate normalized dose as a function of z
        self.normalized_dose = self._calc_normalized_dose()

        # Fit normalized dose to models
        self.ha_model_params = self._fit_to_ha_model()
        self.a_b_model_params = self._fit_to_a_b_model()
        self.a_b_c_model_params = self._fit_to_a_b_c_model()

        # Calculate normalized dose for each model
        self.ha_model = ha_model(self.z_um, self.ha_model_params["ha"])
        self.a_b_model = a_b_model(
            self.z_um, self.a_b_model_params["a"], self.a_b_model_params["b"]
        )
        self.a_b_c_model = a_b_c_model(
            self.z_um,
            self.a_b_c_model_params["a"],
            self.a_b_c_model_params["b"],
            self.a_b_c_model_params["c"],
        )

    def _calc_normalized_dose(self):
        """Calculate normalized dose as a function of z."""
        norm_dose = np.zeros(len(self.z_um))
        for i, z_value in enumerate(self.z_um):
            norm_dose[i] = (
                integrate.simps(self.irradiance(z_value), self.irradiance.wavelengths)
                / self.source_integral
            )
        return norm_dose

    def _fit_to_ha_model(self):
        popt, pcov = fit_ha_model(self.z_um, self.normalized_dose)
        ha_model_params = {}
        ha_model_params["ha"] = popt[0]
        ha_model_params["stdev"] = np.sqrt(np.diag(pcov))
        return ha_model_params

    def _fit_to_a_b_model(self):
        popt, pcov = fit_a_b_model(self.z_um, self.normalized_dose)
        a_b_model_params = {}
        a_b_model_params["a"] = popt[0]
        a_b_model_params["b"] = popt[1]
        a_b_model_params["stdev"] = np.sqrt(np.diag(pcov))
        return a_b_model_params

    def _fit_to_a_b_c_model(self):
        popt, pcov = fit_a_b_c_model(self.z_um, self.normalized_dose)
        a_b_c_model = {}
        a_b_c_model["a"] = popt[0]
        a_b_c_model["b"] = popt[1]
        a_b_c_model["c"] = popt[2]
        a_b_c_model["stdev"] = np.sqrt(np.diag(pcov))
        return a_b_c_model

    def plot(self, grid=True, title=None, file=None):
        fig, ax = plt.subplots()
        ax.plot(self.z_um, self.normalized_dose, "r", label="$D_n(z)$")

        text_func3 = "fit: y = a*exp(-z/b) + c\n"
        model = self.a_b_c_model_params
        ax.plot(
            self.z_um,
            self.a_b_c_model,
            "r--",
            label=text_func3
            + "a={:4.3}, b={:5.3f}, c={:5.3f}".format(model["a"], model["b"], model["c"]),
        )

        text_func2 = "fit: y = a*exp(-z/b) + (1-a)\n"
        model = self.a_b_model_params
        ax.plot(
            self.z_um,
            self.a_b_model,
            "g-.",
            label=text_func2 + "a={:4.3}, b={:5.3f}".format(model["a"], model["b"]),
        )

        text_func1 = "fit: y = exp(-z/b)\n"
        model = self.ha_model_params
        ax.plot(
            self.z_um,
            self.ha_model,
            "r:",
            label=text_func1 + "b={:7.5f}".format(model["ha"]),
        )

        ax.set_xlim(0,)
        ax.set_xlabel(r"z ($\mu$m)")
        ax.set_ylabel("D'(z)")
        ax.set_ylim(0, 1)
        ax.legend()

        if grid:
            ax.grid()

        if title:
            ax.set_title(title)

        if file:
            plt.savefig(file)

        return fig, ax
