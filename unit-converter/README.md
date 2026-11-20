# Unit Converter

Converts values between US ("freedom") units and metric units — miles to
kilometers, pounds to kilograms, inches to centimeters, and a few more.
Seriously, can we switch to metric?

## How to run

```bash
python unit_converter.py 10 miles kilometers
python unit_converter.py 5 pounds kg
python unit_converter.py --gui        # Tkinter window version
python unit_converter.py --list       # see all supported units
```

## Options

| Argument | What it does |
| --- | --- |
| `value` | The number to convert. |
| `from_unit` | Unit to convert from (miles, km, lb, in, ft, oz, …). |
| `to_unit` | Unit to convert to. |
| `--gui` | Open the Tkinter window: type a value, pick the units, hit Convert. |
| `--list` | List the supported units and exit. |

## Requirements

Python 3.10+, standard library only (Tkinter ships with Python) — no installs needed.
