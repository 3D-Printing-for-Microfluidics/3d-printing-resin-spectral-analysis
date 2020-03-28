import json
from pathlib import Path
from dataclasses import dataclass

import numpy as np

import spectra.data as data
from spectra.absorberspectrum import AbsorberSpectrum
from spectra.monomer import Monomer


@dataclass
class ResinConstituentAbsorber:
    """Container with 2 pieces of information:
    1. Absorber material
    2. Concentration w/w (percent) in resin
    
    Examples 
    --------
    1% Irgacure 819:
        `irgacure819 = ResinConstituentAbsorber(
            data.photoinitiators['irgacure819_in_PEGDA_2020-01-20'],
            1.0
        )`
    0.38% avobenzone:
        `avobenzone = ResinConstituentAbsorber(
            data.absorbers['avobenzone_in_PEGDA_2020-01-20'],
            0.38
        )`
    """

    material: AbsorberSpectrum
    concentration_ww_percent: (int, float)

    def __post_init__(self):

        # Enforce data types
        assert isinstance(self.material, AbsorberSpectrum)
        assert isinstance(self.concentration_ww_percent, (int, float))


@dataclass
class ResinConstituentMonomer:
    """Container with 2 pieces of information:
    1. Monomer material
    2. Concentration as percent of all MONOMERS in resin (not percent of total resin)
    
    Example: monomers for 60-40 PEGDA-HDDA resin:
        `pegda = ResinConstituentMonomer(data.monomers['PEGDA'], 60)`
        `hdda = ResinConstituentMonomer(data.monomers['HDDA'], 40)`
    """

    material: Monomer
    concentration_percent_monomer: (int, float)

    def __post_init__(self):

        # Enforce data types
        assert isinstance(self.material, Monomer)
        assert isinstance(self.concentration_percent_monomer, (int, float))


