"""
Checking the plan and showing the roadmap.

Owner: Hugo (Check and save)
User stories:
  7. Check my plan and list every problem            (Step 8)
  9. Personal 180-ECTS roadmap per semester          (Step 9)

US7 checks — return a list of warning texts; an empty list means the plan is OK:
  - a specialisation is chosen
  - electives reach 12 ECTS
  - no unknown specialisation or elective ids (my_plan.json can be hand-edited)
  - no duplicate electives
  - no more than 12 elective ECTS

US9 renders the personal 180-ECTS roadmap: the plan per semester with the
specialisation and electives in place, empty elective slots, and a progress
bar toward 180 (rounded down).

Both US7 and US9 live in this file.
"""

# A complete plan needs exactly this many elective ECTS
# (data/electives.json: info.elective_ects_required)
REQUIRED_ELECTIVE_ECTS = 12


# --- US7: check the plan ---

def check_plan(plan, specialisations, electives):
    """Return every problem with the plan. An empty list means it is OK."""
    problems = []

    # Sets of the ids that actually exist, so each lookup is one line
    known_specialisations = {
        specialisation.id for specialisation in specialisations
    }
    known_electives = {elective.id for elective in electives}

    # 1. A specialisation is chosen, and it exists
    if plan.specialisation_id is None:
        problems.append("No specialisation chosen.")
    elif plan.specialisation_id not in known_specialisations:
        problems.append(
            f"Unknown specialisation id: {plan.specialisation_id}"
        )

    # 2. The electives add up to exactly 12 ECTS
    total = sum(elective.ects for elective in plan.electives)
    if total < REQUIRED_ELECTIVE_ECTS:
        missing = REQUIRED_ELECTIVE_ECTS - total
        problems.append(
            f"Electives: {total}/{REQUIRED_ELECTIVE_ECTS} ECTS"
            f" — {missing} ECTS missing."
        )
    elif total > REQUIRED_ELECTIVE_ECTS:
        extra = total - REQUIRED_ELECTIVE_ECTS
        problems.append(
            f"Electives: {total}/{REQUIRED_ELECTIVE_ECTS} ECTS"
            f" — {extra} ECTS over the limit."
        )

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


# --- US9: personal 180-ECTS roadmap ---

# TODO (Hugo): write the roadmap function.
