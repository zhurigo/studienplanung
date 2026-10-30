"""
Checking the plan and showing the roadmap.

Owner: Hugo (Check and save)
User stories:
  7. Check my plan and list every problem            (Step 8)
  9. Personal 180-ECTS roadmap per semester          (Step 9)

US7 checks — return warning texts; an empty list means the plan is OK:
  - a specialisation is chosen
  - electives reach 12 ECTS
  - no unknown specialisation or elective ids (my_plan.json can be hand-edited)
  - no duplicate electives
  - no more than 12 elective ECTS

US9 renders the personal 180-ECTS roadmap: the plan per semester with the
specialisation and electives in place, the remaining elective ECTS, and a
progress bar toward 180 (rounded down). The elective wording is shared with
US7 through elective_line.

Both US7 and US9 live in this file.
"""

from planner.prompts import pause, show_header, show_success, show_warning

# A complete plan needs exactly this many elective ECTS
# (data/electives.json: info.elective_ects_required)
REQUIRED_ELECTIVE_ECTS = 12

# The roadmap counts a chosen specialisation as one 36-ECTS block
# (data/specialisations.json: ects)
SPECIALISATION_ECTS = 36
TOTAL_ECTS = 180
BAR_WIDTH = 20

# The name column is never narrower than this, like in the degree plan
MIN_NAME_WIDTH = 31

# The label column is 22 wide, as on the degree-plan screen
LABEL_WIDTH = 22


# --- Wording shared by US7 and US9 ---

def elective_line(total):
    """Return the line about missing or extra elective ECTS, or None."""
    if total < REQUIRED_ELECTIVE_ECTS:
        missing = REQUIRED_ELECTIVE_ECTS - total
        return (
            f"Electives: {total}/{REQUIRED_ELECTIVE_ECTS} ECTS"
            f" — {missing} ECTS missing."
        )
    if total > REQUIRED_ELECTIVE_ECTS:
        extra = total - REQUIRED_ELECTIVE_ECTS
        return (
            f"Electives: {total}/{REQUIRED_ELECTIVE_ECTS} ECTS"
            f" — {extra} ECTS over the limit."
        )
    return None


# --- US7: check the plan ---

def check_plan(plan, specialisations, electives):
    """Return every problem with the plan. An empty list means it is OK."""
    problems = []

    # Sets of the ids that actually exist, so each lookup is one line
    known_specialisations = set()
    for specialisation in specialisations:
        known_specialisations.add(specialisation.id)

    known_electives = set()
    for elective in electives:
        known_electives.add(elective.id)

    # 1. A specialisation is chosen, and it exists
    if plan.specialisation_id is None:
        problems.append("No specialisation chosen.")
    elif plan.specialisation_id not in known_specialisations:
        problems.append(
            f"Unknown specialisation id: {plan.specialisation_id}"
        )

    # 2. The electives add up to exactly 12 ECTS
    total = plan.total_elective_ects()
    line = elective_line(total)
    if line is not None:
        problems.append(line)

    # 3. Every elective id exists in the catalogue
    for elective in plan.electives:
        if elective.id not in known_electives:
            problems.append(f"Unknown elective id: {elective.id}")

    # 4. No elective is chosen twice
    counts = {}
    names = {}
    for elective in plan.electives:
        counts[elective.id] = counts.get(elective.id, 0) + 1
        names[elective.id] = elective.name
    for elective_id, count in counts.items():
        if count > 1:
            problems.append(
                f"Elective listed twice: {names[elective_id]}"
            )

    return problems


def show_plan_check(plan, specialisations, electives):
    """US7: print every problem with the plan, then wait for Enter."""
    problems = check_plan(plan, specialisations, electives)

    show_header("Plan check")
    if not problems:
        show_success("Your plan is complete (180/180 ECTS).")
        pause()
        return

    for problem in problems:
        show_warning(problem)

    if len(problems) == 1:
        prompt = "1 warning. Press Enter to return. "
    else:
        prompt = f"{len(problems)} warnings. Press Enter to return. "
    pause(prompt)


# --- US9: personal 180-ECTS roadmap ---

def find_specialisation(plan, specialisations):
    """Return the chosen specialisation, or None."""
    for specialisation in specialisations:
        if specialisation.id == plan.specialisation_id:
            return specialisation
    return None


def roadmap_total(plan, modules, specialisations):
    """Return the ECTS the plan reaches so far, out of 180."""
    total = 0
    for module in modules:
        total = total + module.ects

    # An unknown or missing specialisation counts as not chosen yet
    specialisation = find_specialisation(plan, specialisations)
    if specialisation is not None:
        total = total + SPECIALISATION_ECTS

    total = total + plan.total_elective_ects()
    return total


def progress_bar(total):
    """Return a bar like [###---], rounded down and at most BAR_WIDTH long."""
    filled = total * BAR_WIDTH // TOTAL_ECTS
    # A hand-edited my_plan.json can go above 180 ECTS
    if filled > BAR_WIDTH:
        filled = BAR_WIDTH
    empty = BAR_WIDTH - filled
    return "[" + "#" * filled + "-" * empty + "]"


def name_width(names):
    """Return a column width that fits the longest name."""
    longest = 0
    for name in names:
        if len(name) > longest:
            longest = len(name)
    # 3 spaces between the name and the next column
    return max(MIN_NAME_WIDTH, longest + 3)


def show_roadmap(plan, modules, groups, specialisations):
    """Print the plan as a roadmap from semester 1 to 8."""
    shorts = {}
    for group in groups:
        shorts[group["name"]] = group["short"]

    specialisation = find_specialisation(plan, specialisations)

    names = []
    for module in modules:
        names.append(module.name)
    for elective in plan.electives:
        names.append(elective.name)
    if specialisation is not None:
        names.append(specialisation.name + " modules")
    width = name_width(names)

    show_header("Roadmap")
    for semester in range(1, 9):
        if semester > 1:
            print()
        print(f"Semester {semester}")
        for module in modules:
            if module.semester == semester:
                label = shorts.get(module.group, module.group)
                print(f"  {module.name:<{width}}{label:<{LABEL_WIDTH}}"
                      f"{module.ects:>2} ECTS")

    print()
    print("Semesters 6-8 (specialisation)")
    if specialisation is not None:
        print(f"  {specialisation.name + ' modules':<{width}}"
              f"{'':<{LABEL_WIDTH}}{SPECIALISATION_ECTS:>2} ECTS")
    else:
        print("  Specialisation — not chosen yet")

    print()
    print("Electives")
    for elective in plan.electives:
        print(f"  {elective.name:<{width}}{'Elective':<{LABEL_WIDTH}}"
              f"{elective.ects:>2} ECTS")
    line = elective_line(plan.total_elective_ects())
    if line is not None:
        print(f"  {line}")

    total = roadmap_total(plan, modules, specialisations)
    percent = total * 100 // TOTAL_ECTS
    print()
    print(f"Total  {progress_bar(total)}  {total}/{TOTAL_ECTS} ECTS "
          f"({percent}%)")

    pause()
