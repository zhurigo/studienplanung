"""
Showing the degree plan and the specialisations.

Owner: Angelica (Browse)
User stories:
  1. See all modules per semester                       (Step 4)
  2. Filter modules by group, Enter skips the filter    (Step 4)
  3. Explore the three specialisations and their details (Step 5)

US1 is implemented here. US2 (the group filter) and US3 (the specialisation
screen) are still to write.

Added by Thalita (Plan, US4 + US5):
  - the chosen specialisation's modules in semesters 6 to 8 (place_specialisation)
  - the chosen electives in the semester the student picked (place_electives)
"""

from planner.prompts import ask_menu, pause, show_menu
from planner.styling import APP_WIDTH, ARROW, BOLD, DIM, EMPTY, LABEL_WIDTH, RESET, ects, fit, show_bullet, show_header, show_warning
from planner.rules import TOTAL_ECTS


# --- Group colours, the same as in the FHNW module overview ---

GROUP_COLOURS = {
    "Foundation": "\033[38;5;248m",                       # grey
    "Business Administration": "\033[38;5;68m",           # blue
    "Business Information Technology": "\033[38;5;228m",  # light yellow
    "Information Technology": "\033[38;5;210m",           # light red
    "Student Work": "\033[38;5;150m",                     # light green
    "Specialisation": "\033[38;5;117m",                   # light blue
    "Electives": "\033[38;5;147m",                        # light purple
}


# --- Specialisation modules in semesters 6 to 8 (Thalita, US4) ---

def place_specialisation(specialisation):
    """Sort the specialisation modules into semesters 6, 7 and 8.

    Part-time starts in autumn, so semester 7 is autumn and 6 and 8 are spring.
    Autumn modules go in 7. Spring modules fill 6 up to 12 ECTS, the rest go in 8.
    """
    placed = {6: [], 7: [], 8: []}
    spring_ects = 0
    for module in specialisation.modules:
        if module["semester"] == "autumn":
            placed[7].append(module)
        elif spring_ects + module["ects"] <= 12:
            placed[6].append(module)
            spring_ects = spring_ects + module["ects"]
        else:
            placed[8].append(module)
    return placed


# --- Semester names (Thalita, US5) ---

# Part-time starts in autumn 2026 (data/modules.json: academic_year)
START_YEAR = 2026

# The semesters where the electives go
ELECTIVE_SEMESTERS = [3, 4, 5, 6]


def semester_label(semester):
    """The season and year of a semester, e.g. 3 -> 'HS 2027', 4 -> 'FS 2028'.
    Odd semesters are autumn (HS), even ones spring (FS)."""
    year = START_YEAR + semester // 2
    if semester % 2 == 1:
        return f"HS {year}"
    return f"FS {year}"


# --- Chosen electives in semesters 3 to 6 (Thalita, US5) ---

def place_electives(plan):
    """Sort the chosen electives into semesters 3 to 6, each in the semester
    the student picked for it."""
    placed = {3: [], 4: [], 5: [], 6: []}
    ects = {3: 0, 4: 0, 5: 0, 6: 0}
    for elective in plan.electives:
        semester = plan.semester_of(elective.id)
        placed[semester].append(elective)
        ects[semester] = ects[semester] + elective.ects
    return placed, ects


def free_elective_ects(ects, ects_left):
    """How many elective ECTS are still free in each semester 3 to 6.
    The module overview has one 3-ECTS elective slot per semester, so this fills
    the semesters with less than 3 ECTS, until ects_left is used up."""
    free = {}
    for semester in ELECTIVE_SEMESTERS:
        empty = min(max(3 - ects[semester], 0), ects_left)
        free[semester] = empty
        ects_left = ects_left - empty
    return free


# --- US1: the degree plan ---

