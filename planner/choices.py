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

from planner.prompts import CURRENT, RESET, ask_menu, ask_yes_no, show_header, show_kept, show_success, show_warning


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
        show_header("Choose specialisation", "Your specialisation fills semesters 6 to 8")
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
            show_warning(f"{choice.name} is already your specialisation.")
        else:
            break

    # 5. A different one is already chosen: confirm before replacing
    if current is not None:
        replace = ask_yes_no(f"Replace {current} with {choice.name}? (y/n): ")
        if not replace:
            show_kept(f"Kept {current}.")
            return

    # 6. Save the choice in the plan
    plan.choose_specialisation(choice.id)
    show_success(f"Specialisation set to {choice.name}.")


# --- US5 + US6: plan electives ---

def selected_line(plan):
    """The counter line, e.g. 'Selected: 6/12 ECTS (German Basic A1, Italian A1)'."""
    line = f"Selected: {plan.total_elective_ects()}/12 ECTS"
    names = ""
    for elective in plan.electives:
        if names != "":
            names = names + ", "
        names = names + elective.name
    if names != "":
        line = line + f" ({names})"
    return line


def plan_electives(plan, electives_by_category):
    """Stories 5 and 6: add or remove electives until the student picks 0."""
    while True:
        # 1. Show the counter and the two actions
        show_header("Plan electives", "Your electives must add up to exactly 12 ECTS")
        print(selected_line(plan))
        print()
        number = ask_menu(["Add an elective", "Remove an elective"])

        # 2. Open the action the student chose (pass = not written yet)
        if number == 0:
            return
        if number == 1:
            add_elective(plan, electives_by_category)
        elif number == 2:
            pass  # US6 (Thalita): remove an elective


# --- US5: add an elective ---

def add_elective(plan, electives_by_category):
    """Story 5: pick a category, then an elective to add to the plan."""
    # 1. List the categories with how many electives each one has
    show_header("Categories", "Pick a category to see its electives")
    categories = []
    options = []
    for category in electives_by_category:
        count = 0
        for elective in electives_by_category[category]:
            count = count + 1
        categories.append(category)
        options.append(f"{category} ({count})")
