"""Convert raw spectrometer spectrum file.

Input file must reside in a directory `raw_data`.
Output is a csv file with normalized data and
comment lines preceded with `#`. It is put in the same
directory that contains `raw_data` and has a
standard name, `measured_spectrum_normalized.csv`.

This module is intended to be run on its own and not imported, 
e.g., execute `python -m spectra.process_source_spectrum`.
"""

from pathlib import Path

import numpy as np
import PySimpleGUI as sg

from spectra.utilities import read_FIRE_spectrum_data_file


def main():
    # Open a file browser to get spectrometer data file for input
    layout = [
        [sg.Text("Spectrometer data file for LED source")],
        [sg.Input(), sg.FileBrowse(initial_folder=Path.cwd()),],
        [sg.Submit(), sg.Cancel()],
    ]
    window = sg.Window("Select JSON file", layout)
    event, values = window.read()  # pylint: disable=unused-variable
    window.close()

    # Only continue if file  was selected
    if event != "Submit":
        print("No file selected. Now exiting...")
        exit()

    # Echo chosen file
    input_data_file = Path(values[0])
    print(f"You chose file:\n    {input_data_file}")

    # Make sure file is in 'raw_data' directory
    if input_data_file.parent.name != "raw_data":
        print("\n~~~INVALID DATA FILE LOCATION~~~")
        print("Data file must reside in a directory named 'raw_data'.")
        print("Exiting...\n\n")
        exit()

    # Make sure file has expected suffix
    if input_data_file.suffix != ".txt":
        print("\n~~~INVALID DATA FILE EXTENSION~~~")
        print("Data file must be named '*.txt'")
        print("Exiting...\n\n")
        exit()

    # Read file
    header, data = read_FIRE_spectrum_data_file(input_data_file)

    # Normalize data
    max_value = np.amax(data[:, 1])
    data[:, 1] = data[:, 1] / max_value

    # Add max value to header info
    header.append(f"Maximum value: {max_value}")

    # Write output data file
    output_data_file = input_data_file.parent.parent / "measured_spectrum_normalized.csv"
    np.savetxt(output_data_file, data, delimiter=",", header="\n".join(header))
    print(f"Output data file:\n    {output_data_file}")


if __name__ == "__main__":
    main()
