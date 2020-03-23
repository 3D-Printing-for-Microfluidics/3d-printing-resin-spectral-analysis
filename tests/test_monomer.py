from pathlib import Path
import json

from spectra.monomer import Monomer


def test_monomer():

    json_file = (
        Path(__file__).resolve().parent
        / "files_for_tests"
        / "data_for_test_monomer"
        / "test_monomer.json"
    )

    m = Monomer(json_file)

    with json_file.open("r") as f:
        result = json.load(f)

    assert m.name == result["Name"]
    assert m.long_name == result["Long name"]
    assert m.density == result["Density g/L"]
    assert m.__repr__() == f"Monomer({json_file})"
