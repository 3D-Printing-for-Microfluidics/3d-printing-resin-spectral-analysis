# Purpose

This repository contains spectrum data and associated tools for resin and 3D printer development in the [Nordin Group](https://ece.byu.edu/faculty/greg_nordin) at Brigham Young University. Our focus is the development of 3D printer technology to meet the unique needs of microfluidic device fabrication.

# References

[Optical approach to resin formulation for 3D printed microfluidics](https://www.ncbi.nlm.nih.gov/pubmed/26744624)  
[Custom 3D printer and resin for 18 μm × 20 μm microfluidic flow channels](https://www.ncbi.nlm.nih.gov/pubmed/28726927)  


# Installation

    $ pip install git+https://github.com/gregnordin/3dprinter_spectra_and_tools

# How to use

See `examples/Example_normalized_dose_calculation.ipynb`.

# Class relationships

![](notebooks/200410_class_relationships.png)

# Run tests

    $ pytest --cov spectra --cov-report term-missing -vv -s