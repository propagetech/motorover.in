#!/usr/bin/env python3
"""
Script to standardize header and footer navigation across all HTML files.
"""

import os
import re
from pathlib import Path

# Standard header navigation (full dropdown version)
STANDARD_HEADER_NAV = '''          <ul class="nav__list">
            <li class="nav__item">
              <a href="/" class="nav__link">Home</a>
            </li>
            
            <li class="nav__item nav__dropdown" aria-expanded="false">
              <a href="/tours.html" class="nav__link nav__dropdown-toggle">
                Motorcycle Tours
                <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 9l6 6 6-6" />
                </svg>
              </a>
              <ul class="nav__dropdown-menu">
                <li class="nav__dropdown-item"><a href="/motorcycle-silk-route.html" class="nav__link">Kyrgyzstan - July/August 2025</a></li>
                <li class="nav__dropdown-item"><a href="/motorcycle-spain-and-france.html" class="nav__link">Spain & France - September 2025</a></li>
                <li class="nav__dropdown-item"><a href="/motorcycle-south-africa.html" class="nav__link">South Africa - Oct/Nov 2025</a></li>
                <li class="nav__dropdown-item"><a href="/motorcycle-new-zealand.html" class="nav__link">New Zealand - Feb/Mar 2026</a></li>
                <li class="nav__dropdown-item"><a href="/motorcycle-andalucia.html" class="nav__link">Spain & Portugal - Mar 2026</a></li>
                <li class="nav__dropdown-item"><a href="/motorcycle-balkan.html" class="nav__link">Balkan - April 2026</a></li>
                <li class="nav__dropdown-item"><a href="/motorcycle-morocco.html" class="nav__link">Morocco - May 2026</a></li>
                <li class="nav__dropdown-item"><a href="/motorcycle-ultimate-alps.html" class="nav__link">Ultimate Alps - July 2026</a></li>
                <li class="nav__dropdown-item"><a href="/motorcycle-northern-europe.html" class="nav__link">Northern Europe - Aug 2026</a></li>
              </ul>
            </li>
            
            <li class="nav__item nav__dropdown" aria-expanded="false">
              <a href="/tours.html" class="nav__link nav__dropdown-toggle">
                Car Tours
                <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 9l6 6 6-6" />
                </svg>
              </a>
              <ul class="nav__dropdown-menu">
                <li class="nav__dropdown-item"><a href="/car-kyrgyzstan-spring-edition.html" class="nav__link">Kyrgyzstan Spring Edition - June 2025</a></li>
                <li class="nav__dropdown-item"><a href="/car-silk-route.html" class="nav__link">Kyrgyzstan Summer Edition - August 2025</a></li>
                <li class="nav__dropdown-item"><a href="/car-georgia.html" class="nav__link">Georgia - Sept 2025</a></li>
                <li class="nav__dropdown-item"><a href="/car-silk-route-autumn-edition.html" class="nav__link">Kyrgyzstan Autumn Edition - Oct 2025</a></li>
                <li class="nav__dropdown-item"><a href="/car-south-africa.html" class="nav__link">South Africa - Nov 2025</a></li>
                <li class="nav__dropdown-item"><a href="/car-silk-route-snow-drive.html" class="nav__link">Kyrgyzstan Winter Edition - Dec 2025</a></li>
                <li class="nav__dropdown-item"><a href="/car-georgia-winter-adventure.html" class="nav__link">Georgia Snow Drive - Feb 2026</a></li>
                <li class="nav__dropdown-item"><a href="/car-new-zealand.html" class="nav__link">NewZealand - Feb 2026</a></li>
                <li class="nav__dropdown-item"><a href="/russia-winter-adventure.html" class="nav__link">Russia Winter Edition - Feb/Mar 2026</a></li>
                <li class="nav__dropdown-item"><a href="/car-balkan.html" class="nav__link">Balkan Self-Drive Road Trip - April 2026</a></li>
                <li class="nav__dropdown-item"><a href="/car-morocco.html" class="nav__link">Morocco - Apr/May 2026</a></li>
                <li class="nav__dropdown-item"><a href="/car-kyrgyzstan-spring-edition.html" class="nav__link">Kyrgyzstan Spring Edition - May 2026</a></li>
                <li class="nav__dropdown-item"><a href="/car-northern-europe.html" class="nav__link">Northern Europe - Sept 2026</a></li>
              </ul>
            </li>
            
            <li class="nav__item nav__dropdown" aria-expanded="false">
              <a href="/about.html" class="nav__link nav__dropdown-toggle">
                About Us
                <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 9l6 6 6-6" />
                </svg>
              </a>
              <ul class="nav__dropdown-menu">
                <li class="nav__dropdown-item"><a href="/about.html" class="nav__link">Our Story</a></li>
                <li class="nav__dropdown-item"><a href="/the-team.html" class="nav__link">Team</a></li>
                <li class="nav__dropdown-item"><a href="/the-team.html#official-team" class="nav__link">Official Team</a></li>
                <li class="nav__dropdown-item"><a href="/the-team.html#guides" class="nav__link">Guides / Tour Managers</a></li>
              </ul>
            </li>
            
            <li class="nav__item">
              <a href="/contactus.html" class="nav__link">Contact Us</a>
            </li>
            
            <li class="nav__item">
              <a href="/why-us.html" class="nav__link">Why Us</a>
            </li>
            
            <li class="nav__item">
              <a href="/FAQ.html" class="nav__link">FAQ</a>
            </li>
          </ul>'''

