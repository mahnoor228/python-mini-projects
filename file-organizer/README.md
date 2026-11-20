# File Organizer

Sorts the files in a folder into subfolders by type: Images, Documents,
Videos, Audio, Archives, Code, and Other (based on file extension). Hidden
files are skipped, directories are never moved, and name collisions are
resolved by adding a number, e.g. `photo (1).jpg`.

## How to run

```bash
python organize.py ~/Downloads
python organize.py ~/Downloads --dry-run    # preview the moves, change nothing
python organize.py ./messy-folder
```

## Options

| Flag | Default | What it does |
| --- | --- | --- |
| `target` | `~/Downloads` | Folder to organize. |
| `--dry-run` | off | Print the planned moves without moving anything. |

## Requirements

Python 3.10+, standard library only — no installs needed.
