#!/usr/bin/env python3
"""
I Love You in 20 Languages — a heart in the terminal.

Prints "I love you" in 20 languages, one language per row,
arranged so the lines form a heart.

From the Instagram reel by @buildmeri (irem):
    "Coding 'I love you' in 20 languages in the terminal"
    https://www.instagram.com/reel/DgOHHR3owsV/

Run it:
    python heart.py            # line-by-line, like the reel
    python heart.py --fast     # print the whole heart at once

Standard library only. Python 3.10+.
"""

import argparse
import sys
import time
import unicodedata

# (language, phrase, pronunciation / transliteration)
PHRASES = [
    ("English", "I love you", "I love you"),
    ("Spanish", "Te amo", "Te amo"),
    ("French", "Je t'aime", "Je t'aime"),
    ("German", "Ich liebe dich", "Ich liebe dich"),
    ("Portuguese", "Eu te amo", "Eu te amo"),
    ("Italian", "Ti amo", "Ti amo"),
    ("Dutch", "Ik hou van je", "Ik hou van je"),
    ("Swedish", "Jag älskar dig", "Jag älskar dig"),
    ("Polish", "Kocham cię", "Kocham cię"),
    ("Turkish", "Seni seviyorum", "Seni seviyorum"),
    ("Russian", "Я тебя люблю", "Ya tebya lyublyu"),
    ("Greek", "Σ' αγαπώ", "S' agapó"),
    ("Arabic", "أحبك", "Uhibbuk"),
    ("Hindi", "मैं तुमसे प्यार करती हूँ", "Main tumse pyaar karti hoon"),
    ("Urdu", "میں تم سے محبت کرتی ہوں", "Main tum se mohabbat karti hoon"),
    ("Indonesian", "Aku cinta padamu", "Aku cinta padamu"),
    ("Vietnamese", "Tôi yêu bạn", "Tôi yêu bạn"),
    ("Japanese", "愛してる", "Aishiteru"),
    ("Korean", "사랑해", "Saranghae"),
    ("Chinese", "我爱你", "Wǒ ài nǐ"),
]

# Colours: bright red and bright magenta, alternating by row.
RED = "\033[1;91m"
PINK = "\033[1;95m"
RESET = "\033[0m"


def display_width(text: str) -> int:
    """Visible terminal width, counting wide CJK characters as 2."""
    width = 0
    for char in text:
        width += 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
    return width


def trim_to_width(text: str, width: int) -> str:
    """Trim text to exactly `width` display columns, without splitting a wide char."""
    out = []
    used = 0
    for char in text:
        char_width = 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
        if used + char_width > width:
            break
        out.append(char)
        used += char_width
    return "".join(out) + " " * (width - used)


def fill_segment(phrase: str, length: int) -> str:
    """Repeat `phrase` until it fills a segment of `length` display columns."""
    repeated = (phrase + " ") * ((length // max(display_width(phrase) + 1, 1)) + 2)
    return trim_to_width(repeated, length)


def heart_rows(width: int = 72, height: int = 25) -> list[str]:
    """Build the heart mask.

    Uses the classic heart curve (x^2 + y^2 - 1)^3 - x^2 * y^3 <= 0.
    With height=25 the mask has exactly 20 non-empty rows,
    one for each language.
    """
    rows = []
    for row in range(height):
        y = 1.25 - row * (2.60 / (height - 1))
        line = ""
        for col in range(width):
            x = -1.6 + col * (3.2 / (width - 1))
            inside = (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0
            line += "#" if inside else " "
        if "#" in line:
            rows.append(line)
    return rows


def build_heart(use_color: bool = True) -> list[str]:
    """Return the heart as a list of printable lines, one language per row."""
    lines = []
    for i, mask in enumerate(heart_rows()):
        _, phrase, _ = PHRASES[i]
        line = ""
        col = 0
        while col < len(mask):
            if mask[col] == "#":
                end = col
                while end < len(mask) and mask[end] == "#":
                    end += 1
                line += fill_segment(phrase, end - col)
                col = end
            else:
                line += " "
                col += 1
        if use_color:
            colour = RED if i % 2 == 0 else PINK
            line = colour + line.rstrip() + RESET
        else:
            line = line.rstrip()
        lines.append(line)
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print 'I love you' in 20 languages as a heart."
    )
    parser.add_argument("--fast", action="store_true", help="print the whole heart at once")
    parser.add_argument("--delay", type=float, default=0.35, help="seconds between lines (default 0.35)")
    parser.add_argument("--no-color", action="store_true", help="print without colour")
    parser.add_argument("--no-legend", action="store_true", help="skip the language list at the end")
    args = parser.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    use_color = not args.no_color

    print()
    print("  One heart. 20 languages. Just Python.")
    print()

    for line in build_heart(use_color=use_color):
        print(line, flush=True)
        if not args.fast:
            time.sleep(args.delay)

    if not args.no_legend:
        print()
        for i, (language, phrase, pron) in enumerate(PHRASES, start=1):
            extra = f"  ({pron})" if pron != phrase else ""
            print(f"  {i:>2}. {language:<12} {phrase}{extra}")
        print()
        print("  Which language is yours?")


if __name__ == "__main__":
    main()