STANDARD_HEADER_ACTIONS = '''        <div class="header__actions">
          <a href="/contactus.html" class="btn btn--primary btn--small">Contact Us</a>
          <button class="theme-toggle" aria-label="Toggle theme" aria-pressed="false" id="theme-toggle">'''

STANDARD_FOOTER_TOURS = '''        <div>
          <h3 class="footer__section-title">Tours</h3>
          <ul class="footer__list">
            <li class="footer__item"><a href="/tours.html" class="footer__link">All Tours</a></li>
            <li class="footer__item"><a href="/tours.html" class="footer__link">Motorcycle Tours</a></li>
            <li class="footer__item"><a href="/tours.html" class="footer__link">Self-Drive Tours</a></li>
          </ul>
        </div>'''

STANDARD_FOOTER_COMPANY = '''        <div>
          <h3 class="footer__section-title">Company</h3>
          <ul class="footer__list">
            <li class="footer__item"><a href="/about.html" class="footer__link">About Us</a></li>
            <li class="footer__item"><a href="/the-team.html" class="footer__link">Team</a></li>
            <li class="footer__item"><a href="/FAQ.html" class="footer__link">FAQ</a></li>
            <li class="footer__item"><a href="/contactus.html" class="footer__link">Contact</a></li>
          </ul>
        </div>'''

STANDARD_FOOTER_LEGAL = '''        <div>
          <h3 class="footer__section-title">Legal</h3>
          <ul class="footer__list">
            <li class="footer__item"><a href="/privacy-terms-refund-pricing.html" class="footer__link">Terms</a></li>
            <li class="footer__item"><a href="/privacy-terms-refund-pricing.html" class="footer__link">Privacy</a></li>
          </ul>
        </div>'''


