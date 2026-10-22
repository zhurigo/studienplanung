"""
Tests for saving and loading the plan.

Owner: Hugo (Check and save)
Run with:  python -m unittest discover tests
"""

import json
import tempfile
import unittest
from pathlib import Path

from planner.models import Elective, StudentPlan
from planner.storage import StorageError, load_plan, save_plan


class StorageTests(unittest.TestCase):
    """US8: the plan survives a save and a load, and bad files fail cleanly."""

    def setUp(self):
        # A throwaway folder per test, so the real my_plan.json is never used
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "my_plan.json"

        # Two fake electives, so these tests do not depend on data/
        self.german = Elective("LANG-DE-A1", "German Basic A1",
                               "Languages", 3, "HS/FS", [])
        self.spanish = Elective("LANG-ES-A1", "Spanish A1",
                                "Languages", 3, "HS/FS", [])
        self.catalogue = [self.german, self.spanish]

    def make_plan(self):
        """A plan with Digital Trust and two electives."""
        plan = StudentPlan()
        plan.specialisation_id = "DT"
        plan.electives = [self.german, self.spanish]
        return plan

    def write_plan_file(self, data):
        """Write raw data to the temp plan file, as a hand-edited file."""
        self.path.write_text(json.dumps(data), encoding="utf-8")

    def test_save_then_load_round_trip(self):
        save_plan(self.make_plan(), self.path)
        loaded = load_plan(self.catalogue, self.path)

        self.assertEqual(loaded.specialisation_id, "DT")
        self.assertEqual([e.id for e in loaded.electives],
                         ["LANG-DE-A1", "LANG-ES-A1"])

    def test_missing_file_returns_none(self):
        self.assertIsNone(load_plan(self.catalogue, self.path))

    def test_broken_json_raises(self):
        self.path.write_text("{oops", encoding="utf-8")

        with self.assertRaises(StorageError):
            load_plan(self.catalogue, self.path)

    def test_unknown_elective_is_kept(self):
        self.write_plan_file({
            "version": 1,
            "specialisation": "DT",
            "electives": ["LANG-XX"],
        })

        loaded = load_plan(self.catalogue, self.path)

        self.assertEqual(loaded.electives[0].id, "LANG-XX")
        self.assertEqual(loaded.electives[0].name, "LANG-XX")
        self.assertEqual(loaded.electives[0].ects, 0)

    def test_duplicates_are_kept(self):
        self.write_plan_file({
            "version": 1,
            "specialisation": "DT",
            "electives": ["LANG-DE-A1", "LANG-DE-A1"],
        })

        loaded = load_plan(self.catalogue, self.path)

        self.assertEqual(len(loaded.electives), 2)

    def test_unknown_version_raises(self):
        self.write_plan_file({
            "version": 2,
            "specialisation": "DT",
            "electives": [],
        })

        with self.assertRaises(StorageError):
            load_plan(self.catalogue, self.path)


if __name__ == "__main__":
    unittest.main()
