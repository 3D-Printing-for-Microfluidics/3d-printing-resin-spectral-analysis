from pathlib import Path


def _get_data_directories(directory):
    filename_bad_first_characters = [".", "_"]
    return sorted(
        [
            d
            for d in directory.iterdir()
            if d.is_dir() and d.name[0] not in filename_bad_first_characters
        ]
    )


# -----------------------------------------------------------------------------
#  Absorbers
# -----------------------------------------------------------------------------

from spectra.absorberspectrum import AbsorberSpectrum

absorbers_directory = Path(__file__).resolve().parent / "absorbers"
_directories = _get_data_directories(absorbers_directory)
absorbers = {}
for _d in _directories:
    absorbers[_d.name] = AbsorberSpectrum(_d)


# -----------------------------------------------------------------------------
#  Photoinitiators
# -----------------------------------------------------------------------------

photoinitiators_directory = Path(__file__).resolve().parent / "photoinitiators"
_directories = _get_data_directories(photoinitiators_directory)
photoinitiators = {}
for _d in _directories:
    photoinitiators[_d.name] = AbsorberSpectrum(_d)


# -----------------------------------------------------------------------------
#  Sources
# -----------------------------------------------------------------------------

from spectra.sourcespectrum import SourceSpectrum

sources_directory = Path(__file__).resolve().parent / "sources"
_directories = _get_data_directories(sources_directory)
sources = {}
for _d in _directories:
    sources[_d.name] = SourceSpectrum(_d)
