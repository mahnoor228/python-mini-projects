# Expense Tracker

A small command-line expense tracker. Expenses are stored in `expenses.csv`
next to the script (created automatically on first use).

## How to run

```bash
python expenses.py add --amount 12.50 --category food --note "lunch"
python expenses.py add --amount 45 --category transport --date 2026-11-15
python expenses.py list
python expenses.py list --category food
python expenses.py summary
python expenses.py summary --month 2026-11
```

## Commands

| Command | What it does |
| --- | --- |
| `add --amount X --category C [--note N] [--date YYYY-MM-DD]` | Record an expense (date defaults to today). |
| `list [--category C]` | Show all recorded expenses. |
| `summary [--month YYYY-MM]` | Monthly totals by category, plus an overall total. |

## Requirements

Python 3.10+, standard library only — no installs needed.
