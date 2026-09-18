from pathlib import Path

import numpy as np

from resin_spectral_analysis.utilities import (
    find_index_of_max,
    shift,
    shift_peak_wavelength,
    ArrayParams,
    read_spectrometer_file,
    read_FIRE_spectrum_data_file,
    read_OE65PRO_spectrum_data_file,
)


def test_find_index_of_max():
    test_array = np.array([0, 1, 3, 2, 5, 0, 1])
    test_array_index_of_max = find_index_of_max(test_array)
    assert test_array_index_of_max == 4


def test_shift():
    start_array = np.array([x + 1 for x in range(10)])

    result = np.array([5, 6, 7, 8, 9, 10, 0, 0, 0, 0])
    assert np.array_equal(shift(start_array, -4), result)

    result = np.array([20, 20, 20, 20, 1, 2, 3, 4, 5, 6])
    assert np.array_equal(shift(start_array, 4, fill_value=20), result)

    assert np.array_equal(shift(start_array, 0), start_array)


def test_shift_peak_wavelength():
    w = np.linspace(
        360, 400, 9
    )  # array([360., 365., 370., 375., 380., 385., 390., 395., 400.])
    p = np.array([1, 2, 3, 4, 3.5, 2.5, 1.5, 1.0, 1.0])
    result = np.array([0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 3.5, 2.5, 1.5])
    assert np.array_equal(shift_peak_wavelength(385, w, p), result)


def test_ArrayParams():
    temp = ArrayParams(300, 440, 11)

    # Check individual values
    assert temp.min_value == 300
    assert temp.max_value == 440
    assert temp.num_pnts == 11

    # Check intended use with numpy.linspace
    temp_array = np.linspace(*temp)
    result = np.array(
        [300.0, 314.0, 328.0, 342.0, 356.0, 370.0, 384.0, 398.0, 412.0, 426.0, 440.0]
    )
    assert np.allclose(temp_array, result)


def test_read_spectrometer_file():
    csv_file = (
        Path(__file__).resolve().parent
        / "files_for_tests"
        / "data_for_test_utilities"
        / "Avobenzone_01per_25ms_1_01.csv"
    )

    header_lines, data = read_spectrometer_file(csv_file)
    assert len(header_lines) == 2
    assert data.shape == (1044, 2)


def test_read_FIRE_spectrum_data_file():
    FIRE_file = (
        Path(__file__).resolve().parent
        / "files_for_tests"
        / "data_for_test_utilities"
        / "FLMS155811_13-39-15-538.txt"
    )

    header_lines, data = read_FIRE_spectrum_data_file(FIRE_file)
    assert len(header_lines) == 14
    assert data.shape == (2048, 2)


def test_read_OE65PRO_spectrum_data_file():
    OE65PRO_file = (
        Path(__file__).resolve().parent
        / "files_for_tests"
        / "data_for_test_utilities"
        / "QEPB00791_17-07-21-669.txt"
    )

    header_lines, data = read_OE65PRO_spectrum_data_file(OE65PRO_file)
    assert len(header_lines) == 14
    assert data.shape == (1044, 2)
