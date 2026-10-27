#!/usr/bin/env python3
"""Save a webpage as a single HTML file for offline reading.

No account, no subscription, no secrets required.
"""

import argparse
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

DEFAULT_USER_AGENT = "Mozilla/5.0 (compatible; AsdaleDynamics SavePage/1.0)"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read()
    charset = resp.headers.get_content_charset() or "utf-8"
    return html.decode(charset, errors="replace")


def suggest_name(html: str, url: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    title = match.group(1).strip() if match else "page"
    title = re.sub(r"\s+", " ", title)
    title = re.sub(r"[^A-Za-z0-9_.\-]", "_", title) or "page"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{title}.html"


def run(url: str, dest: Path, name: str | None) -> int:
    try:
        html = fetch(url)
    except Exception as exc:  # noqa: BLE001 - network errors are expected
        print(f"Error: could not download {url}: {exc}")
        return 1

    filename = name or suggest_name(html, url)
    if not filename.lower().endswith(".html"):
        filename += ".html"

    dest.mkdir(parents=True, exist_ok=True)
    target = dest / filename
    target.write_text(html, encoding="utf-8")

    print(f"Saved: {target}")
    print(f"Source: {url}")
    print(f"Size: {target.stat().st_size} bytes")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Save a webpage as a single HTML file for offline reading."
    )
    parser.add_argument("url", help="Webpage URL to save")
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path("saved-pages"),
        help="Folder to save pages into (default: saved-pages)",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Custom filename (default: timestamp + page title)",
    )
    args = parser.parse_args(argv)
    return run(args.url, args.dest, args.name)


if __name__ == "__main__":
    sys.exit(main())
