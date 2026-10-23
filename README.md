# studienplanung — BIT Study Planner

An interactive command-line tool that helps FHNW Business Information Technology (BIT) students choose a specialisation and 12 ECTS of electives, then generates a personal 180-ECTS study roadmap.

## The problem

In the BIT programme you pick one of three specialisations and 12 ECTS of electives (each elective is worth 2, 3, 5 or 6 ECTS, so the number you pick varies), but the information needed to decide is spread across the FHNW programme page and many individual module descriptions. It is also hard to see how a single swap changes the whole 180-ECTS plan. This tool brings the choices into one place and keeps the plan consistent as you change it.

## What it does

- **Shows the degree plan**: all modules per semester, filterable by group (e.g. Information Technology).
- **Lets you explore** the three specialisations (Business Analytics and Data Science, Digital Business Management, Digital Trust) and the elective categories.
- **Builds your plan**: one specialisation (36 ECTS — 30 core modules plus 6 flexible) plus 12 ECTS of electives (any mix of 2, 3, 5 or 6 ECTS), with an ECTS counter that stops at 12.
- **Lets you swap**: remove an elective and add another in its place (swap = remove, then add); the roadmap changes with it.
- **Shows your roadmap**: your personal 180-ECTS plan per semester, with your specialisation and electives in place, the remaining elective ECTS flagged as still to fill, and a progress bar toward 180.
- **Checks and saves**: warns about problems in the plan and saves it to `my_plan.json`.

## Scope (MVP)

| In                                                                | Out                                                               |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| Console application (interactive, with input validation)          | Graphical or web interface                                        |
| Browsing the degree plan, filtered by group                       | Questionnaire-based specialisation suggestion (planned after MVP) |
| Choosing one specialisation and 12 ECTS of electives              | Languages of instruction other than English                       |
| Full 180-ECTS roadmap per semester that updates with every change | Official specialisation modules (names are placeholders)          |
| Plan check and personal roadmap                                   | Multiple users or accounts                                        |
| Save / load of a single plan (`my_plan.json`)                     |                                                                   |

## How to run

Requires Python 3.12 or newer.

```bash
# 1. Create the virtual environment (first time only)
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Start the planner
python main.py

# Run the tests
python -m unittest discover tests
```

The app reads its curriculum data from the `data/` folder on start-up. If a file is missing or broken it prints an error and stops.

```
studienplanung/
├── main.py          # entry point and main menu
├── planner/         # planning logic
├── data/            # modules, specialisations and electives
├── docs/            # user stories with acceptance criteria
├── tests/
└── my_plan.json     # your saved plan (created on first save)
```

## Team

| Member            | GitHub           | Area           | User stories |
| ----------------- | ---------------- | -------------- | ------------ |
| Angelica Bertalli | `angio-eng`      | Browse         | 1, 2, 3      |
| Thalita dos Reis  | `ThalitadosReis` | Plan           | 4, 5, 6      |
| Hugo Antero       | `zhurigo`        | Check and save | 7, 8, 9      |

## User stories

Each team member implements three user stories. The last column shows which course requirement the story demonstrates. The acceptance criteria for every story are in [docs/user_stories.md](docs/user_stories.md).

| Owner                 | #   | User story                                                                                                                                                                           | Course requirement shown      |
| --------------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------- |
| Angelica (Browse)     | 1   | As a student, I want to see all modules per semester so that I know what's coming.                                                                                                   | Interactive, file reading     |
| Angelica (Browse)     | 2   | As a student, I want to filter modules by group (e.g. Information Technology) so that I see where my ECTS come from.                                                                 | Interactive, input validation |
| Angelica (Browse)     | 3   | As a student, I want to explore the three specialisations so that I can compare them.                                                                                                | Interactive, file reading     |
| Thalita (Plan)        | 4   | As a student, I want to choose one specialisation and have it stored in my plan, so that I can plan my electives around it.                                                          | Input validation              |
| Thalita (Plan)        | 5   | As a student, I want to pick electives with an ECTS counter so that I don't go over 12.                                                                                              | Input validation              |
| Thalita (Plan)        | 6   | As a student, I want to remove or swap an elective so that I can change my plan.                                                                                                     | Input validation              |
| Hugo (Check and save) | 7   | As a student, I want the app to check my current plan (built in the app or loaded from `my_plan.json`) and warn me about problems, so that I can fix them before I finalise my plan. | Data validation               |
| Hugo (Check and save) | 8   | As a student, I want to save and load my plan so that it is there next time.                                                                                                         | File writing and reading      |
| Hugo (Check and save) | 9   | As a student, I want to see my personal 180-ECTS roadmap per semester, with my specialisation and electives in place, so that I can see how my choices fit into my studies.          | Interactive                   |

