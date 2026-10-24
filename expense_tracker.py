"""
========================================================
  Personal Expense Tracker — Command-Line Edition
  Data is stored in a plain text file (CSV-style).
========================================================

  Features:
    1. Add a new expense
    2. View all expenses
    3. Delete an expense by ID
    4. View a spending summary (total & per-category)
    5. Filter expenses by category
    6. Search expenses by keyword
    7. Exit

  File format (expenses.txt):
    Each line: ID|Date|Category|Description|Amount
    Example:   1|2026-10-25|Food|Lunch at cafe|12.50
"""

import os
import sys
from datetime import datetime

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────

# The file where all expenses are stored.
DATA_FILE = "expenses.txt"

# Predefined categories the user can pick from.
CATEGORIES = [
    "Food",
    "Transport",
    "Entertainment",
    "Health",
    "Shopping",
    "Utilities",
    "Education",
    "Other",
]

# Separator used inside the text file between fields.
DELIMITER = "|"

# ─────────────────────────────────────────────
#  HELPER UTILITIES
# ─────────────────────────────────────────────

def clear_screen():
    """Clear the terminal screen on Windows and Unix."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title: str):
    """Print a decorated section header."""
    width = 55
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_divider():
    """Print a thin divider line."""
    print("-" * 55)


def pause():
    """Wait for the user to press Enter before continuing."""
    input("\nPress Enter to return to the menu...")


# ─────────────────────────────────────────────
#  FILE I/O
# ─────────────────────────────────────────────

def load_expenses():
    """
    Read all expenses from the data file and return them as a
    list of dictionaries.

    Returns an empty list if the file does not yet exist.
    Each expense dict has keys: id, date, category, description, amount
    """
    expenses = []

    # If the file doesn't exist yet, return an empty list.
    if not os.path.exists(DATA_FILE):
        return expenses

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            # Skip blank lines silently.
            if not line:
                continue

            parts = line.split(DELIMITER)

            # A valid record has exactly 5 fields; skip malformed lines.
            if len(parts) != 5:
                print(f"  [Warning] Skipping malformed line {line_number}: {line}")
                continue

            try:
                expense = {
                    "id":          int(parts[0]),
                    "date":        parts[1],
                    "category":    parts[2],
                    "description": parts[3],
                    "amount":      float(parts[4]),
                }
                expenses.append(expense)
            except ValueError as e:
                # Handle cases where id or amount cannot be parsed.
                print(f"  [Warning] Could not parse line {line_number} ({e}), skipping.")

    return expenses


def save_expenses(expenses):
    """
    Write the full list of expenses back to the data file,
    overwriting any previous content.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for expense in expenses:
            line = DELIMITER.join([
                str(expense["id"]),
                expense["date"],
                expense["category"],
                expense["description"],
                f"{expense['amount']:.2f}",   # always save 2 decimal places
            ])
            f.write(line + "\n")


def next_id(expenses):
    """
    Generate the next unique ID.
    Simply returns max existing ID + 1, or 1 if there are no expenses.
    """
    if not expenses:
        return 1
    return max(e["id"] for e in expenses) + 1


# ─────────────────────────────────────────────
#  INPUT HELPERS
# ─────────────────────────────────────────────

