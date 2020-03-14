# Contents

This directory contains data for absorbers, photoinitiators, resins, and sources organized in the following directories.

    data
    ├── README.md
    ├── __init__.py
    ├── absorbers
    ├── photoinitiators
    ├── resins
    └── sources

The `absorbers`, `photoinitiators`, and `sources` directories contain spectrum data for various materials. Spectrum data is measured with the following equipment:

- Sources: [Ocean Optics Flame Spectrometer FLMS15581](https://www.oceaninsight.com/products/spectrometers/), 300-440 nm range, 0.23 nm resolution, purchased August 2019
- Absorbers/photoinitiators/resins: Ocean Optics QE65PRO-ABS with 100 &mu;m fiber and 10 &mu;m slit, 191-994 nm range, 1.6 nm resolution, purchased October 2012

This data can be used to derive $h_a$ for Model 1 and $a$ and $b$ for Model 2 in [Custom 3D printer and resin for 18 μm × 20 μm microfluidic flow channels](https://www.ncbi.nlm.nih.gov/pubmed/28726927).

The `resins` directory contains measured polymerization thickness as a function of exposure time. This data can be used to derive $h_a$ and $T_c$ for Model 3 and $a$, $b$, and $T_c$ for Model 4 in [Custom 3D printer and resin for 18 μm × 20 μm microfluidic flow channels](https://www.ncbi.nlm.nih.gov/pubmed/28726927).

# Adding new spectrum data

See the README.md file in each sub-directory (sources, absorbers, photoinitiators) for directions on how to add new spectrum data.
