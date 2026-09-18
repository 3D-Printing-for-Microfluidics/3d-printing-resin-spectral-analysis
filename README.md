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
# Make the environment available as a Jupyter kernel
uv run python -m ipykernel install --user --name resin_spectral_analysis --display-name=resin_spectral_analysis
```

`uv sync` creates a `.venv` automatically and installs the package in editable mode along with all dependencies.

# How to run a notebook

From the terminal in the `3d-printing-resin-spectral-analysis` directory, execute `uv run jupyter lab`, which will open Jupyter Lab in a window in your default browser. In Jupyter Lab navigate to the notebook you wish to open and double click on it. A dialog box will pop up for you to select a Python kernel. Select `resin_spectral_analysis`. Now you can run the code cells as usual in a notebook.

# How to learn how to use

Start with `notebooks/Example_normalized_dose_calculation.ipynb`, which shows how to use the package to create resins, plot spectra, and show the normalized dose as a function of `z`.

Also look at the analyses in `notebooks/220515...` and `notebooks/220516...` for further examples. Other notebooks may also be helpful.

Using what you learn from the examples, create your own notebook and write code to analyze/design your own resins.

# Class relationships

Once the example notebook is understood, the following class diagram may be helpful in understanding the organization and use of the code.

![](notebooks/200410_class_relationships.png)

# Data

The `resin_spectral_analysis` package has built-in spectral data stored in the `data` directory. UV absorber and photoinitiator absorption spectra are found in `resin_spectral_analysis.data.absorbers` and `resin_spectral_analysis.data.photoinitiators`, respectively, while LED emission spectra are found in `resin_spectral_analysis.data.sources`. See [`src/resin_spectral_analysis/data/README.md`](src/resin_spectral_analysis/data/README.md) for more details.

You can also process your own raw spectrometer measurements into the format the package expects. Run `process-absorber-spectrum` from the terminal — a GUI opens to select a `spectrum_config.json` file and produce `absorbance.csv` and `molar_absorptivity.csv`. See [`src/resin_spectral_analysis/data/absorbers/README.md`](src/resin_spectral_analysis/data/absorbers/README.md) for the required directory layout, file format, and config options.

# Run tests

```bash
uv run pytest
```
