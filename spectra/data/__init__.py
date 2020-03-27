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
    main_directory = Path(__file__).resolve().parent / dir_name
    data_directories = _get_data_directories(main_directory)
    result = {}
    for d in data_directories:
        result[d.name] = class_type(d)
    return result, main_directory


def _populate_data_from_json_files(dir_name, class_type):
    main_directory = Path(__file__).resolve().parent / dir_name
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

monomer_names = ["PEGDA", "HDDA", "TET", "Lauryl acrylate"]

absorber_names = [
    "Avobenzone",
    "NPS",
    "Benetex OBplus",
    "BLS99-2",
    "Martius Yellow",
    "Octocrylene",
    "Phenazine",
    "Salicylaldehyde",
    "Sudan I",
]

photoinitiator_names = ["Irgacure 819", "TMDPO"]


def material_name_and_type(test_string):
    material_type = None
    material_name = None

    def lower_and_split(names):
        temp_names = []
        for n in names:
            temp_names.append(n.lower().split(" ")[0])
        return temp_names

    temp_monomer_names = lower_and_split(monomer_names)
    temp_absorber_names = lower_and_split(absorber_names)
    temp_photoinitiator_names = lower_and_split(photoinitiator_names)

    temp_test_string = test_string.lower().split(" ")[0]

    if temp_test_string in temp_monomer_names:
        material_type = "Monomer"
        material_name = test_string[:3]
        return material_type, material_name

    if temp_test_string in temp_absorber_names:
        material_type = "Absorber"
        material_name = test_string[:3]
        return material_type, material_name

    if temp_test_string in temp_photoinitiator_names:
        material_type = "Photoinitiator"
        material_name = test_string[:3]
        return material_type, material_name

    raise ValueError(
        f"Material '{test_string}' is not in 'monomer_names', 'absorber_names', or 'photoinitiator_names.'"
    )