def show_degree_plan(modules, groups, plan=None, specialisations=None):
    """US1: print every module, grouped by semester 1 to 8.

    If the plan has a specialisation, its modules are shown in semesters 6 to 8.
    """
    # The rows show the short group label ("BIT"), but the data stores the
    # long name ("Business Information Technology"), so build a lookup.
    shorts = {}
    for group in groups:
        shorts[group["name"]] = group["short"]

    # Place the chosen electives, and find the ECTS still to choose (Thalita, US5)
    if plan is not None:
        electives_placed, elective_ects = place_electives(plan)
        free = free_elective_ects(elective_ects, plan.ects_left())
    else:
        electives_placed = {3: [], 4: [], 5: [], 6: []}
        free = free_elective_ects({3: 0, 4: 0, 5: 0, 6: 0}, 12)

    # Find the chosen specialisation and place its modules
    placed = {6: [], 7: [], 8: []}
    chosen = False
    if plan is not None and specialisations is not None:
        for specialisation in specialisations:
            if specialisation.id == plan.specialisation_id:
                placed = place_specialisation(specialisation)
                chosen = True

    # All names in the plan, to find the longest one
    names = []
    for module in modules:
        names.append(module.name)
    for semester in placed:
        for module in placed[semester]:
            names.append(module["name"])

    # Wide enough for the longest module name, never narrower than 31.
    longest = 0
    for module in modules:
        if len(module.name) > longest:
            longest = len(module.name)
    width = max(31, longest + 3)

    # The ECTS per semester, for the semester headings and the total (Thalita, US5)
    semester_ects = {}
    for semester in range(1, 9):
        semester_ects[semester] = 0
    for module in modules:
        semester_ects[module.semester] = semester_ects[module.semester] + module.ects
    for semester in electives_placed:
        for elective in electives_placed[semester]:
            semester_ects[semester] = semester_ects[semester] + elective.ects
        semester_ects[semester] = semester_ects[semester] + free[semester]
    for semester in placed:
        if chosen:
            for module in placed[semester]:
                semester_ects[semester] = semester_ects[semester] + module["ects"]
        else:
            semester_ects[semester] = semester_ects[semester] + 12

    show_header("Degree plan")
    total = 0
    for semester in range(1, 9):
        # Empty line between semesters, not right under the header
        if semester > 1:
            print()
        # The heading with the season and year, e.g. "Semester 3  HS 2027 · 30 ECTS"
        print(f"{BOLD}Semester {semester}{RESET}  "
              f"{DIM}{semester_label(semester)} · {semester_ects[semester]} ECTS{RESET}")
        print()
        total = total + semester_ects[semester]
        for module in modules:
            if module.semester == semester:
                label = shorts.get(module.group, module.group)
                # Colour the group label in its group's colour
                colour = ""
                if module.group in GROUP_COLOURS:
                    colour = GROUP_COLOURS[module.group]
                print(f"{module.name:<{width}}{colour}{label:<{LABEL_WIDTH}}{RESET}"
                      f"{ects(module.ects)}")

        # The chosen electives, the label in light purple (Thalita, US5)
        if semester in electives_placed:
            colour = GROUP_COLOURS["Electives"]
            for elective in electives_placed[semester]:
                print(f"{elective.name:<{width}}{colour}{'Electives':<{LABEL_WIDTH}}{RESET}"
                      f"{ects(elective.ects)}")
            if free[semester] > 0:
                # One placeholder row for the ECTS still to choose, dim italic
                print(f"{EMPTY}{'(choose an elective)':<{width}}{RESET}{colour}{'Electives':<{LABEL_WIDTH}}{RESET}"
                      f"{EMPTY}{ects(free[semester])}{RESET}")

        # The chosen specialisation's modules, the label in light blue
        if semester in placed:
            colour = GROUP_COLOURS["Specialisation"]
            if chosen:
                for module in placed[semester]:
                    print(f"{module['name']:<{width}}{colour}{'Specialisation':<{LABEL_WIDTH}}{RESET}"
                          f"{ects(module['ects'])}")
            else:
                # Nothing chosen: one placeholder row for the 12 ECTS slot, dim italic
                print(f"{EMPTY}{'(choose a specialisation)':<{width}}{RESET}{colour}{'Specialisation':<{LABEL_WIDTH}}{RESET}"
                      f"{EMPTY}{ects(12)}{RESET}")
    print()
    print(f"{BOLD}Total: {total}/{TOTAL_ECTS} ECTS{RESET}")

    # The group filter, with the same menu and messages as the other screens
    print()
    print("Filter by group:")
    options = []
    for group in groups:
        options.append(group["short"])
    show_menu(options, "Back")
    while True:
        print()
        answer = input(
            f"{ARROW}Choose an option (0-{len(groups)}), or press Enter to skip: "
        ).strip()
        if answer == "0":
            return
        if answer == "":
            break
        if answer.isdigit() and 1 <= int(answer) <= len(groups):
            break
        show_warning(f"Please enter a number from 0 to {len(groups)}")
    if answer != "":
        selected_group = groups[int(answer) -1]
        print()
        print(f"{selected_group['name']} ({selected_group['ects']} ECTS)")
        for module in modules:
            if module.group == selected_group["name"]:
                print("  " + fit(f"S{module.semester}  {module.name}", ects(module.ects), APP_WIDTH - 2))
        pause()

def explore_specialisations(specialisations):
    """Show the specialisation and let the student pick one."""
    names = []
    for specialisation in specialisations:
        names.append(specialisation.name)
    while True:
        show_header("Explore specialisations")
        number = ask_menu(names)
        if number == 0:
            return
        specialisation = specialisations[number -1]
        show_header(specialisation.name)
        print(specialisation.focus)
        placed = place_specialisation(specialisation)
        total_ects = 0
        for semester in placed:
            print(f"\nSemester {semester}")
            for module in placed[semester]:
                show_bullet(module["name"], ects(module["ects"]))
                total_ects = total_ects + module["ects"]
        print(f"\nTotal: {total_ects} ECTS")
        print("\nPossible careers:")
        for career in specialisation.careers:
            show_bullet(career)
        pause() 