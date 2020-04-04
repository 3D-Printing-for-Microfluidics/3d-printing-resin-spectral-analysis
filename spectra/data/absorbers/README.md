
# How to create a new absorber spectrum

## Basic process

1. Create directory with name `<dir_name>` in `spectra/data/absorbers`.
2. Inside this directory create directory `raw_data`
3. Inside `raw_data`, copy 2 spectrometer measurement files:
    - Solvent spectrum data
    - Solvent + absorber spectrum data
4. Create `spectrum_config.json` in `<dir_name>`
5. Edit `spectrum_config.json` with information needed to do absorbance (required) and molar absorptivity (optional but strongly recommended) calculations
6. Edit `data/__init__.py` to add 3 letter abbreviation to `_absorber_abbreviations` dict. The key in the dict should be the value of `Absorber` in the `spectrum_config.json` file below.

## Example `spectrum_config.json` file

    {
      "Measurement": "Avobenzone absorption in PEGDA",
      "Measurement Date": "2020-01-20",
      "Measurement Spectrometer": "Ocean Optics OE65PRO",
      "Absorber": "Avobenzone",
      "Concentration w/w percent": 0.24,
      "Film thickness microns": 60,
      "Molar mass g/mole": 310.39,
      "Solvent": "PEGDA",
      "Solvent density g/L": 1110,
      "Solvent absorption measurement file": "QEPB00791_17-10-07-458.txt",
      "Solvent + absorber absorption measurement file": "QEPB00791_17-18-57-140.txt"
    }


## Required parameters in JSON file

- Spectrometer transmission measurements
    - Monomer
    - Monomer + absorber
        - `spectrum_config.json` with the following entries
        
        
                {
                    "Measurement": "Avobenzone absorption in PEGDA",
                    "Measurement Date": "2020-01-20",
                    "Measurement Spectrometer": "Ocean Optics FIRE",
                    "Absorber": "Avobenzone",
                    "Concentration w/w percent": 0.24,
                    "Solvent": "PEGDA",
                    "Solvent absorption measurement file": "QEPB00791_17-10-07-458.txt",
                    "Solvent + absorber absorption measurement file": "QEPB00791_17-18-57-140.txt"
                }

With the above parameters and data the absorbance will be calculated.

## Optional (but strongly recommended) parameters

- Film thickness in microns
- Molar mass in g/mole
- solvent density in g/L

The `spectrum_config.json` will have the following entries:

      {
        "Measurement": "Avobenzone absorption in PEGDA",
        "Measurement Date": "2020-01-20",
        "Measurement Spectrometer": "Ocean Optics FIRE",
        "Absorber": "Avobenzone",
        "Concentration w/w percent": 0.24,
        "Film thickness microns": 70,
        "Molar mass g/mole": 310.39,
        "Solvent": "PEGDA",
        "Solvent density g/L": 1110,
        "Solvent absorption measurement file": "QEPB00791_17-10-07-458.txt",
        "Solvent + absorber absorption measurement file": "QEPB00791_17-18-57-140.txt"
      }


With the above parameters and data the absorbance and molar absorptivity will be calculated.