def input_amount(prompt):
    """
    Prompt for a monetary amount, repeating until a valid
    positive number is entered.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value <= 0:
                print("  [X]  Amount must be greater than zero.")
                continue
            return value
        except ValueError:
            print("  [X]  Invalid amount. Please enter a number (e.g. 12.50).")


def choose_category():
    """
    Display the category list and return the user's choice.
    Keeps asking until a valid number is entered.
    """
    print("\n  Choose a category:")
    for idx, cat in enumerate(CATEGORIES, start=1):
        print(f"    {idx:>2}. {cat}")

    while True:
        raw = input("\n  Enter category number: ").strip()
        try:
            choice = int(raw)
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            else:
                print(f"  [X]  Please enter a number between 1 and {len(CATEGORIES)}.")
        except ValueError:
            print("  [X]  Invalid input. Please enter a number.")


def input_nonempty(prompt, max_length=100):
    """
    Prompt for a non-empty string (stripped whitespace).
    Also enforces a maximum character length to prevent very long entries.
    """
    while True:
        value = input(prompt).strip()
        if not value:
            print("  [X]  This field cannot be empty.")
        elif len(value) > max_length:
            print(f"  [X]  Input too long (max {max_length} characters).")
        else:
            return value


# ─────────────────────────────────────────────
#  CORE FEATURES
# ─────────────────────────────────────────────

def add_expense():
    """
    Prompt the user for expense details, then append the new
    expense to the data file.
    """
    print_header("ADD NEW EXPENSE")

    # Gather details from the user.
    category    = choose_category()
    description = input_nonempty("\n  Description : ")
    amount      = input_amount(  "  Amount ($)  : ")

    # Use today's date automatically.
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Load existing data, create new record, save everything back.
    expenses    = load_expenses()
    new_expense = {
        "id":          next_id(expenses),
        "date":        date_str,
        "category":    category,
        "description": description,
        "amount":      amount,
    }
    expenses.append(new_expense)
    save_expenses(expenses)

    print(f"\n  [OK] Expense #{new_expense['id']} saved successfully!")
    print(f"     {date_str}  |  {category}  |  {description}  |  ${amount:.2f}")


def view_all_expenses(expenses=None):
    """
    Display every expense in a formatted table.
    If `expenses` is not provided, loads from file.
    """
    print_header("ALL EXPENSES")

    if expenses is None:
        expenses = load_expenses()

    if not expenses:
        print("  No expenses recorded yet.")
        return

    # Column widths for a tidy table.
    print(f"  {'ID':>4}  {'Date':<12}  {'Category':<14}  {'Description':<28}  {'Amount':>8}")
    print_divider()

    for e in expenses:
        desc_truncated = e["description"][:26] + ".." if len(e["description"]) > 28 else e["description"]
        print(
            f"  {e['id']:>4}  {e['date']:<12}  {e['category']:<14}  "
            f"{desc_truncated:<28}  ${e['amount']:>7.2f}"
        )

    print_divider()
    total = sum(e["amount"] for e in expenses)
    print(f"  {'TOTAL':>4}  {'':12}  {'':14}  {'':28}  ${total:>7.2f}")


def delete_expense():
    """
    Show all expenses, ask for an ID, confirm deletion, then
    remove that record from the file.
    """
    print_header("DELETE EXPENSE")

    expenses = load_expenses()

    if not expenses:
        print("  No expenses to delete.")
        return

    view_all_expenses(expenses)

    # Ask which record to delete.
    raw = input("\n  Enter the ID to delete (or 0 to cancel): ").strip()
    try:
        target_id = int(raw)
    except ValueError:
        print("  [X]  Invalid ID entered.")
        return

    if target_id == 0:
        print("  Deletion cancelled.")
        return

    # Find the matching expense.
    match = next((e for e in expenses if e["id"] == target_id), None)
    if match is None:
        print(f"  [X]  No expense found with ID {target_id}.")
        return

    # Show what will be deleted and ask for confirmation.
    print(f"\n  You are about to delete:")
    print(f"    #{match['id']}  {match['date']}  |  {match['category']}  |  "
          f"{match['description']}  |  ${match['amount']:.2f}")
    confirm = input("\n  Are you sure? (yes/no): ").strip().lower()

    if confirm in ("yes", "y"):
        expenses = [e for e in expenses if e["id"] != target_id]
        save_expenses(expenses)
        print(f"  [OK] Expense #{target_id} deleted.")
    else:
        print("  Deletion cancelled.")


def view_summary():
    """
    Show total spending and a breakdown by category,
    along with the percentage each category represents.
    """
    print_header("SPENDING SUMMARY")

    expenses = load_expenses()

    if not expenses:
        print("  No expenses recorded yet.")
        return

    total = sum(e["amount"] for e in expenses)

    # Build a dict of { category: total_amount }.
    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = (
            category_totals.get(e["category"], 0.0) + e["amount"]
        )

    # Sort categories by spending (highest first).
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)

    print(f"\n  {'Category':<16}  {'Total':>9}  {'Share':>7}  Bar")
    print_divider()
    for cat, cat_total in sorted_cats:
        pct = (cat_total / total) * 100
        bar = "#" * int(pct / 5)           # simple ASCII bar (each block ~= 5%)
        print(f"  {cat:<16}  ${cat_total:>8.2f}   {pct:>5.1f}%  {bar}")

    print_divider()
    print(f"  {'GRAND TOTAL':<16}  ${total:>8.2f}")
    print(f"\n  Expense count: {len(expenses)}")
    if expenses:
        avg = total / len(expenses)
        print(f"  Average per entry: ${avg:.2f}")


def filter_by_category():
    """
    Let the user pick a category, then display only those expenses.
    """
    print_header("FILTER BY CATEGORY")

    category = choose_category()
    expenses  = load_expenses()

    filtered = [e for e in expenses if e["category"].lower() == category.lower()]

    if not filtered:
        print(f"\n  No expenses found in category '{category}'.")
        return

    print(f"\n  Showing {len(filtered)} expense(s) in '{category}':\n")
    view_all_expenses(filtered)


def search_expenses():
    """
    Search all expense descriptions for a keyword (case-insensitive)
    and display matching results.
    """
    print_header("SEARCH EXPENSES")

    keyword  = input_nonempty("  Enter search keyword: ")
    expenses = load_expenses()

    # Case-insensitive substring match on description.
    results = [
        e for e in expenses
        if keyword.lower() in e["description"].lower()
    ]

    if not results:
        print(f"\n  No expenses matched '{keyword}'.")
        return

    print(f"\n  Found {len(results)} matching expense(s):\n")
    view_all_expenses(results)


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

# Each entry: "key": (display_label, function_to_call)
# None as the function signals "exit".
MENU_OPTIONS = {
    "1": ("Add Expense",           add_expense),
    "2": ("View All Expenses",     lambda: view_all_expenses()),
    "3": ("Delete Expense",        delete_expense),
    "4": ("Spending Summary",      view_summary),
    "5": ("Filter by Category",    filter_by_category),
    "6": ("Search Expenses",       search_expenses),
    "7": ("Exit",                  None),
}


def show_menu():
    """Render the main menu and return the user's choice."""
    print_header("Personal Expense Tracker")
    for key, (label, _) in MENU_OPTIONS.items():
        print(f"    {key}. {label}")
    print_divider()
    return input("  Choose an option [1-7]: ").strip()


