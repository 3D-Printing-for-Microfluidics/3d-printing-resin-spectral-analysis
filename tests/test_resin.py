import json
from pathlib import Path

import numpy as np
import pytest

import spectra.data as data
from spectra.absorberspectrum import AbsorberSpectrum
from spectra.monomer import Monomer
from spectra.resin import ResinConstituentAbsorber, ResinConstituentMonomer, Resin


def test_ResinConstituentAbsorber():
    temp_absorber = ResinConstituentAbsorber(
        data.absorbers["avobenzone_in_PEGDA_2020-01-20"], 0.38
    )
    assert temp_absorber.concentration_ww_percent == 0.38


def test_ResinConstituentMonomer():
    temp_monomer = ResinConstituentMonomer(data.monomers["PEGDA"], 50)
    assert temp_monomer.concentration_percent_monomer == 50


def test_Resin():

    # PEGDA - Avobenzone - Irgacure 819
    pegda = ResinConstituentMonomer(data.monomers["PEGDA"], 100)
    avobenzone = ResinConstituentAbsorber(
        data.absorbers["avobenzone_in_PEGDA_2020-01-20"], 0.38
    )
    irgacure819 = ResinConstituentAbsorber(
        data.photoinitiators["irgacure819_in_PEGDA_2020-01-20"], 1.0
    )
    resin = Resin(monomers=pegda, absorbers=avobenzone, photoinitiators=irgacure819)
    assert resin.name == "PEG-100__Avo-0.38__Irg-1"
    result = 738.6
    assert np.isclose(resin.calc_absorption_coef_inv_cm(365.0), result, rtol=1.0e-4)
    assert np.isclose(
        resin.calc_absorption_coef_inv_um(365.0), result * 1e-4, rtol=1.0e-4
    )

    # PEGDA only
    with pytest.raises(ValueError):
        temp = Resin(monomers=pegda)  # pylint: disable=unused-variable

    # PEGDA & wrong absorber data type in list
    with pytest.raises(AssertionError):
        temp = Resin(monomers=pegda, absorbers=[1])  # pylint: disable=unused-variable

    # PEGDA & wrong absorber data type
    with pytest.raises(TypeError):
        temp = Resin(monomers=pegda, absorbers=1)  # pylint: disable=unused-variable

    # Only monomers and no absorbers or photoinitiators
    with pytest.raises(ValueError):
        pegda1 = ResinConstituentMonomer(data.monomers["PEGDA"], 50)
        pegda2 = ResinConstituentMonomer(data.monomers["PEGDA"], 49)
        temp = Resin(monomers=[pegda1, pegda2])  # pylint: disable=unused-variable

    # Name with only an absorber
    temp = Resin(monomers=pegda, absorbers=avobenzone)
    assert temp.name == "PEG-100__Avo-0.38__"

    # Name with only a photoinitiator
    temp = Resin(monomers=pegda, photoinitiators=irgacure819)
    assert temp.name == "PEG-100____Irg-1"

    # Extreme name case
    hdda = ResinConstituentMonomer(data.monomers["PEGDA"], 85)
    la = ResinConstituentMonomer(data.monomers["TET"], 15)
    avobenzone = ResinConstituentAbsorber(
        data.absorbers["avobenzone_in_PEGDA_2020-01-20"], 1.5
    )
    nps = ResinConstituentAbsorber(data.absorbers["nps_in_PEGDA_2017-04-13"], 2.0)
    irgacure819 = ResinConstituentAbsorber(
        data.photoinitiators["irgacure819_in_PEGDA_2020-01-20"], 1
    )
    tmdpo = ResinConstituentAbsorber(
        data.photoinitiators["tmdpo_in_PEGDA_2017-04-13"], 0.25
    )
    resin = Resin(
        monomers=[hdda, la],
        absorbers=[avobenzone, nps],
        photoinitiators=[irgacure819, tmdpo],
    )
    assert resin.name == "PEG-85_TET-15__Avo-1.5_NPS-2__Irg-1_TMD-0.25"


def test_resin_with_ideal_data():
    monomer = ResinConstituentMonomer(data.monomers["Ideal"], 100)
    absorber = ResinConstituentAbsorber(data.absorbers["ideal_uniform_absorber"], 1)
    resin = Resin(monomers=monomer, absorbers=absorber)

    assert resin.name == "Ide-100__Uni-1__"

    # See my notes at "data/README.md" under section "Ideal uniform source and absorber for tests":
    assert np.isclose(resin.calc_absorption_coef_inv_cm(365), 1e3)
    assert np.isclose(resin.calc_absorption_coef_inv_um(365), 0.1)
