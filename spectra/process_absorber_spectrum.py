import json
from pathlib import Path
import sys

import numpy as np

from spectra.utilities import read_OE65PRO_spectrum_data_file, find_index_of_nearest


def read_spectrum_config_json(spectrum_config_file):
    assert isinstance(spectrum_config_file, Path)
    with spectrum_config_file.open() as f:
        temp = json.load(f)
    return temp


def find_indices_of_range(arr, low, high):
    assert len(arr.shape) == 1

    index_low = find_index_of_nearest(arr, low)
    index_high = find_index_of_nearest(arr, high)

    return index_low, index_high


def select_wavelength_range(data, wavelength_low, wavelength_high):
    assert len(data.shape) == 2
    assert data.shape[1] == 2

    index_low, index_high = find_indices_of_range(
        data[:, 0], wavelength_low, wavelength_high
    )

    return data[index_low : index_high + 1]


def calc_absorbance(
    source_spectrum,
    absorber_spectrum,
    wavelength_low,
    wavelength_high,
    force_zero=True,
    num_samples_for_average=10,
):

    # Make sure wavelengths are the same for both data sets
    assert np.allclose(source_spectrum[:, 0], absorber_spectrum[:, 0])

    # Select only the wavelength range we need
    temp_source = select_wavelength_range(
        source_spectrum, wavelength_low, wavelength_high
    )
    temp_absorber = select_wavelength_range(
        absorber_spectrum, wavelength_low, wavelength_high
    )

    # Calculate absorbance
    absorbance = np.column_stack(
        (temp_source[:, 0], -np.log10(temp_absorber[:, 1] / temp_source[:, 1]))
    )

    # Make sure the average absorbance is 0 in the high wavelength range
    # where there is presumably no absorption
    if force_zero:
        avg = np.mean(absorbance[-num_samples_for_average:, 1])
        absorbance[:, 1] -= avg

    return absorbance


def calc_molar_concentration(
    concentration_w_w_percent, density_of_solute_g_per_L, molar_mass_g_per_mole
):
    """Calculates molar concentration in moles per Liter"""
    return (concentration_w_w_percent / 100.0) * (
        density_of_solute_g_per_L / molar_mass_g_per_mole
    )


def calc_molar_absorptivity(absorbance, molar_concentration, length_um):
    length_cm = 1.0e-4 * length_um
    return absorbance / (molar_concentration * length_cm)


def process_spectrum_data(
    directory,
    spectrum_config,
    wavelength_range=[300, 540],
    force_zero=True,
    num_samples_for_average=10,
):
    """Process spectrometer data to create absorbance and molar absorptivity csv files.
    
    Parameters
    ----------
    directory - Path object
        Directory in which `raw_data` folder is present, and in which the 2 output files
        will be written.
    spectrum_config - dict
        Specify files and parameters needed to create absorbance and molar absorptivity.
    wavelength_range - list
        Wavelength range over which to do calculations. Low end is set by signal to noise
        ratio of data, and high end is larger than 532 nm laser wavelength, but smaller than
        saturated measurement data starting at 543 nm.
    force_zero - bool
        Used in calc_absorbance()
    num_samples_for_average - int
        Used in calc_absorbance()
        
    Returns
    -------
    Nothing
    
    Outputs
    -------
    absorbance.csv file
    molar_absorptivity.csv file
    """

    assert isinstance(directory, Path)
    assert isinstance(spectrum_config, dict)

    # Check that parameters required for absorbance calculation are in spectrum_config
    required_params_for_absorbance_calc = [
        "Solvent absorption measurement file",
        "Solvent + absorber absorption measurement file",
    ]
    for p in required_params_for_absorbance_calc:
        if p not in spectrum_config:
            msg = f"Required parameter '{p}' for absorbance calculation is not in 'spectrum_config.json'"
            raise KeyError(msg)

    raw_data_directory = directory / "raw_data"

    # Read solvent data
    solvent_file = (
        raw_data_directory / spectrum_config["Solvent absorption measurement file"]
    )
    (
        solvent_spectrometer_header,
        solvent_spectrometer_data,
    ) = read_OE65PRO_spectrum_data_file(solvent_file)

    # Read solvent + absorber data
    solvent_and_absorber_file = (
        raw_data_directory
        / spectrum_config["Solvent + absorber absorption measurement file"]
    )
    (
        solvent_and_absorber_spectrometer_header,
        solvent_and_absorber_spectrometer_data,
    ) = read_OE65PRO_spectrum_data_file(solvent_and_absorber_file)

    # Create absorbance data & write to file
    absorbance = calc_absorbance(
        solvent_spectrometer_data,
        solvent_and_absorber_spectrometer_data,
        *wavelength_range,
        force_zero=force_zero,
        num_samples_for_average=num_samples_for_average,
    )
    output_data_file = directory / "absorbance.csv"
    np.savetxt(
        output_data_file, absorbance, delimiter=",", header=json.dumps(spectrum_config)
    )

    # Check that parameters required for molar absorptivity calculation are in spectrum_config
    required_params_for_molar_absorptivity_calc = [
        "Concentration w/w percent",
        "Film thickness microns",
        "Molar mass g/mole",
        "Solvent density g/L",
    ]
    for p in required_params_for_molar_absorptivity_calc:
        if p not in spectrum_config:
            msg = f"Required parameter '{p}' for molar absorptivity calculation is not in 'spectrum_config.json'."
            msg += "\n'molar_absorptivity.csv` file not created."
            sys.exit()

    # Create molar absorbance data & write to file
    molar_concentration = calc_molar_concentration(
        spectrum_config["Concentration w/w percent"],
        spectrum_config["Solvent density g/L"],
        spectrum_config["Molar mass g/mole"],
    )
    molar_absorptivity = absorbance.copy()
    molar_absorptivity[:, 1] = calc_molar_absorptivity(
        absorbance[:, 1], molar_concentration, spectrum_config["Film thickness microns"]
    )
    output_data_file = directory / "molar_absorptivity.csv"
    np.savetxt(
        output_data_file,
        molar_absorptivity,
        delimiter=",",
        header=json.dumps(spectrum_config),
    )


if __name__ == "__main__":
    import PySimpleGUI as sg

    # Open a file browser to get spectrum_config.json file
    layout = [
        [sg.Text("Select JSON spectrum config file")],
        [sg.Input(), sg.FileBrowse(initial_folder=Path.cwd()),],
        [sg.Submit(), sg.Cancel()],
    ]
    window = sg.Window("Select JSON file", layout)
    event, values = window.read()  # pylint: disable=unused-variable
    window.close()

    # Only continue if file was selected
    if event != "Submit":
        print("No file selected. Now exiting...")
        exit()

    # Echo chosen file
    input_json_file = Path(values[0])
    print(f"You chose file:\n    {input_json_file}")

    # Make sure file has expected suffix
    if input_json_file.suffix != ".json":
        print("\n~~~INVALID DATA FILE EXTENSION~~~")
        print("Data file must be named '*.json'")
        print("Exiting...\n\n")
        exit()

    spectrum_config = read_spectrum_config_json(input_json_file)
    print()
    print(spectrum_config)

    process_spectrum_data(input_json_file.parent, spectrum_config)
    print(
        f"Spectrum successfully processed to create 'absorbance.csv' and 'molar_absorptivity.csv'"
    )
