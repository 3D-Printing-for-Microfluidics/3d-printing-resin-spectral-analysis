
# Next

- &#9989; Create module process_absorber_spectrum.py
- &#9989; Add tests for process_absorber_spectrum.py
- Change process_absorber_spectrum.py so that it handles FIRE files and older csv files
- Add 2017 avobenzone measurements using a pull request
- Create an AbsorberSpectrum class similar to the SourceSpectrum class
- Compare 2020 and 2017 avobenzone molar absorptivity
- Create a PhotoinitiatorSpectrum class?
- Add 2020 Irgacure 819 absorption measurements
- Add 2017 Irgacure 819 absorption measurements and compare to 2020
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


