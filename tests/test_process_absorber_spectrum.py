from pathlib import Path

import numpy as np
import pytest

from spectra.process_absorber_spectrum import (
    read_spectrum_config_json,
    find_indices_of_range,
    select_wavelength_range,
    calc_absorbance,
    calc_molar_concentration,
    calc_molar_absorptivity,
    process_spectrum_data,
)


def test_read_spectrum_config_json():
    pass


def test_select_wavelength_range():
    temp = np.array([[1, 10], [2, 20], [3, 30], [4, 40], [5, 50], [6, 60],])

    temp2 = select_wavelength_range(temp, 2.1, 4.9)

    assert np.array_equal(temp2, np.array([[2, 20], [3, 30], [4, 40], [5, 50]]))

