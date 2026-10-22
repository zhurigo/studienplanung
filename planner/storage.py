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

US8 save is implemented here. load_plan() is still to write.
"""

import json
from pathlib import Path

# my_plan.json sits next to main.py, whatever folder the app is run from.
PLAN_FILE = Path(__file__).resolve().parent.parent / "my_plan.json"


class StorageError(Exception):
    """The plan file could not be written or read."""


def save_plan(plan, path=PLAN_FILE):
    """Write the plan's ids to my_plan.json (US8, save)."""
    path = Path(path)
    data = {
        "version": 1,
        "specialisation": plan.specialisation_id,
        "electives": [elective.id for elective in plan.electives],
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
        raise StorageError("Could not save my_plan.json.")
