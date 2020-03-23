import json
from pathlib import Path


class Monomer:
    def __init__(self, json_file):

        assert isinstance(json_file, Path)
        self._json_file = json_file
        with self._json_file.open("r") as f:
            self._from_json = json.load(f)

        assert isinstance(self._from_json["Name"], str)
        assert isinstance(self._from_json["Long name"], str)
        assert isinstance(self._from_json["Density g/L"], (float, int))

        self.name = self._from_json["Name"]
        self.long_name = self._from_json["Long name"]
        self.density = self._from_json["Density g/L"]

    def __repr__(self):
        return f"Monomer({self._json_file})"

    def print(self):
        print(self.__dict__)
