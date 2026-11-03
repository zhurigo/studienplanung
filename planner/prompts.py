"""
Input helpers that every menu uses.

Owner: Thalita (moved here from choices.py so the whole team can use them)

Basic questions:
  ask_number   ask until the answer is a whole number in a range
  ask_yes_no   ask until the answer is y or n
  pause        wait for Enter, so an output screen can be read

Headers:
  show_header  print a title in a box, to start a new screen,
               with an optional short description under it

Boxes:
  show_box     a centered box with a bold title and a body, e.g. the current choices

Messages (empty line and emoji in one call, no full stop at the end):
  show_kept     🔒 nothing changed, the current choice was kept
  show_success  ✅ something was saved or changed
  show_warning  ❗️ check your answer, like "Please enter ..."
  show_error    ❌ a problem, like a missing file

Lines as wide as the app (so every list ends at the same edge as the headers):
  fit          left text, then right text against the right edge, APP_WIDTH wide
  show_bullet  "  • " and a fit line

Menus (built on the basic questions):
  show_menu    print a numbered list with 0 at the bottom (Back or Exit)
  ask_menu     show_menu with 0. Back, then ask for a number

Colours (so the screens look the same in every menu):
  CURRENT  cyan    the current choice and the electives already in the plan
  SUCCESS  green   the ❯❯ arrow in front of every question
  BOLD     bold    names that stand out, like the new specialisation
  ITALIC   italic  the short description under a header
  RESET   back to normal (no colour, no bold, no italics), put it at the end of every coloured or bold text

Use the show_ messages instead of printing an emoji yourself.

The error messages live only here, so the wording is the same in every menu.
"""


# --- Colours ---

# Codes that tell the terminal to change the text colour
CURRENT = "\033[36m"
SUCCESS = "\033[32m"
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
DIM = "\033[2m"

# Width of the whole app: headers, the welcome box and the degree plan all line up to it
APP_WIDTH = 70

# Bold green arrow in front of every question, like a terminal prompt
ARROW = f"{BOLD}{SUCCESS}❯❯{RESET} "

# Emoji in front of each message (see Messages below)
WARNING_MARK = f"{BOLD}❗️{RESET} "
SUCCESS_MARK = f"{BOLD}✅{RESET} "
KEPT_MARK = f"{BOLD}🔒{RESET} "
ERROR_MARK = f"{BOLD}❌{RESET} "


# --- Lines as wide as the app ---

def fit(left, right="", width=APP_WIDTH):
    """One line exactly width characters wide: left text, then right text
    against the right edge, e.g. fit("Italian A1", "3 ECTS")."""
    space = width - len(left) - len(right)
    # At least one space, so a long left text never touches the right one
    if space < 1:
        space = 1
    return left + " " * space + right


def show_bullet(left, right="", style=""):
    """Print '  • ' and a fit line, as wide as the app. style colours the whole line."""
    print(f"  • {style}{fit(left, right, APP_WIDTH - 4)}{RESET}")


# --- Headers ---

def show_header(title, description=""):
    width = APP_WIDTH

    print()
    print("-" * width)
    print(f"{title:^{width}}")
    print("-" * width)
    # A description can have more than one line, each one is centered
    if description != "":
        for line in description.split("\n"):
            print(f"\033[2m{ITALIC}{line:^{width}}{RESET}")
    print()


# --- Boxes ---

# Inside width of a box, wide enough for the longest elective name and its semester
BOX_WIDTH = 62
# Width of the text in a box, without the space on each side
BOX_TEXT_WIDTH = BOX_WIDTH - 2


def show_box(title, body, center=False):
    """A box centered in the app: the title bold in the middle, an empty line,
    then the body, one line per item. center=True centers the body lines too.

    ╭──────────────╮
    │    Title     │
    │              │
    │ body line 1  │
    ╰──────────────╯
    """
    margin = " " * ((APP_WIDTH - BOX_WIDTH - 2) // 2)
    print(f"{margin}╭{'─' * BOX_WIDTH}╮")
    print(f"{margin}│ {BOLD}{title:^{BOX_TEXT_WIDTH}}{RESET} │")
    print(f"{margin}│ {'':<{BOX_TEXT_WIDTH}} │")
    for line in body:
        if center:
            print(f"{margin}│ {line:^{BOX_TEXT_WIDTH}} │")
        else:
            print(f"{margin}│ {line:<{BOX_TEXT_WIDTH}} │")
    print(f"{margin}╰{'─' * BOX_WIDTH}╯")


# --- Messages ---

def show_kept(message):
    print()
    print(f"{KEPT_MARK}{message}{RESET}")


def show_success(message):
    print()
    print(f"{SUCCESS_MARK}{message}{RESET}")


def show_warning(message):
    print()
    print(f"{WARNING_MARK}{message}{RESET}")


def show_error(message):
    print()
    print(f"{ERROR_MARK}{message}{RESET}")


# --- Basic questions ---

def ask_number(prompt, low, high):
    """Ask until the user types a whole number from low to high."""
    while True:
        print()
        answer = input(f"{ARROW}{prompt}").strip()
        # isdigit() first, so int() never gets text like "abc"
        if answer.isdigit():
            number = int(answer)
            if number >= low and number <= high:
                return number
        show_warning(f"Please enter a number from {low} to {high}")


def ask_yes_no(prompt):
    """Ask until the user types y or n"""
    while True:
        print()
        answer = input(f"{ARROW}{prompt}").strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        show_warning("Please enter y or n")


def pause(prompt="Press Enter to return"):
    """Wait for Enter so the screen can be read. Returns nothing."""
    print()
    input(f"{ARROW}{prompt}")


# --- Menus ---

def show_menu(options, last_option):
    """Print options as 1, 2, 3 ... and 0 with last_option. Returns the highest number.

    An option is a text, or a tuple that is fitted to the app's width:
      (left, right)               right text against the right edge
      (left, right, style)        the whole line in a colour, e.g. CURRENT
      (left, right, style, note)  plus a dim second line, e.g. the campus
    """
    # Numbers are right-aligned to the widest one, so " 9." and "10." line up
    digits = len(str(len(options)))
    # "10. " takes digits + 2 characters, the rest is for the option
    width = APP_WIDTH - digits - 2

    # Show the options, counting from 1 and keeping 0 as the last option
    number = 0
    for option in options:
        number = number + 1
        if isinstance(option, tuple):
            style = option[2] if len(option) > 2 else ""
            print(f"{number:>{digits}}. {style}{fit(option[0], option[1], width)}{RESET}")
            if len(option) > 3:
                print(f"{' ' * (digits + 2)}\033[2m{option[3]}{RESET}")
        else:
            print(f"{number:>{digits}}. {option}")

    print(f"{0:>{digits}}. {last_option}")
    return number


def ask_menu(options, prompt=None):
    """Show options with 0. Back and ask for one. Returns the number, 0 means back."""
    highest = show_menu(options, "Back")
    if prompt is None:
        prompt = f"Choose an option (0-{highest}): "
    return ask_number(prompt, 0, highest)
