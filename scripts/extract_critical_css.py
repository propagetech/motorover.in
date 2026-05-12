#!/usr/bin/env python3
"""
Extract Critical CSS
Extracts above-the-fold CSS for inlining.
"""

import re
from pathlib import Path


def extract_critical_css(css_file: str = "css/styles.css", output_file: str = "css/critical.css") -> str:
    """Extract critical CSS for above-the-fold content."""
    css_path = Path(css_file)
    
    if not css_path.exists():
        return ""
    
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    
    # Critical CSS sections (above-the-fold)
    critical_sections = [
        r':root\s*\{[^}]*\}',  # CSS variables
        r'\*[^}]*\{[^}]*\}',  # Reset
        r'html[^}]*\{[^}]*\}',
        r'body[^}]*\{[^}]*\}',
        r'\.skip-link[^}]*\{[^}]*\}',
        r'\.header[^}]*\{[^}]*\}',
        r'\.header__[^}]*\{[^}]*\}',
        r'\.nav[^}]*\{[^}]*\}',
        r'\.nav__[^}]*\{[^}]*\}',
        r'\.hero[^}]*\{[^}]*\}',
        r'\.hero__[^}]*\{[^}]*\}',
        r'\.container[^}]*\{[^}]*\}',
        r'\.btn[^}]*\{[^}]*\}',
        r'\.theme-toggle[^}]*\{[^}]*\}',
    ]
    
    critical_css = ""
    for pattern in critical_sections:
        matches = re.findall(pattern, css, re.MULTILINE | re.DOTALL)
        for match in matches:
            if match not in critical_css:
                critical_css += match + "\n"
    
    # Save critical CSS
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(critical_css)
    
    print(f"Extracted {len(critical_css)} characters of critical CSS")
    return critical_css


if __name__ == "__main__":
    extract_critical_css()
