
# How to create a new absorber spectrum

## Required

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

## Optional

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
