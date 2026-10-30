"""
BIT Study Planner - start of the program.

Run with:  python main.py

Owner: whole team (set up together in CW 42)

What goes here:
  - Show the welcome message                          (Step 1)
  - Load the data files through planner/data_loader    (Step 1)
  - Ask whether to load a saved plan                  (Step 2)
  - Main menu loop: show options 0-7, read the choice,
    call the matching function, repeat until 0        (Step 3)
  - On exit: offer to save unsaved changes            (Step 11)

Keep this file short. The menu only calls functions from the planner package.
"""

import sys

from planner.choices import choose_specialisation, plan_electives
from planner.data_loader import DataError, electives_by_category, load_all
from planner.display import explore_specialisations, show_degree_plan
from planner.models import StudentPlan
from planner.prompts import BOLD, ITALIC, RESET, ask_number, ask_yes_no, show_error, show_header, show_menu, show_success
from planner.rules import show_plan_check, show_roadmap
from planner.storage import StorageError, load_plan, save_plan


# --- Helpers ---

def count_items(items):
    """Count the items in a list, one by one."""
    total = 0
    for item in items:
        total = total + 1
    return total


def plan_summary(plan, specialisations):
    """One line describing a loaded plan (US8 AC2)."""
    name = "no specialisation"
    for specialisation in specialisations:
        if specialisation.id == plan.specialisation_id:
            name = specialisation.name

    ects = 0
    for elective in plan.electives:
        ects = ects + elective.ects

    indent = "     "
    summary = "Plan loaded"
    summary = summary + f"\n\n{indent}Specialisation: {name}"
    if plan.electives == []:
        summary = summary + f"\n{indent}Electives: none"
    else:
        summary = summary + f"\n{indent}Electives ({ects}/12 ECTS):"
        for elective in plan.electives:
            summary = summary + f"\n{indent}  • {elective.name} ({elective.ects} ECTS)"
    return summary


def show_goodbye():
    width = 60
    print()
    print(f"{BOLD}{'Thanks for using the BIT Study Planner':^{width}}{RESET}")
    print(f"\033[2m{ITALIC}{'Good luck with your studies at FHNW 🍀':^{width}}{RESET}")
    print()


# --- Main menu ---

def show_main_menu():
    """Print the main menu, with 0. Exit at the bottom"""
    show_header("Main menu")
    options = [
        "View degree plan",
        "Explore specialisations",
        "Choose specialisation",
        "Plan electives",
        "Check my plan",
        "Roadmap",
        "Save plan",
    ]
    return show_menu(options, "Exit")


# --- Program ---

def main():
    width = 60

    print("╔" + "═" * width + "╗")
    print("║" + " " * width + "║")
    print("║" + " " * width + "║")
    print(f"║{'Welcome to the BIT Study Planner':^{width}}║")
    print("║" + " " * width + "║")
    print(f"║{'FHNW School of Business · Academic year 2026/2027':^{width}}║")
    print("║" + " " * width + "║")
    print("║" + " " * width + "║")
    print("╚" + "═" * width + "╝")

    # Step 1: load the data files (stops with an error if one is missing or broken)
    try:
        groups, modules, specialisations, electives = load_all()
    except DataError as error:
        show_error(error)
        sys.exit(1)
    print()
    print(f"Loaded {count_items(modules)} modules, {count_items(specialisations)} specialisations and {count_items(electives)} electives")

    # Step 2: offer to load a saved plan (US8)
    try:
        saved = load_plan(electives)
    except StorageError as error:
        show_error(error)
        saved = None

    # One plan for the whole session, so choices are kept between menus
    plan = StudentPlan()
    unsaved = False
    if saved is not None:
        if ask_yes_no("A saved plan was found. Load it? (y/n): "):
            plan = saved
            show_success(plan_summary(plan, specialisations))

    # Step 3: the menu comes back after every action, until the user picks 0
    while True:
        highest = show_main_menu()
        choice = ask_number(f"Choose an option (0-{highest}): ", 0, highest)
        if choice == 0:
            if unsaved and ask_yes_no(
                    "You have unsaved changes. Save now? (y/n): "):
                try:
                    save_plan(plan)
                except StorageError as error:
                    show_error(error)
                else:
                    show_success("Plan saved to my_plan.json")
            break

        # Open the option the student chose (pass = not written yet)
        if choice == 1:
            show_degree_plan(modules, groups, plan, specialisations)
        elif choice == 2:
            explore_specialisations(specialisations)
        elif choice == 3:
            before = plan.specialisation_id
            choose_specialisation(plan, specialisations)
            if plan.specialisation_id != before:
                unsaved = True
        elif choice == 4:
            before = plan.electives.copy()
            plan_electives(plan, electives_by_category(electives))
            if plan.electives != before:
                unsaved = True
        elif choice == 5:
            show_plan_check(plan, specialisations, electives)
        elif choice == 6:
            show_roadmap(plan, modules, groups, specialisations)
        elif choice == 7:
            try:
                save_plan(plan)
            except StorageError as error:
                show_error(error)
            else:
                show_success("Plan saved to my_plan.json")
                unsaved = False
    show_goodbye()

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
        show_goodbye()
        sys.exit(0)
