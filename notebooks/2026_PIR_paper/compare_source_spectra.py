import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import resin_spectral_analysis.data as data
    from resin_spectral_analysis.resin import (
        Resin,
        ResinConstituentMonomer,
        ResinConstituentAbsorber,
    )
    from resin_spectral_analysis.irradiance import Irradiance
    from resin_spectral_analysis.normalizeddose import NormalizedDose
    from resin_spectral_analysis.utilities import ArrayParams

    return (
        ArrayParams,
        Irradiance,
        NormalizedDose,
        Resin,
        ResinConstituentAbsorber,
        ResinConstituentMonomer,
        data,
        mo,
        np,
        plt,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Source spectra for the PIR paper

    Normalized LED source spectra measured 2026-05-12, loaded from
    `resin_spectral_analysis.data.sources`. Irradiances are from the raw data file names.
    HR3.3u spectra were measured off the turning mirror.
    """)
    return


@app.cell(hide_code=True)
def _(data):
    # key in data.sources: (plot label, irradiance in mW/cm^2)
    new_sources = {
        "HR3.3u_365nm_Asahi_370nm_short_pass_filter_2026-05-12": (
            "HR3.3u 365 nm, Asahi 370 nm SP filter",
            39.35,
        ),
        "Asiga_385nm_MAX_X27_2026-05-12": ("Asiga MAX X27 385 nm", 20.5),
        "Anycubic_405nm_Photon_D2_2026-05-12": ("Anycubic Photon D2 405 nm", 2.50),
        "Elegoo_405nm_Mars4_Ultra_2026-05-12": ("Elegoo Mars 4 Ultra 405 nm", 2.78),
    }
    spectra = {key: data.sources[key] for key in new_sources}
    return new_sources, spectra


@app.cell(hide_code=True)
def _(data):
    # key in data.absorbers: plot label
    absorber_labels = {
        "nps_in_PEGDA_2017-04-13": "NPS in PEGDA (2017)",
        "sudanI_in_PEGDA_2017-04-13": "Sudan I in PEGDA (2017)",
    }
    absorbers = {key: data.absorbers[key] for key in absorber_labels}
    return absorber_labels, absorbers


@app.cell(hide_code=True)
def _(absorber_labels, absorbers, new_sources, plt, spectra):
    # Categorical palette, fixed order (validated for color-vision deficiency)
    colors = ["#2a78d6", "#1baf7a", "#eda100", "#e87ba4", "#4a3aa7", "#e34948"]
    source_colors, absorber_colors = colors[: len(new_sources)], colors[len(new_sources) :]

    fig, ax = plt.subplots(figsize=(11, 5))
    for (key, (label, _)), color in zip(new_sources.items(), source_colors):
        s = spectra[key]
        ax.plot(s.wavelength, s.power, color=color, linewidth=2, label=label)

    # Absorbers on the right axis, dashed to separate them from the sources
    ax_right = ax.twinx()
    for (key, label), color in zip(absorber_labels.items(), absorber_colors):
        a = absorbers[key]
        ax_right.plot(
            a.wavelength, a.molar_absorptivity, color=color, linewidth=2, linestyle="--",
            label=label,
        )

    ax.set_xlim(340, 440)
    ax.set_ylim(0, 1.05)
    ax_right.set_ylim(bottom=0)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Normalized source power (solid)")
    ax_right.set_ylabel("Molar absorptivity, L/(mol·cm) (dashed)")
    ax.grid(color="0.9", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax_right.spines["top"].set_visible(False)

    handles, labels = ax.get_legend_handles_labels()
    handles_right, labels_right = ax_right.get_legend_handles_labels()
    ax.legend(
        handles + handles_right, labels + labels_right, frameon=False, loc="upper left",
        bbox_to_anchor=(1.13, 1),
    )
    fig.tight_layout()
    fig
    return


@app.cell(hide_code=True)
def _(mo, new_sources, np, spectra):
    def summarize(s):
        above_half = s.wavelength[s.power >= 0.5]
        return {
            "Peak (nm)": round(float(s.wavelength[np.argmax(s.power)]), 1),
            "Half-max low (nm)": round(float(above_half.min()), 1),
            "Half-max high (nm)": round(float(above_half.max()), 1),
            "FWHM (nm)": round(float(above_half.max() - above_half.min()), 1),
        }


    mo.ui.table(
        [
            {"Source": label, "Irradiance (mW/cm²)": irradiance, **summarize(spectra[key])}
            for key, (label, irradiance) in new_sources.items()
        ],
        selection=None,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Normalized dose

    Normalized dose $D'(z)$ for each source, computed as in the "Putting it all together"
    cell of `notebooks/Example_normalized_dose_calculation.ipynb`. Resins are 100% PEGDA
    with 1% w/w Irgacure 819 (2017 spectrum) plus either 2% w/w NPS (HR3.3u, Asiga) or
    0.145% w/w Sudan I (Anycubic, Elegoo).
    """)
    return


