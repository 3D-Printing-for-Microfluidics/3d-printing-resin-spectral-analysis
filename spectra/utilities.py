from pathlib import Path
import typing

import numpy as np


def find_index_of_nearest(var_array, value):
    """
    Find index of nearest value to value

    Example:
        idx_low = find_index_of_nearest(var_array[0:idx_peak], 0.5)
    """
    idx = (np.abs(var_array - value)).argmin()
    return idx


class ArrayParams(typing.NamedTuple):
    """Container with named attributes for making 1D arrays of values.
    Intended for use with numpy.linspace.
    """

    min_value: float
    max_value: float
    num_pnts: int


def read_spectrometer_file(file, clip_to_zero=True):
    """Read spectrometer-generated spectrum data file.

    Parameters
    ----------
    file - Path object
    skiprows - Skip the first `skiprows` rows in data file
    clip_to_zero - If true, set minimum spectrometer value to zero.
                   If false, don't change any values.

    Returns
    -------
    header_lines - list
        Each list entry is one header line
    data - numpy array
        two column array 2D array, first column is wavelength and 2nd is spectrometer value
    """

    assert isinstance(file, Path)
    assert isinstance(clip_to_zero, bool)

    # Data
    if file.name.endswith(".txt"):
        skiprows = 14
        data = np.loadtxt(file, skiprows=skiprows)
    elif file.name.endswith(".csv"):
        skiprows = None
        delimiter = ","
        data = np.loadtxt(file, delimiter=delimiter)

    if clip_to_zero:
        data = np.clip(data, 0, None)

    # Header
    header_lines = []
    with file.open() as f:
        if skiprows:
            for i in range(skiprows):  # pylint: disable=unused-variable
                header_lines.append(f.readline().strip())
        else:
            for line in f:
                if line.startswith("#"):
                    header_lines.append(line.strip())
                else:
                    break

    return header_lines, data


def read_OE65PRO_spectrum_data_file(file, clip_to_zero=True):
    """Read header and data from spectrum data file collected by Ocean Optics QE65PRO-ABS spectrometer.

    See docstring for `read_spectrometer_file`.
    """

    # print(file)
    return read_spectrometer_file(file, clip_to_zero)


def read_FIRE_spectrum_data_file(file, clip_to_zero=True):
    """Read header and data from spectrum data file collected by Ocean Optics FIRE spectrometer.

    See docstring for `read_spectrometer_file`.
    """

    # print(file)
    return read_spectrometer_file(file, clip_to_zero)
