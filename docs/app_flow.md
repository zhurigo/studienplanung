# Program flow and contracts

**Status:** draft for Milestone 3 (2026-10-23) · **Owner:** Hugo
**Reviewers:** Thalita (navigation) · Angelica (display)

This file is the implementation contract. The [`README`](../README.md) describes
the app for a reader; this file fixes the things three people cannot guess
identically: navigation, function boundaries, the save format, and message
wording. If the two disagree, fix both in one commit.

---

## 1. Navigation rules

**Rule 1 — `0` leaves the current screen.** On the main menu, `0` exits the app
(after the unsaved-changes prompt). On every other screen, `0` goes one level
up. `0` is always listed in the prompt.

**Rule 2 — output screens are dismissed with Enter.** Plan check and roadmap
print information and take no decision, so they end with
`Press Enter to return.` This is acknowledgement, not navigation.

**Rule 3 — Enter is never "back".** The one exception is the group filter
(US2): there Enter means *no filter*, and the degree plan stays on screen.

So a screen either **asks for a choice** (`0` = back) or **shows output**
(Enter = return). Nothing else.

| Screen | Prompt | `0` | Enter | Invalid input |
|---|---|---|---|---|
| Main menu | `Choose an option (0-7):` | exit | invalid | `Please enter a number from 0 to 7.` |
| Degree plan → group filter | `Enter a number, or press Enter to skip:` | back | no filter, stay | `Please enter a number from 1 to 7.` |
| Explore specialisations | `Pick one to see details (0 to go back):` | back | invalid | `Please enter a number from 0 to 3.` |
| Choose specialisation | `Pick one (0 to go back):` | back | invalid | `Please enter a number from 0 to 3.` |
| Replace prompt | `Replace X with Y? (y/n):` | — | — | `Please enter y or n.` |
| Plan electives | `Choose (0-2):` | back | invalid | `Please enter a number from 0 to 2.` |
| Pick category | `Choose a category (0 to go back):` | back | invalid | `Please enter a number from 0 to 4.` |
| Pick elective | `Pick an elective (0 to go back):` | back | invalid | `Please enter a number from 0 to N.` |
| Plan check / roadmap | `Press Enter to return.` | — | back | — |
| Save prompt | `Save now? (y/n):` | — | — | `Please enter y or n.` |

Validation happens **before** anything is changed: a rejected input must leave
the plan exactly as it was.

---

## 2. Menu → function map

`main.py` owns the menu and the loop. It never contains business rules; it calls
one function per option and comes back.

| Option | Screen | Function | File | Owner |
|---|---|---|---|---|
| — (start-up) | load curriculum data | `data_loader.load_all()` | `planner/data_loader.py` | Hugo (shared) |
| — (start-up) | offer saved plan | `main.offer_load()` → `storage.load_plan()` | `main.py`, `storage.py` | Hugo |
| 1 | View degree plan | `display.show_degree_plan(modules, groups)` | `planner/display.py` | Angelica |
| 2 | Explore specialisations | `display.explore_specialisations(specs)` | `planner/display.py` | Angelica |
| 3 | Choose specialisation | `choices.choose_specialisation(plan, specs)` | `planner/choices.py` | Thalita |
| 4 | Plan electives | `choices.plan_electives(plan, electives_by_category)` | `planner/choices.py` | Thalita |
| 5 | Check my plan | `rules.check_plan(plan)` | `planner/rules.py` | Hugo |
| 6 | Roadmap | `rules.show_roadmap(plan, modules, specs)` | `planner/rules.py` | Hugo |
| 7 | Save plan | `storage.save_plan(plan)` | `planner/storage.py` | Hugo |
| 0 | Exit | `main.offer_save_if_dirty(plan)` | `main.py` | Hugo |

**Dependency order:** `models` → `data_loader` → `display` / `choices` →
`rules` / `storage`. Nobody starts before the layer above exists.

`main.py` keeps a single dispatch table, so adding a screen is a one-line
change and the menu text cannot drift from the behaviour.

### Shared prompt helpers

Put in `planner/ui.py` (new, shared — Thalita writes it with the menu work):

