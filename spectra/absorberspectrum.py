import numpy as np
import json


class AbsorberSpectrum:
    """Optical absorption spectrum data.
    """

    def __init__(self, directory):

        # Read absorbance data
        self._data_absorbance = np.loadtxt(directory / "absorbance.csv", delimiter=",")
        self.wavelength_absorbance = self._data_absorbance[:, 0]
        self.absorbance = self._data_absorbance[:, 1]

        # Read molar absorptivity data
        self._data = np.loadtxt(directory / "molar_absorptivity.csv", delimiter=",")
        self.wavelength = self._data[:, 0]
        self.molar_absorptivity = self._data[:, 1]

        # Make sure the two datasets have the same wavelengths (this helps ensure they
        # came from the same calculation and are consistent)
        assert np.allclose(self.wavelength_absorbance, self.wavelength)

        # Extract information from json string on first line of molar absorptivity file
        with (directory / "molar_absorptivity.csv").open("r") as f:
            temp = f.readline()
        # remove leading '#' character
        temp = temp[1:].strip()
        self.parameters = json.loads(temp)
        self.molar_mass_g_per_mole = self.parameters["Molar mass g/mole"]

    def calc_molar_absorptivity(self, wavelength):
        """Given wavelength, interpolate corresponding molar absorptivity value.

        See numpy.interp documentation for interpolation details.

        Parameters
        ----------
        wavelength - array_like (can be single value or 1D list/numpy.array of values)

        Returns
        -------
        single value or 1D numpy array corresponding to shape of wavelength
        """
        return np.interp(
            wavelength, self.wavelength, self.molar_absorptivity, left=0.0, right=0.0
        )

    def calc_absorbance(self, wavelength):
        """Given wavelength, interpolate corresponding absorbance value.

        See numpy.interp documentation for interpolation details.

        Parameters
        ----------
        wavelength - array_like (can be single value or 1D list/numpy.array of values)

        Returns
        -------
        single value or 1D numpy array corresponding to shape of wavelength
        """
        return np.interp(
            wavelength, self.wavelength, self.absorbance, left=0.0, right=0.0
        )
