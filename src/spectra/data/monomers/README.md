# Loading your own monomer data

To load a monomer from an arbitrary JSON file in a notebook or script:

```python
import spectra.data as data

data.load_monomer("/path/to/my_monomer.json")

print(data.monomers.keys())   # bundled + newly loaded entries
```

The JSON file must contain these fields:

    {
      "Name": "PEGDA",
      "Long name": "poly ethylene glycol diacrylate",
      "Density g/L": 1110
    }

The monomer is registered in `data.monomers` under the value of `"Name"`. Loaded entries are in-memory only and do not persist across sessions.


# Adding a new monomer to the package

To permanently add a new monomer to the bundled package data:

1. Create a JSON file in `spectra/data/monomers` named `<abbreviation>.json` with contents like the following, with values appropriate for the new monomer:

       {
         "Name": "PEGDA",
         "Long name": "poly ethylene glycol diacrylate",
         "Density g/L": 1110
       }

2. Add a new entry to the `_monomer_abbreviations` dict in `data/__init__.py` for the 3-letter abbreviation of the monomer, where the key is the value of `"Name"` in the JSON file and the value is the 3-letter abbreviation. For example, the entry for the data above is:

       "PEGDA": "PEG",
