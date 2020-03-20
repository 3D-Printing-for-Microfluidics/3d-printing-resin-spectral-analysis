import numpy as np


class AbsorberSpectrum:
    """Optical absorption spectrum data.
    """

    def __init__(self, directory):
        self._data = np.loadtxt(directory / "molar_absorptivity.csv", delimiter=",")
        self.wavelength = self._data[:, 0]
        self.molar_absorptivity = self._data[:, 1]
