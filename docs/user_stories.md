# studienplanung — User Stories

**Team:** Angelica Bertalli (`angio-eng`), Thalita dos Reis (`ThalitadosReis`), Hugo Antero (`zhurigo`)

Each team member implements three user stories. Every story follows the template
_As a ⟨role⟩, I want ⟨goal⟩, so that ⟨benefit⟩_ and has at least one acceptance criterion.

Acceptance criteria are written as _Given ⟨situation⟩, when ⟨action⟩, then ⟨expected result⟩_.

| #   | Owner    | Area           | Course criteria shown         |
| --- | -------- | -------------- | ----------------------------- |
| 1   | Angelica | Browse         | Interactive, file reading     |
| 2   | Angelica | Browse         | Interactive, input validation |
| 3   | Angelica | Browse         | Interactive, file reading     |
| 4   | Thalita  | Plan           | Input validation              |
| 5   | Thalita  | Plan           | Input validation              |
| 6   | Thalita  | Plan           | Input validation              |
| 7   | Hugo     | Check and save | Data validation               |
| 8   | Hugo     | Check and save | File writing and reading      |
| 9   | Hugo     | Check and save | Interactive                   |

## Angelica — Browse

### US1: See modules per semester

> As a student, I want to see all modules per semester so that I know what's coming.

**Acceptance criteria**

- **AC1** — _Happy path: the degree plan is shown, grouped by semester_
  - **Given** the modules are loaded from `data/`
  - **When** I choose "View degree plan" from the main menu
  - **Then** I can see all modules sorted by semester (1 to 8) with their name, group and ECTS
- **AC2** — _Data comes from the file_
  - **Given** `data/modules.json` is missing or contains invalid data
  - **When** I start the app
  - **Then** I see an error message with the file name and the app stops

### US2: Filter modules by group

> As a student, I want to filter modules by group (e.g. Information Technology) so that I see where my ECTS come from.

**Acceptance criteria**

- **AC1** — _Happy path: a valid group number is entered_
  - **Given** the degree plan is displayed
  - **When** I choose 4 (IT)
  - **Then** I only see the IT modules with their semester and ECTS
- **AC2** — _Invalid input: a number outside the menu, or text instead of a number_
  - **Given** the degree plan is shown
  - **When** I enter a wrong number (e.g. `9`) or text (e.g. `abc`)
  - **Then** I see the message "Please enter a number from 1 to 7." and I can try again
- **AC3**
  - **Given** the degree plan is shown
  - **When** I press Enter without typing anything
  - **Then** I go back to the main menu without applying a filter

### US3: Explore the specialisations

> As a student, I want to explore the three specialisations so that I can compare them.

**Acceptance criteria**

- **AC1** — _Happy path: the user picks a specialisation_
  - **Given** I am in "Explore specialisations"
  - **When** I choose `3`
  - **Then** I can see the Digital Trust specialisation with its ECTS, semesters, modules and career options
- **AC2** — _Invalid input: a number outside 0-3_
  - **Given** I am in "Explore specialisations"
  - **When** I enter a number that is not between 0 and 3, or I enter text
  - **Then** the app shows "Please enter a number from 0 to 3." and asks me to try again
- **AC3** — _Going back: the user enters 0_
  - **Given** I am in "Explore specialisations"
  - **When** I enter `0`
  - **Then** I will go back to the main menu

## Thalita — Plan

### US4: Choose a specialisation

> As a student, I want to choose one specialisation and have it stored in my plan, so that I can plan my electives around it.

**Acceptance criteria**

- **AC1**
  - **Given** I haven't picked a specialisation yet
  - **When** I type `3` in "Choose specialisation"
  - **Then** Digital Trust gets saved in my plan, and next time I get to open the menu it will show up as my current choice
- **AC2**
  - **Given** I'm in "Choose specialisation"
  - **When** I type something wrong, like a word or an option that is not available, e.g. `5`
  - **Then** the app will tell me to enter a number from 1 to 3 and let me try again, and nothing in my plan changes
- **AC3**
  - **Given** I already picked a specialisation, e.g. Digital Trust
  - **When** I pick a different one
  - **Then** it asks me first if I really want to replace it: `n` keeps Digital Trust, `y` swaps it for the new one

### US5: Pick electives with an ECTS counter

> As a student, I want to pick electives with an ECTS counter so that I don't go over 12.

**Acceptance criteria**

- **AC1**
  - **Given** I have 6 of 12 ECTS of electives so far
  - **When** I add a 3-ECTS elective, e.g. Spanish A1
  - **Then** it is added and the counter goes up to 9/12
- **AC2**
  - **Given** I have 9 of 12 ECTS
  - **When** I try to add a 6-ECTS elective
  - **Then** the app doesn't add it and shows me why: it would take me to 15/12 ECTS and I only have 3 ECTS left. The counter stays at 9/12
- **AC3**
  - **Given** I'm looking at the electives in a category
  - **When** I type a number that isn't on the list or pick one I already have
  - **Then** the app tells me what's wrong and doesn't add anything

### US6: Remove or swap an elective

> As a student, I want to remove or swap an elective so that I can change my plan.

Swapping is done by removing an elective and adding another in its place — there is no separate "swap" action.

**Acceptance criteria**

- **AC1**
  - **Given** I have Spanish A1 (3 ECTS) in my plan and I'm at 6/12
  - **When** I remove Spanish A1
  - **Then** it is removed from my plan and the counter will update to 3/12
