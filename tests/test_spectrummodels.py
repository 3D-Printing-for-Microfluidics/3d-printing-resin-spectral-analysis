import numpy as np

from spectra.spectrummodels import (
    ha_model,
    a_b_model,
    a_b_c_model,
    fit_ha_model,
    fit_a_b_model,
    fit_a_b_c_model,
)


def test_ha_model():
    ha = 10.0
    temp_z = np.linspace(0, 20, 3)
    result = np.array([1.0, 0.36787944, 0.13533528])
    assert np.allclose(ha_model(temp_z, ha), result)

    params, cov = fit_ha_model(temp_z, ha_model(temp_z, ha))
    assert np.allclose(params, [ha])
    assert np.allclose(cov, [0])


def test_a_b_model():
    a = 0.5
    b = 10.0
    temp_z = np.linspace(0, 20, 3)
    result = np.array([1.0, 0.68393972, 0.56766764])
    assert np.allclose(a_b_model(temp_z, a, b), result)

    params, cov = fit_a_b_model(temp_z, a_b_model(temp_z, a, b))
    assert np.allclose(params, [a, b])
    assert np.allclose(cov, [[0, 0], [0, 0]])


def test_a_b_c_model():
    a = 0.5
    b = 10.0
    c = 0.3
    temp_z = np.linspace(0, 20, 7)
    result = np.array(
        [0.8, 0.65826566, 0.55670856, 0.48393972, 0.43179857, 0.3944378, 0.36766764]
    )
    assert np.allclose(a_b_c_model(temp_z, a, b, c), result)

    params, cov = fit_a_b_c_model(temp_z, a_b_c_model(temp_z, a, b, c))
    assert np.allclose(params, [a, b, c])
    assert np.allclose(cov, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
