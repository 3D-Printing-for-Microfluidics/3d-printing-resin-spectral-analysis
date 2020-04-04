To add a monomer, create a json file in `data\monomers` named `XXX.json` with contents like the following, except with values appropriate for the new monomer:

    {
      "Name": "PEGDA",
      "Long name": "poly ethylene glycol diacrylate",
      "Density g/L": 1110
    }
    
Also, add a new entry to the `_monomer_abbreviations` dict in `data/__init__.py` for the 3 letter abbreviation of the monomer where the key is the value of `Name` in the monomer's json file, and its value is the 3 letter abbreviation. For example, the entry for the data above is

    "PEGDA": "PEG",