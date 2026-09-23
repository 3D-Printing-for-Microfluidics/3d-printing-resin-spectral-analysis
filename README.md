# Purpose

This repository contains spectrum data and associated tools for resin and 3D printer development in the [Nordin Group](https://ece.byu.edu/faculty/greg_nordin) at Brigham Young University. Our focus is the development of 3D printer technology to meet the unique needs of microfluidic device fabrication.

# References

[Optical approach to resin formulation for 3D printed microfluidics](https://www.ncbi.nlm.nih.gov/pubmed/26744624)  
[Custom 3D printer and resin for 18 μm × 20 μm microfluidic flow channels](https://www.ncbi.nlm.nih.gov/pubmed/28726927)  

# Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if not already present, then:

```bash
git clone https://github.com/3D-Printing-for-Microfluidics/3d-printing-resin-spectral-analysis
cd 3d-printing-resin-spectral-analysis
uv sync --all-groups
# Make the environment available as a Jupyter kernel (Jupyter only)
uv run python -m ipykernel install --user --name resin_spectral_analysis --display-name=resin_spectral_analysis
```

`uv sync` creates a `.venv` automatically and installs the package in editable mode along with all dependencies.

If the repository directory has been moved after the environment was created, rebuild the environment so its command-line entry points use the current path:

```bash
uv sync --all-groups --reinstall
```

# How to run a notebook

The repository contains two kinds of notebooks:

- **Jupyter notebooks** (`*.ipynb`), used for older analyses
- **marimo notebooks** (`*.py`), used for new work starting with `notebooks/2026_PIR_paper/`

## marimo notebooks

From the `3d-printing-resin-spectral-analysis` directory, open an existing notebook:

```bash
uv run marimo edit notebooks/2026_PIR_paper/compare_source_spectra.py
```

marimo opens the notebook in your browser. No kernel selection is needed: the notebook runs in the project's environment, so `resin_spectral_analysis` imports directly.

To create a new notebook, give `marimo edit` a new file name. Put each analysis in its own dated directory under `notebooks/`:

```bash
mkdir -p notebooks/2026_my_analysis
uv run marimo edit notebooks/2026_my_analysis/my_analysis.py
```

A typical first cell:

```python
import marimo as mo
import numpy as np
import matplotlib.pyplot as plt
import resin_spectral_analysis.data as data
from resin_spectral_analysis.resin import (
    Resin,
    ResinConstituentMonomer,
    ResinConstituentAbsorber,
)
from resin_spectral_analysis.irradiance import Irradiance
from resin_spectral_analysis.normalizeddose import NormalizedDose
from resin_spectral_analysis.utilities import ArrayParams
```

Things to know:

- **Cells rerun automatically.** When a cell changes, marimo reruns every cell that depends on it. Each variable can be defined in only one cell. Prefix loop and temporary variables with `_` (for example `_fig`) to keep them local to a cell.
- **Restart after adding data.** `resin_spectral_analysis.data` loads the source, absorber, and monomer directories once, when it's imported. After adding a data directory, restart the notebook (stop `marimo edit` and run it again) so it picks up the new data.
- **Notebooks are plain Python.** They diff cleanly in git and can run as a script, which is a quick way to check that a notebook runs from start to finish: `uv run python notebooks/2026_PIR_paper/compare_source_spectra.py`
- **Don't use `--sandbox`.** It creates an isolated environment that doesn't include the local package.

## Jupyter notebooks

From the terminal in the `3d-printing-resin-spectral-analysis` directory, execute `uv run python -m jupyter lab`, which will open Jupyter Lab in a window in your default browser. In Jupyter Lab navigate to the notebook you wish to open and double click on it. A dialog box will pop up for you to select a Python kernel. Select `resin_spectral_analysis`. Now you can run the code cells as usual in a notebook.

# How to learn how to use

Start with `notebooks/Example_normalized_dose_calculation.ipynb`, which shows how to use the package to create resins, plot spectra, and show the normalized dose as a function of `z`.

Also look at the analyses in [`notebooks/240515_NPS_25um_depth_385nmLED/2024-05-15_resin_spectra_Voronov.ipynb`](notebooks/240515_NPS_25um_depth_385nmLED/2024-05-15_resin_spectra_Voronov.ipynb) and [`notebooks/240516_NPS_25um_depth_405nmLED/2024-05-16_NPS_25um_depth_405nmLED.ipynb`](notebooks/240516_NPS_25um_depth_405nmLED/2024-05-16_NPS_25um_depth_405nmLED.ipynb) for further examples. Other notebooks may also be helpful.

For a marimo example, see [`notebooks/2026_PIR_paper/compare_source_spectra.py`](notebooks/2026_PIR_paper/compare_source_spectra.py), which plots source spectra with absorber molar absorptivity, builds resins, and plots the normalized dose `D'(z)` for several sources.

Using what you learn from the examples, create your own notebook and write code to analyze/design your own resins.

# Class relationships

Once the example notebook is understood, the following class diagram may be helpful in understanding the organization and use of the code.

![](notebooks/200410_class_relationships.png)

# Data

The `resin_spectral_analysis` package has built-in spectral data stored in the `data` directory. UV absorber and photoinitiator absorption spectra are found in `resin_spectral_analysis.data.absorbers` and `resin_spectral_analysis.data.photoinitiators`, respectively, while LED emission spectra are found in `resin_spectral_analysis.data.sources`. See [`src/resin_spectral_analysis/data/README.md`](src/resin_spectral_analysis/data/README.md) for more details.

You can also process your own raw spectrometer measurements into the format the package expects. Run `process-absorber-spectrum` from the terminal — a GUI opens to select a `spectrum_config.json` file and produce `absorbance.csv` and `molar_absorptivity.csv`. See [`src/resin_spectral_analysis/data/absorbers/README.md`](src/resin_spectral_analysis/data/absorbers/README.md) for the required directory layout, file format, and config options.

# Run tests

```bash
uv run python -m pytest
```
