# How to create a new source spectrum resource

1. Make directory in `spectra/data/sources` to contain source spectrum files. The name of the directory, `<directory name>`, will be the name used to identify this source spectrum; this includes using it as a key in a sources dict.
2. Move (`cd`) into the new directory.
3. Make a directory, `raw_data`, and put data file with measured spectrum from spectrometer into it.
4. Create a file, `measured_spectrum_normalized.csv`, in the main directory, `<directory name>`:
    - This is a data file in format suitable to read with numpy.loadtxt with comment lines that begin with `#` and normalized data (i.e., max spectrum value is 1.0).
    - This file can be created by running `python -m spectra.process_source_spectrum`, which uses `pysimplegui` to create a file browser dialog to select which raw data file the user wants to convert.

## Notes

- The main directory can have other files if desired, such as jupyter notebooks. So can the `raw_data` directory, except that all `*.txt` files are considered spectrum data files.
- If there are multiple `*.txt` files in `raw_data`, I generally choose the first one from which to create `measured_spectrum_normalized.csv`

## Directory structure

After performing the above process for 2 directories of data, the directory structure looks like this:

    sources
    ├── HR3.2_365nm_370nm_short_pass_filter-2019-12-31
    │   ├── 200311_process_data.ipynb
    │   ├── measured_spectrum_normalized.csv
    │   └── raw_data
    │       ├── FLMS155811_13-39-15-538.txt
    │       ├── FLMS155811_13-39-28-747.txt
    │       └── FLMS155811_13-43-46-130.txt
    ├── HR3.2_365nm_no_filter-2019-12-31
    │   ├── measured_spectrum_normalized.csv
    │   └── raw_data
    │       ├── FLMS155811_13-50-52-580.txt
    │       ├── FLMS155811_13-51-15-744.txt
    │       └── FLMS155811_13-51-27-377.txt
    ├── README.md
    └── __init__.py
