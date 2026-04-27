from importlib.resources import files
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


def test_load_absorber():
    path = files("spectra.data") / "absorbers" / "avobenzone_in_PEGDA_2017-04-13"
    obj = data.load_absorber(path, name="test_absorber")
    assert isinstance(obj, AbsorberSpectrum)
    assert "test_absorber" in data.absorbers
    assert data.absorbers["test_absorber"] is obj
    del data.absorbers["test_absorber"]


def test_load_photoinitiator():
    path = files("spectra.data") / "photoinitiators" / "irgacure819_in_PEGDA_2017-04-13"
    obj = data.load_photoinitiator(path, name="test_photoinitiator")
    assert isinstance(obj, AbsorberSpectrum)
    assert "test_photoinitiator" in data.photoinitiators
    assert data.photoinitiators["test_photoinitiator"] is obj
    del data.photoinitiators["test_photoinitiator"]


def test_load_source():
    path = (
        files("spectra.data") / "sources" / "365nm_visitech_with_50mm_asahi_filter_2018-11-22"
    )
    obj = data.load_source(path, name="test_source")
    assert isinstance(obj, SourceSpectrum)
    assert "test_source" in data.sources
    assert data.sources["test_source"] is obj
    del data.sources["test_source"]


def test_load_monomer():
    json_file = files("spectra.data") / "monomers" / "hdda.json"
    obj = data.load_monomer(json_file)
    assert isinstance(obj, Monomer)
    assert obj.name in data.monomers
    assert data.monomers[obj.name] is obj


# def test_material_name_and_type():
#     assert data.material_name_and_type("Avobenzone") == ("Absorber", "Avo")
#     assert data.material_name_and_type("avobenzone") == ("Absorber", "avo")
#     assert data.material_name_and_type("Irgacure 819") == ("Photoinitiator", "Irg")
#     assert data.material_name_and_type("NPS") == ("Absorber", "NPS")
#     assert data.material_name_and_type("PEGDA") == ("Monomer", "PEG")
#     assert data.material_name_and_type("TMDPO") == ("Photoinitiator", "TMD")
#     assert data.material_name_and_type("Benetex OB+") == ("Absorber", "Ben")
#     assert data.material_name_and_type("Benetex OBplus") == ("Absorber", "Ben")

#     with pytest.raises(ValueError):
#         temp = data.material_name_and_type("not a name")
