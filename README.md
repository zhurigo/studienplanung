# studienplanung

A tool that is here to help BIT students of FHNW to find Electives (4 x 3 ECTS that can be filled in during the 2nd and 3rd years of the degree)

IDEA SKETCH
"Specialization explorer" with an "Electives picker".

Specialization:
* There's 3 paths for specialization
* Each specialization will require 6 modules


Electives [Reference - https://modulbeschreibungen.webapps.fhnw.ch/]:
* Electives are not directly related to a specialization
* Electives can be selected on a freestyle motto


There are 180 ECTS where some are Specialization specific modules and some are Elective specific modules. A user will interact with the CLI application by being asked a questionnaire and receive a suggestive specialization such as [Reference - https://www.fhnw.ch/en/business/degree-programmes/offerings/programmes/bachelor-in-business-information-technology]:
* Business Analytics and Data Science: Focuses on analyzing large volumes of data, identifying patterns, and using insights for smart business forecasting and decision-making.
* Digital Business Management: Concentrates on designing digital business models, managing organizational change, and aligning IT strategies with corporate goals.
* Digital Trust: Centers on cybersecurity, risk management, data protection, and operating secure IT infrastructures.


MVP
* A cli application
* 1. A welcome message describing our intention
* 2. Ask the user
     2.1. If they have a clue of where they're heading
     2.2. If they'd like to take a quiz and be given a suggestion
* 3. The user will see a list of Specializations (that are 3), specific Electives based on the degree and language of learning (ENG for now but probably all options after MVP)
* 4. Give them the option to see the full list of swappable modules.
* 5. After the initial interaction, we will show the user their ROADMAP according to their selections. I.E. if they choose to swap Applied Mathematics 2 for an Elective, their ROADMAP will look different.


TECHNICAL
* 

ROUGH IDEA OF HOW IT WILL LOOK


---

## How to use the BIT Study Planner

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

> **Note:** Specialisation module names and electives are placeholders until the official Curriculum 2025 lists are published.