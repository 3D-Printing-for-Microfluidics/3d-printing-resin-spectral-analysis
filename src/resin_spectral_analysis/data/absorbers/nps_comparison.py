import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import json

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    import resin_spectral_analysis.data as data

    return data, json, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # NPS in PEGDA: comparing the two measured spectra

    The package has two NPS (2-nitrophenyl phenyl sulfide) absorption measurements in PEGDA:

    - **`nps_in_PEGDA_2017-04-13`**: the original measurement, used in earlier work.
    - **`nps_in_PEGDA_2024-09-02`**: a new measurement by Dallin Miner.

    Both were processed with `process-absorber-spectrum`, which computes
    $A(\lambda) = -\log_{10}(I_\text{sample}/I_\text{solvent})$ over 300–540 nm, shifts it so
    the mean of the last 10 points (about 532–540 nm) is zero, and converts to molar
    absorptivity with $\varepsilon = A / (c\,L)$. The 2024 dark file is kept in `raw_data/`
    but isn't used.

    A second 2024 sample (`nps_in_PEGDA_2024-2` in Dallin's data, measured 2024-09-03) was
    left out of the package. Its sample spectrum was brighter than its solvent reference
    wherever NPS doesn't absorb, and it was saturated in the 532–540 nm baseline window, so
    its absorbance can't be trusted.
    """)
    return


@app.cell
def _(data, json, mo, np):
    absorbers_dir = mo.notebook_dir()
    nps_keys = [
        "nps_in_PEGDA_2017-04-13",
        "nps_in_PEGDA_2024-09-02",
    ]
    labels = {
        "nps_in_PEGDA_2017-04-13": "2017",
        "nps_in_PEGDA_2024-09-02": "2024",
    }
    # Colorblind-validated categorical palette; line styles give a second cue
    colors = {
        "nps_in_PEGDA_2017-04-13": "#2a78d6",
        "nps_in_PEGDA_2024-09-02": "#eb6834",
    }
    linestyles = {
        "nps_in_PEGDA_2017-04-13": "-",
        "nps_in_PEGDA_2024-09-02": "--",
    }
    SATURATION_COUNTS = 60000  # QE65PRO 16-bit detector saturates near 63,600 counts


    def read_raw(path):
        if path.suffix == ".txt":
            return np.loadtxt(path, skiprows=14)
        raw = np.genfromtxt(path, delimiter=",", comments="#", invalid_raise=False)
        return raw[~np.isnan(raw).any(axis=1)]


    configs = {}
    raw_spectra = {}
    for key in nps_keys:
        cfg = json.loads((absorbers_dir / key / "spectrum_config.json").read_text())
        configs[key] = cfg
        raw_dir = absorbers_dir / key / "raw_data"
        raw_spectra[key] = {
            "solvent": read_raw(raw_dir / cfg["Solvent absorption measurement file"]),
            "sample": read_raw(raw_dir / cfg["Solvent + absorber absorption measurement file"]),
        }
    absorbers = {key: data.absorbers[key] for key in nps_keys}
    return (
        SATURATION_COUNTS,
        absorbers,
        colors,
        configs,
        labels,
        linestyles,
        nps_keys,
        raw_spectra,
    )


@app.cell
def _(absorbers, configs, labels, mo, np, nps_keys):
    _rows = []
    for _key in nps_keys:
        _cfg = configs[_key]
        _a = absorbers[_key]
        _i = np.argmax(_a.molar_absorptivity)
        _rows.append(
            {
                "Measurement": labels[_key],
                "Date": _cfg["Measurement Date"],
                "Conc. (w/w %)": _cfg["Concentration w/w percent"],
                "Film (µm)": _cfg["Film thickness microns"],
                "Conc. × film (%·µm)": round(
                    _cfg["Concentration w/w percent"] * _cfg["Film thickness microns"], 1
                ),
                "Peak A": round(float(_a.absorbance.max()), 3),
                "Peak λ (nm)": round(float(_a.wavelength[_i]), 1),
                "Peak ε (L/mol·cm)": round(float(_a.molar_absorptivity[_i])),
            }
        )
    mo.vstack([mo.md("## Measurement parameters"), mo.ui.table(_rows, selection=None)])
    return


@app.cell(expand_output=True)
def _(absorbers, colors, labels, linestyles, mo, np, nps_keys, plt):
    _ref = absorbers["nps_in_PEGDA_2017-04-13"]
    _fig, _axes = plt.subplots(3, 1, figsize=(8, 10), sharex=True, layout="constrained")
    for _key in nps_keys:
        _a = absorbers[_key]
        _style = dict(color=colors[_key], ls=linestyles[_key], lw=2, label=labels[_key])
        _axes[0].plot(_a.wavelength_absorbance, _a.absorbance, **_style)
        _axes[1].plot(_a.wavelength, _a.molar_absorptivity, **_style)
        if _key != "nps_in_PEGDA_2017-04-13":
            _ratio = _a.calc_molar_absorptivity(_ref.wavelength) / _ref.molar_absorptivity
            # Ratio is meaningless where the 2017 absorption is near zero
            _ratio[_ref.molar_absorptivity < 0.05 * _ref.molar_absorptivity.max()] = np.nan
            _axes[2].plot(_ref.wavelength, _ratio, **_style)
    _axes[2].axhline(1.0, color="0.5", lw=1)
    _axes[2].set_ylim(0, 1.5)
    _axes[2].set_xlim(300, 540)
    _axes[0].set_ylabel("Absorbance")
    _axes[1].set_ylabel("Molar absorptivity (L/mol·cm)")
    _axes[2].set_ylabel("ε / ε(2017)")
    _axes[2].set_xlabel("Wavelength (nm)")
    _axes[0].set_title("Measured absorbance")
    _axes[1].set_title("Molar absorptivity")
    _axes[2].set_title("Ratio to the 2017 spectrum (shown only where ε(2017) > 5% of its peak)")
    for _ax in _axes:
        _ax.axvspan(300, 330, color="0.85", zorder=0)
        _ax.axvspan(434, 440, color="#f6e7c8", zorder=0)
        for _wl in (365, 385, 405):
            _ax.axvline(_wl, color="0.7", lw=0.8, ls=":", zorder=0)
        _ax.grid(alpha=0.3)
        _ax.legend(loc="upper right", frameon=False)
    _axes[0].text(302, _axes[0].get_ylim()[1] * 0.92, "low signal", fontsize=9, color="0.35")
    _axes[0].text(441, _axes[0].get_ylim()[1] * 0.92, "saturated", fontsize=9, color="0.35")
    for _wl in (365, 385, 405):
        _axes[0].text(_wl + 1, 0.02, f"{_wl}", fontsize=8, color="0.45")
    mo.vstack(
        [
            mo.md(
                "## Spectra\n\nGray band: fewer than about 1000 counts, so the result is noisy. "
                "Tan band: the spectrometer saturates at the 436 nm lamp line (434–439 nm). "
                "Dotted lines: common LED wavelengths (365, 385, 405 nm)."
            ),
            _fig,
        ]
    )
    return


@app.cell
def _(absorbers, labels, mo, nps_keys):
    _rows = []
    for _wl in (365, 385, 405):
        _row = {"λ (nm)": _wl}
        for _key in nps_keys:
            _row[f"ε {labels[_key]}"] = round(float(absorbers[_key].calc_molar_absorptivity(_wl)))
        _ref_eps = float(absorbers["nps_in_PEGDA_2017-04-13"].calc_molar_absorptivity(_wl))
        for _key in nps_keys[1:]:
            _row[f"{labels[_key]} / 2017"] = round(
                float(absorbers[_key].calc_molar_absorptivity(_wl)) / _ref_eps, 3
            )
        _rows.append(_row)
    eps_at_leds = _rows
    mo.vstack(
        [
            mo.md("### Molar absorptivity at LED wavelengths (L/mol·cm)"),
            mo.ui.table(_rows, selection=None),
        ]
    )
    return


@app.cell
def _(SATURATION_COUNTS, colors, labels, mo, nps_keys, plt, raw_spectra):
    _fig, _axes = plt.subplots(
        1, len(nps_keys), figsize=(9, 3.6), sharey=True, layout="constrained"
    )
    for _ax, _key in zip(_axes, nps_keys):
        for _which, _c, _ls in (("solvent", "0.45", "-"), ("sample", colors[_key], "-")):
            _d = raw_spectra[_key][_which]
            _ax.plot(_d[:, 0], _d[:, 1], color=_c, ls=_ls, lw=1.5, label=_which)
        _ax.axhline(SATURATION_COUNTS, color="#c0392b", lw=1, ls="--")
        _ax.axvspan(532, 540, color="0.88", zorder=0)
        _ax.set_xlim(300, 545)
        _ax.set_title(labels[_key])
        _ax.set_xlabel("Wavelength (nm)")
        _ax.grid(alpha=0.3)
        _ax.legend(loc="center left", frameon=False, fontsize=9)
    _axes[0].set_ylabel("Spectrometer counts")
    _axes[0].text(302, SATURATION_COUNTS * 0.94, "≈ saturation", fontsize=8, color="#c0392b")
    mo.vstack(
        [
            mo.md(
                "## Raw spectrometer data\n\nRed dashed line: saturation. "
                "Gray band: the 532–540 nm window the script uses to set the zero baseline."
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What explains the differences

    **1. The 2024 spectrum is about 14–18% below the 2017 spectrum at the 365–405 nm LED
    wavelengths.** Across the main band the ratio drifts only slowly, from about 0.92 at
    340 nm to 0.78 at 430 nm. The peak shape and position are almost the same; the 2024
    peak is only about 3 nm bluer. So the difference is mostly one of **scale**, not a
    different spectrum. The likely causes are errors in the numbers used to convert
    absorbance to $\varepsilon = A/(c\,L)$:

    - **Film thickness (the most likely cause).** The 2024 film thickness (88 µm) was
      measured with a **Keyence confocal distance sensor**. That should be much more
      accurate than the 2017 method, which may have been to estimate the 63.5 µm thickness
      from microscope focus. If the real 2017 film was thicker than 63.5 µm, the 2017
      $\varepsilon$ would come out too high. A 2017 film of about 74–77 µm would account
      for the whole difference at 365–405 nm.
    - **Concentration.** Weighing error in making up the 2017 (0.5%) or 2024 (0.396%) sample.
    - **Sample age or purity.** A different NPS lot, or degradation of the NPS stock.

    Absorbance alone shows the same thing. From the conc. × film values in the table, the
    2024 sample should have about 10% *more* absorbance than the 2017 sample, but its
    measured peak is about 7% *lower*.

    **2. Both sets of raw data are clean.** In each, solvent and sample were measured at the
    same integration time, and the sample counts closely match the solvent counts wherever
    NPS doesn't absorb (above about 450 nm). So the baseline is well defined. Their only
    saturated region is a narrow band (434–439 nm) at the lamp's 436 nm line, where the
    solvent reference saturates (and, in 2024, the sample too). The dip in the 2024
    absorbance there is an artifact of that saturation.

    **3. Below about 330 nm both spectra are noisy.** Very little light reaches the detector
    there (under about 1000 counts), so the ratio scatters. These wavelengths matter little
    for the 365–405 nm LEDs used for printing.

    ### Which spectrum to use

    - Both sets of raw data are sound. The difference between them is mainly in the overall
      scale of $\varepsilon$, not in the shape of the spectrum.
    - Because the 2024 film thickness was measured more accurately, **prefer
      `nps_in_PEGDA_2024-09-02`** for new work. The roughly 15% difference in $\varepsilon$
      changes the predicted penetration depth $h_a$ by about the same amount, so keep this in
      mind when comparing with earlier results that used the 2017 spectrum.
    """)
    return


if __name__ == "__main__":
    app.run()
