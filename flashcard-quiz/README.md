# Flashcard Quiz

A study flashcard quizzer. Loads a deck from a JSON file, shuffles the cards,
quizzes you, shows your score, then re-quizzes only the cards you missed.

## How to run

```bash
python flashcards.py                                   # bundled CS deck
python flashcards.py --deck decks/cs-fundamentals.json
python flashcards.py --deck my-deck.json --no-shuffle
```

## Deck format

A JSON list of `{"q": ..., "a": ...}` objects:

```json
[
  {"q": "What does OOP stand for?", "a": "Object-Oriented Programming"},
  {"q": "In Python, what keyword defines a function?", "a": "def"}
]
```

Answers are compared case-insensitively, ignoring extra whitespace. The
bundled deck (`decks/cs-fundamentals.json`) has 10 questions on Python, Java,
and data structures basics.

## Options

| Flag | Default | What it does |
| --- | --- | --- |
| `--deck` | `decks/cs-fundamentals.json` | Path to a JSON deck file. |
| `--no-shuffle` | off | Ask cards in file order instead of shuffling. |

## Requirements

Python 3.10+, standard library only — no installs needed.
