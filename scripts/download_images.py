#!/usr/bin/env python3
"""
Image Downloader and Optimizer
Downloads all images referenced in assets.json and optimizes them.
"""

import json
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests
from PIL import Image


class ImageDownloader:
    """Download and optimize images."""
    
    def __init__(self, content_dir: str = "content", assets_dir: str = "assets/img"):
        self.content_dir = Path(content_dir)
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MotoRoverImageDownloader/1.0"
        })
        
        self.downloaded = {}
        self.failed = []
    
    def load_assets(self) -> List[Dict]:
        """Load assets from assets.json."""
        assets_file = self.content_dir / "assets.json"
        if not assets_file.exists():
            print("assets.json not found. Run scraper first.")
            return []
        
        with open(assets_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return data.get("assets", [])
    
    def sanitize_filename(self, url: str) -> str:
        """Create a safe filename from URL."""
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        
        # Get filename
        filename = os.path.basename(path)
        if not filename or "." not in filename:
            # Generate filename from path
            filename = path.replace("/", "-").replace("\\", "-")
            if not filename:
                filename = "image"
            filename += ".jpg"
        
        # Remove query params from filename
        filename = filename.split("?")[0]
        
        # Sanitize
        filename = re.sub(r'[^\w\-_\.]', '_', filename)
        filename = filename[:200]  # Limit length
        
        return filename
    
    def download_image(self, url: str) -> Optional[Path]:
        """Download a single image."""
        if url in self.downloaded:
            return self.downloaded[url]
        
        try:
            print(f"Downloading: {url}")
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get("content-type", "").lower()
            if "image" not in content_type:
                print(f"  Skipping (not an image): {content_type}")
                return None
            
            # Determine file extension
            ext = ".jpg"
            if "png" in content_type:
                ext = ".png"
            elif "gif" in content_type:
                ext = ".gif"
            elif "webp" in content_type:
                ext = ".webp"
            elif "jpeg" in content_type:
                ext = ".jpg"
            
            filename = self.sanitize_filename(url)
            # Ensure correct extension
            base_name = os.path.splitext(filename)[0]
            filename = base_name + ext
            
            filepath = self.assets_dir / filename
            
            # Save original
            with open(filepath, "wb") as f:
                shutil.copyfileobj(response.raw, f)
            
            self.downloaded[url] = filepath
            return filepath
            
        except Exception as e:
            print(f"  Error downloading {url}: {e}")
            self.failed.append(url)
            return None
    
    def optimize_image(self, filepath: Path) -> Dict:
        """Optimize image and create WebP/AVIF versions."""
        if not filepath.exists():
            return {}
        
        try:
            img = Image.open(filepath)
            
            # Get original dimensions
            width, height = img.size
            
            # Convert RGBA to RGB if needed (for JPEG)
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background
            
            # Create optimized versions
            base_name = filepath.stem
            parent = filepath.parent
            
            # WebP version
            webp_path = parent / f"{base_name}.webp"
            img.save(webp_path, "WEBP", quality=85, method=6)
            
            # AVIF version (if pillow supports it)
            avif_path = None
            try:
                avif_path = parent / f"{base_name}.avif"
                img.save(avif_path, "AVIF", quality=80)
            except Exception:
                pass  # AVIF not supported
            
            # Generate responsive sizes
            sizes = []
            max_width = width
            
            # Generate srcset entries
            srcset_webp = []
            srcset_avif = []
            srcset_orig = []
            
            # Standard responsive breakpoints
            breakpoints = [320, 640, 768, 1024, 1280, 1920]
            
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
                srcset_webp.append(f"{webp_resized_path.name} {bp}w")
                
                # Save AVIF if supported
                if avif_path:
                    try:
                        avif_resized_path = parent / f"{base_name}-{bp}w.avif"
                        resized.save(avif_resized_path, "AVIF", quality=80)
                        srcset_avif.append(f"{avif_resized_path.name} {bp}w")
                    except:
                        pass
                
                # Save original format resized
                orig_resized_path = parent / f"{base_name}-{bp}w{filepath.suffix}"
                resized.save(orig_resized_path, quality=85)
                srcset_orig.append(f"{orig_resized_path.name} {bp}w")
            
            return {
                "original": {
                    "path": str(filepath.relative_to(Path("."))),
                    "width": width,
                    "height": height
                },
                "webp": {
                    "path": str(webp_path.relative_to(Path("."))),
                    "srcset": ",\n    ".join(srcset_webp)
                },
                "avif": {
                    "path": str(avif_path.relative_to(Path("."))) if avif_path else None,
                    "srcset": ",\n    ".join(srcset_avif) if srcset_avif else None
                },
                "srcset": ",\n    ".join(srcset_orig),
                "sizes": "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
            }
            
        except Exception as e:
            print(f"  Error optimizing {filepath}: {e}")
            return {}
    
    def process_all(self):
        """Download and optimize all images."""
        assets = self.load_assets()
        
        image_assets = [a for a in assets if a.get("type") == "image"]
        
        print(f"Found {len(image_assets)} images to download")
        
        optimized_data = {}
        
        for i, asset in enumerate(image_assets, 1):
            url = asset.get("url")
            if not url:
                continue
            
            print(f"[{i}/{len(image_assets)}] Processing: {url}")
            
            filepath = self.download_image(url)
            if filepath:
                optimized = self.optimize_image(filepath)
                if optimized:
                    optimized_data[url] = {
                        **asset,
                        **optimized
                    }
        
        # Update assets.json with optimization data
        assets_file = self.content_dir / "assets.json"
        with open(assets_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Update assets with optimization info
        for asset in data.get("assets", []):
            url = asset.get("url")
            if url in optimized_data:
                asset.update(optimized_data[url])
        
        with open(assets_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\nDownload complete!")
        print(f"  Downloaded: {len(self.downloaded)}")
        print(f"  Failed: {len(self.failed)}")
        if self.failed:
            print(f"\nFailed URLs:")
            for url in self.failed[:10]:  # Show first 10
                print(f"  - {url}")


def main():
    """Main entry point."""
    downloader = ImageDownloader()
    downloader.process_all()


if __name__ == "__main__":
    main()
