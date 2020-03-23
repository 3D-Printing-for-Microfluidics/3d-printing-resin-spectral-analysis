from pathlib import Path

from spectra.absorberspectrum import AbsorberSpectrum
from spectra.sourcespectrum import SourceSpectrum
from spectra.monomer import Monomer


def _get_data_directories(directory):
    filename_bad_first_characters = [".", "_"]
    return sorted(
        [
            d
            for d in directory.iterdir()
            if d.is_dir() and d.name[0] not in filename_bad_first_characters
        ]
    )


def _populate_data_type(dir_name, class_type):
    """Get all data for a particular type (sources, absorbers, photoinitiators).

    Parameters
    ----------
    dir_name - str
        Name of directory that contains data for a particular type
    class_type - Class
        Class to contain data (either AbsorberSpectrum or SourceSpectrum)
    """
    main_directory = Path(__file__).resolve().parent / dir_name
    data_directories = _get_data_directories(main_directory)
    result = {}
    for d in data_directories:
        result[d.name] = class_type(d)
    return result, main_directory


# -----------------------------------------------------------------------------
#  Absorbers
# -----------------------------------------------------------------------------

absorbers, absorbers_directory = _populate_data_type("absorbers", AbsorberSpectrum)


# -----------------------------------------------------------------------------
#  Photoinitiators
# -----------------------------------------------------------------------------

photoinitiators, photoinitiators_directory = _populate_data_type(
    "photoinitiators", AbsorberSpectrum
)


# -----------------------------------------------------------------------------
#  Sources
# -----------------------------------------------------------------------------

sources, sources_directory = _populate_data_type("sources", SourceSpectrum)


# -----------------------------------------------------------------------------
#  Monomers
# -----------------------------------------------------------------------------

monomers, monomers_directory = _populate_data_type("monomers", Monomer)
