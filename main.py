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

from planner.data_loader import load_electives, load_modules, load_specialisations


def count_items(items):
    """Count the items in a list, one by one."""
    total = 0
    for item in items:
        total = total + 1
    return total


def main():
    print("=======================================================")
    print("           Welcome to the BIT Study Planner")
    print("   FHNW School of Business · Academic year 2026/2027")
    print("=======================================================")

    # Step 1: load the data files (stops with an error if one is missing or broken)
    modules = load_modules()
    specialisations = load_specialisations()
    electives = load_electives()
    print(f"Loaded {count_items(modules)} modules, {count_items(specialisations)} specialisations and {count_items(electives)} electives.")

    while True:
        choice = input("Choose an option (0-7): ")
        if choice == "0":
            break
        print(f"You chose {choice}")
    print("Goodbye.")


if __name__ == "__main__":
    main()
