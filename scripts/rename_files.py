#!/usr/bin/env python3
"""Rename batches of files into clean, consistent names.

Safety first: by default this runs in dry-run mode (prints a plan, changes
nothing). With --apply it COPIES renamed files into a destination folder.
Originals are never moved or deleted.
"""

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

DEFAULT_TEMPLATE = "{name}_{date}_{counter}.{ext}"


def slugify(text: str) -> str:
    text = text.strip().replace(" ", "_")
    text = re.sub(r"[^A-Za-z0-9_.\-]", "_", text)
    return text or "file"


def build_name(template: str, index: int, src: Path) -> str:
    today = date.today().isoformat()
    stem = slugify(src.stem)
    ext = src.suffix.lstrip(".")
    counter = f"{index:02d}"
    name = (
        template.replace("{name}", stem)
        .replace("{date}", today)
        .replace("{counter}", counter)
        .replace("{ext}", ext)
    )
    return name


def unique_path(dest: Path, name: str) -> Path:
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


def run(source: Path, pattern: str, dest: Path, template: str, apply: bool) -> int:
    if not source.exists() or not source.is_dir():
        print(f"Error: source folder not found: {source}")
        return 1

    files = sorted(source.glob(pattern))
    files = [f for f in files if f.is_file() and not f.name.startswith(".")]
    if not files:
        print(f"No files matching '{pattern}' in {source}")
        return 0

    mode = "APPLY (copying renamed files)" if apply else "DRY-RUN (nothing changes)"
    print(f"Renaming files in: {source}")
    print(f"Pattern: {pattern}")
    print(f"Template: {template}")
    print(f"Mode: {mode}")
    print()

    copied = 0
    for index, src_path in enumerate(files, start=1):
        new_name = build_name(template, index, src_path)
        target = unique_path(dest, new_name)
        print(f"  {src_path.name}  ->  {target.name}")
        if apply:
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, target)
            copied += 1

    print()
    if apply:
        print(f"Done. Copied {copied} renamed file(s) into {dest}")
        print("Originals are untouched.")
    else:
        print("Dry-run complete. Re-run with --apply to copy renamed files.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Batch rename files into clean names. Dry-run by default."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("."),
        help="Folder containing files to rename (default: current folder)",
    )
    parser.add_argument(
        "--pattern",
        default="*",
        help="Glob pattern for files to rename (default: *)",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path("renamed-output"),
        help="Destination folder for renamed copies (default: renamed-output)",
    )
    parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE,
        help=f"Name template (default: {DEFAULT_TEMPLATE})",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually copy renamed files. Without this, only a plan is printed.",
    )
    args = parser.parse_args(argv)
    return run(args.source, args.pattern, args.dest, args.template, args.apply)


if __name__ == "__main__":
    sys.exit(main())
