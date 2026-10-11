# studienplanung — User Stories

**Team:** Angelica Bertalli (`angio-eng`), Thalita dos Reis (`ThalitadosReis`), Hugo (`zhurigo`)

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

> As a student, I want to see all modules per semester so I know what's coming.

**Acceptance criteria**

- **AC1** — _Happy path: the degree plan is shown, grouped by semester (what does each line show?)_
  - **Given** the modules are loaded from `data/`
  - **When** I choose "View degree plan" from the main menu
  - **Then** I can see all modules sorted by semester (1 to 8) with their name, group and ECTS
- **AC2** — _Data comes from the file: what happens if the modules file is missing or can't be read?_
  - **Given** `data/modules.json` is missing or contains invalid data
  - **When** I start the app
  - **Then** I see an error message with the file name and the app stops
- **AC3**
  - **Given** I am in "Explore specialisations" @angie-eng <!-- Does this belong here? Or should it be exclusive to US3? -->
  - **When** I enter `0`
  - **Then** I go back to the main menu

### US2: Filter modules by group

> As a student, I want to filter modules by group (e.g. Information Technology) so I see where my ECTS come from.

**Acceptance criteria**

- **AC1** — _Happy path: a valid group number is entered (what is listed, and what total is shown?)_
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

> As a student, I want to explore the three specialisations so I can compare them.

**Acceptance criteria**

- **AC1** — _Happy path: the user picks a specialisation (which details must appear?)_
  - **Given** I am in "Explore specialisations"
  - **When** I choose `3`
  - **Then** I can see the Digital Trust specialisation with its ECTS, semesters, modules and career options
- **AC2** — _Invalid input: a number outs I am in "Explore specialisations" @angio-eng <!-- What do you mean here? I can see it's a typo but cound't make sense of it to correct it :) -->
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

> As a student, I want to pick electives with an ECTS counter so I don't go over 12.

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

> As a student, I want to remove or swap an elective so I can change my plan.

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
  - **When** I swap Spanish A1 for the Spanish intensive course A1/A2 (6 ECTS)
  - **Then** Spanish A1 is replaced by the intensive course and the counter goes up to 12/12

## Hugo — Check and save

### US7: Check my plan

> As a student, I want the app to check my plan and warn me about problems, so that I can fix them before I finalise my plan.

**Acceptance criteria**

- **AC1** — _Complete plan: everything is filled in (what confirmation is shown?)_
  - **Given** a plan where a specialisation is chosen, 12/12 elective ECTS are selected and every group meets its target (180/180 ECTS total)
  - **When** I choose "Check my plan"
  - **Then** the app shows no warnings and confirms "Your plan is complete (180/180 ECTS)."
- **AC2** — _Incomplete plan: e.g. no specialisation or fewer than 12 elective ECTS (what warnings, with which numbers?)_
  - **Given** a plan with no specialisation chosen, 9/12 elective ECTS and 177/180 total ECTS
  - **When** I choose "Check my plan"
  - **Then** the app lists each problem on its own line, e.g. "No specialisation chosen.", "Electives: 9/12 ECTS — 3 ECTS missing.", "Total: 177/180 ECTS — 3 ECTS missing."
- **AC3** — _Empty plan: nothing chosen yet (does it crash?)_
  - **Given** a brand-new plan with no specialisation and no electives
  - **When** I choose "Check my plan"
  - **Then** the app lists the missing items and does not crash

### US8: Save and load my plan

> As a student, I want to save and load my plan so it's there next time.

**Acceptance criteria**

- **AC1** — _Save: the user saves (which file, and what must be in it?)_
  - **Given** I have chosen the specialisation "Digital Trust" (id `DT`) and two electives
  - **When** I choose "Save plan"
  - **Then** the app writes `my_plan.json` containing the specialisation id and the ids of both electives, and confirms "Plan saved to my_plan.json."
- **AC2** — _Load: the app starts and a saved plan exists (what is restored?)_
  - **Given** a valid `my_plan.json` exists from a previous session
  - **When** I start the app and answer `y` to "A saved plan was found. Load it? (y/n):"
  - **Then** my specialisation and electives are restored and shown, e.g. "Plan loaded: Digital Trust, 2 electives (6/12 ECTS)"
- **AC3** — _Error case: no saved file yet, or the file is damaged_
  - **Given** there is no `my_plan.json`, or the file exists but is damaged or unreadable
  - **When** I start the app
  - **Then** a missing file starts an empty plan without a load question, a damaged file shows a clear message, and the app does not crash in either case

### US9: Progress toward 180 ECTS

> As a student, I want to see my planned ECTS per group and my progress toward 180, so that I know how much is still missing.

**Acceptance criteria**

- **AC1** — _Happy path: the report shows each group's planned/required ECTS_
  - **Given** a plan with a specialisation and some electives
  - **When** I choose "Progress report"
  - **Then** each group from `data/modules.json` is listed as planned/required ECTS, e.g. "Foundation 24/24", "BIT 33/33", "Electives 9/12"
- **AC2** — _Total: the progress toward 180 ECTS is shown as a number + percentage/bar (check with an incomplete plan)_
  - **Given** my plan totals 177 ECTS
  - **When** I choose "Progress report"
  - **Then** the app shows the total as "177/180 ECTS (98%)" with a progress bar
- **AC3** — _Update: the numbers follow the current plan_
  - **Given** I have just added or removed an elective
  - **When** I open the progress report again
  - **Then** the per-group and total ECTS reflect the change