```python
ask_number(prompt, low, high)   -> int      # loops until valid; "0" allowed if low == 0
ask_yes_no(prompt)              -> bool     # accepts y/n, case-insensitive; loops otherwise
pause(prompt="Press Enter to return.")      # waits for Enter
```

Every prompt in the app goes through these three functions. That is what makes
the wording in §1 and §5 true everywhere instead of in nine places.

---

## 3. Data contracts

`planner/models.py` — field names are fixed here so `display`, `choices`,
`rules` and `storage` can be written in parallel.

```python
@dataclass
class Module:            # from data/modules.json
    name: str; semester: int; group: str; ects: int; project_based: bool

@dataclass
class Specialisation:    # from data/specialisations.json
    id: str; name: str; focus: str
    modules: list[dict]; builds_on: list[str]; careers: list[str]
    ects: int; core_ects: int; remaining_ects: int; semesters: list[int]

@dataclass
class Elective:          # from data/electives.json
    id: str; name: str; category: str; ects: int
    semester: str; campus: list[str]

@dataclass
class StudentPlan:
    specialisation: Specialisation | None = None
    electives: list[Elective] = field(default_factory=list)
    dirty: bool = False          # set by every change, cleared by a save
```

`StudentPlan` methods (Thalita confirms the names):

| Method | Used by |
|---|---|
| `total_elective_ects() -> int` | US5 counter, US7 check, US9 roadmap |
| `choose_specialisation(spec)` | US4 |
| `add_elective(elective) -> str \| None` | US5 — returns an error text or `None` |
| `remove_elective(elective_id) -> bool` | US6 |
| `has_elective(elective_id) -> bool` | US5 duplicate check |

Returning an error string (instead of raising) keeps the loop in `choices.py`
simple: print it, ask again.

---

## 4. Save format — `my_plan.json`

Written next to `main.py`, git-ignored. **Ids only** — never whole objects, so
descriptions can change without breaking a saved plan.

```json
{
  "version": 1,
  "specialisation": "DT",
  "electives": ["LANG-DE-A1", "LANG-IT-A1", "LANG-ES-A1"]
}
```

| Field | Type | Rules |
|---|---|---|
| `version` | int | currently `1`. A higher number → treat as unreadable, start empty |
| `specialisation` | string \| null | id from `data/specialisations.json`, or `null` |
| `electives` | list of string | ids from `data/electives.json`, order kept |

Reading rules:

- file missing → start with an empty plan, **no message**
- file not valid JSON, or not an object → `Could not read my_plan.json — starting with an empty plan.`
- valid JSON but unknown ids → **load it anyway**; US7 reports the ids
- duplicates in the file → load them; US7 reports the duplicate
- extra keys → ignore

Writing rules: overwrite the whole file atomically (write, then replace), end
with a newline, indent 2. `Plan saved to my_plan.json.` on success;
`Could not save my_plan.json.` on `OSError` — never a traceback.

---

## 5. Message wording

One sentence per line, no `Error:` prefix. Input errors start with `Please`.
Domain warnings are statements of fact.

| Kind | Pattern | Example |
|---|---|---|
| Prompt | ends with `:` and shows the accepted range | `Choose an option (0-7):` |
| Bad number | `Please enter a number from {low} to {high}.` | `Please enter a number from 1 to 3.` |
| Bad yes/no | `Please enter y or n.` | |
| Back hint | `(0 to go back)` in the prompt, not a separate line | `Pick an elective (0 to go back):` |
| Duplicate | `That elective is already in your plan.` | |
| Over the limit | `That would make {total}/12 ECTS — you can add at most {left} more ECTS.` | `That would make 15/12 ECTS — you can add at most 3 more ECTS.` |
| Over the limit (check) | `Electives: {total}/12 ECTS — {extra} ECTS over the limit.` | `Electives: 15/12 ECTS — 3 ECTS over the limit.` |
| Missing electives | `Electives: {x}/12 ECTS — {y} ECTS missing.` | `Electives: 9/12 ECTS — 3 ECTS missing.` |
| No specialisation | `No specialisation chosen.` | |
| Unknown id | `Unknown elective id: {id}` / `Unknown specialisation id: {id}` | |
| Duplicate (loaded) | `Elective listed twice: {name}` | |
| Bad data file | `Could not read {path} — stopping.` | |
| Bad plan file | `Could not read my_plan.json — starting with an empty plan.` | |

