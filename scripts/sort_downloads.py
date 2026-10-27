#!/usr/bin/env python3
"""Sort downloads into folders by file type.

Safety first: by default this runs in dry-run mode (prints a plan, changes
nothing). With --apply it COPIES files into a destination folder. Originals
are never moved or deleted.
"""

import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico"],
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx",
        ".ppt", ".pptx", ".csv", ".md",
    ],
    "Audio": [".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".wma"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
}


def category_for(suffix: str) -> str:
    suffix = suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Other"


def unique_path(dest: Path, name: str) -> Path:
    """Return a non-colliding path inside dest for the given file name."""
    candidate = dest / name
    if not candidate.exists():
        return candidate
    stem = Path(name).stem
    suffix = Path(name).suffix
    counter = 1
    while True:
        candidate = dest / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def plan_files(source: Path):
    """Yield (source_path, category, dest_name) for every file in source."""
    for item in sorted(source.iterdir()):
        if item.is_file() and not item.name.startswith("."):
            cat = category_for(item.suffix)
            yield item, cat, item.name


def run(source: Path, dest: Path, apply: bool) -> int:
    if not source.exists() or not source.is_dir():
        print(f"Error: source folder not found: {source}")
        return 1

    items = list(plan_files(source))
    if not items:
        print(f"No files to sort in {source}")
        return 0

    mode = "APPLY (copying files)" if apply else "DRY-RUN (nothing changes)"
    print(f"Sorting downloads from: {source}")
    print(f"Mode: {mode}")
    print()

    copied = 0
    for src_path, category, name in items:
        dest_dir = dest / category
        target = unique_path(dest_dir, name)
        print(f"  {src_path.name}  ->  {target}")
        if apply:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, target)
            copied += 1

    print()
    if apply:
        print(f"Done. Copied {copied} file(s) into {dest}")
        print("Originals are untouched.")
    else:
        print("Dry-run complete. Re-run with --apply to copy files.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Sort downloads into folders by file type. Dry-run by default."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.home() / "Downloads",
        help="Folder to sort (default: ~/Downloads)",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path.home() / "Sorted Downloads",
        help="Destination folder for sorted copies (default: ~/Sorted Downloads)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually copy files. Without this, only a plan is printed.",
    )
    args = parser.parse_args(argv)
    return run(args.source, args.dest, args.apply)


if __name__ == "__main__":
    sys.exit(main())
