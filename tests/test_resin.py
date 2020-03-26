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

    pegda = ResinConstituentMonomer(data.monomers["PEGDA"], 100)
    avobenzone = ResinConstituentAbsorber(
        data.absorbers["avobenzone_in_PEGDA_2020-01-20"], 0.38
    )
    irgacure819 = ResinConstituentAbsorber(
        data.photoinitiators["irgacure819_in_PEGDA_2020-01-20"], 1.0
    )
    resin = Resin(monomers=pegda, absorbers=avobenzone, photoinitiators=irgacure819)

    result = 738.6
    assert np.isclose(resin.calc_absorption_coef_inv_cm(365.0), result, rtol=1.0e-4)

    with pytest.raises(ValueError):
        temp = Resin(monomers=pegda)  # pylint: disable=unused-variable

    with pytest.raises(AssertionError):
        temp = Resin(monomers=pegda, absorbers=[1])  # pylint: disable=unused-variable

    with pytest.raises(TypeError):
        temp = Resin(monomers=pegda, absorbers=1)  # pylint: disable=unused-variable

    with pytest.raises(ValueError):
        pegda1 = ResinConstituentMonomer(data.monomers["PEGDA"], 50)
        pegda2 = ResinConstituentMonomer(data.monomers["PEGDA"], 49)
        temp = Resin(monomers=[pegda1, pegda2])  # pylint: disable=unused-variable
