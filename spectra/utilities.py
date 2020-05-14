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


def find_index_of_max(var_array):
    idx = np.argmax(var_array, axis=0)
    return idx


def shift(arr, num, fill_value=0):
    """Shift a 1D numpy array to the right or left.

    This is shift5 from gzc's answer at
    https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array

    Parameters
    ----------
    arr - 1D numpy array
        Array to be shifted
    num - int
        Number of positions to shift array, can be positive or negative
    fill_value - int, float
        Value to fill shifted array locations with
    """

    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result


def shift_peak_wavelength(new_peak_wavelength, original_wavelengths, original_power):
    """Take an LED spectrum and shift it left or right so that the peak is at new_peak_wavelength.

    Parameters
    ----------
    new_peak_wavelength - float, int
        Wavelength to which LED peak power should be shifted
    original_wavelengths - 1D numpy array
        Wavelength array for original power array
    original_power - 1D numpy array
        Array containing original LED power values
    """

    index_peak_wavelength = find_index_of_max(original_power)
    index_new_peak_wavelength = find_index_of_nearest(
        original_wavelengths, new_peak_wavelength
    )
    delta_index = index_new_peak_wavelength - index_peak_wavelength
    return shift(original_power, delta_index)


class ArrayParams(typing.NamedTuple):
    """Container with named attributes for making 1D arrays of linearly spaced values.
    Intended for use with numpy.linspace.

    Attributes:
        min_value (float): Minimum value in array
        max_value (float): Maximum value in array
        num_pnts (int): number of values in array
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
