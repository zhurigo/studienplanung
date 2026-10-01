# studienplanung — BIT Study Planner

An interactive command-line tool that helps FHNW Business Information Technology (BIT) students choose a specialisation and four electives, then generates a personal 180-ECTS study roadmap.

## The problem

In the BIT programme you pick one of three specialisations and four 3-ECTS electives, but the information needed to decide is spread across the FHNW programme page and many individual module descriptions. It is also hard to see how a single swap changes the whole 180-ECTS plan. This tool brings the choices into one place and keeps the plan consistent as you change it.

## What it does

- **Shows the degree plan**: all modules per semester, filterable by group (e.g. Information Technology).
- **Lets you explore** the three specialisations (Business Analytics and Data Science, Digital Business Management, Digital Trust) and the elective categories.
- **Builds your plan**: one specialisation (6 modules, 36 ECTS) plus four 3-ECTS electives, with an ECTS counter that stops at 12.
- **Lets you swap**: remove or replace an elective and the roadmap changes with it.
- **Checks and saves**: warns about problems in the plan, shows a per-group progress report toward 180 ECTS, and saves to `my_plan.json`.

## Scope (MVP)

| In                                                       | Out                                                                |
| -------------------------------------------------------- | ------------------------------------------------------------------ |
| Console application (interactive, with input validation) | Graphical or web interface                                         |
| Browsing the degree plan, filtered by group              | Questionnaire-based specialisation suggestion (planned after MVP)  |
| Choosing one specialisation and four electives           | Languages of instruction other than English                        |
| Full 180-ECTS roadmap that updates on every swap         | Official module lists (names are placeholders until published)     |
| Plan check and per-group progress report                 | Multiple users or accounts                                         |
| Save / load of a single plan (`my_plan.json`)            |                                                                    |

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
├── data/            # modules and specialisations
├── tests/
└── my_plan.json     # your saved plan (created on first save)
```

## Team

| Member            | GitHub           | Area           | User stories |
| ----------------- | ---------------- | -------------- | ------------ |
| Angelica Bertalli | `angio-eng`      | Browse         | 1, 2, 3      |
| Thalita dos Reis  | `ThalitadosReis` | Plan           | 4, 5, 6      |
| Hugo              | `zhurigo`        | Check and save | 7, 8, 9      |

## User stories

Each team member implements three user stories. The last column shows which course acceptance criteria the story demonstrates.

| Owner                 | #   | User story                                                                                                         | Course criteria shown          |
| --------------------- | --- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------ |
| Angelica (Browse)     | 1   | As a student, I want to see all modules per semester so I know what's coming.                                      | Interactive, file reading      |
| Angelica (Browse)     | 2   | As a student, I want to filter modules by group (e.g. Information Technology) so I see where my ECTS come from.    | Interactive, input validation  |
| Angelica (Browse)     | 3   | As a student, I want to explore the three specialisations so I can compare them.                                   | Interactive, file reading      |
| Thalita (Plan)        | 4   | As a student, I want to choose one specialisation and have it stored in my plan.                                   | Input validation               |
| Thalita (Plan)        | 5   | As a student, I want to pick electives with an ECTS counter so I don't go over 12.                                 | Input validation               |
| Thalita (Plan)        | 6   | As a student, I want to remove or swap an elective so I can change my plan.                                        | Input validation               |
| Hugo (Check and save) | 7   | As a student, I want the app to check my plan and warn me about problems.                                          | Data validation                |
| Hugo (Check and save) | 8   | As a student, I want to save and load my plan so it's there next time.                                             | File writing and reading       |
| Hugo (Check and save) | 9   | As a student, I want to see my planned ECTS per group and my progress toward 180.                                  | Interactive                    |

## How it works

A step-by-step walkthrough of a typical session.

### Step 1: Start and welcome

The app loads the data files from the `data/` folder and shows how much it found. If a file is missing or broken, it prints an error and stops.

```
==============================================
   Welcome to the BIT Study Planner
   FHNW School of Business · Curriculum 2026/2027
==============================================
Loaded 34 modules and 3 specialisations.
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
6. Progress report
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
Modules:   6 modules x 6 ECTS (names provisional)
Builds on: IT Security, Digital Law, Digital Ethics
Careers:   Cybersecurity Consultant, Compliance Officer, IS Auditor
```

### Step 6: Choose specialisation

Your plan can hold one specialisation. If you already chose one, the app asks before replacing it.

```
--- Choose specialisation ---
Current choice: Digital Trust
1. Business Analytics and Data Science
2. Digital Business Management
3. Digital Trust
Your choice (1-3): 5
Please enter a number from 1 to 3.
Your choice (1-3): 1
Replace Digital Trust with Business Analytics and Data Science? (y/n): n
Kept Digital Trust.
```

### Step 7: Plan electives

Add or remove electives. The counter never goes above 12 ECTS, and you can't pick the same elective twice.

```
--- Plan electives ---
Selected: 6/12 ECTS (Python, Entrepreneurship)
1. Add an elective
2. Remove an elective
0. Back
Choose (0-2): 1

--- Categories ---
1. Languages (10)
2. Technology (5)
3. Business and Management (4)
4. Personal Skills (1)
5. Job Reflection (1)
Choose a category (0 to go back): 1

--- Languages ---
 1. Spanish 1 (Beginner)       3 ECTS   HS
 2. Spanish 2 (Intermediate)   3 ECTS   FS
 3. French 1                   3 ECTS   HS
 4. Italian 1                  3 ECTS   FS
 5. German for Business 1      3 ECTS   FS
 6. Russian 1                  3 ECTS   HS
 7. Portuguese 1               3 ECTS   FS
 8. Chinese 1                  3 ECTS   HS
 9. Japanese 1                 3 ECTS   FS
10. Arabic 1                   3 ECTS   HS
Pick an elective (0 to go back): 12
Please enter a number from 0 to 10.
Pick an elective (0 to go back): 1
Added Spanish 1 (Beginner). Selected: 9/12 ECTS
```

### Step 8: Check my plan

Checks your plan and lists every problem, or confirms that it's complete.

```
--- Plan check ---
Specialisation: Digital Trust        OK
Electives:      9/12 ECTS            1 slot still empty
Total:          177/180 ECTS         3 ECTS missing

2 warnings. Press Enter to return.
```

### Step 9: Progress report

Shows your planned ECTS per group and a progress bar toward 180 ECTS.

```
--- Progress report ---
Foundation              24/24
Business Admin.         21/21
BIT                     33/33
IT                      27/27
Student Work            27/27
Specialisation          36/36
Electives                9/12

Total  [###################-]  177/180 ECTS (98%)
```

### Step 10: Save plan

Saves your plan to `my_plan.json` so it's there next time you start the app.

```
Plan saved to my_plan.json (Digital Trust, 3 electives).
```

### Step 11: Exit

If you changed something since the last save, the app offers to save first.

```
Choose an option (0-7): 0
You have unsaved changes. Save now? (y/n): y
Plan saved to my_plan.json.
Goodbye, and good luck with your studies!
```

> **Note:** Specialisation module names and electives are placeholders until the official curriculum lists are published.

## Sources

- FHNW module descriptions: https://modulbeschreibungen.webapps.fhnw.ch/
- FHNW Bachelor in Business Information Technology: https://www.fhnw.ch/en/business/degree-programmes/offerings/programmes/bachelor-in-business-information-technology
