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
"""

# --- Input validation helpers ---

def ask_number(prompt, low, high):
    """Ask until the user types a whole number from low to high."""
    while True:
        answer = input(prompt).strip()
        # isdigit() first, so int() never gets text like "abc"
        if answer.isdigit():
            number = int(answer)
            if number >= low and number <= high:
                return number
        print(f"Please enter a number from {low} to {high}.")


def ask_yes_no(prompt):
    """Ask until the user types y or n. Returns True for y."""
    while True:
        answer = input(prompt).strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Please enter y or n.")


# --- US4: choose a specialisation ---

def choose_specialisation(plan, specialisations):
    """Story 4: let the student pick one specialisation for their plan."""
    # 1. Find the name of the current choice (the plan only stores the id)
    current = plan.specialisation_id
    for specialisation in specialisations:
        if specialisation.id == plan.specialisation_id:
            current = specialisation.name
