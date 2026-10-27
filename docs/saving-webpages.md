# Saving Webpages

Found an article, recipe, or guide you want to read later? This automation
saves a webpage as a single HTML file you can open offline — no account, no
subscription, no clipping service required.

## What it does

Downloads a webpage and saves it to a `saved-pages/` folder with a timestamped
filename, so you can read it anytime without an internet connection.

## How to run

1. Copy `scripts/save_webpage.py` to your computer.
2. Run:

   ```bash
   python3 scripts/save_webpage.py "https://example.com/article"
   ```

   It prints where the page was saved.

3. Open the saved `.html` file in your browser.

## Options

- `--dest` — where to save pages (default: `saved-pages`)
- `--name` — choose your own filename (default: timestamp + page title)

## No-code alternative

Every browser can do this natively:

- **Chrome / Edge:** File > Save as > "Webpage, HTML only"
- **Firefox:** File > Save Page As
- **Safari:** File > Save As > "Web Archive" or "Page Source"

Keyboard shortcut: `Ctrl+S` (Windows/Linux) or `Cmd+S` (Mac).

## Privacy tip

Only save pages you're allowed to keep for personal use. Don't save pages that
contain other people's personal data.

**Asdale Dynamics, LLC** — tested, local-first, no secrets.
