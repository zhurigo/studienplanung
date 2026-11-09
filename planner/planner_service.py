"""
The middle layer between main.py and the files.

Owner: Hugo (Check and save)
User stories:
  5. Plan electives: group the electives by category for the menu
  8. Save the plan to my_plan.json and load it next time (Steps 2, 10 and 11)

main.py calls these functions instead of data_loader and storage, so the
menu never reaches the files directly (see docs/architecture.md).
"""

from planner.data_loader import load_all
from planner.storage import PLAN_FILE, load_plan, save_plan


def load_catalogue():
    """Return the groups, modules, specialisations and electives."""
    return load_all()


def load_saved_plan(electives, path=PLAN_FILE):
    """Return the saved plan with a semester for every elective, or None."""
    plan = load_plan(electives, path)
    if plan is None:
        return None
    # Every elective needs a semester, older plans have none yet
    plan.fill_missing_semesters()
    return plan


def save_current_plan(plan, path=PLAN_FILE):
    """Write the plan to my_plan.json."""
    save_plan(plan, path)


def electives_by_category(electives):
    """Group the electives by category for the US5 menu."""
    categories = {}
    for elective in electives:
        if elective.category not in categories:
            categories[elective.category] = []
        categories[elective.category].append(elective)
    return categories
