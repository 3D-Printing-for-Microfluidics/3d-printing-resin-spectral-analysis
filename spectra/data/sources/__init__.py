from pathlib import Path

from spectra.sourcespectrum import SourceSpectrum

sources = {}

this_dir = Path(__file__).parent

directories = sorted(
    [d for d in this_dir.iterdir() if d.is_dir() and d.name[0] not in [".", "_"]]
)

for d in directories:
    sources[d.name] = SourceSpectrum(d)
