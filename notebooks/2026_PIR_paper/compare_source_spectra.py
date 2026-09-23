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

    The plot also shows the molar absorptivity (right axis) of two absorbers
    (dashed) and of the photoinitiator Irgacure 819 (dotted, scaled ×10 to be
    visible) for comparison.
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

    # Photoinitiator, scaled so it is visible next to the absorbers
    photoinitiator = data.photoinitiators["irgacure819_in_PEGDA_2017-04-13"]
    photoinitiator_multiplier = 10
    photoinitiator_label = f"Irgacure 819 in PEGDA (2017) ×{photoinitiator_multiplier}"
    return (
        absorber_labels,
        absorbers,
        photoinitiator,
        photoinitiator_label,
        photoinitiator_multiplier,
    )


@app.cell(hide_code=True)
def _(
    absorber_labels,
    absorbers,
    data,
    new_sources,
    photoinitiator,
    photoinitiator_label,
    photoinitiator_multiplier,
    plt,
):
    # Colors follow each spectrum so they stay the same across plots. Categorical palette
    # in fixed order, validated for color-vision deficiency.
    series_colors = {
        "HR3.3u_365nm_Asahi_370nm_short_pass_filter_2026-05-12": "#2a78d6",
        "HR3.3_365nm_Asahi_370nm_short_pass_filter_grayscale_2026-05-12": "#eb6834",
        "Asiga_385nm_MAX_X27_2026-05-12": "#1baf7a",
        "Anycubic_405nm_Photon_D2_2026-05-12": "#eda100",
        "Elegoo_405nm_Mars4_Ultra_2026-05-12": "#e87ba4",
        "OS1_365nm_Asahi_370nm_short_pass_filter_grayscale_2026-05-12": "#008300",
        "nps_in_PEGDA_2017-04-13": "#4a3aa7",
        "sudanI_in_PEGDA_2017-04-13": "#e34948",
        # Neutral gray so the photoinitiator is less prominent than the other curves
        "irgacure819_in_PEGDA_2017-04-13": "#898781",
    }


    def plot_spectra(sources, wavelength_min=340, wavelength_max=440):
        """Plot normalized source spectra (left axis) with absorber and photoinitiator
        molar absorptivity (right axis).

        sources - dict of data.sources key: (plot label, irradiance in mW/cm^2)
        """
        fig, ax = plt.subplots(figsize=(11, 5))
        for key, (label, _) in sources.items():
            s = data.sources[key]
            ax.plot(s.wavelength, s.power, color=series_colors[key], linewidth=2, label=label)

        # Absorbers and photoinitiator on the right axis, broken lines to separate them
        # from the sources
        ax_right = ax.twinx()
        for key, label in absorber_labels.items():
            a = absorbers[key]
            ax_right.plot(
                a.wavelength, a.molar_absorptivity, color=series_colors[key], linewidth=2,
                linestyle="--", label=label,
            )
        # Photoinitiator dotted so it is less prominent than the absorbers
        ax_right.plot(
            photoinitiator.wavelength,
            photoinitiator_multiplier * photoinitiator.molar_absorptivity,
            color=series_colors["irgacure819_in_PEGDA_2017-04-13"], linewidth=2,
            linestyle=":", label=photoinitiator_label,
        )

        ax.set_xlim(wavelength_min, wavelength_max)
        ax.set_ylim(0, 1.05)
        # Scale the right axis to the data shown, not the data outside the x limits
        right_max = max(
            line.get_ydata()[
                (line.get_xdata() >= wavelength_min) & (line.get_xdata() <= wavelength_max)
            ].max()
            for line in ax_right.get_lines()
        )
        ax_right.set_ylim(0, 1.05 * right_max)
        ax.set_xlabel("Wavelength (nm)")
        ax.set_ylabel("Normalized source power (solid)")
        ax_right.set_ylabel("Molar absorptivity, L/(mol·cm) (dashed, dotted)")
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
        return fig


    plot_spectra(new_sources)
    return (plot_spectra,)


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
    return dose_cases, norm_doses, wavelength_array_params


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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Source spectra including the HR3.3 and OS1

    The first plot with the HR3.3 and OS1 365 nm, Asahi 370 nm short pass filter spectra
    added. Both were measured with a grayscale image. The HR3.3 was measured off the turning
    mirror, like the HR3.3u; the OS1 was not.
    """)
    return


@app.cell(hide_code=True)
def _(new_sources, plot_spectra):
    # new_sources with the HR3.3 spectrum inserted after the HR3.3u, and the OS1 spectrum
    # after the other sources (keeps the validated color order)
    _items = list(new_sources.items())
    extended_sources = dict(
        [
            _items[0],
            (
                "HR3.3_365nm_Asahi_370nm_short_pass_filter_grayscale_2026-05-12",
                ("HR3.3 365 nm, Asahi 370 nm SP filter", 46.7),
            ),
            *_items[1:],
            (
                "OS1_365nm_Asahi_370nm_short_pass_filter_grayscale_2026-05-12",
                ("OS1 365 nm, Asahi 370 nm SP filter", 47.5),
            ),
        ]
    )

    plot_spectra(extended_sources)
    return (extended_sources,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Normalized dose for the HR3.3

    $D'(z)$ for the HR3.3 365 nm, Asahi 370 nm short pass filter source in the NPS resin,
    with the same settings as the HR3.3u plot above for direct comparison.
    """)
    return


@app.cell(hide_code=True)
def _(
    Irradiance,
    NormalizedDose,
    data,
    dose_cases,
    extended_sources,
    resins,
    wavelength_array_params,
):
    hr33_key = "HR3.3_365nm_Asahi_370nm_short_pass_filter_grayscale_2026-05-12"
    hr33_norm_dose = NormalizedDose(
        irradiance=Irradiance(
            source=data.sources[hr33_key],
            resin=resins["NPS"],
            wavelength_array_params=wavelength_array_params,
        ),
        z_array_params=dose_cases["HR3.3u_365nm_Asahi_370nm_short_pass_filter_2026-05-12"][1],
    )

    hr33_dose_fig, _ = hr33_norm_dose.plot(
        title=hr33_norm_dose.irradiance.resin.name + "\n" + extended_sources[hr33_key][0]
    )
    hr33_dose_fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Normalized dose for the OS1

    $D'(z)$ for the OS1 365 nm, Asahi 370 nm short pass filter source in the NPS resin,
    with the same settings as the HR3.3u and HR3.3 plots above for direct comparison.
    """)
    return


@app.cell(hide_code=True)
def _(
    Irradiance,
    NormalizedDose,
    data,
    dose_cases,
    extended_sources,
    resins,
    wavelength_array_params,
):
    os1_key = "OS1_365nm_Asahi_370nm_short_pass_filter_grayscale_2026-05-12"
    os1_norm_dose = NormalizedDose(
        irradiance=Irradiance(
            source=data.sources[os1_key],
            resin=resins["NPS"],
            wavelength_array_params=wavelength_array_params,
        ),
        z_array_params=dose_cases["HR3.3u_365nm_Asahi_370nm_short_pass_filter_2026-05-12"][1],
    )

    os1_dose_fig, _ = os1_norm_dose.plot(
        title=os1_norm_dose.irradiance.resin.name + "\n" + extended_sources[os1_key][0]
    )
    os1_dose_fig
    return


if __name__ == "__main__":
    app.run()
