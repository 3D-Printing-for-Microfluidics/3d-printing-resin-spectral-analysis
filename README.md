# Purpose

This repository contains spectrum data and associated tools for resin and 3D printer development in the [Nordin Group](https://ece.byu.edu/faculty/greg_nordin) at Brigham Young University. Our focus is the development of 3D printer technology to meet the unique needs of microfluidic device fabrication.

# References

[Optical approach to resin formulation for 3D printed microfluidics](https://www.ncbi.nlm.nih.gov/pubmed/26744624)  
[Custom 3D printer and resin for 18 μm × 20 μm microfluidic flow channels](https://www.ncbi.nlm.nih.gov/pubmed/28726927)  

# Installation

Create a new python virtual environment and activate it.

```
# Make sure you are in a directory in which you want your virtual environment
# and the 3dprinter_spectra_and_tools package to reside.
python -m venv .venv --prompt spectra
source .venv/bin/activate
```

Install package

    git clone https://github.com/gregnordin/3dprinter_spectra_and_tools
    cd 3dprinter_spectra_and_tools
    pip install -e .
    # Make this virtual environment a generally-available Jupyter kernel to use with notebooks
    python -m ipykernel install --user --name spectra_and_tools --display-name=spectra_and_tools

# How to use

Start with `examples/Example_normalized_dose_calculation.ipynb`, which shows how to use the package to create resins, plot spectra, and show the normalized dose as a function of `z`.

Also look at the analyses in `notebooks/220515...` and `notebooks/220516...` for futher examples. Other notebooks may also be helpful.

# Class relationships

Once the example notebook is understood, the following class diagram may be helpful in understanding the organization and use of the code.

![](notebooks/200410_class_relationships.png)

# Run tests

    $ pytest --cov spectra --cov-report term-missing -vv -s