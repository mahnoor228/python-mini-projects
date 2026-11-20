#!/usr/bin/env python3
"""A flashcard quizzer: loads a JSON deck, quizzes you, re-tests missed cards.

Usage:
    python flashcards.py                                   # bundled CS deck
    python flashcards.py --deck decks/cs-fundamentals.json
    python flashcards.py --deck my-deck.json --no-shuffle

Deck format: a JSON list of {"q": "...", "a": "..."} objects.
Answers are compared case-insensitively, ignoring extra whitespace.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

DEFAULT_DECK = Path(__file__).resolve().parent / "decks" / "cs-fundamentals.json"


def load_deck(path: Path) -> list[dict[str, str]]:
    """Load and validate a JSON flashcard deck."""
    if not path.exists():
        raise FileNotFoundError(f"deck not found: {path}")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or not data:
        raise ValueError(
            'deck must be a non-empty JSON list of {"q", "a"} objects'
        )
    for i, card in enumerate(data):
        if not isinstance(card, dict) or "q" not in card or "a" not in card:
            raise ValueError(f"card {i} must have 'q' and 'a' fields")
    return data


def _normalize(text: str) -> str:
    """Lowercase and collapse whitespace so answers compare forgivingly."""
    return " ".join(text.strip().lower().split())


def ask_cards(cards: list[dict[str, str]],
              label: str) -> tuple[list[dict[str, str]], int]:
    """Quiz the given cards; return (missed cards, number correct)."""
    missed: list[dict[str, str]] = []
    correct = 0
    for i, card in enumerate(cards, start=1):
        print(f"\n[{label} {i}/{len(cards)}] {card['q']}")
        answer = input("Your answer: ")
        if _normalize(answer) == _normalize(card["a"]):
            print("Correct!")
            correct += 1
        else:
            print(f"Not quite. The answer is: {card['a']}")
            missed.append(card)
    return missed, correct


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Quiz yourself with flashcards from a JSON deck."
    )
    parser.add_argument("--deck", type=Path, default=DEFAULT_DECK,
                        help="Path to a JSON deck file "
                             "(default: decks/cs-fundamentals.json).")
    parser.add_argument("--no-shuffle", action="store_true",
                        help="Ask cards in file order instead of shuffling.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        cards = load_deck(args.deck)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if not args.no_shuffle:
        random.shuffle(cards)
    total = len(cards)
    print(f"Loaded {total} cards from {args.deck.name}. Good luck!")
    try:
        missed, correct = ask_cards(cards, "Q")
    except (EOFError, KeyboardInterrupt):
        print("\nQuiz stopped early.")
        return 0
    print(f"\nRound 1 score: {correct}/{total}")
    if not missed:
        print("Perfect score! Nice work!")
        return 0
    print(f"\nYou missed {len(missed)} card(s). Let's review them!")
    if not args.no_shuffle:
        random.shuffle(missed)
    try:
        missed_again, correct_again = ask_cards(missed, "Review")
    except (EOFError, KeyboardInterrupt):
        print("\nQuiz stopped early.")
        return 0
    correct += correct_again
    print(f"\nFinal score: {correct}/{total}")
    if missed_again:
        print("\nStill missed — review these:")
        for card in missed_again:
            print(f"  - {card['q']} → {card['a']}")
    else:
        print("All cards answered correctly. Nice work!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
