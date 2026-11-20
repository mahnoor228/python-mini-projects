#!/usr/bin/env python3
"""A simple CLI expense tracker backed by a CSV file.

Usage:
    python expenses.py add --amount 12.50 --category food --note "lunch"
    python expenses.py list
    python expenses.py list --category food
    python expenses.py summary
    python expenses.py summary --month 2026-11
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent / "expenses.csv"
FIELDNAMES = ["date", "category", "amount", "note"]


def _ensure_csv() -> None:
    """Create the CSV file with a header row if it does not exist yet."""
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()


def _read_expenses() -> list[dict[str, str]]:
    _ensure_csv()
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("amount must be greater than 0")
    return number


def _valid_date(value: str) -> str:
    try:
        date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"invalid date {value!r}: use YYYY-MM-DD"
        ) from None
    return value


def cmd_add(args: argparse.Namespace) -> int:
    """Append one expense row to the CSV file."""
    _ensure_csv()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "date": args.date,
            "category": args.category,
            "amount": f"{args.amount:.2f}",
            "note": args.note or "",
        })
    message = f"Added ${args.amount:.2f} to {args.category} on {args.date}"
    if args.note:
        message += f" ({args.note})"
    print(message)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """Print all recorded expenses, optionally filtered by category."""
    rows = _read_expenses()
    if args.category:
        rows = [r for r in rows
                if r["category"].lower() == args.category.lower()]
    if not rows:
        print("No expenses recorded yet.")
        return 0
    print(f"{'Date':<12} {'Category':<15} {'Amount':>10}  Note")
    print("-" * 60)
    for row in rows:
        print(f"{row['date']:<12} {row['category']:<15} "
              f"${float(row['amount']):>9.2f}  {row['note']}")
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    """Print monthly totals broken down by category, plus an overall total."""
    rows = _read_expenses()
    month = args.month or date.today().strftime("%Y-%m")
    rows = [r for r in rows if r["date"].startswith(month)]
    if not rows:
        print(f"No expenses recorded for {month}.")
        return 0
    totals: dict[str, float] = defaultdict(float)
    for row in rows:
        totals[row["category"]] += float(row["amount"])
    overall = sum(totals.values())
    print(f"Summary for {month}")
    print("-" * 30)
    for category in sorted(totals):
        print(f"{category:<15} ${totals[category]:>9.2f}")
    print("-" * 30)
    print(f"{'Total':<15} ${overall:>9.2f}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Track expenses in a local CSV file."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add an expense.")
    p_add.add_argument("--amount", type=_positive_float, required=True,
                       help="Amount spent, e.g. 12.50.")
    p_add.add_argument("--category", required=True,
                       help="Category, e.g. food, transport, fun.")
    p_add.add_argument("--note", help="Optional note about the expense.")
    p_add.add_argument("--date", type=_valid_date,
                       default=date.today().isoformat(),
                       help="Date as YYYY-MM-DD (default: today).")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List recorded expenses.")
    p_list.add_argument("--category",
                        help="Only show expenses in this category.")
    p_list.set_defaults(func=cmd_list)

    p_sum = sub.add_parser("summary", help="Monthly totals by category.")
    p_sum.add_argument("--month",
                       help="Month as YYYY-MM (default: current month).")
    p_sum.set_defaults(func=cmd_summary)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
