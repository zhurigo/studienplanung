"""
Input helpers that every menu uses.

Basic questions:
  ask_number   ask until the answer is a whole number in a range
  ask_yes_no   ask until the answer is y or n
  pause        wait for Enter, so an output screen can be read

Menus (built on the basic questions):
  show_menu    print a numbered list with 0 at the bottom (Back or Exit)
  ask_menu     show_menu with 0. Back, then ask for a number

The colours, headers, boxes and messages are in styling.py
The error messages live only here, so the wording is the same in every menu.
"""

from planner.styling import APP_WIDTH, ARROW, DIM, RESET, fit, show_warning


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
    """Ask until the user types y or n. Adds " (y/n): " to the question"""
    while True:
        print()
        answer = input(f"{ARROW}{prompt} (y/n): ").strip().lower()
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
                print(f"{' ' * (digits + 2)}{DIM}{option[3]}{RESET}")
        else:
            print(f"{number:>{digits}}. {option}")

    print(f"{0:>{digits}}. {last_option}")
    return number


def ask_menu(options, prompt=None):
    """Show options with 0. Back and ask for one."""
    highest = show_menu(options, "Back")
    if prompt is None:
        prompt = f"Choose an option (0-{highest}): "
    return ask_number(prompt, 0, highest)
