from pathlib import Path

import pytest

from spectra.absorberspectrum import AbsorberSpectrum
from spectra.sourcespectrum import SourceSpectrum
import spectra.data as data


def test_everything():
    for key in data.sources:
        assert isinstance(data.sources[key], SourceSpectrum)
    for key in data.absorbers:
        assert isinstance(data.absorbers[key], AbsorberSpectrum)
    for key in data.photoinitiators:
        assert isinstance(data.photoinitiators[key], AbsorberSpectrum)
