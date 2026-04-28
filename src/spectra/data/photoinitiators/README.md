# Loading your own photoinitiator data

To load photoinitiator data from an arbitrary directory in a notebook or script:

```python
import spectra.data as data

# Key defaults to the directory name
data.load_photoinitiator("/path/to/my_photoinitiator_dir")

# Or supply an explicit key
data.load_photoinitiator("/path/to/my_photoinitiator_dir", name="my_key")

print(data.photoinitiators.keys())   # bundled + newly loaded entries
```

The required directory structure and file formats are identical to those for absorbers — see [absorbers/README.md](../absorbers/README.md) for details. Loaded entries are in-memory only and do not persist across sessions.


# Processing your own raw spectrometer data

The workflow for converting raw spectrometer CSV files into `absorbance.csv` and `molar_absorptivity.csv` is identical to the absorber workflow. See the **"Processing your own raw spectrometer data"** section in [absorbers/README.md](../absorbers/README.md) for the directory layout, `spectrum_config.json` format, and instructions for running `process-absorber-spectrum`.


# Adding a new photoinitiator to the package

To permanently add a new photoinitiator to the bundled package data, follow the same instructions as for adding an absorber in [absorbers/README.md](../absorbers/README.md), with two differences:

- Perform Step 1 in the `spectra/data/photoinitiators/` directory instead of `spectra/data/absorbers/`.
- In Step 4, add the entry to `_photoinitiator_abbreviations` instead of `_absorber_abbreviations`.
