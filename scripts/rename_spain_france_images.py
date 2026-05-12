#!/usr/bin/env python3

import re
from pathlib import Path


BASE_PATTERN = re.compile(r"(spain-france-tra\d+)")


def main() -> None:
    images_dir = Path("assets/img")

    # Collect unique old bases from .avif and .webp (and .jpeg if any remain)
    bases = set()
    for pattern in ("spain-france-tra*.avif", "spain-france-tra*.webp", "spain-france-tra*.jpeg"):
        for p in images_dir.glob(pattern):
            m = BASE_PATTERN.match(p.stem)
            if m:
                bases.add(m.group(1))
    sorted_bases = sorted(bases)
    base_to_index = {b: i for i, b in enumerate(sorted_bases, start=1)}

    if not base_to_index:
        print("No matching files found.")
        return

    # Rename all spain-france-tra* files (avif, webp, jpeg and responsive variants)
    for pattern in ("spain-france-tra*.avif", "spain-france-tra*.webp", "spain-france-tra*.jpeg"):
        for src in sorted(images_dir.glob(pattern)):
            m = BASE_PATTERN.match(src.stem)
            if not m:
                continue
            base = m.group(1)
            index = base_to_index[base]
            # Suffix is everything after the base (e.g. "" or "-320w")
            suffix = src.stem[len(base) :]
            ext = src.suffix.lower()
            new_name = f"spain-france-motorcycle-tour-{index}{suffix}{ext}"
            dst = src.with_name(new_name)

            if dst.resolve() == src.resolve():
                continue
            if dst.exists():
                print(f"SKIP (exists): {dst.name}")
                continue

            print(f"{src.name} -> {dst.name}")
            src.rename(dst)

    print("Done.")


if __name__ == "__main__":
    main()

