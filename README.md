# AI Automation for Busy People

Simple automations for everyday life: sorting downloads, renaming files,
bill reminders, and saving webpages — using built-in tools, free apps, and
small no-code scripts.

Written plain English, step by step, never condescending — like a friend
would explain it. Safety first: every script is tested on copies, never on
your originals.

## What's inside

| Folder | What's in it |
|--------|--------------|
| `docs/` | Beginner manuals in Markdown (plain English, step by step) |
| `static/` | A small HTML site you can open in any browser |
| `scripts/` | Small Python scripts (dry-run by default, copy never move) |
| `tests/` | Automated checks that prove the scripts work |

## Who this is for

Dylan Asdale is a registered nurse turned AI author and founder of
**Asdale Dynamics, LLC** (Indiana, formed October 2026). His book *The
Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a
friend would." This guide is published by **Asdale Dynamics, LLC** as part
of its beginner-friendly AI education line.

## Quick start

1. Read `docs/safety.md` first — it explains the golden rules (test on
   copies, never move originals, dry-run before apply).
2. Pick an automation and read its page in `docs/`.
3. Run the matching script in `scripts/` in dry-run mode (the default):

   ```bash
   python3 scripts/sort_downloads.py        # see what it would do
   python3 scripts/sort_downloads.py --apply  # copy files for real
   ```

4. When you're comfortable, make a backup of your folder and run with
   `--apply`.

## What you need

- A computer (Windows, Mac, or Linux)
- Python 3 (built-in on Mac and Linux; free download from python.org on Windows)
- A web browser (for saving webpages)
- About 30 minutes

## The four automations

- **Sorting downloads** — tidy your Downloads folder by file type
- **Renaming files** — give batches of files clean, consistent names
- **Bill reminders** — see which bills are due soon
- **Saving webpages** — save pages to read offline

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## Safety promise

- Test on copies first. Never move your originals.
- Every script has a dry-run mode that shows what it *would* do before it
  changes anything.
- No secrets, API keys, or personal data are stored anywhere in this
  project.

Published by **Asdale Dynamics, LLC** — beginner-friendly AI education,
tested and local-first.
