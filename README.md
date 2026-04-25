# Purpose

This repository contains spectrum data and associated tools for resin and 3D printer development in the [Nordin Group](https://ece.byu.edu/faculty/greg_nordin) at Brigham Young University. Our focus is the development of 3D printer technology to meet the unique needs of microfluidic device fabrication.

# References

[Optical approach to resin formulation for 3D printed microfluidics](https://www.ncbi.nlm.nih.gov/pubmed/26744624)  
[Custom 3D printer and resin for 18 μm × 20 μm microfluidic flow channels](https://www.ncbi.nlm.nih.gov/pubmed/28726927)  

# Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if not already present, then:

```bash
git clone https://github.com/gregnordin/3dprinter_spectra_and_tools
cd 3dprinter_spectra_and_tools
uv sync --all-groups
# Make the environment available as a Jupyter kernel
uv run python -m ipykernel install --user --name spectra --display-name=spectra
```

`uv sync` creates a `.venv` automatically and installs the package in editable mode along with all dependencies.

# How to use

Start with `notebooks/examples/Example_normalized_dose_calculation.ipynb`, which shows how to use the package to create resins, plot spectra, and show the normalized dose as a function of `z`.

Also look at the analyses in `notebooks/220515...` and `notebooks/220516...` for further examples. Other notebooks may also be helpful.

# Class relationships

Once the example notebook is understood, the following class diagram may be helpful in understanding the organization and use of the code.

![](notebooks/200410_class_relationships.png)

# Run tests

```bash
uv run pytest
```
