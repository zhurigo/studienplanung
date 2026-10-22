"""
Showing the degree plan and the specialisations.

Owner: Angelica (Browse)
User stories:
  1. See all modules per semester                       (Step 4)
  2. Filter modules by group, Enter skips the filter    (Step 4)
  3. Explore the three specialisations and their details (Step 5)

US1 is implemented here. US2 (the group filter) and US3 (the specialisation
screen) are still to write.
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


def show_degree_plan(modules, groups):
    """US1: print every module, grouped by semester 1 to 8."""
    # The rows show the short group label ("BIT"), but the data stores the
    # long name ("Business Information Technology"), so build a lookup.
    shorts = {}
    for group in groups:
        shorts[group["name"]] = group["short"]

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
                print(f"  {colour}{module.name:<{width}}{label:<22}"
                      f"{module.ects:>1} ECTS{RESET}")
