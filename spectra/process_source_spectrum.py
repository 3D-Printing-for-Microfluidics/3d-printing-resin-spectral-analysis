"""Convert raw spectrometer spectrum file.

Input file must reside in a directory `raw_data`.
Output is a csv file with normalized data and
comment lines preceded with `#`. It is put in the same
directory that contains `raw_data` and has a
standard name, `measured_spectrum_normalized.csv`.

This module is intended to be run on its own and not imported,
e.g., execute `python -m spectra.process_source_spectrum`.

5/17/24 - Convert from using PySimpleGUI to tkinter with ChatGPT 4o.
Prompt: "Convert the following python code to use tkinter instead of pysimplegui:" and
copy all code below this docstring. The converted code ran as-is.
"""

from pathlib import Path
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from spectra.utilities import read_FIRE_spectrum_data_file, read_spectrometer_file


def main():
    # Create the root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to get spectrometer data file for input
    messagebox.showinfo(
        "Select spectrometer data file", "Select Spectrometer data file for LED source"
    )
    input_data_file = filedialog.askopenfilename(
        initialdir=Path.cwd(),
        title="Select file",
        filetypes=(
            ("Text files", "*.txt"),
            ("CSV files", "*.csv"),
            ("all files", "*.*"),
        ),
    )

    # Only continue if file was selected
    if not input_data_file:
        print("No file selected. Now exiting...")
        return

    # Echo chosen file
    input_data_file = Path(input_data_file)
    print(f"You chose file:\n    {input_data_file}")

    # Make sure file is in 'raw_data' directory
    if input_data_file.parent.name != "raw_data":
        print("\n~~~INVALID DATA FILE LOCATION~~~")
        print("Data file must reside in a directory named 'raw_data'.")
        print("Exiting...\n\n")
        return

    # Make sure file has expected suffix
    if not (input_data_file.suffix == ".txt" or input_data_file.suffix == ".csv"):
        print("\n~~~INVALID DATA FILE EXTENSION~~~")
        print("Data file must be named '*.txt' or '*.csv'")
        print("Exiting...\n\n")
        return

    # Read file
    header, data = read_spectrometer_file(input_data_file)
    # header, data = read_FIRE_spectrum_data_file(input_data_file)

    # Normalize data
    max_value = np.amax(data[:, 1])
    data[:, 1] = data[:, 1] / max_value

    # Add max value to header info
    header.append(f"Maximum value: {max_value}")

    # Write output data file
    output_data_file = (
        input_data_file.parent.parent / "measured_spectrum_normalized.csv"
    )
    np.savetxt(output_data_file, data, delimiter=",", header="\n".join(header))
    print(f"Output data file:\n    {output_data_file}")


if __name__ == "__main__":
    main()
