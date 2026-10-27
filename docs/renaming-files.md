# Renaming Files

Files named `IMG_4829.jpg`, `document (1).pdf`, or `final_v2_REALLYFINAL.docx`
are hard to find later. This automation renames batches of files into clean,
consistent names — on copies, never your originals.

## What it does

Renames every matching file using a template you choose, then copies the
renamed files into an output folder. Default template:

```
{name}_{date}_{counter}.{ext}
```

Example: `vacation_2026-10-27_01.jpg`

## How to run

1. Copy `scripts/rename_files.py` to your computer.
2. Dry-run mode (safe, nothing changes):

   ```bash
   python3 scripts/rename_files.py --source ./my-photos --pattern "*.jpg"
   ```

   It prints the old name and the new name side by side.

3. Apply (copies renamed files to `./renamed-output`):

   ```bash
   python3 scripts/rename_files.py --source ./my-photos --pattern "*.jpg" --apply
   ```

   Originals are untouched.

## Options

- `--template` — choose your own name pattern (use `{name}`, `{date}`, `{counter}`, `{ext}`)
- `--pattern` — only rename files matching this glob (default: `*`)
- `--dest` — where renamed copies go (default: `renamed-output`)

## Test it first

Make a test folder with 3–5 dummy files, run dry-run, confirm the names look
right, then apply.

**Asdale Dynamics, LLC** — tested, local-first, no secrets.
