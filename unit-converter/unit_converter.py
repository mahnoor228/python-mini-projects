#!/usr/bin/env python3
"""Convert values between US ("freedom") units and metric units.

Usage:
    python unit_converter.py 10 miles kilometers
    python unit_converter.py 5 pounds kg
    python unit_converter.py --gui

Run with --gui for the Tkinter window version (an input box, from/to
dropdowns, and a Convert button), or convert straight from the command
line. Units are matched case-insensitively and accept common abbreviations
(mi, km, lb, kg, in, cm, ft, m, oz, g).
"""

from __future__ import annotations

import argparse
import sys

# Conversion rates: (from_unit, to_unit) -> multiply the value by this.
CONVERSION_RATES: dict[tuple[str, str], float] = {
    ("miles", "kilometers"): 1.60934,
    ("kilometers", "miles"): 0.621371,
    ("pounds", "kilograms"): 0.453592,
    ("kilograms", "pounds"): 2.20462,
    ("inches", "centimeters"): 2.54,
    ("centimeters", "inches"): 0.393701,
    ("feet", "meters"): 0.3048,
    ("meters", "feet"): 3.28084,
    ("ounces", "grams"): 28.3495,
    ("grams", "ounces"): 0.035274,
}

ALIASES: dict[str, str] = {
    "mi": "miles",
    "mile": "miles",
    "km": "kilometers",
    "kilometer": "kilometers",
    "kph": "kilometers",
    "lb": "pounds",
    "lbs": "pounds",
    "pound": "pounds",
    "kg": "kilograms",
    "kilogram": "kilograms",
    "in": "inches",
    "inch": "inches",
    "cm": "centimeters",
    "centimeter": "centimeters",
    "centimetre": "centimeters",
    "ft": "feet",
    "foot": "feet",
    "m": "meters",
    "meter": "meters",
    "metre": "meters",
    "oz": "ounces",
    "ounce": "ounces",
    "g": "grams",
    "gram": "grams",
}

UNITS: list[str] = sorted({unit for pair in CONVERSION_RATES for unit in pair})


def normalize_unit(unit: str) -> str:
    """Return the canonical unit name for a name or abbreviation."""
    return ALIASES.get(unit.strip().lower(), unit.strip().lower())


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert value from from_unit to to_unit. Raises ValueError if unknown."""
    source, target = normalize_unit(from_unit), normalize_unit(to_unit)
    if source == target:
        return value
    try:
        return value * CONVERSION_RATES[(source, target)]
    except KeyError:
        raise ValueError(
            f"Cannot convert {source} to {target}. "
            f"Supported units: {', '.join(UNITS)}."
        ) from None


def run_gui() -> None:
    """Open the Tkinter Unit Converter window."""
    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title("Unit Converter")

    input_entry = ttk.Entry(root, width=20)
    input_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    input_entry.insert(0, "10")

    from_unit_var = tk.StringVar(value="Miles")
    to_unit_var = tk.StringVar(value="Kilometers")

    from_menu = ttk.OptionMenu(
        root, from_unit_var, "Miles", *[u.title() for u in UNITS]
    )
    from_menu.grid(row=1, column=0, padx=10, pady=5)
    to_menu = ttk.OptionMenu(
        root, to_unit_var, "Kilometers", *[u.title() for u in UNITS]
    )
    to_menu.grid(row=1, column=1, padx=10, pady=5)

    result_label = ttk.Label(root, text="")
    result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def on_convert() -> None:
        try:
            input_value = float(input_entry.get())
            result = convert(
                input_value, from_unit_var.get(), to_unit_var.get()
            )
            result_label.config(
                text=f"{input_value:g} {from_unit_var.get()} = "
                f"{result:.4g} {to_unit_var.get()}"
            )
        except ValueError:
            result_label.config(text="Enter a number, then pick two units.")

    ttk.Button(root, text="Convert", command=on_convert).grid(
        row=2, column=0, columnspan=2, pady=5
    )

    root.mainloop()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert a value between US and metric units."
    )
    parser.add_argument("value", type=float, nargs="?",
                        help="value to convert, e.g. 10")
    parser.add_argument("from_unit", nargs="?",
                        help="unit to convert from, e.g. miles")
    parser.add_argument("to_unit", nargs="?",
                        help="unit to convert to, e.g. kilometers")
    parser.add_argument("--gui", action="store_true",
                        help="open the Tkinter window instead of the CLI")
    parser.add_argument("--list", action="store_true",
                        help="list the supported units and exit")
    args = parser.parse_args(argv)

    if args.list:
        print("Supported units:", ", ".join(UNITS))
        return 0

    if args.gui:
        run_gui()
        return 0

    if args.value is None or not args.from_unit or not args.to_unit:
        parser.error("give a value, a from-unit and a to-unit, or use --gui")
        return 2

    try:
        result = convert(args.value, args.from_unit, args.to_unit)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"{args.value:g} {normalize_unit(args.from_unit)} = "
          f"{result:.4g} {normalize_unit(args.to_unit)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
