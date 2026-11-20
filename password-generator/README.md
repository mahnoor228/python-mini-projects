# Password Generator

Generates cryptographically secure passwords with the `secrets` module, or
memorable hyphen-joined passphrases. Every password includes at least one
character from each enabled character type, and each result gets a simple
strength rating (Weak / Okay / Strong).

## How to run

```bash
python passgen.py                              # one 16-character password
python passgen.py --length 24 --count 3
python passgen.py --length 12 --no-symbols
python passgen.py --passphrase                 # e.g. river-coffee-falcon-meadow
python passgen.py --passphrase --words 5 --count 2
```

## Options

| Flag | Default | What it does |
| --- | --- | --- |
| `--length` | 16 | Password length. |
| `--no-symbols` | off | Exclude symbols. |
| `--no-digits` | off | Exclude digits. |
| `--count` | 1 | How many passwords to generate. |
| `--passphrase` | off | Generate a passphrase instead of a random password. |
| `--words` | 4 | Words in a passphrase (use 5+ for anything important). |

## Requirements

Python 3.10+, standard library only — no installs needed.
