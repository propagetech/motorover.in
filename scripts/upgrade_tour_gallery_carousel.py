#!/usr/bin/env python3
"""Wrap tour gallery grids in .tour-gallery carousel markup (one-time / idempotent)."""

from __future__ import annotations

import sys
from pathlib import Path

MARKER_OPEN = '<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:6px;">'
CAROUSEL_PREFIX = (
    '<div class="tour-gallery" data-tour-gallery>\n'
    '              <button type="button" class="tour-gallery__btn tour-gallery__btn--prev" '
    'aria-label="Previous images"><i class="fa-solid fa-chevron-left" aria-hidden="true"></i></button>\n'
    '              <div class="tour-gallery__viewport">\n'
    '                <div class="tour-gallery__track">\n'
)
CAROUSEL_SUFFIX = (
    '                </div>\n'
    '              </div>\n'
    '              <button type="button" class="tour-gallery__btn tour-gallery__btn--next" '
    'aria-label="Next images"><i class="fa-solid fa-chevron-right" aria-hidden="true"></i></button>\n'
    '            </div>'
)


def find_matching_close_div(html: str, open_start: int) -> int:
    """Return start index of closing </div> for the <div> that begins at open_start."""
    i = open_start
    n = len(html)
    depth = 0
    while i < n:
        if html.startswith("<div", i) and (i + 4 >= n or html[i + 4] in " \t\n\r/>"):
            depth += 1
            i += 1
            continue
        if html.startswith("</div>", i):
            depth -= 1
            if depth == 0:
                return i
            i += 6
            continue
        i += 1
    return -1


def upgrade_html(html: str) -> str:
    if MARKER_OPEN not in html:
        return html
    start = html.find(MARKER_OPEN)
    close_start = find_matching_close_div(html, start)
    if close_start < 0:
        return html
    close_end = close_start + len("</div>")
    inner = html[start + len(MARKER_OPEN) : close_start].rstrip()
    inner = inner.replace(
        'class="gallery-item" style="aspect-ratio:4/3;"',
        'class="gallery-item"',
    )
    replacement = CAROUSEL_PREFIX + inner + CAROUSEL_SUFFIX
    return html[:start] + replacement + html[close_end:]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    changed = 0
    for path in sorted(root.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if MARKER_OPEN not in text:
            continue
        new_text = upgrade_html(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
            print(path.name)
    print(f"Updated {changed} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
