from pathlib import Path

import numpy as np


class SourceSpectrum:
    """Optical spectrum data.
    """

    def __init__(self, directory):
        assert isinstance(directory, Path)
        self.name = directory.name
        self._data = np.loadtxt(
            directory / "measured_spectrum_normalized.csv", delimiter=","
        )
        self.wavelength = self._data[:, 0]
        self.power = self._data[:, 1]

    def calc_power(self, wavelength):
        """Given wavelength, interpolate corresponding power value.

        See numpy.interp documentation for interpolation details.

        Parameters
        ----------
        wavelength - array_like (can be single value or 1D list/numpy.array of values)

        Returns
        -------
        single value or 1D numpy array corresponding to shape of wavelength
        """
        return np.interp(wavelength, self.wavelength, self.power, left=0.0, right=0.0)