def fix_header_navigation(content):
    """Replace simple navigation with standard dropdown navigation."""
    # Pattern to match simple navigation
    simple_nav_pattern = r'<ul class="nav__list">\s*<li class="nav__item"><a href="/" class="nav__link">Home</a></li>\s*<li class="nav__item"><a href="/tours/" class="nav__link">Tours</a></li>\s*<li class="nav__item"><a href="/about/" class="nav__link">About</a></li>\s*<li class="nav__item"><a href="/contact\.html" class="nav__link">Contact</a></li>\s*</ul>'
    
    if re.search(simple_nav_pattern, content):
        content = re.sub(simple_nav_pattern, STANDARD_HEADER_NAV, content)
    
    # Also handle variations
    simple_nav_pattern2 = r'<ul class="nav__list">.*?<li class="nav__item"><a href="/" class="nav__link">Home</a></li>.*?<li class="nav__item"><a href="/tours/" class="nav__link">Tours</a></li>.*?<li class="nav__item"><a href="/about/" class="nav__link">About</a></li>.*?<li class="nav__item"><a href="/contact\.html" class="nav__link">Contact</a></li>.*?</ul>'
    content = re.sub(simple_nav_pattern2, STANDARD_HEADER_NAV, content, flags=re.DOTALL)
    
    # Fix header actions - add if missing, or fix contact link
    if '<div class="header__actions">' not in content:
        # Check if there's a theme-toggle button that needs header__actions wrapper
        theme_toggle_pattern = r'(<button class="theme-toggle[^>]*>.*?</button>\s*</div>\s*</div>\s*</header>)'
        if re.search(theme_toggle_pattern, content, re.DOTALL):
            # Insert header__actions before theme-toggle
            content = re.sub(
                r'(<button class="theme-toggle)',
                STANDARD_HEADER_ACTIONS.replace('<button class="theme-toggle', r'\1'),
                content,
                count=1
            )
    
    # Fix contact link in header actions
    content = re.sub(
        r'<a href="/contact\.html" class="btn btn--primary btn--small">Contact Us</a>',
        '<a href="/contactus.html" class="btn btn--primary btn--small">Contact Us</a>',
        content
    )
    
    return content


def fix_footer_navigation(content):
    """Standardize footer navigation links."""
    # Fix Tours section
    tours_pattern = r'<div>\s*<h3 class="footer__section-title">Tours</h3>\s*<ul class="footer__list">.*?</ul>\s*</div>'
    content = re.sub(tours_pattern, STANDARD_FOOTER_TOURS, content, flags=re.DOTALL)
    
    # Fix Company section
    company_pattern = r'<div>\s*<h3 class="footer__section-title">Company</h3>\s*<ul class="footer__list">.*?</ul>\s*</div>'
    content = re.sub(company_pattern, STANDARD_FOOTER_COMPANY, content, flags=re.DOTALL)
    
    # Fix Legal section
    legal_pattern = r'<div>\s*<h3 class="footer__section-title">Legal</h3>\s*<ul class="footer__list">.*?</ul>\s*</div>'
    content = re.sub(legal_pattern, STANDARD_FOOTER_LEGAL, content, flags=re.DOTALL)
    
    # Fix individual links
    replacements = [
        (r'href="/tours/"', 'href="/tours.html"'),
        (r'href="/about/"', 'href="/about.html"'),
        (r'href="/contact\.html"', 'href="/contactus.html"'),
        (r'href="/faq\.html"', 'href="/FAQ.html"'),
        (r'href="/FAQ\.html"', 'href="/FAQ.html"'),
        (r'href="/team\.html"', 'href="/the-team.html"'),
        (r'href="/terms\.html"', 'href="/privacy-terms-refund-pricing.html"'),
        (r'href="/privacy\.html"', 'href="/privacy-terms-refund-pricing.html"'),
        (r'href="/tours/motorcycle\.html"', 'href="/tours.html"'),
        (r'href="/tours/self-drive\.html"', 'href="/tours.html"'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    return content


def process_html_file(file_path):
    """Process a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix header navigation
        content = fix_header_navigation(content)
        
        # Fix footer navigation
        content = fix_footer_navigation(content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to process all HTML files."""
    base_dir = Path(__file__).parent.parent
    html_files = list(base_dir.glob('*.html'))
    
    print(f"Found {len(html_files)} HTML files")
    
    fixed_count = 0
    for html_file in html_files:
        if process_html_file(html_file):
            print(f"Fixed: {html_file.name}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")


if __name__ == '__main__':
    main()
