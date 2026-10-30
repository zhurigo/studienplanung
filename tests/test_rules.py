"""
Tests for the plan checks.

Owner: Hugo (Check and save)
Run with:  python -m unittest discover tests
"""

import io
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from planner.models import Elective, StudentPlan
from planner.rules import check_plan, show_plan_check


def make_elective(elective_id: str, ects: int,
                  name: str | None = None) -> Elective:
    """A catalogue elective with the fields the checks read."""
    return Elective(elective_id, name or elective_id, "Languages",
                    ects, "HS/FS", [])


def make_plan(
    specialisation_id: str | None = "DT",
    electives: list[Elective] | None = None,
) -> StudentPlan:
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

        self.assertEqual(problems, ["No specialisation chosen."])

    def test_too_few_ects(self):
        plan = make_plan(electives=[self.german, self.french, self.spanish])

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(
            problems,
            ["Electives: 9/12 ECTS — 3 ECTS missing."],
        )

    def test_too_many_ects(self):
        plan = make_plan(
            electives=[self.tech, self.business, self.german]
        )

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(
            problems,
            ["Electives: 15/12 ECTS — 3 ECTS over the limit."],
        )

    def test_unknown_elective(self):
        ghost = make_elective("LANG-XX", 0)
        plan = make_plan(electives=[self.tech, self.business, ghost])

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(problems, ["Unknown elective id: LANG-XX"])

    def test_duplicate_elective_uses_its_name(self):
        cloud = make_elective("TECH-01", 6, "Cloud Computing")
        plan = make_plan(electives=[cloud, cloud])

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(
            problems,
            ["Elective listed twice: Cloud Computing"],
        )

    def test_unknown_specialisation(self):
        plan = make_plan(specialisation_id="XX",
                         electives=[self.tech, self.business])

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(problems, ["Unknown specialisation id: XX"])

    def test_empty_plan_reports_both_problems(self):
        plan = make_plan(specialisation_id=None)

        problems = check_plan(plan, self.specialisations, self.catalogue)

        self.assertEqual(problems, [
            "No specialisation chosen.",
            "Electives: 0/12 ECTS — 12 ECTS missing.",
        ])


class ShowPlanCheckTests(unittest.TestCase):
    """US7 screen: the header, the problems and the pause prompt."""

    def setUp(self):
        self.specialisations = [SimpleNamespace(id="DT")]
        self.german = make_elective("LANG-DE-A1", 3)
        self.spanish = make_elective("LANG-ES-A1", 3)
        self.tech = make_elective("TECH-01", 6)
        self.business = make_elective("BIZ-01", 6)
        self.catalogue = [
            self.german, self.spanish, self.tech, self.business,
        ]

    def run_check(self, plan):
        """Run the screen with a mocked Enter and captured stdout."""
        with patch("builtins.input", return_value="") as mocked:
            with redirect_stdout(io.StringIO()) as output:
                show_plan_check(
                    plan, self.specialisations, self.catalogue
                )
        return output.getvalue(), mocked

    def test_complete_plan_confirms_180(self):
        plan = make_plan(electives=[self.tech, self.business])

        output, mocked = self.run_check(plan)

        self.assertIn("Your plan is complete (180/180 ECTS).", output)
        self.assertEqual(mocked.call_count, 1)
        self.assertIn("Press Enter to return.",
                      mocked.call_args.args[0])

    def test_one_problem_uses_singular_warning(self):
        plan = make_plan(specialisation_id=None,
                         electives=[self.tech, self.business])

        output, mocked = self.run_check(plan)

        self.assertIn("No specialisation chosen.", output)
        self.assertIn("1 warning. Press Enter to return.",
                      mocked.call_args.args[0])

    def test_two_problems_use_plural_warnings(self):
        plan = make_plan(specialisation_id=None)

        output, mocked = self.run_check(plan)

        self.assertIn("No specialisation chosen.", output)
        self.assertIn("Electives: 0/12 ECTS — 12 ECTS missing.", output)
        self.assertIn("2 warnings. Press Enter to return.",
                      mocked.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
