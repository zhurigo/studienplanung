"""
BIT Study Planner - start of the program.

Run with:  python main.py

Owner: whole team (set up together in CW 42)

What goes here:
  - Show the welcome message                          (Step 1)
  - Load the data files through planner/data_loader    (Step 1)
  - Ask whether to load a saved plan                  (Step 21)
  - Main menu loop: show options 0-7, read the choice,
    call the matching function, repeat until 0        (Step 3)
  - On exit: offer to save unsaved changes            (Step 11)

Keep this file short. The menu only calls functions from the planner package.
"""


def main():
    print("Welcome to StudienPlan, your FHNW Specialization assistant.")
    while True:
        choice = input("Choose an option (0-7): ")
        if choice == "0":
            break
        print(f"You chose {choice}")
        print("Goodbye.")


if __name__ == "__main__":
    main()