class Resin:
    """Combine materials into a resin and calculate its absorption coefficient
    as a function of wavelength.

    Note: self.absorption_coeff is in units of inverse cm
    
    Parameters
    ----------
    monomers - ResinConstituentMonomer of list of ResinConstituentMonomer
    photoinitiators - ResinConstituentAbsorber or list of ResinConstituentAbsorber
    absorbers - ResinConstituentAbsorber or list of ResinConstituentAbsorber
    
    Examples
    -------
    PEGDA with 0.38% avobenzone and 1% Irgacure 819:
        pegda = ResinConstituentMonomer(data.monomers['PEGDA'], 100)
        avobenzone = ResinConstituentAbsorber(
            data.absorbers['avobenzone_in_PEGDA_2020-01-20'],
            0.38
        )
        irgacure819 = ResinConstituentAbsorber(
            data.photoinitiators['irgacure819_in_PEGDA_2020-01-20'],
            1.0
        )
        resin = Resin(monomers=pegda, absorbers=avobenzone, photoinitiators=irgacure819)
    60-40 PEGDA-HDDA with 2% NPS, 1% avobenzone and 1% Irgacure 819:
        pegda = ResinConstituentMonomer(data.monomers['PEGDA'], 60)
        hdda = ResinConstituentMonomer(data.monomers['HDDA'], 40)
        nps = ResinConstituentAbsorber(
            data.absorbers['nps_in_PEGDA_2017-04-13'],
            2.0
        )
        avobenzone = ResinConstituentAbsorber(
            data.absorbers['avobenzone_in_PEGDA_2020-01-20'],
            1.0
        )
        irgacure819 = ResinConstituentAbsorber(
            data.photoinitiators['irgacure819_in_PEGDA_2020-01-20'],
            1.0
        )
        resin = Resin(monomers=[pegda, hdda], absorbers=[nps, avobenzone], photoinitiators=irgacure819)
    """

    def __init__(self, *, monomers, absorbers=[], photoinitiators=[]):

        # Handle inputs. Treat photoinitiators as absorbers for purpose of calculating absorption coefficient
        self.monomers = self.create_list(monomers, ResinConstituentMonomer)
        self.check_monomers(self.monomers)
        self.absorbers = self.create_list(absorbers, ResinConstituentAbsorber)
        self.photoinitiators = self.create_list(photoinitiators, ResinConstituentAbsorber)
        self._absorbers = self.absorbers + self.photoinitiators
        if not self._absorbers:
            raise ValueError("There must be at least one absorber or one photoinitiator.")

        self.build_name()

        # Calculate molar concentration for absorbers, photoinitiators in list of absorbers
        self._density = self.calc_density(self.monomers)
        self._molar_concentrations = []
        for a in self._absorbers:
            self._molar_concentrations.append(
                (a.concentration_ww_percent / 100)
                * self._density
                / a.material.molar_mass_g_per_mole
            )

        # Set wavelength to be the same as for the first absorber material
        self.wavelength = self._absorbers[0].material.wavelength.copy()

        # Calculate absorption coefficient as a function of wavelength
        self.absorption_coeff = np.zeros(
            self._absorbers[0].material.molar_absorptivity.shape
        )
        for a in self._absorbers:
            self.absorption_coeff += (
                np.log(10)
                * a.material.calc_molar_absorptivity(self.wavelength)
                * (a.concentration_ww_percent / 100)
                * (self._density / a.material.molar_mass_g_per_mole)
            )

    def build_name(self):

        material_separator = "_"
        material_type_separator = "__"
        number_separator = "-"

        def number_maker(number):
            """Return number as a string without trailing 0's or decimal point

            Examples
            --------
            100 -> 100.00 -> 100
            0.38 -> 0.38 -> 0.38
            55.2 -> 55.20 -> 55.2
            2.0 -> 2.00 -> 2
            """
            temp = f"{number:.2f}"
            # Remove trailing zeros
            while temp.endswith("0"):
                temp = temp[:-1]
            # Remove trailing decimal
            if temp.endswith("."):
                temp = temp[:-1]
            return temp

        temp_name = ""

        for i, m in enumerate(self.monomers):
            if i:
                temp_name += material_separator
            temp_name += data.material_abbreviations[m.material.name]
            temp_name += number_separator + number_maker(m.concentration_percent_monomer)

        temp_name += material_type_separator

        for i, a in enumerate(self.absorbers):
            if i:
                temp_name += material_separator
            temp_name += data.material_abbreviations[a.material.name]
            temp_name += number_separator + number_maker(a.concentration_ww_percent)

        temp_name += material_type_separator

        for i, p in enumerate(self.photoinitiators):
            if i:
                temp_name += material_separator
            temp_name += data.material_abbreviations[p.material.name]
            temp_name += number_separator + number_maker(p.concentration_ww_percent)

        self.name = temp_name

    def calc_absorption_coef_inv_cm(self, wavelength):
        """Given wavelength, interpolate corresponding absorption coefficient value.
        Units: cm^(-1)

        See numpy.interp documentation for interpolation details.

        Parameters
        ----------
        wavelength - array_like (can be single value or 1D list/numpy.array of values)

        Returns
        -------
        single value or 1D numpy array corresponding to shape of wavelength
        """
        return np.interp(
            wavelength, self.wavelength, self.absorption_coeff, left=0.0, right=0.0
        )

    @staticmethod
    def create_list(item, desired_type):

        if isinstance(item, desired_type):
            return [item]

        if isinstance(item, list):
            for i in item:
                assert isinstance(i, desired_type)
            return item

        raise TypeError(f"Wrong type. Must be {desired_type} or list of {desired_type}.")

    @staticmethod
    def check_monomers(monomers):
        """Make sure percentages add to 100
        """
        total = 0
        for m in monomers:
            total += m.concentration_percent_monomer
        if total != 100:
            raise ValueError("Sum of monomer concentrations must equal 100 (percent)")

    @staticmethod
    def calc_density(monomers):
        weighted_average = 0
        for m in monomers:
            weighted_average += m.material.density * (
                m.concentration_percent_monomer / 100.0
            )
        return weighted_average
