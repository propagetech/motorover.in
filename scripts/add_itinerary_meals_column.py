#!/usr/bin/env python3
"""
Insert a Meals column (before Distance) in all tour itinerary tables.
Idempotent: skips files that already have <th scope="col">Meals</th>.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOUR_GLOB = [
    "car-*.html",
    "motorcycle-*.html",
]

MEALS_FIRST = "Meals included — Dinner"
MEALS_MIDDLE = "Meals included — Breakfast, Lunch, Dinner"
MEALS_LAST = "Meals included — Breakfast"
MEALS_SINGLE = "Meals included — Breakfast, Lunch, Dinner"


def meal_text(row_index: int, total_rows: int) -> str:
    if total_rows <= 1:
        return MEALS_SINGLE
    if row_index == 0:
        return MEALS_FIRST
    if row_index == total_rows - 1:
        return MEALS_LAST
    return MEALS_MIDDLE


def patch_tbody_rows(tbody: str) -> str:
    rows = list(re.finditer(r"<tr\b[^>]*>[\s\S]*?</tr>", tbody, re.IGNORECASE))
    if not rows:
        return tbody
    n = len(rows)
    out_parts: list[str] = []
    last_end = 0
    for i, m in enumerate(rows):
        out_parts.append(tbody[last_end : m.start()])
        row = m.group(0)
        tds = re.findall(r"<td\b[^>]*>[\s\S]*?</td>", row, re.IGNORECASE)
        if len(tds) not in (4, 5):
            out_parts.append(row)
            last_end = m.end()
            continue
        if any(">Meals included" in t for t in tds):
            out_parts.append(row)
            last_end = m.end()
            continue
        mtxt = meal_text(i, n)
        meal_td = f'                    <td>{mtxt}</td>\n'
        if len(tds) == 5:
            new_inner = "".join(tds[:4]) + "\n" + meal_td + tds[4]
        else:
            new_inner = "".join(tds[:3]) + "\n" + meal_td + tds[3]
        open_tr = re.match(r"(<tr\b[^>]*>)", row, re.IGNORECASE)
        close = "</tr>"
        if not open_tr:
            out_parts.append(row)
            last_end = m.end()
            continue
        new_row = open_tr.group(1) + "\n" + new_inner + "\n                  " + close
        out_parts.append(new_row)
        last_end = m.end()
    out_parts.append(tbody[last_end:])
    return "".join(out_parts)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "itinerary-table" not in text:
        return False
    if '<th scope="col">Meals</th>' in text:
        return False

    new_text, n_head = re.subn(
        r'(<th scope="col">Activity</th>\s*\n\s*)(<th scope="col">Distance</th>)',
        r'\1<th scope="col">Meals</th>\n                    \2',
        text,
        count=1,
    )
    if n_head != 1:
        return False

    def repl_tbody(m: re.Match[str]) -> str:
        return m.group(1) + patch_tbody_rows(m.group(2)) + m.group(3)

    new_text2, n_body = re.subn(
        r'(<table class="itinerary-table"[^>]*>[\s\S]*?<tbody>)([\s\S]*?)(</tbody>)',
        repl_tbody,
        new_text,
        count=1,
        flags=re.IGNORECASE,
    )
    if n_body != 1:
        return False

    path.write_text(new_text2, encoding="utf-8")
    return True


def main() -> None:
    paths: set[Path] = set()
    for pattern in TOUR_GLOB:
        paths.update(ROOT.glob(pattern))
    touched = []
    for p in sorted(paths, key=lambda x: x.name):
        if patch_file(p):
            touched.append(p.name)
    print("Patched:", ", ".join(touched) if touched else "(none)")


if __name__ == "__main__":
    main()
