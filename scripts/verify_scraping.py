#!/usr/bin/env python3
"""
Verification Script
Verifies that all URLs from sitemap.xml have been scraped and all images downloaded.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Set, List, Dict


def load_sitemap_urls(sitemap_path: str = "sitemap.xml") -> Set[str]:
    """Load all URLs from sitemap.xml."""
    sitemap_file = Path(sitemap_path)
    if not sitemap_file.exists():
        print(f"Error: Sitemap file not found: {sitemap_path}")
        return set()
    
    try:
        tree = ET.parse(sitemap_file)
        root = tree.getroot()
        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        
        urls = set()
        for url_elem in root.findall("ns:url", ns):
            loc_elem = url_elem.find("ns:loc", ns)
            if loc_elem is not None and loc_elem.text:
                url = loc_elem.text.strip()
                urls.add(url)
        
        return urls
    except Exception as e:
        print(f"Error parsing sitemap.xml: {e}")
        return set()


def load_scraped_urls(content_path: str = "content/content.json") -> Set[str]:
    """Load all scraped URLs from content.json."""
    content_file = Path(content_path)
    if not content_file.exists():
        print(f"Error: Content file not found: {content_path}")
        return set()
    
    try:
        with open(content_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        urls = set()
        for page in data.get("pages", []):
            url = page.get("url")
            if url:
                urls.add(url)
        
        return urls
    except Exception as e:
        print(f"Error loading content.json: {e}")
        return set()


def load_image_assets(assets_path: str = "content/assets.json") -> List[Dict]:
    """Load all image assets from assets.json."""
    assets_file = Path(assets_path)
    if not assets_file.exists():
        print(f"Error: Assets file not found: {assets_path}")
        return []
    
    try:
        with open(assets_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return [asset for asset in data.get("assets", []) if asset.get("type") == "image"]
    except Exception as e:
        print(f"Error loading assets.json: {e}")
        return []


def get_images_from_pages(content_path: str = "content/content.json") -> Set[str]:
    """Extract all image URLs referenced in scraped pages."""
    content_file = Path(content_path)
    if not content_file.exists():
        return set()
    
    try:
        with open(content_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        image_urls = set()
        for page in data.get("pages", []):
            for image in page.get("images", []):
                src = image.get("src")
                if src:
                    image_urls.add(src)
        
        return image_urls
    except Exception as e:
        print(f"Error extracting images from pages: {e}")
        return set()


def check_downloaded_images(assets_dir: str = "assets/img") -> Set[str]:
    """Check which images have been downloaded locally."""
    assets_path = Path(assets_dir)
    if not assets_path.exists():
        return set()
    
    # Get all image files
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"}
    downloaded = set()
    
    for img_file in assets_path.iterdir():
        if img_file.is_file() and img_file.suffix.lower() in image_extensions:
            # Extract base filename (without size suffix)
            name = img_file.stem
            # Remove size suffix like "-640w"
            if "-" in name and name.split("-")[-1].endswith("w"):
                name = "-".join(name.split("-")[:-1])
            downloaded.add(name)
    
    return downloaded


def main():
    """Main verification function."""
    print("=" * 60)
    print("Scraping Verification Report")
    print("=" * 60)
    print()
    
    # Load URLs
    print("Loading URLs from sitemap.xml...")
    sitemap_urls = load_sitemap_urls()
    print(f"  Found {len(sitemap_urls)} URLs in sitemap.xml")
    
    print("Loading scraped URLs from content.json...")
    scraped_urls = load_scraped_urls()
    print(f"  Found {len(scraped_urls)} scraped pages")
    
    # Normalize URLs for comparison (handle trailing slash differences)
    def normalize_for_comparison(url):
        """Normalize URL for comparison - treat root with/without slash as same."""
        if url in ("https://www.motorover.in", "https://www.motorover.in/"):
            return "https://www.motorover.in/"
        return url.rstrip("/")
    
    normalized_sitemap = {normalize_for_comparison(url) for url in sitemap_urls}
    normalized_scraped = {normalize_for_comparison(url) for url in scraped_urls}
    
    # Compare URLs
    print()
    print("URL Verification:")
    print("-" * 60)
    # Filter out robots.txt and non-HTML URLs
    html_sitemap_urls = {u for u in normalized_sitemap if not u.endswith("/robots.txt") and not u.endswith(".txt")}
    missing_urls = html_sitemap_urls - normalized_scraped
    extra_urls = normalized_scraped - html_sitemap_urls
    
    if missing_urls:
        print(f"  ❌ Missing URLs: {len(missing_urls)}")
        print("  First 10 missing URLs:")
        for url in list(missing_urls)[:10]:
            print(f"    - {url}")
    else:
        print(f"  ✅ All {len(sitemap_urls)} URLs from sitemap have been scraped")
    
    if extra_urls:
        print(f"  ⚠️  Extra URLs (not in sitemap): {len(extra_urls)}")
        print("  First 5 extra URLs:")
        for url in list(extra_urls)[:5]:
            print(f"    - {url}")
    
    # Check images
    print()
    print("Image Verification:")
    print("-" * 60)
    
    image_assets = load_image_assets()
    print(f"  Found {len(image_assets)} image references in assets.json")
    
    images_from_pages = get_images_from_pages()
    print(f"  Found {len(images_from_pages)} unique image URLs in scraped pages")
    
    downloaded_images = check_downloaded_images()
    print(f"  Found {len(downloaded_images)} downloaded image files")
    
    # Check if all images from pages are in assets
    missing_in_assets = images_from_pages - {img.get("url") for img in image_assets}
    if missing_in_assets:
        print(f"  ⚠️  {len(missing_in_assets)} image URLs from pages not in assets.json")
        print("  First 5:")
        for url in list(missing_in_assets)[:5]:
            print(f"    - {url}")
    else:
        print("  ✅ All image URLs from pages are in assets.json")
    
    # Summary
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  URLs in sitemap (HTML only): {len(html_sitemap_urls)}")
    print(f"  URLs scraped: {len(scraped_urls)}")
    print(f"  URLs missing: {len(missing_urls)}")
    print(f"  Image references: {len(image_assets)}")
    print(f"  Images downloaded: {len(downloaded_images)}")
    
    # Check if all HTML URLs are scraped
    if not missing_urls:
        if len(image_assets) > 0:
            print()
            print("  ✅ All HTML URLs scraped and images found!")
        else:
            print()
            print("  ✅ All HTML URLs scraped!")
            print("  ⚠️  Images may still be downloading - check assets.json")
    elif missing_urls:
        print()
        print(f"  ❌ {len(missing_urls)} URLs still need to be scraped")
    else:
        print()
        print("  ⚠️  No images found - may need to run download_images.py")


if __name__ == "__main__":
    main()
