#!/usr/bin/env python3
"""
Script to rename image files in assets/img with meaningful names.
Removes timestamps and normalizes filenames.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

def normalize_name(name):
    """Convert a name to a normalized format: lowercase with dashes."""
    # Remove leading numbers (timestamps)
    name = re.sub(r'^\d+', '', name)
    
    # Insert dash before numbers (e.g., "gallery2" -> "gallery-2")
    name = re.sub(r'([a-zA-Z])(\d)', r'\1-\2', name)
    # Insert dash after numbers before letters (e.g., "2image" -> "2-image")
    name = re.sub(r'(\d)([a-zA-Z])', r'\1-\2', name)
    
    # Convert camelCase to kebab-case (handle multiple capital letters)
    # First, insert dash before capital letters that follow lowercase
    name = re.sub(r'([a-z])([A-Z])', r'\1-\2', name)
    # Then, insert dash before capital letters that follow numbers
    name = re.sub(r'(\d)([A-Z])', r'\1-\2', name)
    # Insert dash before capital letters that follow other capital letters (but not at start)
    # This handles cases like "BMW3Series" -> "BMW-3-Series"
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', name)
    
    # Handle cases like "Scotlandgallery" -> "Scotland-gallery"
    # Split on word boundaries: lowercase letter followed by uppercase
    # But also handle: uppercase word followed by lowercase word (like "Scotlandgallery")
    # We'll do this by finding patterns like [A-Z][a-z]+[A-Z] and splitting
    def split_camel(match):
        s = match.group(0)
        # Find where lowercase ends and uppercase begins
        for i in range(len(s) - 1, 0, -1):
            if s[i].isupper() and s[i-1].islower():
                return s[:i] + '-' + s[i:]
        return s
    
    # Apply splitting for camelCase words
    name = re.sub(r'[A-Z][a-z]+[A-Z]', split_camel, name)
    
    # Convert to lowercase
    name = name.lower()
    
    # Replace spaces and underscores with dashes
    name = re.sub(r'[\s_]+', '-', name)
    
    # Remove multiple consecutive dashes
    name = re.sub(r'-+', '-', name)
    
    # Remove leading/trailing dashes
    name = name.strip('-')
    
    return name

def extract_base_name(filename):
    """Extract the meaningful part of a filename."""
    # Remove extension
    base = os.path.splitext(filename)[0]
    
    # Remove width suffixes like -320w, -640w, etc.
    base = re.sub(r'-\d+w$', '', base)
    
    # Remove timestamp prefix (numbers at the start)
    base = re.sub(r'^\d+', '', base)
    
    return base

def get_all_image_files(img_dir):
    """Get all image files and group them by base name."""
    files = []
    base_groups = defaultdict(list)
    
    for filepath in Path(img_dir).rglob('*'):
        if filepath.is_file() and filepath.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif']:
            files.append(filepath)
            base_name = extract_base_name(filepath.name)
            base_groups[base_name].append(filepath)
    
    return files, base_groups

def create_rename_mapping(base_groups):
    """Create a mapping from old names to new names."""
    mapping = {}
    numeric_counter = {}  # Track counters for numeric-only files
    
    for base_name, files in base_groups.items():
        if not base_name:  # Files with no meaningful name after removing timestamp
            # Give them generic names based on the original filename
            for filepath in files:
                old_name = filepath.name
                ext = filepath.suffix.lower()
                
                # Extract the numeric part (timestamp)
                numeric_part = re.match(r'^(\d+)', old_name)
                if numeric_part:
                    # Use last 6 digits as a short identifier
                    short_id = numeric_part.group(1)[-6:]
                    base_normalized = f"image-{short_id}"
                else:
                    base_normalized = "image-unknown"
                
                # Check if it has a width suffix
                width_match = re.search(r'-(\d+w)$', os.path.splitext(old_name)[0])
                if width_match:
                    width_suffix = width_match.group(1)
                    new_name = f"{base_normalized}-{width_suffix}{ext}"
                else:
                    new_name = f"{base_normalized}{ext}"
                
                # Ensure uniqueness
                if new_name in mapping.values():
                    counter = numeric_counter.get(base_normalized, 1)
                    numeric_counter[base_normalized] = counter + 1
                    base_new = os.path.splitext(new_name)[0]
                    ext = os.path.splitext(new_name)[1]
                    new_name = f"{base_new}-{counter}{ext}"
                
                mapping[str(filepath)] = new_name
            continue
            
        normalized = normalize_name(base_name)
        
        # For each file, create the new name
        for filepath in files:
            old_name = filepath.name
            ext = filepath.suffix.lower()
            
            # Check if it has a width suffix
            width_match = re.search(r'-(\d+w)$', os.path.splitext(old_name)[0])
            if width_match:
                width_suffix = width_match.group(1)
                new_name = f"{normalized}-{width_suffix}{ext}"
            else:
                new_name = f"{normalized}{ext}"
            
            # Ensure uniqueness
            if new_name in mapping.values():
                # Add a counter if needed
                counter = 1
                base_new = os.path.splitext(new_name)[0]
                ext = os.path.splitext(new_name)[1]
                while new_name in mapping.values():
                    new_name = f"{base_new}-{counter}{ext}"
                    counter += 1
            
            mapping[str(filepath)] = new_name
    
    return mapping

def update_file_references(root_dir, mapping):
    """Update all file references in the codebase."""
    # Create reverse mapping: old filename -> new filename
    filename_mapping = {}
    for old_path, new_name in mapping.items():
        old_filename = os.path.basename(old_path)
        filename_mapping[old_filename] = new_name
    
    # Find all files that might reference images
    text_files = []
    for ext in ['.html', '.js', '.json', '.css', '.py', '.ts', '.tsx', '.jsx', '.md']:
        for filepath in Path(root_dir).rglob(f'*{ext}'):
            if filepath.is_file():
                # Skip node_modules, .git, etc.
                if any(skip in str(filepath) for skip in ['node_modules', '.git', '__pycache__', '.venv']):
                    continue
                text_files.append(filepath)
    
    # Update references
    updated_files = []
    for filepath in text_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            for old_filename, new_filename in filename_mapping.items():
                # Replace various path formats
                patterns = [
                    (f'assets/img/{old_filename}', f'assets/img/{new_filename}'),
                    (f'/assets/img/{old_filename}', f'/assets/img/{new_filename}'),
                    (f'"assets/img/{old_filename}"', f'"assets/img/{new_filename}"'),
                    (f"'assets/img/{old_filename}'", f"'assets/img/{new_filename}'"),
                    (f'assets/img/{old_filename}', f'assets/img/{new_filename}'),  # without quotes
                    # Also handle in srcset attributes
                    (f'{old_filename} ', f'{new_filename} '),
                    (f'{old_filename}"', f'{new_filename}"'),
                    (f'{old_filename}\'', f'{new_filename}\''),
                ]
                
                for old_pattern, new_pattern in patterns:
                    content = content.replace(old_pattern, new_pattern)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(str(filepath))
        except Exception as e:
            print(f"Error updating {filepath}: {e}")
    
    return updated_files

def main():
    import sys
    
    # Check for --yes flag
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    
    root_dir = Path(__file__).parent.parent
    img_dir = root_dir / 'assets' / 'img'
    
    print(f"Scanning {img_dir}...")
    files, base_groups = get_all_image_files(img_dir)
    print(f"Found {len(files)} image files in {len(base_groups)} groups")
    
    print("Creating rename mapping...")
    mapping = create_rename_mapping(base_groups)
    
    # Filter out files that don't need renaming
    actual_renames = {k: v for k, v in mapping.items() 
                     if os.path.basename(k) != v}
    
    print(f"Will rename {len(actual_renames)} files")
    
    # Show some examples
    print("\nExample renames:")
    for i, (old, new) in enumerate(list(actual_renames.items())[:10]):
        print(f"  {os.path.basename(old)} -> {new}")
    
    if len(actual_renames) > 10:
        print(f"  ... and {len(actual_renames) - 10} more")
    
    # Ask for confirmation unless auto-confirm
    if not auto_confirm:
        response = input(f"\nProceed with renaming {len(actual_renames)} files? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
    else:
        print(f"\nAuto-confirming: proceeding with renaming {len(actual_renames)} files...")
    
    # Rename files
    print("\nRenaming files...")
    renamed_count = 0
    for old_path, new_name in actual_renames.items():
        old_file = Path(old_path)
        new_file = old_file.parent / new_name
        
        if new_file.exists():
            print(f"Warning: {new_file} already exists, skipping {old_file}")
            continue
        
        try:
            old_file.rename(new_file)
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming {old_file}: {e}")
    
    print(f"Renamed {renamed_count} files")
    
    # Update references
    print("\nUpdating file references...")
    updated_files = update_file_references(root_dir, actual_renames)
    print(f"Updated {len(updated_files)} files with new references")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
