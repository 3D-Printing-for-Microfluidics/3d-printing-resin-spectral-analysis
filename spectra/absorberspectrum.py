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
