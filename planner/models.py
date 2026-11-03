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
        # The semester (3 to 6) the student picked for each elective, by id
        self.elective_semesters = {}

    # --- US4 (Thalita) ---

    def choose_specialisation(self, specialisation_id):
        """Save the chosen specialisation, replacing any earlier one."""
        self.specialisation_id = specialisation_id

    # --- US5 (Thalita) ---

    def total_elective_ects(self):
        """Add up the ECTS of all chosen electives."""
        total = 0
        for elective in self.electives:
            total = total + elective.ects
        return total

    def ects_left(self):
        """How many elective ECTS can still be added before reaching 12."""
        return 12 - self.total_elective_ects()

    def has_elective(self, elective_id):
        """True if the elective is already in the plan."""
        for elective in self.electives:
            if elective.id == elective_id:
                return True
        return False

    def add_elective(self, elective, semester=None):
        """Add the elective if it is new and fits in 12 ECTS. Returns True if added.
        semester is the semester the student picked for it (None = not picked)."""
        if self.has_elective(elective.id):
            return False
        if elective.ects > self.ects_left():
            return False
        self.electives.append(elective)
        if semester is not None:
            self.elective_semesters[elective.id] = semester
        return True

    def semester_of(self, elective_id):
        """The semester picked for the elective, or None if none was picked."""
        if elective_id in self.elective_semesters:
            return self.elective_semesters[elective_id]
        return None

    def fill_missing_semesters(self):
        """Give every elective without a semester the first one of its season,
        e.g. in a plan saved before the semesters were picked: FS -> 4, HS and HS/FS -> 3."""
        for elective in self.electives:
            if elective.id not in self.elective_semesters:
                if elective.semester == "FS":
                    self.elective_semesters[elective.id] = 4
                else:
                    self.elective_semesters[elective.id] = 3

    # --- US6 (Thalita) ---

    def remove_elective(self, elective_id):
        """Remove the elective with this id from the plan."""
        for elective in self.electives:
            if elective.id == elective_id:
                self.electives.remove(elective)
                # Forget its semester too
                if elective_id in self.elective_semesters:
                    del self.elective_semesters[elective_id]
                return
