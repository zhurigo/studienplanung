"""
Showing the degree plan and the specialisations.

Owner: Angelica (Browse)
User stories:
  1. See all modules per semester                       (Step 4)
  2. Filter modules by group, Enter skips the filter    (Step 4)
  3. Explore the three specialisations and their details (Step 5)

US1 is implemented here. US2 (the group filter) and US3 (the specialisation
screen) are still to write.

Added by Thalita (Plan, US4):
  - the chosen specialisation's modules in semesters 6 to 8 (place_specialisation)
"""

from planner.prompts import RESET, show_header


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

    show_header("Degree plan")
    for semester in range(1, 9):
        # Empty line between semesters, not right under the header
        if semester > 1:
            print()
        print(f"Semester {semester}")
        for module in modules:
            if module.semester == semester:
                label = shorts.get(module.group, module.group)
                # Colour the whole row in its group's colour
                colour = ""
                if module.group in GROUP_COLOURS:
                    colour = GROUP_COLOURS[module.group]
                print(f"{colour}{module.name:<{width}}{label:<22}"
                      f"{module.ects:>1} ECTS{RESET}")

        # The chosen specialisation's modules, in light blue
        if semester in placed:
            colour = GROUP_COLOURS["Specialisation"]
            if chosen:
                for module in placed[semester]:
                    print(f"{colour}{module['name']:<{width}}{'Specialisation':<22}"
                          f"{module['ects']:>1} ECTS{RESET}")
            else:
                # Nothing chosen: one placeholder row for the 12 ECTS slot
                print(f"  {colour}{'(choose a specialisation)':<{width}}{'Specialisation':<22}"
                      f"12 ECTS{RESET}")
