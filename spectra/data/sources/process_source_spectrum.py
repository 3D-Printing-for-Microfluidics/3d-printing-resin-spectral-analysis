"""Convert raw spectrometer spectrum file to csv format with normalized data and
comment lines preceded with `#` and put in a standard location
with standard name, `measured_spectrum_normalized`.
"""

from pathlib import Path

import numpy as np
import PySimpleGUI as sg

from spectra.utilities import read_FIRE_spectrum_data_file


# Open a file browser to get spectrometer data file for input
layout = [
    [sg.Text("Spectrometer data file for LED source")],
    [sg.Input(), sg.FileBrowse(initial_folder=Path.cwd()),],
    [sg.Submit(), sg.Cancel()],
]
window = sg.Window("Select JSON file", layout)
event, values = window.read()  # pylint: disable=unused-variable
window.close()

if event != "Submit":
    print("No file selected. Now exiting...")
    exit()

input_data_file = Path(values[0])
print(f"You chose file:\n    {input_data_file}")

if input_data_file.parent.name != "raw_data":
    print("\n~~~INVALID DATA FILE LOCATION~~~")
    print("Data file must reside in a directory named 'raw_data'.")
    print("Exiting...\n\n")
    exit()

if input_data_file.suffix != ".txt":
    print("\n~~~INVALID DATA FILE EXTENSION~~~")
    print("Data file must be named '*.txt'")
    print("Exiting...\n\n")
    exit()

header, data = read_FIRE_spectrum_data_file(input_data_file)

data[:, 1] = data[:, 1] / np.amax(data[:, 1])

output_data_file = input_data_file.parent.parent / "measured_spectrum_normalized.csv"
np.savetxt(output_data_file, data, delimiter=",", header="\n".join(header))
print(f"Output data file:\n    {output_data_file}")
