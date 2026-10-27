#!/usr/bin/env python3
"""Tests for scripts/sort_downloads.py"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "sort_downloads.py"


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


class SortDownloadsTests(unittest.TestCase):
    def test_dry_run_creates_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            source = tmp / "source"
            source.mkdir()
            dest = tmp / "dest"
            write_file(source, "photo.jpg")
            write_file(source, "report.pdf")

            result = run_script("--source", str(source), "--dest", str(dest))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("DRY-RUN", result.stdout)
            self.assertFalse(dest.exists(), "dry-run must not create the dest folder")
            self.assertTrue((source / "photo.jpg").exists())
            self.assertTrue((source / "report.pdf").exists())

    def test_apply_copies_into_categories(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            source = tmp / "source"
            source.mkdir()
            dest = tmp / "dest"
            write_file(source, "photo.jpg")
            write_file(source, "snapshot.PNG")
            write_file(source, "report.pdf")
            write_file(source, "song.mp3")
            write_file(source, "movie.mp4")
            write_file(source, "archive.zip")
            write_file(source, "setup.exe")
            write_file(source, "weird.xyz")

            result = run_script(
                "--source", str(source), "--dest", str(dest), "--apply"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("APPLY", result.stdout)

            # Originals untouched
            for name in [
                "photo.jpg", "snapshot.PNG", "report.pdf", "song.mp3",
                "movie.mp4", "archive.zip", "setup.exe", "weird.xyz",
            ]:
                self.assertTrue(
                    (source / name).exists(), f"original missing: {name}"
                )

            # Copies landed in the right categories
            self.assertTrue((dest / "Images" / "photo.jpg").exists())
            self.assertTrue((dest / "Images" / "snapshot.PNG").exists())
            self.assertTrue((dest / "Documents" / "report.pdf").exists())
            self.assertTrue((dest / "Audio" / "song.mp3").exists())
            self.assertTrue((dest / "Video" / "movie.mp4").exists())
            self.assertTrue((dest / "Archives" / "archive.zip").exists())
            self.assertTrue((dest / "Installers" / "setup.exe").exists())
            self.assertTrue((dest / "Other" / "weird.xyz").exists())

    def test_apply_handles_name_collisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            source = tmp / "source"
            source.mkdir()
            dest = tmp / "dest"
            write_file(source, "photo.jpg")
            run_script("--source", str(source), "--dest", str(dest), "--apply")
            run_script("--source", str(source), "--dest", str(dest), "--apply")
            self.assertTrue((dest / "Images" / "photo.jpg").exists())
            self.assertTrue((dest / "Images" / "photo (1).jpg").exists())

    def test_missing_source_errors(self):
        result = run_script("--source", "/nonexistent/path/xyz", "--dest", "/tmp/x")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
