#!/usr/bin/env python3
"""
Optimize Spain-France images for Lighthouse performance.
Creates WebP/AVIF versions and responsive sizes.
"""

import os
from pathlib import Path
from PIL import Image

def optimize_image(filepath: Path):
    """Optimize a single image and create WebP/AVIF versions with responsive sizes."""
    if not filepath.exists():
        print(f"  ⚠️  File not found: {filepath}")
        return
    
    try:
        img = Image.open(filepath)
        
        # Get original dimensions
        width, height = img.size
        print(f"  📐 Original: {width}x{height}")
        
        # Convert RGBA to RGB if needed (for JPEG)
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background
        
        base_name = filepath.stem
        parent = filepath.parent
        
        # WebP version (full size)
        webp_path = parent / f"{base_name}.webp"
        img.save(webp_path, "WEBP", quality=85, method=6)
        webp_size = webp_path.stat().st_size / 1024
        print(f"  ✅ WebP: {webp_size:.1f}KB")
        
        # AVIF version (full size)
        avif_path = None
        try:
            avif_path = parent / f"{base_name}.avif"
            img.save(avif_path, "AVIF", quality=80)
            avif_size = avif_path.stat().st_size / 1024
            print(f"  ✅ AVIF: {avif_size:.1f}KB")
        except Exception as e:
            print(f"  ⚠️  AVIF not supported: {e}")
        
        # Generate responsive sizes
        breakpoints = [320, 640, 768, 1024, 1280]
        max_width = width
        
        for bp in breakpoints:
            if bp > max_width:
                break
            
            # Resize image
            ratio = bp / max_width
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save WebP
            webp_resized_path = parent / f"{base_name}-{bp}w.webp"
            resized.save(webp_resized_path, "WEBP", quality=85, method=6)
            
            # Save AVIF if supported
            if avif_path:
                try:
                    avif_resized_path = parent / f"{base_name}-{bp}w.avif"
                    resized.save(avif_resized_path, "AVIF", quality=80)
                except:
                    pass
        
        print(f"  ✅ Responsive sizes: {[bp for bp in breakpoints if bp <= max_width]}")
        
    except Exception as e:
        print(f"  ❌ Error optimizing {filepath}: {e}")

def main():
    """Optimize all Spain-France images."""
    assets_dir = Path("assets/img")
    
    # Find all spain-france images
    images = sorted(assets_dir.glob("spain-france-*.jpeg"))
    
    if not images:
        print("No spain-france-*.jpeg images found!")
        return
    
    print(f"Found {len(images)} images to optimize\n")
    
    for i, img_path in enumerate(images, 1):
        print(f"[{i}/{len(images)}] {img_path.name}")
        optimize_image(img_path)
        print()
    
    print("✅ Optimization complete!")

if __name__ == "__main__":
    main()
