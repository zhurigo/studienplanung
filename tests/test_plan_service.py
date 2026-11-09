"""
Tests for the middle layer between main.py and the files.

Owner: Hugo (Check and save)
Run with:  python -m unittest discover tests
"""

import json
import tempfile
import unittest
from pathlib import Path

from planner.models import Elective, StudentPlan
from planner.plan_service import (electives_by_category, load_saved_plan,
                                  save_current_plan)


class PlanServiceTests(unittest.TestCase):
    """US5 and US8: the service loads, completes and saves the plan."""

    def setUp(self):
        # A throwaway folder per test, so the real my_plan.json is never used
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "my_plan.json"

        self.german = Elective("LANG-DE-A1", "German Basic A1",
                               "Languages", 3, "HS/FS", [])
        self.ethics = Elective("SOC-ETH", "Ethics",
                               "Society and Culture", 3, "FS", [])
        self.catalogue = [self.german, self.ethics]

    def test_no_saved_plan_returns_none(self):
        self.assertIsNone(load_saved_plan(self.catalogue, self.path))

    def test_old_plan_gets_a_semester_for_every_elective(self):
        # A file saved before semesters could be picked
        self.path.write_text(json.dumps({
            "version": 1,
            "specialisation": "DT",
            "electives": ["LANG-DE-A1", "SOC-ETH"],
        }), encoding="utf-8")

        loaded = load_saved_plan(self.catalogue, self.path)

        self.assertEqual(loaded.elective_semesters,
                         {"LANG-DE-A1": 3, "SOC-ETH": 4})

    def test_saved_semesters_are_kept(self):
        plan = StudentPlan()
        plan.add_elective(self.german, 5)

        save_current_plan(plan, self.path)
        loaded = load_saved_plan(self.catalogue, self.path)

        self.assertEqual(loaded.elective_semesters, {"LANG-DE-A1": 5})

    def test_electives_are_grouped_by_category(self):
        groups = electives_by_category(self.catalogue)

        self.assertEqual(groups["Languages"], [self.german])
        self.assertEqual(groups["Society and Culture"], [self.ethics])


if __name__ == "__main__":
    unittest.main()
