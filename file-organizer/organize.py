#!/usr/bin/env python3
"""Sort the files in a folder into subfolders by file type.

Usage:
    python organize.py ~/Downloads
    python organize.py ~/Downloads --dry-run
    python organize.py ./messy-folder

Hidden files are skipped, directories are never moved, and name collisions
are resolved by adding a number, e.g. photo (1).jpg.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg",
               ".heic", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".xls",
                  ".xlsx", ".ppt", ".pptx", ".csv", ".odt"},
    "Videos": {".mp4", ".mov", ".mkv", ".avi", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c",
             ".h", ".json", ".sh", ".rs", ".go"},
}


def category_for(path: Path) -> str:
    """Return the category folder for a file based on its extension."""
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Other"


def _unique_destination(folder: Path, name: str) -> Path:
    """Return a non-colliding destination path inside folder."""
    dest = folder / name
    if not dest.exists():
        return dest
    stem, suffix = Path(name).stem, Path(name).suffix
    i = 1
    while True:
        candidate = folder / f"{stem} ({i}){suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def organize(target: Path, dry_run: bool) -> dict[str, int]:
    """Move (or preview moving) every file in target into category folders."""
    planned: list[tuple[Path, Path, str]] = []
    for entry in sorted(target.iterdir()):
        if entry.is_dir() or entry.name.startswith("."):
            continue
        category = category_for(entry)
        dest = _unique_destination(target / category, entry.name)
        planned.append((entry, dest, category))

    counts: dict[str, int] = {}
    for entry, dest, category in planned:
        if dry_run:
            print(f"Would move: {entry.name} -> {category}/{dest.name}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            entry.rename(dest)
            print(f"Moved: {entry.name} -> {category}/{dest.name}")
        counts[category] = counts.get(category, 0) + 1

    print()
    print("Summary (dry run — nothing was moved):" if dry_run else "Summary:")
    for category in sorted(counts):
        print(f"  {category}: {counts[category]} file(s)")
    print(f"  Total: {sum(counts.values())} file(s)")
    return counts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sort a folder's files into subfolders by type."
    )
    parser.add_argument("target", nargs="?", type=Path,
                        default=Path.home() / "Downloads",
                        help="Folder to organize (default: ~/Downloads).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview the moves without moving anything.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.target.exists() or not args.target.is_dir():
        parser.error(f"{args.target} is not an existing directory")
    organize(args.target, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
