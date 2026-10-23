"""
The classes that hold the data.

Owner: whole team for the basic classes (CW 42), then
       Thalita adds the StudentPlan methods for stories 4, 5 and 6.

Classes to write:
  Module          name, semester, group, ects, project_based
  Specialisation  id, name, focus, modules, builds_on, careers
  Elective        id, name, category, ects, semester, campus
  StudentPlan     specialisation_id (one or none), electives (list)

StudentPlan needs, for example:
  - choosing / replacing the specialisation     (story 4, Thalita)
  - adding an elective, max 12 ECTS, no doubles  (story 5, Thalita)
  - removing an elective                         (story 6, Thalita)
  - total elective ECTS                          (used by stories 7 and 9)

Useful: classes, or @dataclass from the dataclasses module
"""

# --- Data from the files ---

class Module:
    """One module of the degree plan (from data/modules.json)."""

    def __init__(self, name, semester, group, ects, project_based):
        self.name = name
        self.semester = semester
        self.group = group
        self.ects = ects
        self.project_based = project_based
        
class Specialisation:
    """One of the three specialisations (from data/specialisations.json)."""

    def __init__(self, id, name, focus, modules, builds_on, careers):
        self.id = id
        self.name = name
        self.focus = focus
        self.modules = modules
        self.builds_on = builds_on
        self.careers = careers


class Elective:
    """One elective module (from data/electives.json)."""

    def __init__(self, id, name, category, ects, semester, campus):
        self.id = id
        self.name = name
        self.category = category
        self.ects = ects
        self.semester = semester
        self.campus = campus


# --- The student's choices ---

class StudentPlan:
    """The student's plan: one specialisation (or none) and a list of electives."""

    def __init__(self):
        # Nothing is chosen when the program starts
        self.specialisation_id = None
        self.electives = []

    # --- US4 (Thalita) ---

    def choose_specialisation(self, specialisation_id):
        """Save the chosen specialisation, replacing any earlier one."""
        self.specialisation_id = specialisation_id
