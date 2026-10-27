# STATUS

## What was built

A beginner-friendly guide to four simple automations, published by Asdale Dynamics, LLC.

**Project contents**

| Folder | Contents |
|--------|----------|
| `docs/` | Six Markdown manuals: intro, safety, sorting-downloads, renaming-files, bill-reminders, saving-webpages |
| `static/` | A small HTML site: `index.html`, `safety.html`, `sorting-downloads.html`, `renaming-files.html`, `bill-reminders.html`, `saving-webpages.html`, plus `style.css` |
| `scripts/` | Four Python scripts: `sort_downloads.py`, `rename_files.py`, `bill_reminders.py`, `save_webpage.py`, plus `bills.json.example` |
| `tests/` | Eleven unit tests using the standard-library `unittest` framework |

**Safety design (core requirement)**

- Every script runs in dry-run mode by default: it prints a plan and changes nothing.
- With `--apply`, scripts COPY files into a new destination folder. Originals are never moved or deleted.
- Name collisions are handled with a `(1)`, `(2)` suffix so nothing is overwritten.
- No secrets, API keys, or personal data anywhere. `bills.json.example` uses clearly example-only data.

## How to run it

**Prerequisites:** Python 3 (Windows, Mac, or Linux). No external packages required.

```bash
# 1. Read the safety rules first
#    (docs/safety.md or static/safety.html)

# 2. Run any script in dry-run mode (safe, nothing changes):
python3 scripts/sort_downloads.py
python3 scripts/rename_files.py --source ./my-photos --pattern "*.jpg"
python3 scripts/bill_reminders.py --bills scripts/bills.json.example
python3 scripts/save_webpage.py "https://example.com"

# 3. When comfortable, back up your folder and run with --apply to copy files for real:
python3 scripts/sort_downloads.py --apply
```

**Static site:** open any file in `static/` (e.g. `static/index.html`) directly in a web browser. No build step required.

## Verification results

- Tests: `python3 -m unittest discover -s tests` → **11 tests, 11 passed, 0 failed** (OK)
- `python3 -m py_compile scripts/*.py` → compile OK
- `scripts/bills.json.example` → valid JSON
- All six `static/*.html` files → parse as valid HTML
- End-to-end smoke tests on temp folders → all four scripts copy files correctly into the right categories/templates; originals left untouched
- `save_webpage.py` → successfully downloaded https://example.com and saved a 577-byte HTML file

## Known gaps

- No linter/formatter configured (e.g. ruff, black). Could add `ruff` or `flake8` later.
- `save_webpage.py` saves raw HTML only (no readability/extraction), matching the beginner "save page as HTML" scope.
- `bill_reminders.py` reads a local `bills.json` only; no calendar sync or email/SMS alerts (intentionally simple, local-first).
- Tests cover sort, rename, and bills; `save_webpage.py` is smoke-tested manually but has no unit test (network-dependent).
- Site is static HTML only; no search, no build pipeline.

Published by Asdale Dynamics, LLC. MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.
