from pathlib import Path

import numpy as np
import pytest

from resin_spectral_analysis.absorberspectrum import AbsorberSpectrum


def test_absorberspectrum():
    directory = Path(__file__).resolve().parent / "files_for_test_absorberspectrum"
    absorber = AbsorberSpectrum(directory)

    assert absorber.molar_mass_g_per_mole == 310.39

    assert absorber.calc_absorbance(325.0) == 1.5
    assert np.allclose(
        absorber.calc_absorbance(np.array([375.0, 425.0])), np.array([3.0, 6.0])
    )

    assert absorber.calc_molar_absorptivity(325.0) == 1.5
    assert np.allclose(
        absorber.calc_molar_absorptivity(np.array([375.0, 425.0])), np.array([3.0, 6.0])
    )

    assert absorber.name == "Avobenzone"
