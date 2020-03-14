# How to create a new source spectrum resource

1. Make directory to contain source spectrum files. The name of the directory will be the name used to identify this source spectrum; this includes using it as a key in a sources dict.
2. Move into the new directory, `<directory name>`.
3. Make a directory, `raw_data`, and put data file with measured spectrum from spectrometer into it.
4. Create one file in the main directory that contains the following:
   - `measured_spectrum_normalized.csv` - data file in format suitable to read with numpy.loadtxt with comment lines that begin with `#` and normalized data (i.e., max spectrum value is 1.0).
   - This can be done by running `process_source_spectrum.py`, which uses `pysimplegui` to create a file browser dialog to select which raw data file the user wants to convert.

## Notes

- The main directory can have other files if desired, such as jupyter notebooks. So can the `raw_data` directory, except that all `*.txt` files are considered spectrum data files.
- If there are multiple `*.txt` files in `raw_data`, I generally choose the first one from which to create `measured_spectrum_normalized.csv`

## Directory structure

After performing the above process for 2 directories of data, the directory structure looks like this:

    sources
    ├── 2019-12-31_HR3.2_365nm_370nm_short_pass_filter
    │   ├── 200311_process_data.ipynb
    │   ├── measured_spectrum_normalized.csv
    │   └── raw_data
    │       ├── FLMS155811_13-39-15-538.txt
    │       ├── FLMS155811_13-39-28-747.txt
    │       └── FLMS155811_13-43-46-130.txt
    ├── 2019-12-31_HR3.2_365nm_no_filter
    │   ├── measured_spectrum_normalized.csv
    │   └── raw_data
    │       ├── FLMS155811_13-50-52-580.txt
    │       ├── FLMS155811_13-51-15-744.txt
    │       └── FLMS155811_13-51-27-377.txt
    ├── README.md
    ├── __init__.py
    └── process_source_spectrum.py
