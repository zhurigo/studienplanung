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

# TODO (Hugo): write the check and roadmap functions.
