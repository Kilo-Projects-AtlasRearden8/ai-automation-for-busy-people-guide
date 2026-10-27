# Sorting Downloads

Your Downloads folder probably mixes images, PDFs, installers, and videos into
one big pile. This automation sorts files into neat folders by type — without
touching your originals.

## What it does

Looks at every file in a folder (default: your Downloads folder), figures out
what kind of file it is by its extension, and copies it into a matching folder:

| Files | Goes to |
|-------|---------|
| .jpg .png .gif .webp .svg | Images/ |
| .pdf .doc .docx .txt .rtf | Documents/ |
| .mp3 .wav .aac .m4a | Audio/ |
| .mp4 .mov .avi .mkv .wmv | Video/ |
| .zip .rar .7z .tar .gz | Archives/ |
| .exe .msi .dmg .pkg | Installers/ |
| everything else | Other/ |

## How to run

1. Copy `scripts/sort_downloads.py` to your computer.
2. Try it in dry-run mode (safe, nothing changes):

   ```bash
   python3 scripts/sort_downloads.py
   ```

   It prints what it *would* copy where.

3. Run it for real (copies files into a new `Sorted Downloads` folder):

   ```bash
   python3 scripts/sort_downloads.py --apply
   ```

   Your originals stay exactly where they are.

## Choose your own folders

```bash
python3 scripts/sort_downloads.py --source ~/Downloads --dest ~/Desktop/MySorted
```

## Test it first (recommended)

Make a test folder with a few dummy files, point the script at it, and confirm
the copies land in the right place before you point it at your real Downloads
folder.

## No-code alternative

On Windows, try **PowerToys** or File Explorer's "Sort by" > "Type." On Mac,
use Finder's "Use Groups" and "Sort by" > "Kind." These are built-in and
require no scripts at all.

**Asdale Dynamics, LLC** — tested, local-first, no secrets.
