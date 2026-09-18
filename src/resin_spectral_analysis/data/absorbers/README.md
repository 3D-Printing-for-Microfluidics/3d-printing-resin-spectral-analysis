# Loading your own absorber data

To load absorber data from an arbitrary directory in a notebook or script:

```python
import resin_spectral_analysis.data as data

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

If you have raw spectrometer measurement files, see the next section to produce these CSV files first.


# Processing your own raw spectrometer data

Use `process-absorber-spectrum` to convert raw spectrometer measurements into the `absorbance.csv` and `molar_absorptivity.csv` files needed by `load_absorber()`.

## Raw data file format

Each raw data file must be a CSV with two columns: wavelength (nm) and intensity. Lines beginning with `#` are treated as comments and skipped. A non-numeric header row (e.g. `wavelength,intensity`) is also handled automatically.

## Directory structure

Create a working directory anywhere on your filesystem with the following layout:

```
my_absorber/
├── spectrum_config.json
└── raw_data/
    ├── solvent.csv
    └── solvent_plus_absorber.csv
```

`raw_data/` holds your two raw spectrometer CSV files:

- **Solvent only** — the resin monomer with no absorber, at the same integration time as the absorber measurement
- **Solvent + absorber** — the same monomer with absorber dissolved in it at a known concentration

## `spectrum_config.json`

| Key | Required | Description |
|-----|----------|-------------|
| `"Solvent absorption measurement file"` | yes | filename inside `raw_data/` |
| `"Solvent + absorber absorption measurement file"` | yes | filename inside `raw_data/` |
| `"Concentration w/w percent"` | yes | absorber concentration (w/w %) |
| `"Film thickness microns"` | recommended | cuvette / spacer thickness in µm |
| `"Molar mass g/mole"` | recommended | absorber molar mass |
| `"Solvent density g/L"` | recommended | solvent density |
| `"Absorber"` | optional | name used in output file header |
| `"Measurement"`, `"Measurement Date"`, etc. | optional | any extra metadata |

The three recommended keys are required to produce `molar_absorptivity.csv`; without them only `absorbance.csv` is written.

Example:

```json
{
  "Measurement": "Avobenzone absorption in PEGDA",
  "Measurement Date": "2024-05-01",
  "Absorber": "Avobenzone",
  "Concentration w/w percent": 0.24,
  "Film thickness microns": 60,
  "Molar mass g/mole": 310.39,
  "Solvent": "PEGDA",
  "Solvent density g/L": 1110,
  "Solvent absorption measurement file": "solvent.csv",
  "Solvent + absorber absorption measurement file": "solvent_plus_absorber.csv"
}
```

## Run the processing script

```bash
process-absorber-spectrum
```

A GUI opens. Click **Browse**, select `spectrum_config.json`, then click **Submit**. The script writes `absorbance.csv` and `molar_absorptivity.csv` into the same directory as `spectrum_config.json` (`my_absorber/` in the example above).

You can then load the result with `data.load_absorber("path/to/my_absorber")`.


# Adding a new absorber to the package

Follow this process to permanently add a new absorber to the bundled package data so it is available to all users.

## Spectrometer measurements

Prepare 2 samples for measurement, each a thin liquid film sandwiched between 2 glass slides with spacers to ensure a known liquid thickness:

1. Solvent (resin monomer) with absorber at known w/w percent concentration. Choose the concentration so that wavelengths of maximum absorption still let some light through — if no light is transmitted at these wavelengths you cannot calculate accurate absorbance.
2. Same solvent with no absorber, at the same integration time as Sample 1.

## Process

1. Create directory `<dir_name>` in `resin_spectral_analysis/data/absorbers/`.
2. Inside it, create `raw_data/` and copy your two spectrometer CSV files into it.
3. Create `spectrum_config.json` in `<dir_name>` following the format described in the previous section.
4. Edit `data/__init__.py` to add a 3-letter abbreviation to `_absorber_abbreviations`. The key must match the value of `"Absorber"` in `spectrum_config.json`.
5. Run `process-absorber-spectrum`, select the JSON file, and click **Submit**. This writes `absorbance.csv` and `molar_absorptivity.csv` into `<dir_name>`.
