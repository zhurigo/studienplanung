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

from planner.data_loader import load_all
from planner.models import Elective, StudentPlan
from planner.rules import check_plan, show_plan_check
from planner.rules import (
    elective_line,
    find_specialisation,
    name_width,
    progress_bar,
    roadmap_total,
    show_roadmap,
)


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
        self.assertIn("Press Enter to return",
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


class ElectiveLineTests(unittest.TestCase):
    """US9: the one wording for missing and extra elective ECTS."""

    def test_zero_ects_is_twelve_missing(self):
        self.assertEqual(
            elective_line(0),
            "Electives: 0/12 ECTS — 12 ECTS missing.",
        )

    def test_nine_ects_is_three_missing(self):
        self.assertEqual(
            elective_line(9),
            "Electives: 9/12 ECTS — 3 ECTS missing.",
        )

    def test_exactly_twelve_returns_none(self):
        self.assertIsNone(elective_line(12))

    def test_fifteen_ects_is_three_over_the_limit(self):
        self.assertEqual(
            elective_line(15),
            "Electives: 15/12 ECTS — 3 ECTS over the limit.",
        )


class FindSpecialisationTests(unittest.TestCase):
    """US9: the lookup shared by the total and the roadmap screen."""

    def setUp(self):
        self.specialisations = [
            SimpleNamespace(id="DT", name="Digital Trust"),
            SimpleNamespace(id="BADS", name="Business Analytics"),
        ]

    def test_finds_the_chosen_specialisation(self):
        plan = make_plan(specialisation_id="DT")

        found = find_specialisation(plan, self.specialisations)

        self.assertEqual(found.name, "Digital Trust")

    def test_none_when_nothing_is_chosen(self):
        plan = make_plan(specialisation_id=None)

        found = find_specialisation(plan, self.specialisations)

        self.assertIsNone(found)

    def test_none_when_the_id_is_unknown(self):
        plan = make_plan(specialisation_id="XX")

        found = find_specialisation(plan, self.specialisations)

        self.assertIsNone(found)


class RoadmapTotalTests(unittest.TestCase):
    """US9: core modules + specialisation + electives, on the real data."""

    @classmethod
    def setUpClass(cls):
        cls.groups, cls.modules, cls.specialisations, cls.electives = (
            load_all()
        )
        cls.by_id = {}
        for elective in cls.electives:
            cls.by_id[elective.id] = elective

    def test_no_specialisation_no_electives_is_132(self):
        plan = make_plan(specialisation_id=None)

        total = roadmap_total(
            plan, self.modules, self.specialisations
        )

        self.assertEqual(total, 132)

    def test_specialisation_and_twelve_ects_is_180(self):
        plan = make_plan(electives=[
            self.by_id["TECH-050721S1"],
            self.by_id["BUS-061033S"],
        ])

        total = roadmap_total(
            plan, self.modules, self.specialisations
        )

        self.assertEqual(total, 180)

    def test_no_specialisation_and_nine_ects_is_141(self):
        plan = make_plan(specialisation_id=None, electives=[
            self.by_id["LANG-DE-A1"],
            self.by_id["LANG-IT-A1"],
            self.by_id["LANG-ES-A1"],
        ])

        total = roadmap_total(
            plan, self.modules, self.specialisations
        )

        self.assertEqual(total, 141)

    def test_unknown_specialisation_does_not_add_36(self):
        plan = make_plan(specialisation_id="XX", electives=[
            self.by_id["TECH-050721S1"],
            self.by_id["BUS-061033S"],
        ])

        total = roadmap_total(
            plan, self.modules, self.specialisations
        )

        self.assertEqual(total, 144)


class ProgressBarTests(unittest.TestCase):
    """US9: twenty characters, rounded down and clamped."""

    def test_zero_is_all_dashes(self):
        bar = progress_bar(0)

        self.assertEqual(bar, "[--------------------]")
        self.assertEqual(len(bar), 22)

    def test_177_leaves_one_dash(self):
        bar = progress_bar(177)

        self.assertEqual(bar, "[###################-]")
        self.assertEqual(bar.count("#"), 19)
        self.assertEqual(bar.count("-"), 1)
        self.assertEqual(len(bar), 22)

    def test_180_is_full(self):
        bar = progress_bar(180)

        self.assertEqual(bar, "[####################]")
        self.assertEqual(bar.count("#"), 20)
        self.assertEqual(len(bar), 22)

    def test_over_180_stays_full(self):
        bar = progress_bar(190)

        self.assertEqual(bar.count("#"), 20)
        self.assertEqual(bar.count("-"), 0)
        self.assertEqual(len(bar), 22)


class NameWidthTests(unittest.TestCase):
    """US9: the name column fits the longest line on the screen."""

    @classmethod
    def setUpClass(cls):
        cls.groups, cls.modules, cls.specialisations, cls.electives = (
            load_all()
        )
        cls.module_names = []
        for module in cls.modules:
            cls.module_names.append(module.name)

    def test_empty_list_uses_the_minimum(self):
        self.assertEqual(name_width([]), 31)

    def test_short_name_uses_the_minimum(self):
        self.assertEqual(name_width(["Statistics 1"]), 31)

    def test_all_module_names_fit_the_longest(self):
        self.assertEqual(name_width(self.module_names), 44)

    def test_specialisation_label_widens_the_column(self):
        names = self.module_names + [
            "Business Analytics and Data Science modules",
        ]

        self.assertEqual(name_width(names), 46)


class ShowRoadmapTests(unittest.TestCase):
    """US9: the printed roadmap follows the plan."""

    @classmethod
    def setUpClass(cls):
        cls.groups, cls.modules, cls.specialisations, cls.electives = (
            load_all()
        )
        cls.by_id = {}
        for elective in cls.electives:
            cls.by_id[elective.id] = elective
        cls.nine = [
            cls.by_id["LANG-DE-A1"],
            cls.by_id["LANG-IT-A1"],
            cls.by_id["LANG-ES-A1"],
        ]
        cls.twelve = [
            cls.by_id["TECH-050721S1"],
            cls.by_id["BUS-061033S"],
        ]

    def run_roadmap(self, plan):
        """Run the screen with a mocked Enter and captured stdout."""
        with patch("builtins.input", return_value="") as mocked:
            with redirect_stdout(io.StringIO()) as output:
                show_roadmap(
                    plan, self.modules, self.groups,
                    self.specialisations,
                )
        return output.getvalue(), mocked

    def test_nine_ects_shows_177_and_the_missing_line(self):
        plan = make_plan(electives=self.nine)

        output, mocked = self.run_roadmap(plan)

        self.assertIn("177/180 ECTS (98%)", output)
        self.assertIn("[###################-]", output)
        self.assertIn(
            "  Electives: 9/12 ECTS — 3 ECTS missing.", output
        )
        self.assertEqual(mocked.call_count, 1)

    def test_no_specialisation_still_renders(self):
        plan = make_plan(specialisation_id=None, electives=self.nine)

        output, mocked = self.run_roadmap(plan)

        self.assertIn("Specialisation — not chosen yet", output)
        self.assertIn("141/180 ECTS (78%)", output)
        self.assertEqual(mocked.call_count, 1)

    def test_twelve_ects_prints_no_elective_line(self):
        plan = make_plan(electives=self.twelve)

        output, mocked = self.run_roadmap(plan)

        self.assertNotIn("missing", output)
        self.assertNotIn("over the limit", output)
        self.assertIn("180/180 ECTS (100%)", output)

    def test_roadmap_follows_a_change(self):
        plan = make_plan(electives=self.nine[:])

        first, first_mocked = self.run_roadmap(plan)
        plan.add_elective(self.by_id["LANG-ZH-A1"])
        second, second_mocked = self.run_roadmap(plan)

        self.assertIn("177/180 ECTS (98%)", first)
        self.assertIn("180/180 ECTS (100%)", second)
        self.assertNotEqual(first, second)
        self.assertEqual(first_mocked.call_count, 1)
        self.assertEqual(second_mocked.call_count, 1)


if __name__ == "__main__":
    unittest.main()
