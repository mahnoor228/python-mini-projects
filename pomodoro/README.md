# Pomodoro Timer

A Pomodoro focus timer for the terminal. Runs focus/break cycles with a live
countdown, rings the terminal bell at each transition, and prints a session
summary at the end. Press Ctrl+C any time to stop early.

## How to run

```bash
python pomodoro.py                              # 4 cycles, 25 min focus / 5 min break
python pomodoro.py --focus 50 --break 10 --cycles 2
python pomodoro.py --focus 0.05 --break 0.05 --cycles 1   # quick test run
```

## Options

| Flag | Default | What it does |
| --- | --- | --- |
| `--focus` | 25 | Focus minutes per cycle. |
| `--break` | 5 | Break minutes between cycles. |
| `--cycles` | 4 | Number of focus cycles. |

## Requirements

Python 3.10+, standard library only — no installs needed.
