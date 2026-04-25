import numpy as np

from spectra.resin import ResinConstituentAbsorber, ResinConstituentMonomer, Resin
from spectra.sourcespectrum import SourceSpectrum
from spectra.utilities import ArrayParams


class Irradiance:
    """Callable class that calculates the irradiance over an array of 
    wavelengths for a given value of z in microns.
    
    Parameters
    ----------
    source - SourceSpectrum
        Spectrum of source
    resin - Resin
        Resin light propagates through
    wavelength_array_params - ArrayParams
        Minimum, maximum wavelength and number of points for array of wavelengths
        
        
    Example
    -------
        # Create irradiance object for particular source, resin, and wavelength parameters
        irradiance = Irradiance(
            source=source,
            resin=resin,
            wavelength_array_params=wavelength_array_parameters
        )
        # Calculate the irradiance over wavelength array
        irradiance_at_z_10_um = irradiance(10)
        # Plot irradiance
        fig, ax = plt.subplots()
        ax.plot(irradiance.wavelengths, irradiance_at_z_10_um)
    """

    def __init__(self, source, resin, wavelength_array_params):

        assert isinstance(source, SourceSpectrum)
        assert isinstance(resin, Resin)
        assert isinstance(wavelength_array_params, ArrayParams)

        self.source = source
        self.resin = resin
        self.wavelength_array_params = wavelength_array_params

        self.wavelengths = np.linspace(*self.wavelength_array_params)

        self.source_spectrum = self.source.calc_power(self.wavelengths)
        self.absorption_coeff_inv_um = self.resin.calc_absorption_coef_inv_um(
            self.wavelengths
        )

    def __call__(self, z_um):
        assert isinstance(z_um, (float, int))
        temp = self.source_spectrum * np.exp(-self.absorption_coeff_inv_um * z_um)
        return temp
