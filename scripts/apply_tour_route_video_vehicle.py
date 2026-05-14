#!/usr/bin/env python3
"""
Insert Route Map, Tour Video (YouTube), and Vehicle Options sections into tour HTML pages.

Source of truth for this content: the `old/` folder — mirror at old/motorover.in/<page>.html
and route images under old/motorover.in/_assets/... (copied into imgs/tour-maps/ for deploy).

Idempotent: skips pages that already contain tour-map-section.
"""

from __future__ import annotations

import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_DIR = ROOT / "old" / "motorover.in"
ASSETS = OLD_DIR / "_assets" / "e9b504c613d9cc9a9f89-fc19c99c231c8a40a78133b97ac321de.ssl.cf1.rackcdn.com"
OUT_MAP_DIR = ROOT / "imgs" / "tour-maps"

VEHICLE_H2 = (
    r"(Rental SUV Options|Rental Vehicle Options|Rental SUV|Rental Motorcycle Options|"
    r"Rental Motorcycle|Motorcycle Options)"
)
VEHICLE_H2_RE = re.compile(
    r'<h2 class="viamagus-heading2"[^>]*>(?:<div[^>]*>)?\s*(?:<span[^>]*>)?\s*'
    + VEHICLE_H2
    + r"\s*(?:</span>)?\s*(?:</div>)?\s*</h2>",
    re.I | re.DOTALL,
)
MOTO_OPTIONS_SPAN = re.compile(
    r'<span style="[^"]*font-size:20px[^"]*">\s*Motorcycle Options\s*</span>', re.I
)


def route_map_filename(page: str) -> str | None:
    i = page.lower().find("route map")
    if i == -1:
        return None
    chunk = page[i : i + 4000]
    m = re.search(
        r'_assets/e9b504c613d9cc9a9f89-fc19c99c231c8a40a78133b97ac321de\.ssl\.cf1\.rackcdn\.com/([^"]+)"',
        chunk,
    )
    return m.group(1).strip() if m else None


def youtube_id(page: str) -> str | None:
    fixed = page.replace("embed//", "embed/")
    ids = re.findall(r'youtube\.com/embed/+([a-zA-Z0-9_-]{6,})', fixed)
    cleaned: list[str] = []
    for vid in ids:
        v = vid.lstrip("/")
        if v and v not in cleaned:
            cleaned.append(v)
    return cleaned[0] if cleaned else None


def vehicle_chunk(page: str) -> str | None:
    m = VEHICLE_H2_RE.search(page)
    if not m:
        m = MOTO_OPTIONS_SPAN.search(page)
        if not m:
            return None
        start = m.end()
    else:
        start = m.end()
    chunk = page[start : start + 25000]
    ends: list[int] = []
    for marker in (
        "Tour Package Includes",
        "Tour Price Includes",
        "Tour Package Excludes",
        "<div> Route Map </div>",
        "Route Map </div>",
        "Tour Video",
        "Tour Highlights",
    ):
        i = chunk.find(marker)
        if i != -1:
            ends.append(i)
    if ends:
        chunk = chunk[: min(ends)]
    return chunk


def extract_vehicle_lines(chunk: str) -> list[str]:
    lines: list[str] = []
    for m in re.finditer(
        r"(?:</td>\s*</tr>\s*<tr>\s*<td>|<br\s*/?>)\s*([^<\n]{2,96}?)\s*(?:</div>|</td>|<br|</tr>)",
        chunk,
        flags=re.I,
    ):
        t = html.unescape(m.group(1)).strip()
        t = re.sub(r"\s+", " ", t)
        if len(t) < 2:
            continue
        low = t.lower()
        if any(
            x in low
            for x in (
                "viamagus",
                "padding",
                "width:",
                "facebook",
                "tour price",
                "euro",
                "nzd",
                "inr",
                "booking",
                "policy",
                "payment",
                "style",
                "clear:",
                "float:",
                "pillion:",
                "rider:",
            )
        ):
            continue
        if t.startswith("*") and "inclusive" in low:
            continue
        if t.startswith("*") and "gst" in low:
            continue
        lines.append(t)
    seen: set[str] = set()
    out: list[str] = []
    for L in lines:
        if L not in seen:
            seen.add(L)
            out.append(L)
    return out[:24]


def slug_title(slug: str, is_car: bool) -> str:
    return slug.replace("car-", "").replace("motorcycle-", "").replace("-", " ").title()


