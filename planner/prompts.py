"""
Input helpers that every menu uses.

Owner: Thalita (moved here from choices.py so the whole team can use them)

Basic questions:
  ask_number   ask until the answer is a whole number in a range
  ask_yes_no   ask until the answer is y or n

Headers:
  show_header  print a title in a box, to start a new screen

Messages (empty line, colour and symbol in one call):
  show_kept     cyan   → nothing changed, the current choice was kept
  show_success  green  → something was saved or changed
  show_warning  yellow ! check your answer, like "Please enter ..."
  show_error    orange ✗ a problem, like a missing file

Menus (built on the basic questions):
  show_menu    print a numbered list with 0 at the bottom (Back or Exit)
  ask_menu     show_menu with 0. Back, then ask for a number

Colours (so messages look the same in every menu):
  CURRENT  cyan    the current choice and what was kept
  BOLD     bold    questions and messages
  SUCCESS  green   something was saved or changed
  WARNING  yellow  check your answer: "Please enter ..." or nothing changed
  ERROR    orange  a problem, like a missing file
  RESET    back to normal (no colour, no bold), put it at the end of every coloured or bold text

Use the show_ messages instead of printing CURRENT, SUCCESS, WARNING or ERROR yourself.

The error messages live only here, so the wording is the same in every menu.
"""


# --- Colours ---

# Codes that tell the terminal to change the text colour
CURRENT = "\033[36m"
BOLD = "\033[1m"
SUCCESS = "\033[32m"
WARNING = "\033[33m"
ERROR = "\033[38;5;208m"
RESET = "\033[0m"


# --- Headers ---

def show_header(title):
    """Print an empty line, then the title centred between two lines."""
    print()
    print("-" * 55)
    print(f"{title:^55}")
    print("-" * 55)
    print()


# --- Messages ---

def show_kept(message):
    """Print an empty line, then the message in cyan with →."""
    print()
    print(f"{CURRENT}→ {message}{RESET}")


def show_success(message):
    """Print an empty line, then the message in green with →."""
    print()
    print(f"{SUCCESS}→ {message}{RESET}")


def show_warning(message):
    """Print an empty line, then the message in yellow with !."""
    print()
    print(f"{WARNING}! {message}{RESET}")


def show_error(message):
    """Print an empty line, then the message in orange with ✗."""
    print()
    print(f"{ERROR}✗ {message}{RESET}")


# --- Basic questions ---

def ask_number(prompt, low, high):
    """Ask until the user types a whole number from low to high."""
    while True:
        # Every question gets an empty line above it and is bold
        print()
        answer = input(f"{BOLD}{prompt}{RESET}").strip()
        # isdigit() first, so int() never gets text like "abc"
        if answer.isdigit():
            number = int(answer)
            if number >= low and number <= high:
                return number
        show_warning(f"Please enter a number from {low} to {high}")


def ask_yes_no(prompt):
    """Ask until the user types y or n. Returns True for y."""
    while True:
        # Every question gets an empty line above it and is bold
        print()
        answer = input(f"{BOLD}{prompt}{RESET}").strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        show_warning("Please enter y or n")


# --- Menus ---

def show_menu(options, last_option):
    """Print options as 1, 2, 3 ... and 0 with last_option. Returns the highest number."""
    # 1. Show the options, counting from 1
    number = 0
    for option in options:
        number = number + 1
        print(f"{number}. {option}")

    # 2. 0 is always last, even though it is the lowest number
    print(f"0. {last_option}")
    return number


def ask_menu(options):
    """Show options with 0. Back and ask for one. Returns the number, 0 means back."""
    highest = show_menu(options, "Back")
    return ask_number(f"Your choice (0-{highest}): ", 0, highest)
