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

from planner.choices import choose_specialisation
from planner.data_loader import (
    load_electives,
    load_groups,
    load_modules,
    load_specialisations,
)
from planner.display import show_degree_plan
from planner.models import StudentPlan
from planner.prompts import ask_number, ask_yes_no, show_header


# --- Helpers ---

def count_items(items):
    """Count the items in a list, one by one."""
    total = 0
    for item in items:
        total = total + 1
    return total


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
    groups = load_groups()
    modules = load_modules()
    specialisations = load_specialisations()
    electives = load_electives()
    print()
    print(f"Loaded {count_items(modules)} modules, {count_items(specialisations)} specialisations and {count_items(electives)} electives.")

    # Step 2: offer to load a saved plan (will be added later)

    # One plan for the whole session, so choices are kept between menus
    plan = StudentPlan()

    # Step 3: the menu comes back after every action, until the user picks 0
    while True:
        show_main_menu()
        choice = ask_number("Choose an option (0-7): ", 0, 7)
        if choice == 0:
            break

        # Open the option the student chose (pass = not written yet)
        if choice == 1:
            show_degree_plan(modules, groups)
        elif choice == 2:
            pass  # US3 (Angelica): explore specialisations
        elif choice == 3:
            choose_specialisation(plan, specialisations)
        elif choice == 4:
            pass  # US5 + US6 (Thalita): plan electives
        elif choice == 5:
            pass  # US7 (Hugo): check my plan
        elif choice == 6:
            pass  # US9 (Hugo): roadmap
        elif choice == 7:
            pass  # US8 (Hugo): save plan
    print()
    print("Goodbye.")

if __name__ == "__main__":
    main()
