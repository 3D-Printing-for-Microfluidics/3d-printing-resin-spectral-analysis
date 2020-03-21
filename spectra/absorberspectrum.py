import numpy as np


class AbsorberSpectrum:
    """Optical absorption spectrum data.
    """

    def __init__(self, directory):

        self._data_absorbance = np.loadtxt(directory / "absorbance.csv", delimiter=",")
        self.wavelength_absorbance = self._data_absorbance[:, 0]
        self.absorbance = self._data_absorbance[:, 1]

        self._data = np.loadtxt(directory / "molar_absorptivity.csv", delimiter=",")
        self.wavelength = self._data[:, 0]
        self.molar_absorptivity = self._data[:, 1]

        assert np.allclose(self.wavelength_absorbance, self.wavelength)

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
        return np.interp(wavelength, self.wavelength, self.molar_absorptivity)

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
        return np.interp(wavelength, self.wavelength, self.absorbance)
