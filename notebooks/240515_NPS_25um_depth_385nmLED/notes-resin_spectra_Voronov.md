# Package installation

In my `3dprinter_spectra_and_tools` folder/package, create virtual environment and set it as a jupyter kernel that I can then access from `Jupyter Desktop`.

```
# Set base python version
conda activate default

# Create virtual environment and activate
python -m venv .venv --prompt spectra
conda deactivate
source .venv/bin/activate

# Confirm
which python
/Users/nordin/Documents/Projects/3D_printer_spectra_repos/3dprinter_spectra_and_tools/.venv/bin/python
python --version
Python 3.12.2

# Install 3dprinter_spectra_and_tools
pip install -e .

# Make this virtual environment a generally-available Jupyter kernel
python -m ipykernel install --user --name spectra_and_tools --display-name=spectra_and_tools
Installed kernelspec spectra_and_tools in /Users/nordin/Library/Jupyter/kernels/spectra_and_tools

```

## Does not work!

Install [3dprinter_spectra_and_tools](https://github.com/3D-Printing-for-Microfluidics/3dprinter_spectra_and_tools):

```
# Set base python version
conda activate default

# Create virtual environment and activate
python -m venv .venv --prompt resin_spectra_Voronov
conda deactivate
source .venv/bin/activate

which python
/Users/nordin/Documents/Projects/2024_projects/resin_spectra_Voronov/.venv/bin/python

# Install 3dprinter_spectra_and_tools
pip install git+ssh://git@github.com/gregnordin/3dprinter_spectra_and_tools
```

