# studienplanung — User Stories

**Team:** Angelica Bertalli (`angio-eng`), Thalita dos Reis (`ThalitadosReis`), Hugo (`zhurigo`)
**Course:** Programming Foundations (BIT), AS 2026, Brugg

Each team member implements three user stories. Every story follows the template
*As a ⟨role⟩, I want ⟨goal⟩, so that ⟨benefit⟩* and has at least one acceptance criterion.

Acceptance criteria are written as *Given ⟨situation⟩, when ⟨action⟩, then ⟨expected result⟩*.

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

---

## Angelica — Browse

### US1: See modules per semester

> As a student, I want to see all modules per semester so I know what's coming.

**Acceptance criteria**

- **AC1** — _Happy path: the degree plan is shown, grouped by semester (what does each line show?)_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC2** — _Data comes from the file: what happens if the modules file is missing or can't be read?_
  - **Given** ___
  - **When** ___
  - **Then** ___

### US2: Filter modules by group

> As a student, I want to filter modules by group (e.g. Information Technology) so I see where my ECTS come from.

**Acceptance criteria**

- **AC1** — _Happy path: a valid group number is entered (what is listed, and what total is shown?)_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC2** — _Invalid input: a number outside the menu, or text instead of a number_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC3** — _Skip: the user presses Enter without choosing a group_
  - **Given** ___
  - **When** ___
  - **Then** ___

### US3: Explore the specialisations

> As a student, I want to explore the three specialisations so I can compare them.

**Acceptance criteria**

- **AC1** — _Happy path: the user picks a specialisation (which details must appear?)_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC2** — _Invalid input: a number outside 1–3 or text_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC3** — _Going back: the user enters 0_
  - **Given** ___
  - **When** ___
  - **Then** ___

---

## Thalita — Plan

### US4: Choose a specialisation

> As a student, I want to choose one specialisation and have it stored in my plan.

<!-- Missing the "so that ..." part of the template -->

**Acceptance criteria**

- **AC1** — _Happy path: no specialisation chosen yet, and the user picks a valid number (what is stored?)_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC2** — _Invalid input: a number outside 1–3 or text (what message, and does it ask again?)_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC3** — _Replacing: a specialisation is already chosen (confirm with y/n; what happens on each answer?)_
  - **Given** ___
  - **When** ___
  - **Then** ___

### US5: Pick electives with an ECTS counter

> As a student, I want to pick electives with an ECTS counter so I don't go over 12.

**Acceptance criteria**

- **AC1** — _Happy path: an elective that still fits under 12 ECTS is added (what does the counter show?)_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC2** — _Limit: an elective that would push the total over 12 ECTS_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC3** — _Invalid input / duplicates: a wrong number, or an elective that's already in the plan_
  - **Given** ___
  - **When** ___
  - **Then** ___

### US6: Remove or swap an elective

> As a student, I want to remove or swap an elective so I can change my plan.

**Acceptance criteria**

- **AC1** — _Happy path: an elective in the plan is removed (what happens to the counter?)_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC2** — _Nothing to remove: the plan has no electives yet_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC3** — _Invalid input: a number that isn't in the list of selected electives_
  - **Given** ___
  - **When** ___
  - **Then** ___

---

## Hugo — Check and save

### US7: Check my plan

> As a student, I want the app to check my plan and warn me about problems.

<!-- Missing the "so that ..." part of the template -->

**Acceptance criteria**

- **AC1** — _Complete plan: everything is filled in (what confirmation is shown?)_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC2** — _Incomplete plan: e.g. no specialisation or fewer than 12 elective ECTS (what warnings, with which numbers?)_
  - **Given** ___
  - **When** ___
  - **Then** ___

### US8: Save and load my plan

> As a student, I want to save and load my plan so it's there next time.

**Acceptance criteria**

- **AC1** — _Save: the user saves (which file, and what must be in it?)_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC2** — _Load: the app starts and a saved plan exists (what is restored?)_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC3** — _Error case: no saved file yet, or the file is damaged_
  - **Given** ___
  - **When** ___
  - **Then** ___

### US9: Progress toward 180 ECTS

> As a student, I want to see my planned ECTS per group and my progress toward 180.

<!-- Missing the "so that ..." part of the template -->

**Acceptance criteria**

- **AC1** — _Happy path: the report shows each group's planned/required ECTS_
  - **Given** ___
  - **When** ___
  - **Then** ___
- **AC2** — _Total: the progress toward 180 ECTS is shown as a number + percentage/bar (check with an incomplete plan)_
  - **Given** ___
  - **When** ___
  - **Then** ___
