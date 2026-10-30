"""
Saving and loading the student's plan.

Owner: Hugo (Check and save)
User story:
  8. Save the plan to my_plan.json and load it next time (Steps 2, 10 and 11)
Course criterion: file processing (writing and reading)

What goes here:
  - save: write the chosen specialisation and elective ids to my_plan.json
  - load: read my_plan.json back into a StudentPlan
  - handle a missing or damaged file with a clear message, never a crash

Save ids (like "LANG-ES-A1"), not whole objects: they are short and
still work if an elective's description changes later.

US8 is implemented here: save_plan() writes the file, load_plan() reads it.
"""

import json
from pathlib import Path

from .models import Elective, StudentPlan

# my_plan.json sits next to main.py, whatever folder the app is run from.
PLAN_FILE = Path(__file__).resolve().parent.parent / "my_plan.json"


class StorageError(Exception):
    """The plan file could not be written or read."""


def _damaged():
    """Build the error for a plan file we cannot use."""
    return StorageError(
        "Could not read my_plan.json — starting with an empty plan."
    )


def save_plan(plan, path=PLAN_FILE):
    """Write the plan's ids to my_plan.json (US8, save)."""
    path = Path(path)
    elective_ids = []
    for elective in plan.electives:
        elective_ids.append(elective.id)
    data = {
        "version": 1,
        "specialisation": plan.specialisation_id,
        "electives": elective_ids,
    }

    # Write to a temporary file first, then swap it in, so a failed write
    # never leaves a half-written my_plan.json behind.
    temp_path = path.with_name(path.name + ".tmp")
    try:
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
            file.write("\n")
        temp_path.replace(path)
    except OSError:
        raise StorageError("Could not save my_plan.json")


def load_plan(electives, path=PLAN_FILE):
    """Read my_plan.json and rebuild the plan (US8, load).

    Returns None when there is no saved plan yet. Raises StorageError when
    the file exists but cannot be used. Unknown elective ids are kept as
    placeholder Electives so US7 can report them.
    """
    path = Path(path)
    if not path.exists():
        return None

    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, ValueError):
        raise _damaged()

    if not isinstance(data, dict) or data.get("version") != 1:
        raise _damaged()

    elective_ids = data.get("electives", [])
    if not isinstance(elective_ids, list):
        raise _damaged()

    specialisation_id = data.get("specialisation")
    if specialisation_id is not None and not isinstance(
            specialisation_id, str):
        raise _damaged()

    catalogue = {}
    for elective in electives:
        catalogue[elective.id] = elective

    plan = StudentPlan()
    plan.specialisation_id = specialisation_id
    for elective_id in elective_ids:
        if not isinstance(elective_id, str):
            raise _damaged()
        if elective_id in catalogue:
            plan.electives.append(catalogue[elective_id])
        else:
            # Keep the unknown id, so US7 can warn about it later.
            plan.electives.append(Elective(
                id=elective_id,
                name=elective_id,
                category="",
                ects=0,
                semester="",
                campus=[],
            ))
    return plan
