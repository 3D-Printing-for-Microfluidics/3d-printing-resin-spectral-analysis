# Models

The following models are from [Custom 3D printer and resin for 18 μm × 20 μm microfluidic flow channels](https://www.ncbi.nlm.nih.gov/pubmed/28726927).

## Spectrum models

- $D_n(z)$ - Normalized dose
- $b$ - optical penetration depth
- $a$ - related to spectral overlap of source and absorber with
  - $a=0$ no overlap
  - $a=1$ complete overlap

### Model 1

$$D_n(z) = \exp(-z/b)$$

### Model 2

$$D_n(z) = 1 - a(1 - \exp(-z/b))$$

## Thickness measurement models

- $t_p$ - exposure time
- $z_p$ - measured polymerization thickness

### Model 3

$$z_p  = h_a \ln \frac{t_p}{T_c}$$

with

- $h_a$ - optical penetration depth
- $T_c$ - polymerization threshold exposure time

### Model 4

$$t_p  = \frac{T_c}{(1-a) + a \exp(-z_p/b)}$$

with

- $b$ - optical penetration depth
- $a$ - related to spectral overlap of source and absorber with
  - $a=0$ no overlap
  - $a=1$ complete overlap
