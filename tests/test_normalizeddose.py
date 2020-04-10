from pathlib import Path
import tempfile

import numpy as np

import matplotlib.pyplot as plt

import spectra.data as data
from spectra.resin import ResinConstituentAbsorber, ResinConstituentMonomer, Resin
from spectra.irradiance import Irradiance
from spectra.utilities import ArrayParams
from spectra.normalizeddose import NormalizedDose
from spectra.spectrummodels import (
    ha_model,
    a_b_model,
    a_b_c_model,
    fit_ha_model,
    fit_a_b_model,
    fit_a_b_c_model,
)


def test_normalizeddose():
    monomer = ResinConstituentMonomer(data.monomers["Ideal"], 100)
    absorber = ResinConstituentAbsorber(data.absorbers["ideal_uniform_absorber"], 1)
    resin = Resin(monomers=monomer, absorbers=absorber)

    source = data.sources["Ideal_uniform_10nm_source"]
    irradiance = Irradiance(
        source=source, resin=resin, wavelength_array_params=ArrayParams(300, 440, 701)
    )

    norm_dose = NormalizedDose(
        irradiance=irradiance, z_array_params=ArrayParams(0, 30, 5)
    )

    assert np.allclose(norm_dose.normalized_dose, np.exp(-norm_dose.z_um / 10))

    with tempfile.TemporaryDirectory() as d:
        temporary_file = Path(d) / "tempfile.png"

        fig, ax = norm_dose.plot(  # pylint: disable=unused-variable
            title="temp title", file=temporary_file
        )
