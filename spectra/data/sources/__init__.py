from pathlib import Path

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


sources = {}

this_dir = Path(__file__).parent

directories = sorted(
    [d for d in this_dir.iterdir() if d.is_dir() and d.name[0] not in [".", "_"]]
)

for d in directories:
    sources[d.name] = SourceSpectrum(d)
