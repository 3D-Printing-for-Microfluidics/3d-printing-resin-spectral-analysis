"""
5/17/24 - Convert from using PySimpleGUI to tkinter with ChatGPT 4o.
Prompt: "Convert the following python code snippet to use tkinter instead of pysimplegui:" and
copy all code from the "if '__name__' == '__main__' block. After adding the tk imports, the
converted code ran as-is. Note that the converted code put all of the action into a new main()
function.
"""

import json
from pathlib import Path
import sys

import numpy as np

from resin_spectral_analysis.utilities import read_spectrometer_file, find_index_of_nearest


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
        Raw data files referenced in spectrum_config must be CSV files with two columns
        (wavelength, intensity). Lines beginning with '#' are treated as comments and
        skipped; all other lines must be numeric.
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
    ) = read_spectrometer_file(solvent_file)

    # Read solvent + absorber data
    solvent_and_absorber_file = (
        raw_data_directory
        / spectrum_config["Solvent + absorber absorption measurement file"]
    )
    (
        solvent_and_absorber_spectrometer_header,
        solvent_and_absorber_spectrometer_data,
    ) = read_spectrometer_file(solvent_and_absorber_file)

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


def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    def browse_file():
        file_path = filedialog.askopenfilename(
            initialdir=Path.cwd(),
            title="Select file",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*")),
        )
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

    def on_submit():
        file_path = Path(file_entry.get())
        if not file_path or file_path.suffix != ".json":
            messagebox.showerror("Invalid File", "Please select a valid JSON file.")
            return
        root.quit()

    root = tk.Tk()
    root.title("Select JSON file")

    size = (40, 1)

    tk.Label(root, text="Select JSON spectrum config file").grid(
        row=0, column=0, columnspan=2
    )

    file_entry = tk.Entry(root, width=size[0])
    file_entry.grid(row=1, column=0)
    ttk.Button(root, text="Browse", command=browse_file).grid(row=1, column=1)

    force_zero_var = tk.BooleanVar(value=True)
    tk.Checkbutton(
        root, text="Correct absorbance to zero at long wavelengths", var=force_zero_var
    ).grid(row=2, column=0, columnspan=2)

    ttk.Button(root, text="Submit", command=on_submit).grid(row=3, column=0)
    ttk.Button(root, text="Cancel", command=root.quit).grid(row=3, column=1)

    root.mainloop()

    input_json_file = Path(file_entry.get())
    force_zero = force_zero_var.get()

    if not input_json_file.exists():
        print("No file selected. Now exiting...")
        return

    print(f"You chose file:\n    {input_json_file}")

    if input_json_file.suffix != ".json":
        print("\n~~~INVALID DATA FILE EXTENSION~~~")
        print("Data file must be named '*.json'")
        print("Exiting...\n\n")
        return

    spectrum_config = read_spectrum_config_json(input_json_file)
    print("spectrum_config.json:")
    print(json.dumps(spectrum_config, indent=2))

    process_spectrum_data(
        input_json_file.parent, spectrum_config, force_zero=force_zero
    )
    print(
        "Spectrum successfully processed to create 'absorbance.csv' and 'molar_absorptivity.csv'"
    )


if __name__ == "__main__":
    main()
