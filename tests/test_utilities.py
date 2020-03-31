from pathlib import Path

import numpy as np

from spectra.utilities import (
    ArrayParams,
    read_spectrometer_file,
    read_FIRE_spectrum_data_file,
    read_OE65PRO_spectrum_data_file,
)


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