- **AC2**
  - **Given** I don't have any electives yet
  - **When** I go to "Remove an elective"
  - **Then** the app tells me there's nothing that can be removed and takes me back to the electives menu
- **AC3**
  - **Given** I have Spanish A1 (3 ECTS) in my plan and I'm at 9/12
  - **When** I swap Spanish A1 for the Spanish intensive course A1/A2 (6 ECTS) by removing it and adding the intensive course
  - **Then** Spanish A1 is replaced by the intensive course and the counter goes up to 12/12

## Hugo — Check and save

### US7: Check my plan

> As a student, I want the app to check my current plan (built in the app or loaded from `my_plan.json`) and warn me about problems, so that I can fix them before I finalise my plan.

**Acceptance criteria**

- **AC1** — _Valid plan: everything is filled in and consistent_
  - **Given** a current plan with a known specialisation, 12/12 elective ECTS and no duplicate electives
  - **When** I choose "Check my plan"
  - **Then** the app shows no warnings and confirms "Your plan is complete (180/180 ECTS)."
- **AC2** — _Missing pieces: no specialisation, or fewer than 12 elective ECTS_
  - **Given** a current plan with no specialisation and 9/12 elective ECTS
  - **When** I choose "Check my plan"
  - **Then** the app prints one line per problem, e.g. "No specialisation chosen." and "Electives: 9/12 ECTS — 3 ECTS missing."
- **AC3** — _Unknown ids: `my_plan.json` was hand-edited to an id that is not in `data/`_
  - **Given** a current plan that references a specialisation id or an elective id not present in the data files
  - **When** I choose "Check my plan"
  - **Then** each unknown id is reported as a warning (e.g. "Unknown elective id: LANG-XX") and the app continues without crashing
- **AC4** — _Duplicates and over-limit: the plan lists the same elective twice, or more than 12 elective ECTS_
  - **Given** a current plan with one elective listed twice, or 15/12 elective ECTS
  - **When** I choose "Check my plan"
  - **Then** the app warns "Elective listed twice: Spanish A1" and/or "Electives: 15/12 ECTS — 3 ECTS over the limit"

### US8: Save and load my plan

> As a student, I want to save and load my plan so that it is there next time.

**Acceptance criteria**

- **AC1** — _Save: the user saves_
  - **Given** I have chosen the specialisation "Digital Trust" (id `DT`) and two electives
  - **When** I choose "Save plan"
  - **Then** the app writes `my_plan.json` containing the specialisation id and the ids of both electives, and confirms "Plan saved to my_plan.json."
- **AC2** — _Load: the app starts and a saved plan exists_
  - **Given** a valid `my_plan.json` exists from a previous session
  - **When** I start the app and answer `y` to "A saved plan was found. Load it? (y/n):"
  - **Then** my specialisation and electives are restored and shown, e.g. "Plan loaded: Digital Trust, 2 electives (6/12 ECTS)"
- **AC3** — _Error case: no saved file yet, or the file is damaged_
  - **Given** there is no `my_plan.json`, or the file exists but is damaged or unreadable
  - **When** I start the app
  - **Then** a missing file starts quietly with an empty plan, a damaged file shows "Could not read my_plan.json — starting with an empty plan.", and the app continues without crashing in either case. A file that is not valid JSON counts as damaged; a file that is valid JSON but contains unknown ids still loads, and US7 reports the problem
- **AC4** — _Unsaved changes on exit: the user quits with changes not yet saved_
  - **Given** I have changed my plan since the last save and choose "Exit"
  - **When** I am asked "You have unsaved changes. Save now? (y/n):"
  - **Then** `y` saves the plan and exits, `n` exits without saving, and the prompt is not shown at all if there is nothing unsaved

### US9: Personal 180-ECTS roadmap

> As a student, I want to see my personal 180-ECTS roadmap per semester, with my specialisation and electives in place, so that I can see how my choices fit into my studies.

An elective **slot** is 3 ECTS: a 6-ECTS elective fills two slots, and the four slots together are the 12 elective ECTS.

**Acceptance criteria**

- **AC1** — _Layout: the roadmap lists all 180 ECTS by semester (1–8)_
  - **Given** a current plan
  - **When** I choose "Roadmap"
  - **Then** every semester is listed with its modules and ECTS, my chosen specialisation is shown as one block for semesters 6–8 (36 ECTS, since module names are provisional), and my electives are listed in their own Electives section
- **AC2** — _Slots: empty elective slots are visible_
  - **Given** a plan with only 2 of the 4 elective slots filled
  - **When** I open the roadmap
  - **Then** the remaining elective slots are shown as empty, e.g. "Elective slot 3 — empty"
- **AC3** — _Reacts to changes: the roadmap follows the current plan_
  - **Given** I have just changed my specialisation or an elective
  - **When** I open the roadmap again
  - **Then** the affected semesters reflect the change
- **AC4** — _Progress: total ECTS toward 180 are shown, rounded down_
  - **Given** my plan totals 177 ECTS
  - **When** I open the roadmap
  - **Then** the total reads "177/180 ECTS (98%)" and the progress bar length is rounded down (a 20-character bar holds 19 `#`)
- **AC5** — _No specialisation yet: the roadmap still opens_
  - **Given** a plan with electives but no specialisation chosen
  - **When** I open the roadmap
  - **Then** the specialisation semesters (6–8) read "Specialisation — not chosen yet" and the rest of the roadmap still renders