def build_sections(
    *,
    slug: str,
    is_car: bool,
    map_src: str,
    map_alt: str,
    video_id: str | None,
    vehicles: list[str],
) -> str:
    heading = "Vehicle" if is_car else "Motorcycle"
    vtitle = f"{heading} <em>Options</em>"
    map_href = map_src
    figcaption = "Overview of the tour route (tap to open full size)."
    map_block = f"""          <section aria-labelledby="route-map-heading" class="reveal tour-map-section">
            <h2 id="route-map-heading" class="section-title" style="font-size:var(--text-3xl); margin-bottom:var(--sp-4);">Route <em>Map</em></h2>
            <figure class="tour-route-map">
              <a href="{map_href}" target="_blank" rel="noopener" class="tour-route-map__link">
                <img src="{map_src}" alt="{html.escape(map_alt)}" class="tour-route-map__img" loading="lazy" />
              </a>
              <figcaption class="tour-route-map__cap">{figcaption}</figcaption>
            </figure>
          </section>"""

    if video_id:
        yt_title = f"{slug_title(slug, is_car)} tour — MotoRover on YouTube"
        video_block = f"""          <section aria-labelledby="tour-video-heading" class="reveal tour-video-section">
            <h2 id="tour-video-heading" class="section-title" style="font-size:var(--text-3xl); margin-bottom:var(--sp-4);">Tour <em>Video</em></h2>
            <div class="tour-video-embed">
              <iframe
                src="https://www.youtube.com/embed/{video_id}"
                title="{html.escape(yt_title)}"
                loading="lazy"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin"
                allowfullscreen></iframe>
            </div>
          </section>"""
    else:
        video_block = """          <section aria-labelledby="tour-video-heading" class="reveal tour-video-section">
            <h2 id="tour-video-heading" class="section-title" style="font-size:var(--text-3xl); margin-bottom:var(--sp-4);">Tour <em>Video</em></h2>
            <p style="font-size:var(--text-base); color:var(--text-muted); line-height:1.75;">A tour film is coming soon. In the meantime, browse our rides on <a href="https://www.youtube.com/@motorover" target="_blank" rel="noopener">MotoRover on YouTube</a>.</p>
          </section>"""

    if vehicles:
        lis = "\n".join(
            f'              <li class="tour-vehicle-section__item"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>{html.escape(v)}</span></li>'
            for v in vehicles
        )
        intro = ""
    else:
        lis = '              <li class="tour-vehicle-section__item"><i class="fa-solid fa-circle-info" aria-hidden="true"></i><span>See the booking card and tour overview for models and trim levels offered on this departure.</span></li>'
        intro = ""

    vehicle_block = f"""          <section aria-labelledby="vehicle-options-heading" class="reveal tour-vehicle-section">
            <h2 id="vehicle-options-heading" class="section-title" style="font-size:var(--text-3xl); margin-bottom:var(--sp-4);">{vtitle}</h2>
{intro}            <ul class="tour-vehicle-section__list" role="list">
{lis}
            </ul>
          </section>"""

    return (
        '\n          <div class="divider"></div>\n\n'
        + map_block
        + '\n\n          <div class="divider"></div>\n\n'
        + video_block
        + '\n\n          <div class="divider"></div>\n\n'
        + vehicle_block
    )


def fallback_video_id(html_name: str) -> str | None:
    if html_name == "car-northern-europe.html":
        return "souLeayx6wg"
    return None


def process_file(path: Path) -> str:
    name = path.name
    if not (name.startswith("motorcycle-") or name.startswith("car-")):
        return "skip"
    text = path.read_text(encoding="utf-8")
    if "tour-map-section" in text:
        return "already"

    old_path = OLD_DIR / name
    if not old_path.is_file():
        print(f"  missing old mirror: {old_path}", file=sys.stderr)
        return "no-old"

    old_page = old_path.read_text(encoding="utf-8", errors="replace")
    rf = route_map_filename(old_page)
    if not rf or not (ASSETS / rf).is_file():
        print(f"  missing route asset for {name}: {rf}", file=sys.stderr)
        return "no-map"

    vid = youtube_id(old_page) or fallback_video_id(name)
    vch = vehicle_chunk(old_page)
    vehicles = extract_vehicle_lines(vch) if vch else []

    OUT_MAP_DIR.mkdir(parents=True, exist_ok=True)
    ext = Path(rf).suffix.lower() or ".png"
    dest_name = Path(name).stem + "-map" + ext
    dest = OUT_MAP_DIR / dest_name
    shutil.copy2(ASSETS / rf, dest)

    map_src = f"imgs/tour-maps/{dest_name}"
    is_car = name.startswith("car-")
    alt = f"{slug_title(Path(name).stem, is_car)} tour route map"
    block = build_sections(
        slug=Path(name).stem,
        is_car=is_car,
        map_src=map_src,
        map_alt=alt,
        video_id=vid,
        vehicles=vehicles,
    )

    needle = '          <div class="divider"></div>\n\n          <!-- Inclusions'
    if needle not in text:
        needle = '          <div class="divider"></div>\r\n\r\n          <!-- Inclusions'
    if needle not in text:
        print(f"  could not find insertion point in {name}", file=sys.stderr)
        return "no-anchor"

    text = text.replace(needle, block + "\n\n" + needle, 1)
    path.write_text(text, encoding="utf-8")
    return "ok"


def main() -> None:
    tours = sorted(ROOT.glob("motorcycle-*.html")) + sorted(ROOT.glob("car-*.html"))
    counts: dict[str, int] = {}
    for p in tours:
        r = process_file(p)
        counts[r] = counts.get(r, 0) + 1
    print("Done:", counts)


if __name__ == "__main__":
    main()
