from pathlib import Path

from spectra.absorberspectrum import AbsorberSpectrum

absorbers = {}

this_dir = Path(__file__).parent

directories = sorted(
    [d for d in this_dir.iterdir() if d.is_dir() and d.name[0] not in [".", "_"]]
)

for d in directories:
    absorbers[d.name] = AbsorberSpectrum(d)
