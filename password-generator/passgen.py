#!/usr/bin/env python3
"""Generate cryptographically secure passwords (or passphrases).

Usage:
    python passgen.py                              # one 16-character password
    python passgen.py --length 24 --count 3
    python passgen.py --length 12 --no-symbols
    python passgen.py --passphrase                 # e.g. river-coffee-falcon-meadow
    python passgen.py --passphrase --words 5 --count 2
"""

from __future__ import annotations

import argparse
import secrets
import string
import sys
from random import SystemRandom

LETTERS = string.ascii_letters
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"

# Short, common words for passphrases. This is a small demo-sized list
# (56 words): four words give about 23 bits of entropy, fine for casual
# use — pass --words 5 or 6 for anything important.
WORDS = [
    "apple", "river", "mountain", "coffee", "guitar", "ocean", "forest",
    "planet", "rocket", "sunset", "harbor", "meadow", "falcon", "marble",
    "velvet", "copper", "silver", "golden", "breeze", "thunder", "crystal",
    "willow", "canyon", "desert", "island", "lantern", "mirror", "orchard",
    "pebble", "quartz", "rainbow", "saddle", "tiger", "umbrella", "valley",
    "walnut", "yonder", "zephyr", "anchor", "bridge", "candle", "diamond",
    "ember", "feather", "glacier", "horizon", "ivory", "jungle", "kitten",
    "lemon", "nutmeg", "onyx", "piano", "quilt", "raven", "saffron",
    "tulip", "violet", "wisdom", "yarn", "zenith", "compass", "meadowlark",
]


def generate_password(length: int, use_digits: bool,
                      use_symbols: bool) -> str:
    """Build a password with at least one character from each enabled pool."""
    pool = LETTERS
    required = [secrets.choice(string.ascii_lowercase),
                secrets.choice(string.ascii_uppercase)]
    if use_digits:
        pool += DIGITS
        required.append(secrets.choice(DIGITS))
    if use_symbols:
        pool += SYMBOLS
        required.append(secrets.choice(SYMBOLS))
    chars = required + [secrets.choice(pool)
                        for _ in range(length - len(required))]
    SystemRandom().shuffle(chars)
    return "".join(chars)


def generate_passphrase(words: int) -> str:
    """Join random words with hyphens, e.g. river-coffee-falcon-meadow."""
    return "-".join(secrets.choice(WORDS) for _ in range(words))


def rate_strength(password: str) -> str:
    """Rate a password Weak / Okay / Strong from length and variety."""
    types = sum((
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in SYMBOLS for c in password),
    ))
    if len(password) >= 14 and types >= 3:
        return "Strong"
    if len(password) >= 10 and types >= 2:
        return "Okay"
    return "Weak"


def rate_passphrase(words: int) -> str:
    """Rate a passphrase from its word count."""
    if words >= 4:
        return "Strong"
    if words == 3:
        return "Okay"
    return "Weak"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate cryptographically secure passwords."
    )
    parser.add_argument("--length", type=int, default=16,
                        help="Password length (default: 16).")
    parser.add_argument("--no-symbols", action="store_true",
                        help="Exclude symbols from the password.")
    parser.add_argument("--no-digits", action="store_true",
                        help="Exclude digits from the password.")
    parser.add_argument("--count", type=int, default=1,
                        help="How many passwords to generate (default: 1).")
    parser.add_argument("--passphrase", action="store_true",
                        help="Generate a hyphen-joined word passphrase "
                             "instead of a random password.")
    parser.add_argument("--words", type=int, default=4,
                        help="Words in a passphrase (default: 4).")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.count < 1:
        parser.error("--count must be at least 1")
    if args.passphrase:
        if args.words < 1:
            parser.error("--words must be at least 1")
        for _ in range(args.count):
            phrase = generate_passphrase(args.words)
            print(f"{phrase}  [{rate_passphrase(args.words)}]")
        return 0
    min_length = 2
    if not args.no_digits:
        min_length += 1
    if not args.no_symbols:
        min_length += 1
    if args.length < min_length:
        parser.error(
            f"--length must be at least {min_length} with the enabled "
            "character types (one of each type is always included)"
        )
    for _ in range(args.count):
        password = generate_password(args.length,
                                     use_digits=not args.no_digits,
                                     use_symbols=not args.no_symbols)
        print(f"{password}  [{rate_strength(password)}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
