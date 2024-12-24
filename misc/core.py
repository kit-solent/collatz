"""
Program to find a counterexample to the Colatz Conjecture using bruteforcing methods.

See https://en.wikipedia.org/wiki/Collatz_conjecture for information on the conjecture.

This program works around the central database `database.json`. Ranges of numbers are checked out to
worker processes who scan the ranges for counterexamples. When all numbers have been scanned the
process confirms the range which is added back to the database. Ranges are generated from a given size
and are just the next n avalable numbers where n is the requested size. If worker tasks ever fail to
confirm their range then a gap will appear in the range of scanned numbers. This gap will just be
added to the next requested task. Tasks are assumed to be honest about their results.
"""
import os,json,pathlib

class ColatzDatabase():
    """
    A class to handle interactions with the central database.
    Manages the assignment and reception of ranges.
    """
    DEFAULT_DATABASE:dict = {
        # The number below which all other numbers have been scanned and confirmed to be compliant with the conjecture.
        "number":1,
        # A list of ranges of numbers that have been checked out to workers and are yet to return.
        "pending ranges": [],
        # A list of ranges that have not been scanned.
        "failed ranges": [],
        # A list of ranges of numbers that have been confirmed to be compliant with the conjecture.
        "confirmed ranges": []
    }

    def __init__(self, database:pathlib.Path|str = None):
        self.data = None
        self.database = None
        if database:
            self.load_database(database)

    @staticmethod
    def pathify(path:pathlib.Path|str):
        """
        Attemps to convert `path` to a `pathlib.Path` object.
        Also asserts that the path exists and is a file.
        """
        try:
            path = pathlib.Path(path)
        except TypeError:
            raise TypeError("Failed to converd `path` to type `pathlib.Path`.")

        if not path.is_file():
            raise ValueError(f"Path: {path} must be a regular or symlink file.")

        if not path.exists():
            raise FileNotFoundError(f"Failed to find path: {path}")

        return path

    def load_database(self, database:pathlib.Path|str):
        self.database = self.pathify(database)

        data = json.load(str(self.database))
        if not self.validate_data(data):
            raise ValueError("Invalid Database")

        self.data = data

    def validate_data(self, data:dict = None) -> dict:
        """
        Confirms that `data` (or `self.data` if `data` is not provided) is a valid database.
        This will return `False` if any of the checks fail and will return `True` otherwise.
        """
        if not data:
            data = self.data

        try:
            assert "number" in data.keys(), "No 'number' key found."
            assert "pending ranges" in data.keys(), "No 'pending ranges' key found."
            assert "failed ranges" in data.keys(), "No 'failed ranges' key found."
            assert "confirmed ranges" in data.keys(), "No 'confirmed ranges' key found."
            assert "needs confirmation" in data.keys(), "No 'needs confirmation' key found."
            assert "steps" in data.keys(), "No 'steps' key found."
            assert type(data["number"]) is int, "'number' must be an integer."
            assert data["number"] > 0, "'number' must be strictly greater than 0."
        except AssertionError:
            return False

    def assign_range(self, size:int, force_size = True, force_consecutive = True):
        """
        Checks a range of numbers out of the central data file of length `size `for scanning.
        `size` is the requested size of the range.
        If `force_consecutive` is `True` then one continuous range will be assigned.
        If `False` the range could be made up of disjointed parts at the discression
        of this method.
        If `force_size` is `True` then the range will be of exactly `size` length.
        If `False` then `size` will be considered a maximum.
        """
        # TODO

    # TODO...