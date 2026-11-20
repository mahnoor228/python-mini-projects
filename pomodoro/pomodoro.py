#!/usr/bin/env python3
"""A Pomodoro focus timer.

Usage:
    python pomodoro.py                            # 4 cycles, 25 min focus / 5 min break
    python pomodoro.py --focus 50 --break 10 --cycles 2
    python pomodoro.py --focus 0.05 --break 0.05 --cycles 1   # quick test run

Press Ctrl+C at any time to stop early; the summary shows what you completed.
"""

from __future__ import annotations

import argparse
import sys
import time


def _countdown(total_seconds: int, label: str) -> None:
    """Print a live mm:ss countdown on a single line."""
    for remaining in range(total_seconds, 0, -1):
        minutes, seconds = divmod(remaining, 60)
        print(f"\r{label}: {minutes:02d}:{seconds:02d} remaining",
              end="", flush=True)
        time.sleep(1)
    print(f"\r{label}: 00:00 done!{' ' * 20}")


def _ring_bell() -> None:
    """Sound the terminal bell to mark a transition."""
    print("\a", end="", flush=True)


def _positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return number


def _positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return number


def run(focus: float, break_minutes: float, cycles: int) -> None:
    """Run the requested number of focus/break cycles."""
    focus_seconds = max(1, int(round(focus * 60)))
    break_seconds = max(1, int(round(break_minutes * 60)))
    total_focus = 0
    total_break = 0
    completed = 0
    try:
        for cycle in range(1, cycles + 1):
            print(f"\n--- Cycle {cycle}/{cycles}: "
                  f"focus for {focus:g} min ---")
            _countdown(focus_seconds, "Focus")
            _ring_bell()
            total_focus += focus_seconds
            completed += 1
            print("Focus session complete. Time for a break!")
            if cycle < cycles:
                print(f"--- Break for {break_minutes:g} min ---")
                _countdown(break_seconds, "Break")
                _ring_bell()
                total_break += break_seconds
                print("Break over. Back to focus!")
    except KeyboardInterrupt:
        print("\nTimer stopped early.")
    print("\n=== Session summary ===")
    print(f"Cycles completed: {completed} focus session(s) finished")
    print(f"Total focus time: {total_focus // 60} min "
          f"{total_focus % 60} sec")
    print(f"Total break time: {total_break // 60} min "
          f"{total_break % 60} sec")
    print("Nice work!")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A Pomodoro focus timer.")
    parser.add_argument("--focus", type=_positive_float, default=25.0,
                        help="Focus minutes per cycle (default: 25).")
    parser.add_argument("--break", dest="break_minutes",
                        type=_positive_float, default=5.0,
                        help="Break minutes between cycles (default: 5).")
    parser.add_argument("--cycles", type=_positive_int, default=4,
                        help="Number of focus cycles (default: 4).")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(args.focus, args.break_minutes, args.cycles)
    return 0


if __name__ == "__main__":
    sys.exit(main())
