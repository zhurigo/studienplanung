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

    print("--- Degree plan ---")
    for semester in range(1, 9):
        print(f"Semester {semester}")
        for module in modules:
            if module.semester == semester:
                label = shorts.get(module.group, module.group)
                print(f"  {module.name:<{width}}{label:<22}"
                      f"{module.ects:>1} ECTS")
