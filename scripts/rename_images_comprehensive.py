#!/usr/bin/env python3
"""
Comprehensive image renaming script that:
1. Extracts all image references from HTML, JSON, JS files
2. Derives meaningful names from alt text, page context, and existing filenames
3. Removes all timestamp prefixes
4. Updates ALL references including srcset attributes in JSON files
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup

def normalize_name(name):
    """Convert a name to a normalized format: lowercase with dashes."""
    if not name:
        return ""
    
    # Remove leading numbers (timestamps)
    name = re.sub(r'^\d+', '', name)
    
    # Insert dash before numbers (e.g., "gallery2" -> "gallery-2")
    name = re.sub(r'([a-zA-Z])(\d)', r'\1-\2', name)
    # Insert dash after numbers before letters
    name = re.sub(r'(\d)([a-zA-Z])', r'\1-\2', name)
    
    # Convert camelCase to kebab-case
    # Insert dash before capital letters that follow lowercase
    name = re.sub(r'([a-z])([A-Z])', r'\1-\2', name)
    # Insert dash before capital letters that follow numbers
    name = re.sub(r'(\d)([A-Z])', r'\1-\2', name)
    # Handle multiple capital letters (e.g., "BMW3Series" -> "BMW-3-Series")
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', name)
    
    # Handle cases like "Scotlandgallery" -> "Scotland-gallery"
    def split_camel(match):
        s = match.group(0)
        for i in range(len(s) - 1, 0, -1):
            if s[i].isupper() and s[i-1].islower():
                return s[:i] + '-' + s[i:]
        return s
    
    name = re.sub(r'[A-Z][a-z]+[A-Z]', split_camel, name)
    
    # Convert to lowercase
    name = name.lower()
    
    # Replace spaces, underscores, commas, and other special chars with dashes
    name = re.sub(r'[\s_\.\,]+', '-', name)
    
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

def extract_html_image_references(root_dir):
    """Extract image references from HTML files with alt text."""
    html_refs = {}
    
    for html_file in Path(root_dir).rglob('*.html'):
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                alt = img.get('alt', '').strip()
                
                if src and 'assets/img' in src:
                    # Extract filename from path
                    filename = os.path.basename(src.split('?')[0])  # Remove query params
                    if filename:
                        if filename not in html_refs:
                            html_refs[filename] = {
                                'alt_texts': set(),
                                'pages': set()
                            }
                        if alt:
                            html_refs[filename]['alt_texts'].add(alt)
                        html_refs[filename]['pages'].add(str(html_file.relative_to(root_dir)))
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
    
    return html_refs

def extract_json_image_references(root_dir):
    """Extract image references from assets.json with alt text and page context."""
    json_refs = {}
    assets_file = Path(root_dir) / 'content' / 'assets.json'
    
    if not assets_file.exists():
        return json_refs
    
    try:
        with open(assets_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for asset in data.get('assets', []):
            alt_text = asset.get('alt', '').strip()
            page_url = asset.get('page_url', '')
            
            # Extract page name from URL
            page_name = ''
            if page_url:
                page_name = os.path.basename(page_url.split('?')[0])
            
            # Check original path
            if 'original' in asset and 'path' in asset['original']:
                path = asset['original']['path']
                if 'assets/img' in path:
                    filename = os.path.basename(path)
                    if filename not in json_refs:
                        json_refs[filename] = {
                            'alt_text': alt_text,
                            'page_url': page_url,
                            'page_name': page_name
                        }
                    elif alt_text and not json_refs[filename].get('alt_text'):
                        json_refs[filename]['alt_text'] = alt_text
            
            # Check webp path
            if 'webp' in asset and 'path' in asset['webp']:
                path = asset['webp']['path']
                if 'assets/img' in path:
                    filename = os.path.basename(path)
                    if filename not in json_refs:
                        json_refs[filename] = {
                            'alt_text': alt_text,
                            'page_url': page_url,
                            'page_name': page_name
                        }
            
            # Check avif path
            if 'avif' in asset and 'path' in asset['avif']:
                path = asset['avif']['path']
                if 'assets/img' in path:
                    filename = os.path.basename(path)
                    if filename not in json_refs:
                        json_refs[filename] = {
                            'alt_text': alt_text,
                            'page_url': page_url,
                            'page_name': page_name
                        }
    except Exception as e:
        print(f"Error processing assets.json: {e}")
    
    return json_refs

def build_context_mapping(root_dir):
    """Build comprehensive context mapping for all images."""
    print("Extracting HTML image references...")
    html_refs = extract_html_image_references(root_dir)
    
    print("Extracting JSON image references...")
    json_refs = extract_json_image_references(root_dir)
    
    # Combine contexts
    context_map = {}
    
    # Add HTML references
    for filename, context in html_refs.items():
        context_map[filename] = {
            'alt_texts': list(context['alt_texts']),
            'pages': list(context['pages']),
            'alt_text': context['alt_texts'].pop() if context['alt_texts'] else '',
            'page_name': ''
        }
    
    # Merge JSON references (prioritize JSON alt text)
    for filename, context in json_refs.items():
        if filename not in context_map:
            context_map[filename] = {
                'alt_texts': [],
                'pages': [],
                'alt_text': context.get('alt_text', ''),
                'page_name': context.get('page_name', '')
            }
        else:
            # Update with JSON data if better
            if context.get('alt_text') and not context_map[filename]['alt_text']:
                context_map[filename]['alt_text'] = context['alt_text']
            if context.get('page_name') and not context_map[filename]['page_name']:
                context_map[filename]['page_name'] = context['page_name']
    
    return context_map

def derive_meaningful_name(filename, context_map, base_groups):
    """Derive meaningful name from context."""
    # Get base name (without extension and width suffix)
    base_name = extract_base_name(filename)
    
    # Priority 1: Alt text from HTML or JSON
    if filename in context_map:
        alt_text = context_map[filename].get('alt_text', '')
        if alt_text:
            normalized = normalize_name(alt_text)
            if normalized:
                return normalized
    
    # Priority 2: Page context + existing name (only if base_name doesn't already contain page context)
    if filename in context_map:
        page_name = context_map[filename].get('page_name', '')
        if page_name:
            # Extract meaningful part from page name
            page_base = os.path.splitext(page_name)[0]
            page_base = normalize_name(page_base)
            normalized_base = normalize_name(base_name) if base_name else ''
            
            # Only combine if base_name doesn't already start with page_base
            if page_base and normalized_base:
                if not normalized_base.startswith(page_base):
                    combined = f"{page_base}-{normalized_base}"
                    if combined:
                        return combined
                else:
                    # Base already contains page context, just use it
                    return normalized_base
    
    # Priority 3: Existing meaningful filename parts
    if base_name:
        normalized = normalize_name(base_name)
        if normalized:
            return normalized
    
    # Priority 4: Fallback for numeric-only files
    # Extract short hash from original filename
    numeric_match = re.match(r'^(\d+)', filename)
    if numeric_match:
        short_id = numeric_match.group(1)[-6:]
        return f"image-{short_id}"
    
    # Final fallback
    return "image-unknown"

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

def create_rename_mapping(base_groups, context_map):
    """Create comprehensive rename mapping."""
    mapping = {}
    name_usage = defaultdict(int)  # Track name usage for uniqueness
    
    for base_name, files in base_groups.items():
        # Derive meaningful name for this base
        # Use first file to get context
        first_file = files[0]
        meaningful_base = derive_meaningful_name(first_file.name, context_map, base_groups)
        
        # Ensure uniqueness
        original_base = meaningful_base
        counter = 0
        while name_usage[meaningful_base] > 0:
            counter += 1
            meaningful_base = f"{original_base}-{counter}"
        name_usage[meaningful_base] += 1
        
        # Create mapping for all variants
        for filepath in files:
            old_name = filepath.name
            ext = filepath.suffix.lower()
            
            # Check if it has a width suffix
            width_match = re.search(r'-(\d+w)$', os.path.splitext(old_name)[0])
            if width_match:
                width_suffix = width_match.group(1)
                new_name = f"{meaningful_base}-{width_suffix}{ext}"
            else:
                new_name = f"{meaningful_base}{ext}"
            
            mapping[str(filepath)] = new_name
    
    return mapping

def fix_srcset_in_assets_json(assets_file, filename_mapping):
    """Fix srcset strings in assets.json that contain old timestamped names."""
    try:
        with open(assets_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated = False
        
        for asset in data.get('assets', []):
            # Get current path to determine the base name
            current_path = None
            if 'original' in asset and 'path' in asset['original']:
                current_path = asset['original']['path']
            elif 'webp' in asset and 'path' in asset['webp']:
                current_path = asset['webp']['path']
            elif 'avif' in asset and 'path' in asset['avif']:
                current_path = asset['avif']['path']
            
            if current_path and 'assets/img' in current_path:
                current_filename = os.path.basename(current_path)
                current_base = extract_base_name(current_filename)
                
                # Fix webp srcset
                if 'webp' in asset and 'srcset' in asset['webp']:
                    srcset = asset['webp']['srcset']
                    if srcset and isinstance(srcset, str):
                        # Find old timestamped names in srcset
                        # Pattern: "1482396555082MotoRoverlogo-320w.webp 320w"
                        pattern = r'(\d+)([A-Za-z][A-Za-z0-9]*?)(?:-(\d+w))?\.(\w+)\s+(\d+w)'
                        
                        def replace_srcset_item(match):
                            timestamp = match.group(1)
                            name_part = match.group(2)
                            width = match.group(3) or ''
                            ext = match.group(4)
                            size = match.group(5)
                            
                            # Use current base name
                            if width:
                                new_name = f"{current_base}-{width}.{ext}"
                            else:
                                new_name = f"{current_base}.{ext}"
                            
                            return f"{new_name} {size}"
                        
                        new_srcset = re.sub(pattern, replace_srcset_item, srcset)
                        if new_srcset != srcset:
                            asset['webp']['srcset'] = new_srcset
                            updated = True
                
                # Fix avif srcset
                if 'avif' in asset and 'srcset' in asset['avif']:
                    srcset = asset['avif']['srcset']
                    if srcset and isinstance(srcset, str):
                        pattern = r'(\d+)([A-Za-z][A-Za-z0-9]*?)(?:-(\d+w))?\.(\w+)\s+(\d+w)'
                        
                        def replace_srcset_item(match):
                            timestamp = match.group(1)
                            name_part = match.group(2)
                            width = match.group(3) or ''
                            ext = match.group(4)
                            size = match.group(5)
                            
                            if width:
                                new_name = f"{current_base}-{width}.{ext}"
                            else:
                                new_name = f"{current_base}.{ext}"
                            
                            return f"{new_name} {size}"
                        
                        new_srcset = re.sub(pattern, replace_srcset_item, srcset)
                        if new_srcset != srcset:
                            asset['avif']['srcset'] = new_srcset
                            updated = True
                
                # Fix main srcset
                if 'srcset' in asset:
                    srcset = asset['srcset']
                    if srcset and isinstance(srcset, str):
                        pattern = r'(\d+)([A-Za-z][A-Za-z0-9]*?)(?:-(\d+w))?\.(\w+)\s+(\d+w)'
                        
                        def replace_srcset_item(match):
                            timestamp = match.group(1)
                            name_part = match.group(2)
                            width = match.group(3) or ''
                            ext = match.group(4)
                            size = match.group(5)
                            
                            if width:
                                new_name = f"{current_base}-{width}.{ext}"
                            else:
                                new_name = f"{current_base}.{ext}"
                            
                            return f"{new_name} {size}"
                        
                        new_srcset = re.sub(pattern, replace_srcset_item, srcset)
                        if new_srcset != srcset:
                            asset['srcset'] = new_srcset
                            updated = True
        
        if updated:
            with open(assets_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        
        return False
    except Exception as e:
        print(f"Error fixing srcset in assets.json: {e}")
        return False

def update_file_references(root_dir, mapping):
    """Update all file references including srcset in JSON."""
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
                if any(skip in str(filepath) for skip in ['node_modules', '.git', '__pycache__', '.venv', '.cursor']):
                    continue
                text_files.append(filepath)
    
    updated_files = []
    
    for filepath in text_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            
            # Update direct filename references
            for old_filename, new_filename in filename_mapping.items():
                # Skip if already updated
                if old_filename == new_filename:
                    continue
                
                # Replace in various path formats
                patterns = [
                    (f'assets/img/{old_filename}', f'assets/img/{new_filename}'),
                    (f'/assets/img/{old_filename}', f'/assets/img/{new_filename}'),
                    (f'"assets/img/{old_filename}"', f'"assets/img/{new_filename}"'),
                    (f"'assets/img/{old_filename}'", f"'assets/img/{new_filename}'"),
                ]
                
                for old_pattern, new_pattern in patterns:
                    content = content.replace(old_pattern, new_pattern)
            
            # Update direct filename references in srcset
            for old_filename, new_filename in filename_mapping.items():
                if old_filename != new_filename:
                    # Direct filename replacement
                    content = re.sub(
                        rf'\b{re.escape(old_filename)}\b',
                        new_filename,
                        content
                    )
            
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
    
    print(f"Comprehensive Image Renaming Script")
    print(f"Root directory: {root_dir}")
    print(f"Image directory: {img_dir}")
    print()
    
    # Step 1: Build context mapping
    print("Step 1: Building context mapping...")
    context_map = build_context_mapping(root_dir)
    print(f"Found context for {len(context_map)} image files")
    print()
    
    # Step 2: Get all image files
    print("Step 2: Scanning image files...")
    files, base_groups = get_all_image_files(img_dir)
    print(f"Found {len(files)} image files in {len(base_groups)} groups")
    print()
    
    # Step 3: Create rename mapping
    print("Step 3: Creating rename mapping...")
    mapping = create_rename_mapping(base_groups, context_map)
    
    # Filter out files that don't need renaming
    actual_renames = {k: v for k, v in mapping.items() 
                     if os.path.basename(k) != v}
    
    print(f"Will rename {len(actual_renames)} files")
    print()
    
    # Show some examples
    print("Example renames:")
    for i, (old, new) in enumerate(list(actual_renames.items())[:15]):
        print(f"  {os.path.basename(old)} -> {new}")
    
    if len(actual_renames) > 15:
        print(f"  ... and {len(actual_renames) - 15} more")
    print()
    
    # Ask for confirmation unless auto-confirm
    if not auto_confirm:
        response = input(f"Proceed with renaming {len(actual_renames)} files? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
    else:
        print(f"Auto-confirming: proceeding with renaming {len(actual_renames)} files...")
        print()
    
    # Step 4: Update references first (before renaming files)
    print("Step 4: Updating file references...")
    updated_files = update_file_references(root_dir, actual_renames)
    
    # Special handling for assets.json srcset
    assets_file = root_dir / 'content' / 'assets.json'
    if assets_file.exists():
        print("Fixing srcset strings in assets.json...")
        if fix_srcset_in_assets_json(assets_file, {os.path.basename(k): v for k, v in actual_renames.items()}):
            print("Updated srcset strings in assets.json")
            if str(assets_file) not in updated_files:
                updated_files.append(str(assets_file))
    
    print(f"Updated {len(updated_files)} files with new references")
    print()
    
    # Step 5: Rename files
    print("Step 5: Renaming files...")
    renamed_count = 0
    errors = []
    
    for old_path, new_name in actual_renames.items():
        old_file = Path(old_path)
        new_file = old_file.parent / new_name
        
        if new_file.exists():
            errors.append(f"Warning: {new_file} already exists, skipping {old_file}")
            continue
        
        try:
            old_file.rename(new_file)
            renamed_count += 1
        except Exception as e:
            errors.append(f"Error renaming {old_file}: {e}")
    
    print(f"Renamed {renamed_count} files")
    
    if errors:
        print(f"\n{len(errors)} errors/warnings:")
        for error in errors[:10]:
            print(f"  {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
    
    print()
    print("Done!")

if __name__ == '__main__':
    main()
