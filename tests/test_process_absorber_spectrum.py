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
    json_file = Path(__file__).parent / "files_for_tests" / "spectrum_config.json"
    temp = read_spectrum_config_json(json_file)
    result = {
        "Measurement": "Avobenzone absorption in PEGDA",
        "Measurement Date": "2020-01-20",
        "Measurement Spectrometer": "Ocean Optics FIRE",
        "Absorber": "Avobenzone",
        "Concentration w/w percent": 0.24,
        "Film thickness microns": 60,
        "Molar mass g/mole": 310.39,
        "Solvent": "PEGDA",
        "Solvent density g/L": 1110,
        "Solvent absorption measurement file": "QEPB00791_17-10-07-458.txt",
        "Solvent + absorber absorption measurement file": "QEPB00791_17-18-57-140.txt",
    }
    assert temp == result


def test_select_wavelength_range():
    temp = np.array([[1, 10], [2, 20], [3, 30], [4, 40], [5, 50], [6, 60],])

    temp2 = select_wavelength_range(temp, 2.1, 4.9)

    assert np.array_equal(temp2, np.array([[2, 20], [3, 30], [4, 40], [5, 50]]))


def test_absorbance():
    # force_positive=False case
    temp1 = np.array([[1, 10], [2, 20], [3, 30], [4, 40], [5, 50], [6, 60],])
    temp2 = np.array([[1, 1], [2, 19], [3, 3], [4, 38], [5, 5], [6, 57],])
    absorbance = calc_absorbance(temp1, temp2, 2.1, 4.9, False)
    result = np.array([[2.0, 0.02227639], [3.0, 1.0], [4.0, 0.02227639], [5.0, 1.0]])
    assert np.allclose(absorbance, result)

    # force_positive=True with num_samples_for_average=2
    temp1 = np.array([[1, 10], [2, 20], [3, 30], [4, 40], [5, 50], [6, 60],])
    temp2 = np.array([[1, 1], [2, 22], [3, 3], [4, 44], [5, 55], [6, 66],])
    absorbance = calc_absorbance(temp1, temp2, 2.1, 4.9, True, num_samples_for_average=2)
    result = np.array([[2.0, 0.0], [3.0, 1.04139269], [4.0, 0.0], [5.0, 0.0]])
    assert np.allclose(absorbance, result)


def test_calc_molar_concentration():
    # Use made-up values
    molar_concentration = calc_molar_concentration(1.0, 1000.0, 500.0)
    assert molar_concentration == 0.02


def test_calc_molar_absorptivity():
    # Use made-up values
    molar_absorptivity = calc_molar_absorptivity(1.0, 0.02, 100)
    assert molar_absorptivity == 5000.0
