
# Next

- &#9989; Create module process_absorber_spectrum.py
- &#9989; Add tests for process_absorber_spectrum.py
- &#9989; Change process_absorber_spectrum.py so that it handles FIRE files and older csv files
- &#9989; Add 2017 avobenzone measurements using a pull request
- &#9989; Create an AbsorberSpectrum class similar to the SourceSpectrum class
    - Read absorbance as well as molar absorptivity
    - Put in error checks for presence of 2 data files
    - Read json string in first line of data files
    - Use json string for various labels, etc.
- &#9989; Compare 2020 and 2017 avobenzone molar absorptivity
- &#9989; Move absorbers and sources to data/__init__.py from data/absorbers/__init__.py and data/sources/__init__.py
- &#9989; Add & process spectrum data for more 2017 absorber measurements
- &#10060; Create a PhotoinitiatorSpectrum class?
- &#9989; Need to be able to override `force_zero` for Sudan I absorber
- &#9989; Re-do Sudan I absorber
- Add 2020 Irgacure 819 absorption measurements
- Add 2017 Irgacure 819 absorption measurements and compare to 2020
- Add photoinitiators and other sources
- Create interpolation function for spectra
- Create a Resin class that includes one or more photoinitiators and absorbers
    - Since they are all absorbers, can probably put them all into a list
    - Calculates absorption coefficient
- Create a ResinAndSource class
    - Calculate D_n(lambda)?
    - Calculate D'(z)
    - Fit to Models 1 and 2
- Use to plot normalized dose as a function of lambda and z
- Add tests for all code


# Saturday, 3/21/20

- Modify `process_absorber_spectrum.py` GUI with checkbox for `force_zero` to handle Sudan I case


# Friday, 3/20/20

- Find that when using `%matplotlib widget` I need to save figure files as `.svg`.
- Move absorbers and sources to data/__init__.py from data/absorbers/__init__.py and data/sources/__init__.py
- DRY refactor of data/__init__.py
- Change flag to zero absorbance in long wavelength, no absorption region
- Add absorbance data to AbsorberSpectrum
- Add a bunch of absorbers from 2017


# Thursday, 3/19/20

- Write tests for `process_spectrum_data` in `process_absorber_spectrum.py`

Current spectrometer data file format is different from several years ago:

- Current
    - `.txt`
    - 14 header lines with no particular starting character
    - ` ` separator between values
- Previous
    - `.csv `
    - 2 header lines starting with `#`
    - `,` separator between values

Modify spectra.utilities.read_spectrometer_file to read both spectrometer file types 

- Process 2017-04-13 avobenzone data
- Create an AbsorberSpectrum class
- Compare 2020 and 2017 avobenzone molar absorptivity


# Wednesday, 3/18/20

## Code to process absorber spectrum

- `process_absorber_spectrum.py` and preceeding notebooks
- Start to develop tests

## pytest

### Install

    $ pip install pytest
    $ pip install pytest-cov
    $ pip freeze > requirement.txt

### Use

Pytest command to get code coverage, verbose, and allow code to print to terminal:

    $ pytest --cov spectra --cov-report term-missing -vv -s