Use an em dash `—` with spaces, `ECTS` in upper case, and never abbreviate
`specialisation`.

---

## 6. Alternate flows (must all work)

| # | Trigger | Expected behaviour |
|---|---|---|
| 1 | Non-number at any number prompt | `Please enter a number from …`, ask again, nothing changes |
| 2 | Number outside the range | same |
| 3 | Empty input on a choice screen | invalid, ask again (`0` is the way back) |
| 4 | Empty input on the group filter | no filter; stay in the degree plan |
| 5 | Invalid input at a y/n prompt | `Please enter y or n.`, ask again |
| 6 | Duplicate elective | refuse, message, counter unchanged |
| 7 | Elective would exceed 12 ECTS | refuse, message with the remaining ECTS, counter unchanged |
| 8 | Remove with no electives | `You have no electives to remove.`, back to the electives menu |
| 9 | Replace specialisation | confirm `y/n`; `n` keeps the current one |
| 10 | Check/roadmap with no specialisation | check warns; roadmap prints `Specialisation — not chosen yet` for semesters 6–8 |
| 11 | `data/*.json` missing or invalid | name the file, stop, exit code 1, no traceback |
| 12 | `my_plan.json` missing | start empty, silently |
| 13 | `my_plan.json` damaged | message, start empty, continue |
| 14 | Exit with unsaved changes | `You have unsaved changes. Save now? (y/n):`; not asked when clean |
| 15 | Ctrl-C / Ctrl-D | `Goodbye.` and exit 0, no traceback |

---

## 7. User-story changes this implies

Suter's point 2 and point 6 need edits in
[`docs/user_stories.md`](user_stories.md) and the README:

1. **US2 AC3** — currently says Enter returns to the main menu. Change to:
   Enter skips the filter and the plan stays on screen; `0` returns.
2. **US9 preamble and AC2** — the "elective slot is 3 ECTS / `Elective slot 3 — empty`"
   model no longer holds once 2/3/5/6-ECTS electives are allowed. Replace with
   the remaining-ECTS line from §5.
3. **US5 AC2** — align the refusal text with §5 (`…you can add at most 3 more ECTS.`).
4. **US6 AC2** — name the message: `You have no electives to remove.`
5. **US7** — the over-limit warning text must match §5
   (`Electives: 15/12 ECTS — 3 ECTS over the limit`).

No re-submission is needed; these land in the README and the story file together.

---

## 8. Open questions

- **`Q:` Roadmap total when no specialisation is chosen.** US9 AC5 says the
  roadmap still renders, but the total is undefined: 144/180, or 180 with the
  specialisation counted as planned? Decide before US9.
- **`Q:` `data/modules.json` still has `slots`** with 4 × 3-ECTS electives and
  12 ECTS of specialisation per semester. That contradicts 2/3/5/6 electives
  and the 30 + 6 structure. Proposal: stop reading `slots` for electives and
  compute the remainder from `total_elective_ects()`; keep the specialisation
  block at 36 ECTS for the roadmap.
- **`Q:` `ects_allowed` vs. actual data.** The rule allows 2/3/5/6, the data
  still stores 3/6. The code must follow the data, not the rule, until
  `electives.json` is corrected.
- **`Q:` Does `dirty` live in `StudentPlan` or in `main.py`?** Proposal: in the
  plan, set by the mutators — otherwise `main` has to compare snapshots.

---

## 9. Milestone 3 checklist (2026-10-23)

- [ ] `models.py`, `data_loader.py` and `main.py` committed and pushed
- [ ] `python main.py` boots, loads all three data files, shows the menu
- [ ] every menu option reaches a function and returns without a traceback
- [ ] all 15 alternate flows in §6 behave as written
- [x] README and §5 wording agree
- [x] user-story edits from §7 applied