## How it works

A step-by-step walkthrough of a typical session.

### Step 1: Start and welcome

The app loads the data files from the `data/` folder and shows how much it found. If a file is missing or broken, it prints an error and stops.

```
=======================================================
           Welcome to the BIT Study Planner
   FHNW School of Business · Academic year 2026/2027
=======================================================
Loaded 28 modules, 3 specialisations and 22 electives.
```

### Step 2: Load a saved plan

If a saved plan (`my_plan.json`) exists, the app asks whether to load it. Answer `y` or `n`.

```
A saved plan was found. Load it? (y/n): yes
Please enter y or n.
A saved plan was found. Load it? (y/n): y
Plan loaded: Digital Trust, 2 electives (6/12 ECTS).
```

### Step 3: Main menu

The main menu appears after every action. Enter the number of the option you want.

```
--- Main menu ---
1. View degree plan
2. Explore specialisations
3. Choose specialisation
4. Plan electives
5. Check my plan
6. Roadmap
7. Save plan
0. Exit
Choose an option (0-7): abc
Please enter a number from 0 to 7.
Choose an option (0-7): 1
```

### Step 4: View degree plan

Shows all modules per semester with their group and ECTS. You can then filter by group, or press Enter to skip.

```
--- Degree plan ---
Semester 1
  Applied Mathematics 1          Foundation            3 ECTS
  Statistics 1                   Foundation            3 ECTS
  Principles of Management       Business Admin.       6 ECTS
  Digital Business               BIT                   6 ECTS
  Programming Foundations        IT                    6 ECTS
Semester 2
  ...

Filter by group? 1 Foundation, 2 Business Admin., 3 BIT,
4 IT, 5 Student Work, 6 Specialisation, 7 Electives
Enter a number, or press Enter to skip: 4

Information Technology (27 ECTS)
  S1  Programming Foundations    6 ECTS
  S2  Advanced Programming       6 ECTS
  S3  Database Technology        6 ECTS
  S4  Web-based Applications     6 ECTS
  S5  IT Security                3 ECTS
```

### Step 5: Explore specialisations

Lists the three specialisations. Pick one to see its focus, modules, related earlier modules and career paths.

```
--- Specialisations ---
1. Business Analytics and Data Science
2. Digital Business Management
3. Digital Trust
Pick one to see details (0 to go back): 3

Digital Trust (36 ECTS, semesters 6-8)
Focus:     Cybersecurity, data protection, IS audit and compliance
Modules:   4 x 6 + 2 x 3 ECTS = 30 core (names provisional)
Flexible:  6 ECTS from other specialisations or a Job Reflection
Builds on: IT Security, Digital Law, Digital Ethics
Careers:   Cybersecurity Consultant, IS and IT Consultant, Compliance Officer, IS and IT Auditor
```

### Step 6: Choose specialisation

Your plan can hold one specialisation. If you already chose one, the app asks before replacing it.

```
--- Choose specialisation ---
Current choice: Digital Trust
1. Business Analytics and Data Science
2. Digital Business Management
3. Digital Trust
Pick one (0 to go back): 5
Please enter a number from 0 to 3.
Pick one (0 to go back): 1
Replace Digital Trust with Business Analytics and Data Science? (y/n): n
Kept Digital Trust.
```

### Step 7: Plan electives

