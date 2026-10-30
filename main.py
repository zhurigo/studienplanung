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
from planner.prompts import ask_number, ask_yes_no, show_error, show_header, show_success
from planner.rules import show_plan_check
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

    count = len(plan.electives)
    word = "elective" if count == 1 else "electives"
    return f"Plan loaded: {name}, {count} {word} ({ects}/12 ECTS)."


# --- Main menu ---

def show_main_menu():
    """Print the main menu, with 0. Exit at the bottom."""
    show_header("Main menu")
    print("1. View degree plan")
    print("2. Explore specialisations")
    print("3. Choose specialisation")
    print("4. Plan electives")
    print("5. Check my plan")
    print("6. Roadmap")
    print("7. Save plan")
    print("0. Exit")


# --- Program ---

def main():
    print("=======================================================")
    print()
    print("           Welcome to the BIT Study Planner")
    print("   FHNW School of Business · Academic year 2026/2027")
    print()
    print("=======================================================")

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
        show_main_menu()
        choice = ask_number("Choose an option (0-7): ", 0, 7)
        if choice == 0:
            if unsaved and ask_yes_no(
                    "You have unsaved changes. Save now? (y/n): "):
                try:
                    save_plan(plan)
                except StorageError as error:
                    show_error(error)
                else:
                    show_success("Plan saved to my_plan.json.")
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
            pass  # US9 (Hugo): roadmap
        elif choice == 7:
            try:
                save_plan(plan)
            except StorageError as error:
                show_error(error)
            else:
                show_success("Plan saved to my_plan.json.")
                unsaved = False
    print()
    print("Goodbye.")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
        print("Goodbye.")
        sys.exit(0)
