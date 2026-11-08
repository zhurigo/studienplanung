"""
The look of every screen: colours, widths, headers, boxes and messages
"""


# --- Colours ---

CURRENT = "\033[36m"   # cyan: the current choice, electives already in the plan
SUCCESS = "\033[32m"   # green: the ❯❯ arrow
BOLD = "\033[1m"
ITALIC = "\033[3m"
DIM = "\033[2m"        # less important text, like the description under a header
RESET = "\033[0m"      # end every coloured or bold text with this
EMPTY = f"{DIM}{ITALIC}"  # a slot that is still to choose, e.g. "(choose an elective)"

# Headers, lists and boxes all end at this edge
APP_WIDTH = 70

# In front of every question
ARROW = f"{SUCCESS}❯❯{RESET} "

# In front of each message, use the show_ functions below instead of printing them
WARNING_MARK = "❗️ "
SUCCESS_MARK = "✅ "
KEPT_MARK = "🔒 "
ERROR_MARK = "❌ "


# Group label column in the degree plan and the roadmap, e.g. "Business Admin."
LABEL_WIDTH = 16


# --- Lines ---

def fit(left, right="", width=APP_WIDTH):
    """Left text, then right text against the right edge, e.g. fit("Italian A1", "3 ECTS")"""
    space = width - len(left) - len(right)
    # At least one space, so long text never touches the right side
    if space < 1:
        space = 1
    return left + " " * space + right


def wrap(text, width=APP_WIDTH):
    """Break the text between words, so no line is wider than width"""
    lines = []
    line = ""
    for word in text.split(" "):
        if line == "":
            line = word
        elif len(line) + 1 + len(word) <= width:
            line = line + " " + word
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return "\n".join(lines)


def ects(value):
    """An ECTS value for a row, e.g. ' 3 ECTS', so 3 and 12 line up"""
    return f"{value:>2} ECTS"


def bullet(left, right="", width=APP_WIDTH):
    """'• ' and a fit line, width wide, e.g. for a row in a box"""
    return "• " + fit(left, right, width - 2)


def show_bullet(left, right="", style=""):
    """Print an indented bullet line as wide as the app. style colours the whole line"""
    print(f"  {style}{bullet(left, right, APP_WIDTH - 2)}{RESET}")


# --- Headers ---

def show_header(title, description=""):
    """Start a new screen: the title between two lines, then an optional
    description, dim and italic. Use \\n for a second description line"""
    width = APP_WIDTH

    print()
    print("-" * width)
    print(f"{title:^{width}}")
    print("-" * width)
    if description != "":
        for line in description.split("\n"):
            print(f"{DIM}{ITALIC}{line:^{width}}{RESET}")
    print()


# --- Boxes ---

BOX_WIDTH = 62                  # inside the borders, fits the longest elective row
BOX_TEXT_WIDTH = BOX_WIDTH - 2  # without the space on each side, use it with fit


def show_box(title, body, center=False):
    """A centered box: bold title, empty line, then one line per item in body centers the body too"""
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
    """🔒 Nothing changed, e.g. 'Kept Digital Trust'"""
    print()
    print(f"{KEPT_MARK}{message}{RESET}")


def show_success(message):
    """✅ Something was saved or changed"""
    print()
    print(f"{SUCCESS_MARK}{message}{RESET}")


def show_warning(message):
    """❗️ The answer can't be used, e.g. 'Please enter a number from 0 to 4'"""
    print()
    print(f"{WARNING_MARK}{message}{RESET}")


def show_error(message):
    """❌ Something went wrong, e.g. a file that can't be read"""
    print()
    print(f"{ERROR_MARK}{message}{RESET}")