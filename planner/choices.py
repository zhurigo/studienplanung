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
The input helpers (ask_menu, ask_yes_no) are in prompts.py.
"""

from planner.display import ELECTIVE_SEMESTERS, semester_label
from planner.prompts import CURRENT, BOLD, RESET, ask_menu, ask_yes_no, show_header, show_kept, show_success, show_warning

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

def ects_bar(plan):
    """A second message line with one block per ECTS, e.g. '   ▰▰▰▰▰▰▰▰▰▱▱▱  9/12 ECTS'.
    Indented 3 spaces, so it lines up under the text after the emoji."""
    used = plan.total_elective_ects()
    return f"\n   {'▰' * used}{'▱' * plan.ects_left()}  {used}/12 ECTS"


def selected_line(plan):
    """The counter line, e.g. 'Selected: 6/12 ECTS'."""
    return f"Selected: {BOLD}{plan.total_elective_ects()}/12 ECTS{RESET}"


def where(plan, elective):
    """The semester picked for the elective, e.g. 'S3'."""
    return f"S{plan.semester_of(elective.id)}"


def electives_by_semester(plan):
    """The chosen electives sorted by semester (3 to 6)."""
    ordered = []
    for semester in ELECTIVE_SEMESTERS:
        for elective in plan.electives:
            if plan.semester_of(elective.id) == semester:
                ordered.append(elective)
    return ordered


def show_selected(plan):
    """The counter, then the chosen electives with their semester, as a bullet list."""
    print(selected_line(plan))
    if plan.electives == []:
        print("  • none yet")
    for elective in electives_by_semester(plan):
        print(f"  • {elective.name:<40}{where(plan, elective):<5}{elective.ects} ECTS")


def chosen_options(plan):
    """One line per elective in the plan: name, semester and ECTS."""
    options = []
    for elective in electives_by_semester(plan):
        options.append(f"{elective.name:<40}{where(plan, elective):<5}{elective.ects} ECTS")
    return options


def plan_electives(plan, electives_by_category):
    """Stories 5 and 6: add or remove electives until the student picks 0."""
    while True:
        # 1. Show the counter and the two actions
        show_header("Plan electives", "Must add up to 12 ECTS. Swap one if it doesn't fit")
        show_selected(plan)
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
    """Story 5: pick a category, then an elective to add to the plan."""
    # 1. List the categories with how many electives each one has
    categories = []
    category_options = []
    for category in electives_by_category:
        count = 0
        for elective in electives_by_category[category]:
            count = count + 1
        categories.append(category)
        category_options.append(f"{category} ({count})")

    # Stay here until the student picks 0 in the categories
    while True:
        # 2. Ask for a category, 0 goes back to Plan electives
        show_header("Categories", "Pick a category to see its electives")
        number = ask_menu(category_options)
        if number == 0:
            return
        # lists start at 0, the menu at 1
        category = categories[number - 1]
        electives = electives_by_category[category]

        # Stay in this category until the student picks 0, so they can add more or try again
        while True:
            # 3. Make one line per elective: name, ECTS, semester and campus
            #    (made again every time, so newly added electives get the "current" colour)
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
            show_header(category, "HS = autumn, FS = spring")
            number = ask_menu(options)
            if number == 0:
                break

            # 5. Add it, or say why it can't be added
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

    # 3. Ask the semester, 0 adds nothing
    semester = ask_semester(elective)
    if semester == 0:
        show_kept(f"{elective.name} was not added")
        return

    # 4. Add it and show the new counter
    plan.add_elective(elective, semester)
    show_success(f"Added {elective.name} to semester {semester}{ects_bar(plan)}")


# --- US5: pick the semester of an elective ---

def fits_season(elective, semester):
    """True if the elective is taught in the semester's season.
    Odd semesters are autumn (HS), even ones spring (FS), HS/FS fits both."""
    if elective.semester == "HS/FS":
        return True
    if semester % 2 == 1:
        return elective.semester == "HS"
    return elective.semester == "FS"


def ask_semester(elective):
    """Ask in which semester (3 to 6) to take the elective. Returns 0 for back.
    Only the semesters of its season are offered."""
    semesters = []
    options = []
    for semester in ELECTIVE_SEMESTERS:
        if fits_season(elective, semester):
            semesters.append(semester)
            # Semesters 3 and 4 are year 2, 5 and 6 are year 3
            year = (semester + 1) // 2
            options.append(f"Semester {semester}   {semester_label(semester)}   year {year}")
    print()
    print(f"In which semester would you like to take {BOLD}{elective.name}{RESET} ({elective.semester})?")
    print()
    number = ask_menu(options)
    if number == 0:
        return 0
    # lists start at 0, the menu at 1
    return semesters[number - 1]


# --- US6: remove or swap an elective ---

def remove_elective(plan):
    """Story 6: remove an elective from the plan."""
    # 1. Nothing to remove: say so and go back to Plan electives
    if plan.electives == []:
        show_warning("You have no electives to remove")
        return

    # 2. List the chosen electives with their ECTS
    show_header("Remove an elective")
    print(selected_line(plan))
    print()
    number = ask_menu(chosen_options(plan))
    if number == 0:
        return

    # 3. Remove it and show the new counter, with the semester it was in
    elective = electives_by_semester(plan)[number - 1]
    semester = plan.semester_of(elective.id)
    plan.remove_elective(elective.id)
    show_success(f"Removed {elective.name} from semester {semester}{ects_bar(plan)}")


def offer_swap(plan, elective):
    """Story 6: the new elective doesn't fit, so offer to swap it for one in the plan."""
    # 1. Ask first, n keeps the plan as it is
    if not ask_yes_no(f"Swap {elective.name} for one of your electives? (y/n): "):
        return

    # 2. Ask which elective to swap out
    print()
    print(f"Which elective would you like to swap for {BOLD}{elective.name}{RESET}?")
    print()
    number = ask_menu(chosen_options(plan))
    if number == 0:
        return
    old = electives_by_semester(plan)[number - 1]

    # 3. Still too many ECTS without the old one: say so and change nothing
    new_total = plan.total_elective_ects() - old.ects + elective.ects
    if new_total > 12:
        show_warning(f"Swapping out {old.name} would still make {new_total}/12 ECTS")
        return

    # 4. Ask the semester for the new one, 0 keeps the plan as it is
    semester = ask_semester(elective)
    if semester == 0:
        show_kept(f"{elective.name} was not added")
        return

    # 5. Swap them and show the new counter. One line for the elective that left
    #    and one for the new one, indented like the counter, the semesters lined up
    old_where = where(plan, old)
    width = max(len(old.name), len(elective.name))
    plan.remove_elective(old.id)
    plan.add_elective(elective, semester)
    out_line = f"\n   - {old.name:<{width}}   {old_where}"
    in_line = f"\n   + {elective.name:<{width}}   S{semester}"
    show_success(f"Swapped electives{out_line}{in_line}{ects_bar(plan)}")
