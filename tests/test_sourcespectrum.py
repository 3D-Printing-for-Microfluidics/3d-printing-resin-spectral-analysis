from pathlib import Path

import numpy as np

from resin_spectral_analysis.sourcespectrum import SourceSpectrum


def test_sourcespectrum():
    directory = Path(__file__).resolve().parent / "files_for_test_sourcespectrum"
    source = SourceSpectrum(directory)

    assert source.calc_power(325.0) == 1.5
    assert np.allclose(source.calc_power(np.array([375.0, 425.0])), np.array([3.0, 6.0]))