def main():
    """
    Application entry point.
    Runs the main menu loop until the user chooses to exit.
    """
    # Greet the user with a welcome banner.
    clear_screen()
    print("\n" + "=" * 55)
    print("  Welcome to the Personal Expense Tracker!")
    print(f"  Data file: {os.path.abspath(DATA_FILE)}")
    print("=" * 55)
    pause()

    # ── Main event loop ──────────────────────────────────
    while True:
        clear_screen()
        choice = show_menu()

        if choice not in MENU_OPTIONS:
            print("\n  [X]  Invalid option. Please choose 1-7.")
            pause()
            continue

        label, action = MENU_OPTIONS[choice]

        # Option 7 means "Exit".
        if action is None:
            clear_screen()
            print("\n  Goodbye! Your expenses are saved in:")
            print(f"      {os.path.abspath(DATA_FILE)}\n")
            sys.exit(0)

        # Run the selected feature, catching any unexpected errors
        # so a bug in one feature doesn't crash the whole program.
        try:
            clear_screen()
            action()
        except KeyboardInterrupt:
            # Allow Ctrl+C inside a sub-menu to return to main menu.
            print("\n\n  Interrupted -- returning to menu.")
        except Exception as exc:
            print(f"\n  [X]  Unexpected error: {exc}")
            print("     Please try again or check the data file for corruption.")

        pause()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()
