#!/usr/bin/env python3
"""Tests for scripts/rename_files.py"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "rename_files.py"


def write_file(folder: Path, name: str, content: str = "x") -> Path:
    p = folder / name
    p.write_text(content, encoding="utf-8")
    return p


def run_script(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


class RenameFilesTests(unittest.TestCase):
    def test_dry_run_creates_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            source = tmp / "source"
            source.mkdir()
            dest = tmp / "dest"
            write_file(source, "IMG_001.jpg")
            write_file(source, "IMG_002.jpg")

            result = run_script("--source", str(source), "--dest", str(dest))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("DRY-RUN", result.stdout)
            self.assertFalse(dest.exists())
            self.assertTrue((source / "IMG_001.jpg").exists())

    def test_apply_renames_and_copies(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            source = tmp / "source"
            source.mkdir()
            dest = tmp / "dest"
            write_file(source, "vacation.jpg")
            write_file(source, "cat.png")

            result = run_script(
                "--source", str(source),
                "--dest", str(dest),
                "--template", "{name}_{date}_{counter}.{ext}",
                "--apply",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("APPLY", result.stdout)

            # Originals untouched
            self.assertTrue((source / "vacation.jpg").exists())
            self.assertTrue((source / "cat.png").exists())

            # Renamed copies exist
            copied = sorted(p.name for p in dest.iterdir())
            self.assertEqual(len(copied), 2)
            self.assertTrue(all(name.endswith((".jpg", ".png")) for name in copied))
            self.assertTrue(all("_" in name for name in copied))

    def test_pattern_filters_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            source = tmp / "source"
            source.mkdir()
            dest = tmp / "dest"
            write_file(source, "a.txt")
            write_file(source, "b.jpg")

            result = run_script(
                "--source", str(source), "--pattern", "*.jpg",
                "--dest", str(dest), "--apply",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            names = sorted(p.name for p in dest.iterdir())
            self.assertEqual(names, [n for n in names if n.endswith(".jpg")])

    def test_missing_source_errors(self):
        result = run_script("--source", "/nonexistent/path/xyz")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
