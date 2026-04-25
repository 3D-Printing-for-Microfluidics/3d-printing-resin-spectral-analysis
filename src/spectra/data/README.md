# Contents

This directory contains data for absorbers, photoinitiators, resins, and sources organized in the following directories.

    data
    ├── README.md
    ├── __init__.py
    ├── absorbers
    ├── photoinitiators
    ├── resins
    └── sources

The `absorbers` and `photoinitiators` directories contain absorption spectrum data for various materials measured with an Ocean Optics QE65PRO-ABS spectrometer with 100 &mu;m core diameter fiber and 10 &mu;m slit, 199-1001 nm range, 1.6 nm resolution, and purchased October 2012.

The `sources` directories contain emission spectrum data for various 3D printers and LEDs. Measurements are made with an [Ocean Optics Flame Spectrometer FLMS15581](https://www.oceaninsight.com/products/spectrometers/) with 300-440 nm range, 0.23 nm resolution, and purchased August 2019. Spectrum measurements before this date were made with the QE65PRO-ABS.

This material absorption data and source emission data can be used to calculate $h_a$ for Model 1 and $a$ and $b$ for Model 2 in [Custom 3D printer and resin for 18 μm × 20 μm microfluidic flow channels](https://www.ncbi.nlm.nih.gov/pubmed/28726927).

The `resins` directory contains measured polymerization thickness as a function of exposure time. This data can be used to derive $h_a$ and $T_c$ for Model 3 and $a$, $b$, and $T_c$ for Model 4 in [Custom 3D printer and resin for 18 μm × 20 μm microfluidic flow channels](https://www.ncbi.nlm.nih.gov/pubmed/28726927).

# Adding new spectrum data

See the README.md file in each sub-directory (sources, absorbers, photoinitiators) for directions on how to add new spectrum data.

# Ideal uniform source and absorber for tests

An ideal uniform source and absorber are included, as well as an ideal monomer, to facilitate testing code. They can also be used in exploratory calculations. Notes on the source and absorber are included below.

![](Ideal_uniform_source_and_absorber.jpg)