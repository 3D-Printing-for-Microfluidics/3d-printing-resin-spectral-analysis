import numpy as np


class SourceSpectrum:
    """Optical spectrum data.
    """

    def __init__(self, directory):
        self._data = np.loadtxt(
            directory / "measured_spectrum_normalized.csv", delimiter=","
        )
        self.wavelength = self._data[:, 0]
        self.power = self._data[:, 1]
