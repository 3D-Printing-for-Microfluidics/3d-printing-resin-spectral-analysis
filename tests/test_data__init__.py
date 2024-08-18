from pathlib import Path

import pytest

from spectra.absorberspectrum import AbsorberSpectrum
from spectra.sourcespectrum import SourceSpectrum
from spectra.monomer import Monomer
import spectra.data as data


def test_sources_absorbers_monomers():
    for key in data.sources:
        assert isinstance(data.sources[key], SourceSpectrum)
    for key in data.absorbers:
        assert isinstance(data.absorbers[key], AbsorberSpectrum)
    for key in data.photoinitiators:
        assert isinstance(data.photoinitiators[key], AbsorberSpectrum)
    for key in data.monomers:
        assert isinstance(data.monomers[key], Monomer)


# def test_material_name_and_type():
#     assert data.material_name_and_type("Avobenzone") == ("Absorber", "Avo")
#     assert data.material_name_and_type("avobenzone") == ("Absorber", "avo")
#     assert data.material_name_and_type("Irgacure 819") == ("Photoinitiator", "Irg")
#     assert data.material_name_and_type("NPS") == ("Absorber", "NPS")
#     assert data.material_name_and_type("PEGDA") == ("Monomer", "PEG")
#     assert data.material_name_and_type("TPO") == ("Photoinitiator", "TPO")
#     assert data.material_name_and_type("Benetex OB+") == ("Absorber", "Ben")
#     assert data.material_name_and_type("Benetex OBplus") == ("Absorber", "Ben")

#     with pytest.raises(ValueError):
#         temp = data.material_name_and_type("not a name")
