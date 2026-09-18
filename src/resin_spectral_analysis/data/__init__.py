from importlib.resources import files
from pathlib import Path

from resin_spectral_analysis.absorberspectrum import AbsorberSpectrum
from resin_spectral_analysis.sourcespectrum import SourceSpectrum
from resin_spectral_analysis.monomer import Monomer


def _get_data_directories(directory):
    filename_bad_first_characters = [".", "_"]
    return sorted(
        [
            d
            for d in directory.iterdir()
            if d.is_dir() and d.name[0] not in filename_bad_first_characters
        ]
    )


def _populate_data_from_directories(dir_name, class_type):
    """Get all data for a particular type (sources, absorbers, photoinitiators).

    This function looks in a directory, `dir_name`, such as `absorbers`,
    and finds all of the directories within it. Each of these are assumed to
    contain data files for a particular material (i.e., a particular absorber).
    Each of these directories is passed to the appropriate class, `AbsorberSpectrum`
    or `SourceSpectrum`, to load the data within the directory so that it is ready
    for use. These are put into a list that is returned by the function.
    
    Parameters
    ----------
    dir_name - str
        Name of directory that contains data for a particular type
    class_type - Class
        Class to contain data (either AbsorberSpectrum or SourceSpectrum)

    Returns
    -------
    list - contains an object for each data directory encountered in `dir_name`.
    Path - Path object for `dir_name` in case the user needs to reach in and directly
        get raw data (which should be extremely rare).
    """
    main_directory = files("resin_spectral_analysis.data") / dir_name
    data_directories = _get_data_directories(main_directory)
    result = {}
    for d in data_directories:
        result[d.name] = class_type(d)
    return result, main_directory


def _populate_data_from_json_files(dir_name, class_type):
    main_directory = files("resin_spectral_analysis.data") / dir_name
    json_files = sorted([f for f in main_directory.glob("*.json")])
    result = {}
    for json_file in json_files:
        temp = Monomer(json_file)
        result[temp.name] = temp

    return result, main_directory


# -----------------------------------------------------------------------------
#  Absorbers
# -----------------------------------------------------------------------------

absorbers, absorbers_directory = _populate_data_from_directories(
    "absorbers", AbsorberSpectrum
)


# -----------------------------------------------------------------------------
#  Photoinitiators
# -----------------------------------------------------------------------------

photoinitiators, photoinitiators_directory = _populate_data_from_directories(
    "photoinitiators", AbsorberSpectrum
)


# -----------------------------------------------------------------------------
#  Sources
# -----------------------------------------------------------------------------

sources, sources_directory = _populate_data_from_directories("sources", SourceSpectrum)


# -----------------------------------------------------------------------------
#  Monomers
# -----------------------------------------------------------------------------

monomers, monomers_directory = _populate_data_from_json_files("monomers", Monomer)


# -----------------------------------------------------------------------------
#  Material names
# -----------------------------------------------------------------------------

_monomer_abbreviations = {
    "PEGDA": "PEG",
    "HDDA": "HDD",
    "TET": "TET",
    "Lauryl acrylate": "Lau",
    "Ideal": "Ide",
}

_absorber_abbreviations = {
    "Avobenzone": "Avo",
    "NPS": "NPS",
    "Benetex OBplus": "BOB",
    "BLS99-2": "B99",
    "Martius Yellow": "MaY",
    "Octocrylene": "Oct",
    "Phenazine": "Phe",
    "Salicylaldehyde": "Sal",
    "Sudan I": "SuI",
    "Uniform absorber": "Uni",
}

_photoinitiator_abbreviations = {"Irgacure 819": "Irg", "TMDPO": "TMD", "BME": "BME"}

material_abbreviations = {
    **_monomer_abbreviations,
    **_absorber_abbreviations,
    **_photoinitiator_abbreviations,
}


# -----------------------------------------------------------------------------
#  Programmatic load functions
# -----------------------------------------------------------------------------


def load_absorber(directory, *, name=None):
    """Load an AbsorberSpectrum from an arbitrary directory and register it in data.absorbers.

    Parameters
    ----------
    directory : str or Path
        Directory containing absorbance.csv and molar_absorptivity.csv.
    name : str, optional
        Key to use in data.absorbers. Defaults to the directory's name.

    Returns
    -------
    AbsorberSpectrum
    """
    path = Path(directory)
    key = name if name is not None else path.name
    absorbers[key] = AbsorberSpectrum(path)
    return absorbers[key]


def load_photoinitiator(directory, *, name=None):
    """Load an AbsorberSpectrum from an arbitrary directory and register it in data.photoinitiators.

    Parameters
    ----------
    directory : str or Path
        Directory containing absorbance.csv and molar_absorptivity.csv.
    name : str, optional
        Key to use in data.photoinitiators. Defaults to the directory's name.

    Returns
    -------
    AbsorberSpectrum
    """
    path = Path(directory)
    key = name if name is not None else path.name
    photoinitiators[key] = AbsorberSpectrum(path)
    return photoinitiators[key]


def load_source(directory, *, name=None):
    """Load a SourceSpectrum from an arbitrary directory and register it in data.sources.

    Parameters
    ----------
    directory : str or Path
        Directory containing measured_spectrum_normalized.csv.
    name : str, optional
        Key to use in data.sources. Defaults to the directory's name.

    Returns
    -------
    SourceSpectrum
    """
    path = Path(directory)
    key = name if name is not None else path.name
    sources[key] = SourceSpectrum(path)
    return sources[key]


def load_monomer(json_file):
    """Load a Monomer from a JSON file and register it in data.monomers.

    Parameters
    ----------
    json_file : str or Path
        Path to a monomer JSON file with keys "Name", "Long name", "Density g/L".

    Returns
    -------
    Monomer
    """
    obj = Monomer(Path(json_file))
    monomers[obj.name] = obj
    return obj
