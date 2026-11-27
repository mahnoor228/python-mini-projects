# Python Mini Projects

A collection of small, genuinely useful programs — each one a complete,
working project in its own folder. Built to practice clean Python:
type hints, docstrings, `argparse` CLIs, and readable code.

**Python 3.10+** — most projects use the standard library only,
except the QR Code Generator, which needs the `qrcode` library
(`pip install -r qr-code-generator/requirements.txt`). The wave-equation,
stock-portfolio and neural-network projects use NumPy, Matplotlib, pandas,
yfinance, and scikit-learn (`pip install -r <project>/requirements.txt`).

| Project | What it does | How to run |
| --- | --- | --- |
| [expense-tracker](expense-tracker/) | CLI expense tracker backed by a CSV file | `python expense-tracker/expenses.py add --amount 12.50 --category food` |
| [pomodoro](pomodoro/) | Pomodoro focus timer with live countdown | `python pomodoro/pomodoro.py` |
| [password-generator](password-generator/) | Secure passwords and passphrases with strength ratings | `python password-generator/passgen.py --length 24` |
| [file-organizer](file-organizer/) | Sorts a folder's files into subfolders by type | `python file-organizer/organize.py ~/Downloads --dry-run` |
| [unit-converter](unit-converter/) | US ↔ metric unit converter, CLI + Tkinter GUI | `python unit-converter/unit_converter.py 10 miles kilometers` |
| [qr-code-generator](qr-code-generator/) | Generates a QR code image from text or a URL | `python qr-code-generator/qr_generator.py "https://example.com"` |
| [flashcard-quiz](flashcard-quiz/) | Flashcard quizzer with a missed-card review round | `python flashcard-quiz/flashcards.py` |
| [wave-equation-simulator](wave-equation-simulator/) | Vibrating drum skin: damped 2D wave equation, finite differences, animated in 3D | `python wave-equation-simulator/wave_simulator.py` |
| [stock-portfolio-dashboard](stock-portfolio-dashboard/) | Portfolio dashboard from real Yahoo Finance prices: returns, volatility, correlations, drawdowns, risk vs return | `python stock-portfolio-dashboard/portfolio_dashboard.py` |
| [neural-network-from-scratch](neural-network-from-scratch/) | MLP in pure NumPy, trained on real handwritten digits, with loss-landscape + gradient-descent-path plots | `python neural-network-from-scratch/neural_network.py` |
| [i-love-you-heart](i-love-you-heart/) | "I love you" in 20 languages, one per row, forming a heart in the terminal | `python i-love-you-heart/heart.py` |

Each project folder has its own README with full usage and examples.

The stock dashboard uses real market prices via yfinance and the neural net trains on the real sklearn digits dataset — no synthetic data presented as real anywhere in this repo.

