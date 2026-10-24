# 💰 Personal Expense Tracker

A lightweight, command-line personal expense tracker written in pure Python. No external libraries required — just Python 3.6+.

---

## Features

| # | Feature |
|---|---------|
| 1 | ➕ Add an expense (category, description, amount) |
| 2 | 📋 View all expenses in a formatted table |
| 3 | 🗑️ Delete an expense by ID (with confirmation) |
| 4 | 📊 Spending summary with ASCII bar chart per category |
| 5 | 🔍 Filter expenses by category |
| 6 | 🔎 Search expenses by keyword |

---

## Requirements

- Python **3.6** or higher
- No third-party packages needed

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/expense-tracker.git
cd expense-tracker

# Run the tracker
python expense_tracker.py
```

---

## How It Works

All expenses are saved to **`expenses.txt`** in the same directory, using a simple pipe-delimited format:

```
ID|Date|Category|Description|Amount
1|2026-10-25|Food|Lunch at cafe|12.50
2|2026-10-25|Transport|Uber to office|8.00
```

This means:
- ✅ No database or setup required
- ✅ Data is human-readable and editable in any text editor
- ✅ Easy to back up or transfer

---

## Menu

```
=======================================================
  Personal Expense Tracker
=======================================================
    1. Add Expense
    2. View All Expenses
    3. Delete Expense
    4. Spending Summary
    5. Filter by Category
    6. Search Expenses
    7. Exit
```

---

## Code Structure

| Section | Description |
|---------|-------------|
| **Configuration** | `DATA_FILE`, `CATEGORIES`, `DELIMITER` constants |
| **File I/O** | `load_expenses()`, `save_expenses()`, `next_id()` |
| **Input Helpers** | Validated prompts — amount, category, text fields |
| **Core Features** | One function per menu item |
| **Main Menu** | Dict-driven menu loop with graceful error handling |

---

## License

MIT — free to use, modify, and share.
