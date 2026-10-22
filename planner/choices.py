"""
The menus where the student makes choices.

Owner: Thalita (Plan)
User stories:
  4. Choose one specialisation, confirm before replacing  (Step 6)
  5. Add an elective: first pick a category, then a module (Step 7)
  6. Remove an elective                                    (Step 7)

Input to validate:
  - numbers must be in range, letters are rejected
  - y/n questions accept only y or n
  - an elective can't be added twice
  - elective total can't go above the limit

The rules themselves (limits, no doubles) live in StudentPlan in models.py.
This file only asks the questions and shows the answers.
The input helpers (ask_menu, ask_yes_no) are in prompts.py.
"""

from planner.prompts import CURRENT, RESET, SUCCESS, WARNING, ask_menu, ask_yes_no, show_header


# --- US4: choose a specialisation ---

def choose_specialisation(plan, specialisations):
    """Story 4: let the student pick one specialisation for their plan."""
    # 1. Find the name of the current choice (the plan only stores the id)
    current = plan.specialisation_id
    for specialisation in specialisations:
        if specialisation.id == plan.specialisation_id:
            current = specialisation.name

    names = []
    for specialisation in specialisations:
        names.append(specialisation.name)

    # Stay in this menu until the student picks a new one or 0
    while True:
        # 2. Show the current choice and the list
        show_header("Choose specialisation")
        if current is not None:
            print(f"Current choice: {CURRENT}{current}{RESET}")
            print()

        # 3. Ask for a valid number, 0 goes back without changing anything
        number = ask_menu(names)
        if number == 0:
            return
        # lists start at 0, the menu at 1
        choice = specialisations[number - 1]

        # 4. Same as before: say so and ask again
        if plan.specialisation_id == choice.id:
            print()
            print(f"{WARNING}! {choice.name} is already your specialisation.{RESET}")
        else:
            break

    # 5. A different one is already chosen: confirm before replacing
    if current is not None:
        replace = ask_yes_no(f"Replace {current} with {choice.name}? (y/n): ")
        if not replace:
            print()
            print(f"{CURRENT}→ Kept {current}.{RESET}")
            return

    # 6. Save the choice in the plan
    plan.choose_specialisation(choice.id)
    print()
    print(f"{SUCCESS}→ Specialisation set to {choice.name}.{RESET}")
