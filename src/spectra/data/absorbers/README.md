# Loading your own absorber data

To load absorber data from an arbitrary directory in a notebook or script:

```python
import spectra.data as data

# Key defaults to the directory name
data.load_absorber("/path/to/my_absorber_dir")

# Or supply an explicit key
data.load_absorber("/path/to/my_absorber_dir", name="my_key")

print(data.absorbers.keys())   # bundled + newly loaded entries
```

The directory must contain these two files:

- `absorbance.csv` — two columns: wavelength, absorbance
- `molar_absorptivity.csv` — two columns: wavelength, molar absorptivity (L/mol·cm); the first line must be a JSON comment (`# {...}`) with at minimum the keys `"Absorber"` and `"Molar mass g/mole"`, for example:

      # {"Absorber": "Avobenzone", "Molar mass g/mole": 310.39, ...}

Loaded entries are in-memory only and do not persist across sessions.


# Adding a new absorber to the package

Follow this process to permanently add a new absorber to the bundled package data so it is available to all users.

## Spectrometer measurements

Prepare 2 samples for measurement, each of which is a thin liquid film sandwiched between 2 glass slides with spacers to ensure a known liquid thickness:

1. Solvent (resin monomer) with absorber at known w/w percent concentration. You want to choose the concentration so that wavelengths of maximum absorption still let some light through. If no light is transmitted at these wavelengths, you cannot calculate accurate absorbance.
2. Same except only the solvent (no absorber). Use the same integration time as for Sample 1 so the data is consistent.

The 2nd sample is used to provide a transmission baseline against which the extra absorption of the absorber is measured with the first sample.

## Basic process

Once the above spectrometer measurements have been made, then:

1. Create directory with name `<dir_name>` in `spectra/data/absorbers`.
2. Inside this directory create directory `raw_data`
3. Inside `raw_data`, copy 2 spectrometer measurement files:
    - Solvent spectrum data
    - Solvent + absorber spectrum data
4. Create `spectrum_config.json` in `<dir_name>`
5. Edit `spectrum_config.json` with information needed to do absorbance (required) and molar absorptivity (optional but strongly recommended) calculations
6. Edit `data/__init__.py` to add 3 letter abbreviation to `_absorber_abbreviations` dict. The key in the dict should be the value of `Absorber` in the `spectrum_config.json` file below.
7. Run `uv run process-absorber-spectrum`, click the `Browse` button and select the JSON file, then click the `Submit` button. New absorbance and molar absorptivity csv files are created in `<dir_name>`.

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
- Solvent density in g/L

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
