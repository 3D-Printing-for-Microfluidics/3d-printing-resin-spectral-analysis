from pathlib import Path

from spectra.absorberspectrum import AbsorberSpectrum

absorbers = {}

_this_dir = Path(__file__).parent

_directories = sorted(
    [_d for _d in _this_dir.iterdir() if _d.is_dir() and _d.name[0] not in [".", "_"]]
)

for _d in _directories:
    absorbers[_d.name] = AbsorberSpectrum(_d)
