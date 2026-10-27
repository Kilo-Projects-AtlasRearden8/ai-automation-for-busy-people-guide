# Safety First

Read this page before you run any script in this guide.

## The golden rules

1. **Test on copies.** Every script here works on copies of your files, never
   your originals — unless you explicitly tell it to.
2. **Never move originals.** Scripts copy, they do not move or delete.
3. **Dry-run first.** Every script has a "dry-run" mode (the default) that
   prints what it *would* do without changing a single file.
4. **Back up before you apply.** Once you're comfortable, make a backup of the
   folder you're working in, then run with `--apply`.

## Why this matters

Automation saves time, but a mistake can rename or scatter a lot of files at
once. Working on copies means you can experiment without risk. If something
looks wrong, delete the copy and try again.

## Dry-run vs apply

| Mode | What it does | Safe? |
|------|--------------|-------|
| `python script.py` (default) | Prints a plan | Yes — nothing changes |
| `python script.py --apply` | Copies files to a new folder | Safe — originals untouched |

## Your responsibility

You are in charge. Review the plan before you apply. If you're not sure,
ask a friend or run it on a test folder first.

**Asdale Dynamics, LLC** — beginner-friendly AI education, tested and local-first.
