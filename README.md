# Python Mini Projects

A collection of small, genuinely useful command-line tools — each one a
complete, working program in a single file. Built to practice clean Python:
type hints, docstrings, `argparse` CLIs, and zero dependencies.

**Python 3.10+** — every project uses the standard library only, except the
QR Code Generator, which needs the `qrcode` library
(`pip install -r qr-code-generator/requirements.txt`).

| Project | What it does | How to run |
| --- | --- | --- |
| [expense-tracker](expense-tracker/) | CLI expense tracker backed by a CSV file | `python expense-tracker/expenses.py add --amount 12.50 --category food` |
| [pomodoro](pomodoro/) | Pomodoro focus timer with live countdown | `python pomodoro/pomodoro.py` |
| [password-generator](password-generator/) | Secure passwords and passphrases with strength ratings | `python password-generator/passgen.py --length 24` |
| [file-organizer](file-organizer/) | Sorts a folder's files into subfolders by type | `python file-organizer/organize.py ~/Downloads --dry-run` |
| [unit-converter](unit-converter/) | US ↔ metric unit converter, CLI + Tkinter GUI | `python unit-converter/unit_converter.py 10 miles kilometers` |
| [qr-code-generator](qr-code-generator/) | Generates a QR code image from text or a URL | `python qr-code-generator/qr_generator.py "https://example.com"` |
| [flashcard-quiz](flashcard-quiz/) | Flashcard quizzer with a missed-card review round | `python flashcard-quiz/flashcards.py` |

Each project folder has its own README with full usage and examples.
