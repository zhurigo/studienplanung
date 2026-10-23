"""
Reading the data files in the data/ folder.

Owner: Hugo (Check and save)
Course criterion: file processing (reading)

The functions turn the JSON in data/ into the classes from planner/models.
If a file is missing, unreadable or not shaped as expected, they raise
DataError with a message naming the file, so main.py can stop cleanly
instead of printing a traceback.

load_electives() returns one flat list, because main.py counts it for the
welcome line. The categories are still there on every Elective, and
electives_by_category() groups them again for the US5 menu.
"""

import json
from pathlib import Path

from .models import Elective, Module, Specialisation

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class DataError(Exception):
    """A curriculum file is missing, unreadable or in the wrong shape."""


def _read_json(filename):
    """Return the parsed contents of one data file, or raise DataError."""
    path = DATA_DIR / filename
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        raise DataError(f"Could not read data/{filename} — stopping.")


def _wrong_shape(filename):
    """Build the error for a file that is JSON but not what we expect."""
    return DataError(f"Could not read data/{filename} — stopping.")


def load_groups():
    """Return the seven module groups as dicts, in file order (US1, US2).

    models.py has no Group class yet; until it does, the group entries
    (name, short, ects) are passed around as they are in the JSON.
    """
    data = _read_json("modules.json")
    try:
        return [
            {
                "name": entry["name"],
                "short": entry["short"],
                "ects": entry["ects"],
            }
            for entry in data["groups"]
        ]
    except (KeyError, TypeError):
        raise _wrong_shape("modules.json")


def load_modules():
    """Return all 28 modules, in file order (US1, US2, US9)."""
    data = _read_json("modules.json")
    try:
        return [
            Module(
                name=entry["name"],
                semester=entry["semester"],
                group=entry["group"],
                ects=entry["ects"],
                project_based=entry.get("project_based", False),
            )
            for entry in data["modules"]
        ]
    except (KeyError, TypeError):
        raise _wrong_shape("modules.json")


def load_specialisations():
    """Return the three specialisations, in file order (US3, US4)."""
    data = _read_json("specialisations.json")
    try:
        return [
            Specialisation(
                id=entry["id"],
                name=entry["name"],
                focus=entry["focus"],
                modules=entry.get("modules", []),
                builds_on=entry.get("builds_on", []),
                careers=entry.get("careers", []),
            )
            for entry in data["specialisations"]
        ]
    except (KeyError, TypeError):
        raise _wrong_shape("specialisations.json")


def load_electives():
    """Return all 22 electives as one flat list (main.py Step 1, US5)."""
    data = _read_json("electives.json")
    try:
        electives = []
        for category, entries in data["categories"].items():
            for entry in entries:
                electives.append(
                    Elective(
                        id=entry["id"],
                        name=entry["name"],
                        category=category,
                        ects=entry["ects"],
                        semester=entry.get("semester", ""),
                        campus=entry.get("campus", []),
                    )
                )
        return electives
    except (KeyError, TypeError, AttributeError):
        raise _wrong_shape("electives.json")


def electives_by_category(electives):
    """Group a flat elective list back into {category: [Elective]} (US5)."""
    categories = {}
    for elective in electives:
        categories.setdefault(elective.category, []).append(elective)
    return categories


def electives_by_id(electives):
    """Return {id: Elective} for lookups (US7, storage)."""
    return {elective.id: elective for elective in electives}


def load_all():
    """Load everything once at start-up.

    Returns (groups, modules, specialisations, electives).
    Raises DataError if any file cannot be read.
    """
    groups = load_groups()
    modules = load_modules()
    specialisations = load_specialisations()
    electives = load_electives()
    return groups, modules, specialisations, electives