@app.cell(hide_code=True)
def _(Resin, ResinConstituentAbsorber, ResinConstituentMonomer, data):
    def make_resin(absorber_key, absorber_ww_percent):
        return Resin(
            monomers=ResinConstituentMonomer(data.monomers["PEGDA"], 100),
            absorbers=ResinConstituentAbsorber(
                data.absorbers[absorber_key], absorber_ww_percent
            ),
            photoinitiators=ResinConstituentAbsorber(
                data.photoinitiators["irgacure819_in_PEGDA_2017-04-13"], 1.0
            ),
        )


    resins = {
        "NPS": make_resin("nps_in_PEGDA_2017-04-13", 2.0),
        "Sudan I": make_resin("sudanI_in_PEGDA_2017-04-13", 0.145),
    }
    return (resins,)


@app.cell(hide_code=True)
def _(ArrayParams, Irradiance, NormalizedDose, data, resins):
    wavelength_array_params = ArrayParams(300, 440, 281)

    # source key: (resin name, z array parameters in microns)
    dose_cases = {
        "HR3.3u_365nm_Asahi_370nm_short_pass_filter_2026-05-12": (
            "NPS",
            ArrayParams(0, 100, 201),
        ),
        "Asiga_385nm_MAX_X27_2026-05-12": ("NPS", ArrayParams(0, 100, 201)),
        "Anycubic_405nm_Photon_D2_2026-05-12": ("Sudan I", ArrayParams(0, 200, 401)),
        "Elegoo_405nm_Mars4_Ultra_2026-05-12": ("Sudan I", ArrayParams(0, 200, 401)),
    }

    norm_doses = {
        _key: NormalizedDose(
            irradiance=Irradiance(
                source=data.sources[_key],
                resin=resins[_resin_name],
                wavelength_array_params=wavelength_array_params,
            ),
            z_array_params=_z_array_params,
        )
        for _key, (_resin_name, _z_array_params) in dose_cases.items()
    }
    return (norm_doses,)


@app.cell(hide_code=True, expand_output=True)
def _(mo, new_sources, norm_doses):
    dose_figs = []
    for _key, _norm_dose in norm_doses.items():
        _title = _norm_dose.irradiance.resin.name + "\n" + new_sources[_key][0]
        _fig, _ = _norm_dose.plot(title=_title)
        dose_figs.append(_fig)

    mo.vstack([mo.hstack(dose_figs[:2]), mo.hstack(dose_figs[2:])])
    return


@app.cell(hide_code=True)
def _(mo, new_sources, norm_doses):
    mo.ui.table(
        [
            {
                "Source": new_sources[_key][0],
                "Resin": _nd.irradiance.resin.name,
                "exp(-z/b): b (µm)": round(_nd.ha_model_params["ha"], 3),
                "a·exp(-z/b)+(1-a): a": round(_nd.a_b_model_params["a"], 4),
                "a·exp(-z/b)+(1-a): b (µm)": round(_nd.a_b_model_params["b"], 3),
                "a·exp(-z/b)+c: a": round(_nd.a_b_c_model_params["a"], 4),
                "a·exp(-z/b)+c: b (µm)": round(_nd.a_b_c_model_params["b"], 3),
                "a·exp(-z/b)+c: c": round(_nd.a_b_c_model_params["c"], 4),
            }
            for _key, _nd in norm_doses.items()
        ],
        selection=None,
    )
    return


if __name__ == "__main__":
    app.run()