Add or remove electives — to swap, remove one elective and add another in its place (there is no separate swap action). First pick a category, then a module; each elective shows its ECTS, semester (HS = autumn, FS = spring) and campus. Electives are worth 2, 3, 5 or 6 ECTS each, so the number you pick varies — the total must reach exactly 12 ECTS. The counter never goes above 12 ECTS, and you can't pick the same elective twice.

```
--- Plan electives ---
Selected: 6/12 ECTS (German Basic A1, Italian A1)
1. Add an elective
2. Remove an elective
0. Back
Choose (0-2): 1

--- Categories ---
1. Languages (10)
2. Technology (8)
3. Business and Management (2)
4. Job Reflection (2)
Choose a category (0 to go back): 1

--- Languages ---
 1. Chinese Basic Communication A1      3 ECTS   HS/FS   Olten, Windisch
 2. Chinese Basic Communication A2      3 ECTS   HS      Olten
 3. French B1-B2                        3 ECTS   HS      Olten
 4. German Basic A1                     3 ECTS   HS/FS   Olten
 5. Italian A1                          3 ECTS   HS      Basel, Windisch
 6. Japanese Basic A1.1                 3 ECTS   HS      Basel
 7. Spanish A1                          3 ECTS   HS/FS   Basel, Olten, Windisch
 8. Spanish A2                          3 ECTS   HS/FS   Olten, Windisch
 9. Spanish B1                          3 ECTS   HS/FS   Olten
10. Spanish intensive course A1/A2      6 ECTS   FS      Olten, Windisch
Pick an elective (0 to go back): 11
Please enter a number from 0 to 10.
Pick an elective (0 to go back): 7
Added Spanish A1. Selected: 9/12 ECTS
```

### Step 8: Check my plan

Checks your current plan and prints one line per problem, or confirms that the plan is complete.

```
--- Plan check ---
Electives: 9/12 ECTS — 3 ECTS missing.

1 warning. Press Enter to return.
```

When nothing is wrong:

```
--- Plan check ---
Your plan is complete (180/180 ECTS).

Press Enter to return.
```

### Step 9: Personal roadmap

Shows your personal 180-ECTS roadmap per semester, with your specialisation and electives in place, plus a total progress bar toward 180 ECTS. The percentage and the bar length are rounded down (177/180 shows as 98%, and a 20-character bar holds 19 `#`).

```
--- Roadmap ---
Semester 1
  Applied Mathematics 1          Foundation            3 ECTS
  Statistics 1                   Foundation            3 ECTS
  Principles of Management       Business Admin.       6 ECTS
  Digital Business               BIT                   6 ECTS
  Programming Foundations        IT                    6 ECTS
...
Semesters 6-8 (specialisation)
  Digital Trust modules                               36 ECTS
Electives
  German Basic A1                Elective              3 ECTS
  Italian A1                     Elective              3 ECTS
  Spanish A1                     Elective              3 ECTS
  Electives: 9/12 ECTS — 3 ECTS missing.

Total  [###################-]  177/180 ECTS (98%)
```

### Step 10: Save plan

Saves your plan to `my_plan.json` so it's there next time you start the app.

```
Plan saved to my_plan.json.
```

### Step 11: Exit

If you changed something since the last save, the app offers to save first.

```
Choose an option (0-7): 0
You have unsaved changes. Save now? (y/n): y
Plan saved to my_plan.json.
Goodbye.
```

> **Note:** Electives come from the FHNW module descriptions (HS26 and FS27), limited to regular BIT and language courses. The official rule allows 2, 3, 5 or 6 ECTS; the values here are still rounded to 3/6 pending the source data. Specialisation modules are placeholders following the programme's recommended structure (30 core + 6 flexible, per the BIT administration); the official lists are expected early 2027.

## Sources

- FHNW module descriptions: https://modulbeschreibungen.webapps.fhnw.ch/
- FHNW Bachelor in Business Information Technology: https://www.fhnw.ch/en/business/degree-programmes/offerings/programmes/bachelor-in-business-information-technology
