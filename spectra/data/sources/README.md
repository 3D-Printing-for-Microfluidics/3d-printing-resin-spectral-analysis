# How to create a new source spectrum resource

1. Make directory to contain source spectrum files. The name of the directory will be the name used to identify this source spectrum; this includes using it as a key in a sources dict.
2. Move into the new directory.
3. Make a directory, `raw_data`, and put data file with measured spectrum from spectrometer into it.
4. Create one file in the main directory that contains the following:
   - `measured_spectrum_normalized.csv` - data file in format suitable to read with numpy.loadtxt with comment lines that begin with `#` and normalized data (i.e., max spectrum value is 1.0).
   - This can be done by running `process_source_spectrum.py`, which uses `pysimplegui` to create a file browser dialog to select which raw data file the user wants to convert.

## Notes

- The main directory can have other files if desired, such as jupyter notebooks. So can the `raw_data` directory, except that all `*.txt` files are considered spectrum data files.
- If there are multiple `*.txt` files in `raw_data`, I generally choose the first one from which to create `measured_spectrum_normalized.csv`
