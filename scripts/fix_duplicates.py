#!/usr/bin/env python3
"""
Script to fix duplicate theme-toggle buttons and indentation issues.
"""

import re
from pathlib import Path

def fix_duplicate_theme_toggle(content):
    """Fix duplicate theme-toggle button attributes."""
    # Fix malformed theme-toggle button
    pattern = r'<button class="theme-toggle" aria-label="Toggle theme" aria-pressed="false" id="theme-toggle">" aria-label="Toggle theme" aria-pressed="false" id="theme-toggle">'
    replacement = '<button class="theme-toggle" aria-label="Toggle theme" aria-pressed="false" id="theme-toggle">'
    content = re.sub(pattern, replacement, content)
    return content

def fix_footer_indentation(content):
    """Fix extra indentation in footer sections."""
    # Fix extra indentation before footer divs
    pattern = r'(\s+)                <div>'
    replacement = r'\1        <div>'
    content = re.sub(pattern, replacement, content)
    return content

def fix_header_actions_indentation(content):
    """Fix extra indentation in header actions."""
    # Fix extra indentation before header__actions
    pattern = r'(\s+)                <div class="header__actions">'
    replacement = r'\1        <div class="header__actions">'
    content = re.sub(pattern, replacement, content)
    return content

def process_html_file(file_path):
    """Process a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix duplicate theme-toggle
        content = fix_duplicate_theme_toggle(content)
        
        # Fix footer indentation
        content = fix_footer_indentation(content)
        
        # Fix header actions indentation
        content = fix_header_actions_indentation(content)
        
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
