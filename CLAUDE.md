# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Python package (`resin_spectral_analysis`) for 3D printer resin and light spectrum analysis, supporting microfluidic device fabrication research at the Nordin Group (BYU). It models how UV/visible light propagates through photopolymer resins and computes normalized dose vs. depth.

## Setup

```bash
uv sync --all-groups
# Register Jupyter kernel (run once)
uv run python -m ipykernel install --user --name resin_spectral_analysis --display-name=resin_spectral_analysis
```

## Commands

```bash
# Run all tests with coverage
uv run pytest

# Run a single test file
uv run pytest tests/test_normalizeddose.py

# Run a single test
uv run pytest tests/test_normalizeddose.py::test_normalizeddose

# Process raw absorber spectrometer data (launches tkinter GUI)
uv run process-absorber-spectrum

# Process raw LED source spectrometer data (launches tkinter GUI)
uv run process-source-spectrum

# Start JupyterLab
uv run jupyter lab
```

Code is formatted with ruff at 90-character line length (`uv run ruff format .`).

## Architecture

### Class hierarchy and data flow

The typical workflow builds up from raw materials to a normalized dose calculation:

```
resin_spectral_analysis.data (pre-loaded dicts)
    ├── data.monomers        → Monomer (from JSON)
    ├── data.absorbers       → AbsorberSpectrum (from CSV files)
    ├── data.photoinitiators → AbsorberSpectrum (from CSV files)
    └── data.sources         → SourceSpectrum (from CSV files)
          ↓
ResinConstituentMonomer + ResinConstituentAbsorber
          ↓
        Resin  (computes absorption_coeff_inv_cm vs wavelength)
          ↓
      Irradiance  (callable: irradiance(z_um) → power spectrum at depth z)
          ↓
   NormalizedDose  (D_n(z), auto-fits ha_model, a_b_model, a_b_c_model)
```

### Key modules

- **`src/resin_spectral_analysis/data/__init__.py`** — auto-loads all data from subdirectories into module-level dicts (`absorbers`, `photoinitiators`, `sources`, `monomers`). Keys are directory names for spectrum types and JSON `Name` fields for monomers.
- **`src/resin_spectral_analysis/resin.py`** — `Resin` combines `ResinConstituentMonomer` and `ResinConstituentAbsorber` objects; computes the total absorption coefficient using Beer-Lambert with molar absorptivities. Monomer concentrations must sum to 100%.
- **`src/resin_spectral_analysis/irradiance.py`** — `Irradiance` is a callable that returns the spectral irradiance array at depth `z_um` (microns) via `exp(-α·z)` attenuation.
- **`src/resin_spectral_analysis/normalizeddose.py`** — `NormalizedDose` integrates irradiance over wavelength at each z to get D_n(z), then fits three models from `spectrummodels.py`. Uses `scipy.integrate.simpson`.
- **`src/resin_spectral_analysis/spectrummodels.py`** — Three analytical models: `ha_model` (single exponential), `a_b_model` (exponential + constant), `a_b_c_model` (exponential + free constant). All use `scipy.optimize.curve_fit`.
- **`src/resin_spectral_analysis/utilities.py`** — `ArrayParams` NamedTuple (used with `np.linspace(*params)`); spectrometer file readers for Ocean Optics QE65PRO-ABS and FIRE instruments.

### Data file conventions

Each absorber/photoinitiator directory under `src/resin_spectral_analysis/data/absorbers/` or `src/resin_spectral_analysis/data/photoinitiators/` must contain:
- `absorbance.csv` — two columns: wavelength, absorbance
- `molar_absorptivity.csv` — two columns: wavelength, molar absorptivity (L/mol·cm); first line is a JSON comment (`# {...}`) with keys including `"Absorber"` and `"Molar mass g/mole"`

Each source directory under `src/resin_spectral_analysis/data/sources/` must contain:
- `measured_spectrum_normalized.csv` — two columns: wavelength, normalized power (peak = 1)

Monomers are JSON files in `src/resin_spectral_analysis/data/monomers/` with keys `"Name"`, `"Long name"`, `"Density g/L"`.

### Processing raw spectrometer data

Raw spectrometer files go in a `raw_data/` subdirectory alongside a `spectrum_config.json`. Running `uv run process-absorber-spectrum` opens a GUI to select the config file and produces `absorbance.csv` and `molar_absorptivity.csv` in the parent directory. Similarly, `uv run process-source-spectrum` processes raw LED spectra into `measured_spectrum_normalized.csv`.

### Example usage

See `notebooks/examples/Example_normalized_dose_calculation.ipynb` for a complete walkthrough. The `tests/` directory mirrors the module structure and contains good usage examples for each class.
