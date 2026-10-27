#!/usr/bin/env python3
"""Tests for scripts/bill_reminders.py"""

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "bill_reminders.py"


def run_script(bills_path, *extra):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--bills", str(bills_path), *extra],
        capture_output=True,
        text=True,
    )


class BillRemindersTests(unittest.TestCase):
    def test_upcoming_bills_shown(self):
        today = date.today()
        soon = today + timedelta(days=3)
        later = today + timedelta(days=30)
        bills = [
            {"name": "Electricity", "due_date": soon.isoformat(), "amount": 87.50, "paid": False},
            {"name": "Internet", "due_date": later.isoformat(), "amount": 65.00, "paid": False},
            {"name": "Paid Bill", "due_date": soon.isoformat(), "amount": 10.00, "paid": True},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            bills_path = Path(tmp) / "bills.json"
            bills_path.write_text(json.dumps(bills), encoding="utf-8")

            result = run_script(bills_path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Electricity", result.stdout)
            self.assertNotIn("Internet", result.stdout)
            self.assertNotIn("Paid Bill", result.stdout)
            self.assertIn("$87.50", result.stdout)

    def test_missing_file_errors(self):
        result = run_script(Path("/nonexistent/bills.json"))
        self.assertNotEqual(result.returncode, 0)

    def test_invalid_json_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            bills_path = Path(tmp) / "bills.json"
            bills_path.write_text("{not valid json", encoding="utf-8")
            result = run_script(bills_path)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
