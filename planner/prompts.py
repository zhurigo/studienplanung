"""
Input helpers that every menu uses.

Owner: Thalita (moved here from choices.py so the whole team can use them)

Basic questions:
  ask_number   ask until the answer is a whole number in a range
  ask_numbers  like ask_number, but several numbers at once ("5, 6" or "5 6")
  ask_yes_no   ask until the answer is y or n
  pause        wait for Enter, so an output screen can be read

Headers:
  show_header  print a title in a box, to start a new screen,
               with an optional short description under it

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
  ITALIC   italic  the short description under a header
  RESET   back to normal (no colour, no bold, no italics), put it at the end of every coloured or bold text

Use the show_ messages instead of printing CURRENT, SUCCESS, WARNING or ERROR yourself.

The error messages live only here, so the wording is the same in every menu.
"""


# --- Colours ---

# Codes that tell the terminal to change the text colour
CURRENT = "\033[36m"
SUCCESS = "\033[32m"
WARNING = "\033[33m"
ERROR = "\033[38;5;208m"
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"


# --- Headers ---

def show_header(title, description=""):
    """Print an empty line, then the title centred between two lines.
    If there is a description, print it centred in italics right under the box."""
    print()
    print("-" * 55)
    print(f"{title:^55}")
    print("-" * 55)
    if description != "":
        print(f"\033[2m{ITALIC}{description:^55}{RESET}")
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
        show_warning(f"Please enter a number from {low} to {high}.")


def ask_numbers(prompt, low, high):
    """Ask until the user types one or more numbers from low to high,
    split by commas or spaces, e.g. "5, 6" or "5 6". Returns them as a list."""
    while True:
        # Every question gets an empty line above it and is bold
        print()
        answer = input(f"{BOLD}{prompt}{RESET}")

        # 1. Turn commas into spaces, then split into single words
        words = answer.replace(",", " ").split()

        # 2. Every word must be a number in range, and there must be at least one
        numbers = []
        all_valid = True
        for word in words:
            if word.isdigit() and int(word) >= low and int(word) <= high:
                numbers.append(int(word))
            else:
                all_valid = False
        if all_valid and numbers != []:
            return numbers
        show_warning(f"Please enter a number from {low} to {high}.")


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
        show_warning("Please enter y or n.")


def pause(prompt="Press Enter to return. "):
    """Wait for Enter so the screen can be read. Returns nothing."""
    print()
    input(f"{BOLD}{prompt}{RESET}")


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


def ask_menu(options, prompt=None):
    """Show options with 0. Back and ask for one. Returns the number, 0 means back."""
    highest = show_menu(options, "Back")
    if prompt is None:
        prompt = f"Your choice (0-{highest}): "
    return ask_number(prompt, 0, highest)
