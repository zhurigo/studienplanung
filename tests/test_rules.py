"""
Tests for the plan checks.

Owner: Hugo (Check and save)
Run with:  python -m unittest discover tests
"""

import unittest
from types import SimpleNamespace

from planner.models import Elective, StudentPlan
from planner.rules import check_plan


def make_elective(elective_id, ects):
    """A catalogue elective with the fields the checks read."""
    return Elective(elective_id, elective_id, "Languages", ects, "HS/FS", [])


def make_plan(specialisation_id="DT", electives=None):
    """A plan with the given specialisation and electives."""
    plan = StudentPlan()
    plan.specialisation_id = specialisation_id
    plan.electives = electives if electives is not None else []
    return plan


class CheckPlanTests(unittest.TestCase):
    """US7: a legal plan is silent, every problem is reported."""

    def setUp(self):
        # Only the id is read, so a namespace stands in for the full class.
        # This keeps the tests working even if the class gains fields.
        self.specialisations = [
            SimpleNamespace(id="DT"),
            SimpleNamespace(id="BADS"),
        ]
        self.german = make_elective("LANG-DE-A1", 3)
        self.french = make_elective("LANG-FR-A1", 3)
        self.spanish = make_elective("LANG-ES-A1", 3)
        self.tech = make_elective("TECH-01", 6)
        self.business = make_elective("BIZ-01", 6)
        self.catalogue = [
            self.german, self.french, self.spanish,
            self.tech, self.business,
        ]

    def test_complete_plan_has_no_problems(self):
        plan = make_plan(electives=[self.tech, self.business])

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(problems, [])

    def test_missing_specialisation(self):
        plan = make_plan(specialisation_id=None,
                         electives=[self.tech, self.business])

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(len(problems), 1)
        self.assertIn("No specialisation chosen", problems[0])

    def test_too_few_ects(self):
        plan = make_plan(electives=[self.german, self.french, self.spanish])

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(len(problems), 1)
        self.assertIn("9 of 12 ECTS", problems[0])
        self.assertIn("3 ECTS missing", problems[0])

    def test_too_many_ects(self):
        plan = make_plan(
            electives=[self.tech, self.business, self.german]
        )

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(len(problems), 1)
        self.assertIn("15 of 12 ECTS", problems[0])
        self.assertIn("3 ECTS too many", problems[0])

    def test_unknown_elective(self):
        ghost = make_elective("LANG-XX", 0)
        plan = make_plan(electives=[self.tech, self.business, ghost])

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertIn("Unknown elective ID 'LANG-XX'.", problems)

    def test_duplicate_elective(self):
        plan = make_plan(electives=[self.tech, self.tech])

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(len(problems), 1)
        self.assertIn("appears 2 times", problems[0])

    def test_unknown_specialisation(self):
        plan = make_plan(specialisation_id="XX",
                         electives=[self.tech, self.business])

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(len(problems), 1)
        self.assertIn("Unknown specialisation ID 'XX'.", problems[0])

    def test_empty_plan_reports_both_problems(self):
        plan = make_plan(specialisation_id=None)

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(len(problems), 2)


if __name__ == "__main__":
    unittest.main()
