"""
The menus where the student makes choices.

Owner: Thalita (Plan)
User stories:
  4. Choose one specialisation, confirm before replacing  (Step 6)
  5. Add an elective: first pick a category, then a module (Step 7)
  6. Remove or swap an elective                            (Step 7)

Input to validate:
  - numbers must be in range, letters are rejected
  - y/n questions accept only y or n
  - an elective can't be added twice
  - elective total can't go above the limit

The rules themselves (limits, no doubles) live in StudentPlan in models.py.
This file only asks the questions and shows the answers.
The input helpers (ask_menu, ask_numbers, ask_yes_no) are in prompts.py.
"""

from planner.prompts import CURRENT, BOLD, RESET, ask_menu, ask_numbers, ask_yes_no, show_header, show_kept, show_menu, show_success, show_warning

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
            show_warning(f"{choice.name} is already your specialisation")
        else:
            break

    # 5. A different one is already chosen: confirm before replacing
    if current is not None:
        replace = ask_yes_no(f"Replace {current} with {choice.name}? (y/n): ")
        if not replace:
            show_kept(f"Kept {current}")
            return

    # 6. Save the choice in the plan
    plan.choose_specialisation(choice.id)
    show_success(f"Specialisation set to {BOLD}{choice.name}{RESET}")


# --- US5 + US6: plan electives ---

def selected_line(plan):
    """The counter line, e.g. 'Selected: 6/12 ECTS (German Basic A1, Italian A1)'."""
    line = f"Selected: {plan.total_elective_ects()}/12 ECTS"
    names = ""
    for elective in plan.electives:
        if names != "":
            names = names + ", "
        names = names + elective.name
    # The chosen electives are shown in the "current" colour
    if names != "":
        line = line + f" ({CURRENT}{names}{RESET})"
    return line


def chosen_options(plan):
    """One line per elective in the plan: name and ECTS."""
    options = []
    for elective in plan.electives:
        options.append(f"{elective.name:<40}{elective.ects} ECTS")
    return options


def plan_electives(plan, electives_by_category):
    """Stories 5 and 6: add or remove electives until the student picks 0."""
    while True:
        # 1. Show the counter and the two actions
        show_header("Plan electives", "Must add up to 12 ECTS. Swap one if it doesn't fit")
        print(selected_line(plan))
        print()
        number = ask_menu(["Add an elective", "Remove an elective"])

        # 2. Open the action the student chose
        if number == 0:
            return
        if number == 1:
            add_elective(plan, electives_by_category)
        elif number == 2:
            remove_elective(plan)


# --- US5: add an elective ---

def add_elective(plan, electives_by_category):
    """Story 5: pick a category, then one or more electives to add to the plan."""
    # 1. List the categories with how many electives each one has
    categories = []
    category_options = []
    for category in electives_by_category:
        count = 0
        for elective in electives_by_category[category]:
            count = count + 1
        categories.append(category)
        category_options.append(f"{category} ({count})")

    # Stay here until the student picks electives, or 0 in the categories
    while True:
        # 2. Ask for a category, 0 goes back to Plan electives
        show_header("Categories", "Pick a category to see its electives")
        number = ask_menu(category_options)
        if number == 0:
            return
        # lists start at 0, the menu at 1
        category = categories[number - 1]
        electives = electives_by_category[category]

        # 3. Make one line per elective: name, ECTS, semester and campus
        options = []
        for elective in electives:
            campus = ""
            for place in elective.campus:
                if campus != "":
                    campus = campus + ", "
                campus = campus + place
            # :<40 pads the name to 40 characters, so the columns line up
            line = f"{elective.name:<40}{elective.ects} ECTS {elective.semester:<8}{campus}"
            # Electives already in the plan get the "current" colour
            if plan.has_elective(elective.id):
                line = f"{CURRENT}{line}{RESET}"
            options.append(line)

        # 4. Show the list, 0 goes back to the categories
        show_header(category, "HS = autumn, FS = spring. Pick one or more, e.g. 5, 6")
        highest = show_menu(options, "Back")
        numbers = ask_numbers(f"Choose an option (0-{highest}): ", 0, highest)
        if 0 not in numbers:
            break

    # 5. Try to add each one, in the order they were typed
    for number in numbers:
        try_to_add(plan, electives[number - 1])

def try_to_add(plan, elective):
    """Story 5: add the elective, or say why it can't be added."""
    # 1. Already in the plan: say so and add nothing
    if plan.has_elective(elective.id):
        show_warning(f"{elective.name} is already in your plan")
        return

    # 2. Too many ECTS: say how many are still free, then offer a swap
    if elective.ects > plan.ects_left():
        new_total = plan.total_elective_ects() + elective.ects
        if plan.ects_left() == 0:
            show_warning(f"That would make {new_total}/12 ECTS — you cannot add anything else")
        else:
            show_warning(f"That would make {new_total}/12 ECTS — you can add at most {plan.ects_left()} more ECTS")
        offer_swap(plan, elective)
        return

    # 3. Add it and show the new counter
    plan.add_elective(elective)
    show_success(f"Added {elective.name}. Selected: {plan.total_elective_ects()}/12 ECTS")


# --- US6: remove or swap an elective ---

def remove_elective(plan):
    """Story 6: remove one or more electives from the plan."""
    # 1. Nothing to remove: say so and go back to Plan electives
    if plan.electives == []:
        show_warning("You have no electives to remove")
        return

    # 2. List the chosen electives with their ECTS
    show_header("Remove an elective", "Pick one or more, e.g. 1, 2")
    print(selected_line(plan))
    print()
    highest = show_menu(chosen_options(plan), "Back")
    numbers = ask_numbers(f"Choose an option (0-{highest}): ", 0, highest)
    if 0 in numbers:
        return

    # 3. Find the electives first, because removing one changes the numbers of the others
    chosen = []
    for number in numbers:
        elective = plan.electives[number - 1]
        if elective not in chosen:
            chosen.append(elective)

    # 4. Remove them and show the new counter
    for elective in chosen:
        plan.remove_elective(elective.id)
        show_success(f"Removed {elective.name}. Selected: {plan.total_elective_ects()}/12 ECTS")


def offer_swap(plan, elective):
    """Story 6: the new elective doesn't fit, so offer to swap it for one in the plan."""
    # 1. Ask first, n keeps the plan as it is
    if not ask_yes_no(f"Swap {elective.name} for one of your electives? (y/n): "):
        return

    # 2. Ask which elective to swap out
    print()
    print(selected_line(plan))
    print()
    number = ask_menu(chosen_options(plan))
    if number == 0:
        return
    old = plan.electives[number - 1]

    # 3. Still too many ECTS without the old one: say so and change nothing
    new_total = plan.total_elective_ects() - old.ects + elective.ects
    if new_total > 12:
        show_warning(f"Swapping out {old.name} would still make {new_total}/12 ECTS")
        return

    # 4. Swap them and show the new counter
    plan.remove_elective(old.id)
    plan.add_elective(elective)
    show_success(f"Swapped {old.name} for {elective.name}. Selected: {plan.total_elective_ects()}/12 ECTS")
