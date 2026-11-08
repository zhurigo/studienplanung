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
The input helpers (ask_menu, ask_yes_no) are in prompts.py, the colours and messages in styling.py.
"""

from planner.display import ELECTIVE_SEMESTERS, semester_label
from planner.prompts import ask_menu, ask_yes_no
from planner.styling import BOX_TEXT_WIDTH, CURRENT, BOLD, DIM, RESET, bullet, ects, fit, wrap, show_box, show_header, show_kept, show_success, show_warning

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
        # Like the electives box: "Selected" as the title, the choice under it
        if current is None:
            show_box("Selected", ["none yet"], center=True)
        else:
            show_box("Selected", [current], center=True)
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
        replace = ask_yes_no(f"Replace it with {choice.name}?")
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
    """The counter text, e.g. 'Selected: 6/12 ECTS', for the box title and the remove screen."""
    return f"Selected: {plan.total_elective_ects()}/12 ECTS"


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
    """The counter, then the chosen electives with their semester, in a centered box."""
    # Nothing chosen yet: a message instead of "Selected: 0/12 ECTS"
    if plan.electives == []:
        show_box("No electives selected yet", [])
        return

    rows = []
    for elective in electives_by_semester(plan):
        rows.append(bullet(elective.name, f"{where(plan, elective):<4}{ects(elective.ects)}", BOX_TEXT_WIDTH))
    show_box(selected_line(plan), rows)


def chosen_options(plan):
    """One line per elective in the plan: name, semester and ECTS."""
    options = []
    for elective in electives_by_semester(plan):
        options.append((elective.name, f"{where(plan, elective):<4}{ects(elective.ects)}"))
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
    # Stay here until the student picks 0 in the categories
    while True:
        # 1. Ask for a category, 0 goes back to Plan electives
        category = ask_category(plan, electives_by_category, "Categories", "Pick a category to see its electives")
        if category is None:
            return

        # Stay in this category until the student picks 0, so they can add more or try again
        while True:
            # 2. Ask for an elective, 0 goes back to the categories
            elective = ask_elective(plan, electives_by_category[category], category, "HS = autumn, FS = spring")
            if elective is None:
                break

            # 3. Add it, or say why it can't be added
            try_to_add(plan, elective)


# --- Picking from the electives catalogue ---

def ask_category(plan, electives_by_category, title, description):
    """Ask for a category, with how many electives it has. Returns its name, or None for back."""
    categories = []
    options = []
    for category in electives_by_category:
        count = 0
        for elective in electives_by_category[category]:
            count = count + 1
        categories.append(category)
        options.append(f"{category} ({count})")
    show_header(title, description)
    number = ask_menu(options)
    if number == 0:
        return None
    # lists start at 0, the menu at 1
    return categories[number - 1]


CAMPUS_CODES = {"Basel": "BS", "Olten": "OL", "Windisch": "WI", "Online": "ON"}
CAMPUS_LEGEND = "BS Basel · OL Olten · WI Windisch · ON Online"


def campus_codes(elective):
    """The campus as short codes, e.g. ['Olten', 'Windisch'] -> 'OL WI'."""
    codes = ""
    for place in elective.campus:
        if codes != "":
            codes = codes + " "
        codes = codes + CAMPUS_CODES.get(place, place)
    return codes


def ask_elective(plan, electives, title, description):
    """Ask for one of the electives, one line each: name, ECTS, HS/FS and campus.
    Electives already in the plan get the "current" colour. Returns it, or None for back."""
    # 1. The campus column is as wide as the longest campus in this list
    campus_width = len("Campus")
    for elective in electives:
        campus_width = max(campus_width, len(campus_codes(elective)))

    # 2. One line per elective, the columns line up under the dim column names
    options = []
    for elective in electives:
        style = ""
        if plan.has_elective(elective.id):
            style = CURRENT
        options.append((elective.name, f"{elective.ects:<4}  {elective.semester:<5}  {campus_codes(elective):<{campus_width}}", style))
    show_header(title, description + "\n" + CAMPUS_LEGEND)
    columns = "ECTS  Term   " + "Campus".ljust(campus_width)
    print(f"{DIM}{fit('', columns)}{RESET}")
    number = ask_menu(options)
    if number == 0:
        return None
    return electives[number - 1]


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
            show_warning(f"You cannot add anything else, that would make {new_total}/12 ECTS")
        else:
            show_warning(f"Only {plan.ects_left()} ECTS left, that would make {new_total}/12 ECTS")
        offer_swap(plan, elective)
        return

    # 3. No free semester in its season: say so and add nothing
    semesters = free_semesters(plan, elective)
    if semesters == []:
        show_warning(f"No free semester for {elective.name}\n   each semester can have one elective")
        return

    # 4. Ask the semester, 0 adds nothing
    semester = ask_semester(elective, semesters)
    if semester == 0:
        show_kept(f"{elective.name} was not added")
        return

    # 5. Add it and show the new counter
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


def free_semesters(plan, elective, swapped_out=None):
    """The semesters (3 to 6) of the elective's season that have no elective yet.
    Each semester has one elective slot. In a swap, the semester of the elective
    that leaves (swapped_out) counts as free."""
    free = []
    for semester in ELECTIVE_SEMESTERS:
        taken = False
        for chosen in plan.electives:
            if chosen is not swapped_out and plan.semester_of(chosen.id) == semester:
                taken = True
        if fits_season(elective, semester) and not taken:
            free.append(semester)
    return free


def ask_semester(elective, semesters):
    """Ask in which of the semesters to take the elective. Returns 0 for back."""
    options = []
    for semester in semesters:
        # Semesters 3 and 4 are year 2, 5 and 6 are year 3
        year = (semester + 1) // 2
        options.append((f"Semester {semester}", f"{semester_label(semester)}   year {year}"))
    print()
    print(wrap(f"In which semester would you like to take {BOLD}{elective.name}{RESET} ({elective.semester})?"))
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
    print(f"{BOLD}{selected_line(plan)}{RESET}")
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
    if not ask_yes_no("Swap it for one of your electives?"):
        show_kept("No change was made to your electives")
        return

    # 2. Ask which elective to swap out
    print()
    print(wrap(f"Which elective would you like to swap for {BOLD}{elective.name}{RESET}?"))
    print()
    number = ask_menu(chosen_options(plan))
    if number == 0:
        show_kept(f"{elective.name} was not added, kept your {len(plan.electives)} electives")
        return
    old = electives_by_semester(plan)[number - 1]

    # 3. Still too many ECTS without the old one: say so and change nothing
    new_total = plan.total_elective_ects() - old.ects + elective.ects
    if new_total > 12:
        show_warning(f"Swapping out {old.name}\n   would still make {new_total}/12 ECTS")
        return

    # 4. No free semester for the new one, even without the old one: change nothing
    semesters = free_semesters(plan, elective, old)
    if semesters == []:
        show_warning(f"No free semester for {elective.name}\n   each semester can have one elective")
        return

    # 5. Ask the semester for the new one, 0 keeps the plan as it is
    semester = ask_semester(elective, semesters)
    if semester == 0:
        show_kept(f"{elective.name} was not added, kept your {len(plan.electives)} electives")
        return

    # 6. Swap them and show the new counter. One line for the elective that left
    #    and one for the new one, indented like the counter, the semesters lined up
    old_where = where(plan, old)
    width = max(len(old.name), len(elective.name))
    plan.remove_elective(old.id)
    plan.add_elective(elective, semester)
    out_line = f"\n   - {old.name:<{width}}   {old_where}"
    in_line = f"\n   + {elective.name:<{width}}   S{semester}"
    show_success(f"Swapped electives{out_line}{in_line}{ects_bar(plan)}")
