#!/usr/bin/env python3
"""
MotoRover.in Web Scraper
Scrapes all content from motorover.in and extracts structured data.
"""

import argparse
import json
import re
import time
import urllib.parse
import urllib.robotparser
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup, Tag, NavigableString


class MotoRoverScraper:
    """Scraper for motorover.in website."""
    
    BASE_URL = "https://www.motorover.in"
    DOMAIN = "motorover.in"
    RATE_LIMIT = 1.0  # seconds between requests
    MAX_DEPTH = 10
    USER_AGENT = "MotoRoverScraper/1.0 (+https://www.motorover.in)"
    
    def __init__(self, output_dir: str = "content"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.visited_urls: Set[str] = set()
        self.url_queue: deque = deque()
        self.pages_data: List[Dict] = []
        self.assets: List[Dict] = []
        self.entities: Dict[str, List] = {
            "tours": [],
            "team": [],
            "faqs": [],
            "testimonials": [],
            "payments": [],
            "contact": []
        }
        
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})
        
        # Check robots.txt
        self.robots_parser = urllib.robotparser.RobotFileParser()
        self.robots_parser.set_url(f"{self.BASE_URL}/robots.txt")
        try:
            self.robots_parser.read()
        except:
            pass  # Continue if robots.txt is not accessible
    
    def load_urls_from_sitemap(self, sitemap_path: str = "sitemap.xml") -> List[str]:
        """Load all URLs from sitemap.xml file."""
        sitemap_file = Path(sitemap_path)
        if not sitemap_file.exists():
            print(f"Sitemap file not found: {sitemap_path}")
            return []
        
        try:
            tree = ET.parse(sitemap_file)
            root = tree.getroot()
            ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            
            urls = []
            for url_elem in root.findall("ns:url", ns):
                loc_elem = url_elem.find("ns:loc", ns)
                if loc_elem is not None and loc_elem.text:
                    url = loc_elem.text.strip()
                    # Normalize URL
                    normalized = self.normalize_url(url)
                    if normalized:
                        urls.append(normalized)
            
            print(f"Loaded {len(urls)} URLs from sitemap.xml")
            return urls
        except Exception as e:
            print(f"Error parsing sitemap.xml: {e}")
            return []
    
    def is_allowed(self, url: str) -> bool:
        """Check if URL is allowed by robots.txt."""
        try:
            return self.robots_parser.can_fetch(self.USER_AGENT, url)
        except:
            return True
    
    def normalize_url(self, url: str, base_url: str = None) -> Optional[str]:
        """Normalize and validate URL."""
        if not url:
            return None
        
        # Handle relative URLs
        if base_url:
            url = urljoin(base_url, url)
        
        parsed = urlparse(url)
        
        # Only process same-domain URLs
        if parsed.netloc and parsed.netloc.replace("www.", "") != self.DOMAIN:
            return None
        
        # Remove fragments and normalize
        normalized = urlunparse((
            parsed.scheme or "https",
            parsed.netloc or self.DOMAIN,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            ""  # Remove fragment
        ))
        
        # Ensure https
        if normalized.startswith("http://"):
            normalized = normalized.replace("http://", "https://")
        
        return normalized
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all internal links from page."""
        links = []
        
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            normalized = self.normalize_url(href, base_url)
            if normalized and normalized not in self.visited_urls:
                links.append(normalized)
        
        return links
    
    def extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract page metadata."""
        title = ""
        meta_desc = ""
        canonical = url
        lang = "en-IN"
        
        # Title
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Meta description
        meta_desc_tag = soup.find("meta", attrs={"name": "description"})
        if not meta_desc_tag:
            meta_desc_tag = soup.find("meta", attrs={"property": "og:description"})
        if meta_desc_tag:
            meta_desc = meta_desc_tag.get("content", "").strip()
        
        # Canonical
        canonical_tag = soup.find("link", attrs={"rel": "canonical"})
        if canonical_tag and canonical_tag.get("href"):
            canonical = self.normalize_url(canonical_tag["href"], url)
        
        # Language
        html_tag = soup.find("html")
        if html_tag and html_tag.get("lang"):
            lang = html_tag["lang"]
        
        return {
            "title": title,
            "metaDescription": meta_desc,
            "canonical": canonical,
            "lang": lang
        }
    
    def extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract all headings with hierarchy."""
        headings = {"h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": []}
        
        for level in range(1, 7):
            for heading in soup.find_all(f"h{level}"):
                text = heading.get_text(strip=True)
                if text:
                    headings[f"h{level}"].append(text)
        
        return headings
    
    def extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract all images from page."""
        images = []
        
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
            if not src:
                continue
            
            # Normalize image URL - allow external URLs for images
            img_url = self.normalize_url(src, base_url)
            # If normalize_url returns None (external domain), try to use the original URL
            if not img_url:
                # For images, allow external URLs (CDN, etc.)
                if src.startswith("http://") or src.startswith("https://"):
                    img_url = src
                elif src.startswith("//"):
                    img_url = "https:" + src
                else:
                    # Relative URL
                    img_url = urljoin(base_url, src)
            
            if not img_url:
                continue
            
            alt = img.get("alt", "").strip()
            width = img.get("width")
            height = img.get("height")
            
            # Try to get dimensions from style or data attributes
            if not width:
                width = img.get("data-width")
            if not height:
                height = img.get("data-height")
            
            image_data = {
                "src": img_url,
                "alt": alt,
                "width": int(width) if width and str(width).isdigit() else None,
                "height": int(height) if height and str(height).isdigit() else None,
                "caption": "",
                "context": "page"
            }
            
            # Look for caption (common patterns)
            parent = img.parent
            if parent:
                figcaption = parent.find("figcaption")
                if figcaption:
                    image_data["caption"] = figcaption.get_text(strip=True)
            
            images.append(image_data)
            
            # Track asset
            self.assets.append({
                "url": img_url,
                "type": "image",
                "page_url": base_url,
                "alt": alt
            })
        
        return images
    
    def extract_forms(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract all forms from page."""
        forms = []
        
        for form in soup.find_all("form"):
            form_id = form.get("id", "")
            action = form.get("action", "")
            method = form.get("method", "get").lower()
            
            if action:
                action = self.normalize_url(action, base_url)
            
            fields = []
            for input_tag in form.find_all(["input", "textarea", "select"]):
                field_type = input_tag.get("type", "text")
                name = input_tag.get("name", "")
                field_id = input_tag.get("id", "")
                placeholder = input_tag.get("placeholder", "")
                required = input_tag.has_attr("required")
                
                # Find associated label
                label_text = ""
                if field_id:
                    label = soup.find("label", attrs={"for": field_id})
                    if label:
                        label_text = label.get_text(strip=True)
                
                # If no label by for, check if label wraps input
                if not label_text:
                    parent = input_tag.parent
                    if parent and parent.name == "label":
                        label_text = parent.get_text(strip=True)
                
                fields.append({
                    "name": name,
                    "type": field_type,
                    "id": field_id,
                    "placeholder": placeholder,
                    "label": label_text,
                    "required": required
                })
            
            forms.append({
                "id": form_id,
                "purpose": self._infer_form_purpose(form),
                "action": action,
                "method": method,
                "fields": fields
            })
        
        return forms
    
    def _infer_form_purpose(self, form: Tag) -> str:
        """Infer form purpose from context."""
        form_text = form.get_text().lower()
        
        if "contact" in form_text or "enquiry" in form_text:
            return "contact"
        elif "book" in form_text or "reservation" in form_text:
            return "booking"
        elif "newsletter" in form_text or "subscribe" in form_text:
            return "newsletter"
        elif "payment" in form_text or "pay" in form_text:
            return "payment"
        else:
            return "general"
    
    def extract_content_blocks(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract structured content blocks."""
        blocks = []
        main_content = soup.find("main") or soup.find("article") or soup.find("body")
        
        if not main_content:
            return blocks
        
        # Remove script and style tags
        for tag in main_content.find_all(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        
        # Extract hero section
        hero = main_content.find(class_=re.compile(r"hero|banner|header", re.I))
        if hero:
            blocks.append({
                "type": "hero",
                "content": {
                    "text": hero.get_text(strip=True),
                    "html": str(hero)
                }
            })
        
        # Extract sections
        for section in main_content.find_all(["section", "div"], class_=True):
            classes = " ".join(section.get("class", []))
            text = section.get_text(strip=True)
            
            if not text or len(text) < 10:
                continue
            
            # Identify block type
            block_type = "text"
            if re.search(r"itinerary|day|schedule", classes, re.I):
                block_type = "itinerary"
            elif re.search(r"gallery|image|photo", classes, re.I):
                block_type = "gallery"
            elif re.search(r"testimonial|review|quote", classes, re.I):
                block_type = "testimonial"
            elif re.search(r"faq|question|answer", classes, re.I):
                block_type = "faq"
            elif re.search(r"pricing|price|cost", classes, re.I):
                block_type = "pricing"
            elif re.search(r"feature|highlight|benefit", classes, re.I):
                block_type = "feature-list"
            elif re.search(r"cta|call.*action|button", classes, re.I):
                block_type = "cta"
            
            blocks.append({
                "type": block_type,
                "content": {
                    "text": text,
                    "html": str(section)
                }
            })
        
        # If no blocks found, create a text block from main content
        if not blocks:
            text_content = main_content.get_text(separator="\n", strip=True)
            if text_content:
                blocks.append({
                    "type": "text",
                    "content": {
                        "text": text_content,
                        "html": str(main_content)
                    }
                })
        
        return blocks
    
    def extract_internal_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract internal links with anchor text."""
        links = []
        
        for a in soup.find_all("a", href=True):
            href = a["href"]
            normalized = self.normalize_url(href, base_url)
            
            if normalized and self.DOMAIN in normalized:
                anchor_text = a.get_text(strip=True)
                links.append({
                    "anchor": anchor_text,
                    "target": normalized
                })
        
        return links
    
    def extract_structured_data_hints(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract structured data hints (schema.org, microdata, etc.)."""
        hints = []
        
        # JSON-LD
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                hints.append({
                    "type": "json-ld",
                    "data": data
                })
            except:
                pass
        
        # Microdata
        for item in soup.find_all(attrs={"itemscope": True}):
            item_type = item.get("itemtype", "")
            if item_type:
                hints.append({
                    "type": "microdata",
                    "itemtype": item_type
                })
        
        return hints
    
    def extract_entities(self, soup: BeautifulSoup, url: str, page_data: Dict):
        """Extract normalized entities (tours, team, FAQs, etc.)."""
        # Extract FAQs
        for faq_item in soup.find_all(class_=re.compile(r"faq|question|answer", re.I)):
            question = ""
            answer = ""
            
            q_tag = faq_item.find(class_=re.compile(r"question|q|ask", re.I))
            a_tag = faq_item.find(class_=re.compile(r"answer|a|response", re.I))
            
            if q_tag:
                question = q_tag.get_text(strip=True)
            if a_tag:
                answer = a_tag.get_text(strip=True)
            
            if question and answer:
                self.entities["faqs"].append({
                    "question": question,
                    "answer": answer,
                    "source_url": url
                })
        
        # Extract testimonials
        for testimonial in soup.find_all(class_=re.compile(r"testimonial|review|quote", re.I)):
            quote = testimonial.get_text(strip=True)
            author = ""
            source = ""
            
            author_tag = testimonial.find(class_=re.compile(r"author|name|person", re.I))
            if author_tag:
                author = author_tag.get_text(strip=True)
            
            if quote and len(quote) > 20:  # Minimum length for testimonial
                self.entities["testimonials"].append({
                    "quote": quote,
                    "author": author,
                    "source": source or url
                })
        
        # Extract tour information (if on tour page)
        if "tour" in url.lower() or "motorcycle" in url.lower() or "self-drive" in url.lower():
            tour_data = self._extract_tour_data(soup, url, page_data)
            if tour_data:
                self.entities["tours"].append(tour_data)
        
        # Extract team members (if on team/about page)
        if "team" in url.lower() or "about" in url.lower():
            team_members = self._extract_team_data(soup, url)
            self.entities["team"].extend(team_members)
        
        # Extract contact information
        contact_info = self._extract_contact_data(soup, url)
        if contact_info:
            self.entities["contact"].append(contact_info)
    
    def _extract_tour_data(self, soup: BeautifulSoup, url: str, page_data: Dict) -> Optional[Dict]:
        """Extract tour-specific data."""
        tour = {
            "name": page_data.get("title", ""),
            "url": url,
            "type": "motorcycle" if "motorcycle" in url.lower() else "self-drive",
            "duration": "",
            "dates": [],
            "start_location": "",
            "end_location": "",
            "highlights": [],
            "itinerary": [],
            "inclusions": [],
            "exclusions": [],
            "gallery": [],
            "testimonials": []
        }
        
        # Try to extract duration, dates, locations from content
        content_text = soup.get_text()
        
        # Duration pattern
        duration_match = re.search(r"(\d+)\s*(?:days?|nights?)", content_text, re.I)
        if duration_match:
            tour["duration"] = duration_match.group(0)
        
        # Date patterns
        date_patterns = [
            r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}",
            r"\d{4}-\d{2}-\d{2}"
        ]
        for pattern in date_patterns:
            dates = re.findall(pattern, content_text, re.I)
            tour["dates"].extend(dates)
        
        # Extract highlights, itinerary, etc. from structured content
        for block in page_data.get("contentBlocks", []):
            if block["type"] == "itinerary":
                tour["itinerary"].append(block["content"]["text"])
            elif block["type"] == "feature-list":
                tour["highlights"].append(block["content"]["text"])
        
        return tour if tour["name"] else None
    
    def _extract_team_data(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Extract team member data."""
        team = []
        
        # Look for team member cards/sections
        for member in soup.find_all(class_=re.compile(r"team|member|person|staff", re.I)):
            name = ""
            role = ""
            bio = ""
            image = ""
            
            name_tag = member.find(class_=re.compile(r"name|title", re.I))
            if name_tag:
                name = name_tag.get_text(strip=True)
            
            role_tag = member.find(class_=re.compile(r"role|position|title", re.I))
            if role_tag:
                role = role_tag.get_text(strip=True)
            
            bio_tag = member.find(class_=re.compile(r"bio|description|about", re.I))
            if bio_tag:
                bio = bio_tag.get_text(strip=True)
            
            img_tag = member.find("img")
            if img_tag:
                image = img_tag.get("src", "")
            
            if name:
                team.append({
                    "name": name,
                    "role": role,
                    "bio": bio,
                    "image": image,
                    "socials": {}
                })
        
        return team
    
    def _extract_contact_data(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        """Extract contact information."""
        contact = {
            "url": url,
            "email": "",
            "phone": "",
            "address": "",
            "social": {}
        }
        
        content_text = soup.get_text()
        
        # Email
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", content_text)
        if email_match:
            contact["email"] = email_match.group(0)
        
        # Phone
        phone_match = re.search(r"[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}", content_text)
        if phone_match:
            contact["phone"] = phone_match.group(0)
        
        # Social links
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "facebook.com" in href:
                contact["social"]["facebook"] = href
            elif "twitter.com" in href or "x.com" in href:
                contact["social"]["twitter"] = href
            elif "instagram.com" in href:
                contact["social"]["instagram"] = href
            elif "linkedin.com" in href:
                contact["social"]["linkedin"] = href
        
        return contact if contact["email"] or contact["phone"] else None
    
    def scrape_page(self, url: str, check_robots: bool = True) -> Optional[Dict]:
        """Scrape a single page.
        
        Args:
            url: URL to scrape
            check_robots: Whether to check robots.txt (default: True)
        """
        if url in self.visited_urls:
            return None
        
        if check_robots and not self.is_allowed(url):
            print(f"Skipping {url} (robots.txt disallowed)")
            return None
        
        print(f"Scraping: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get("content-type", "").lower()
            if "text/html" not in content_type:
                print(f"Skipping {url} (not HTML)")
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract all data
            metadata = self.extract_metadata(soup, url)
            slug = self._url_to_slug(url)
            
            page_data = {
                "url": url,
                "slug": slug,
                **metadata,
                "headings": self.extract_headings(soup),
                "contentBlocks": self.extract_content_blocks(soup),
                "images": self.extract_images(soup, url),
                "forms": self.extract_forms(soup, url),
                "internalLinks": self.extract_internal_links(soup, url),
                "structuredDataHints": self.extract_structured_data_hints(soup)
            }
            
            # Extract entities
            self.extract_entities(soup, url, page_data)
            
            self.visited_urls.add(url)
            return page_data
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def _url_to_slug(self, url: str) -> str:
        """Convert URL to slug."""
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        
        if not path or path == "":
            return "index"
        
        # Remove file extension
        path = re.sub(r"\.(html?|php|aspx?)$", "", path, flags=re.I)
        
        # Replace slashes with hyphens
        slug = path.replace("/", "-")
        
        return slug or "index"
    
    def crawl(self, start_url: str = None, url_list: List[str] = None, ignore_robots: bool = False):
        """Crawl the entire site.
        
        Args:
            start_url: Single URL to start crawling from (uses link-following)
            url_list: List of URLs to scrape directly (no link-following)
            ignore_robots: If True, skip robots.txt checks (default: False)
        """
        # If URL list provided, scrape those directly
        if url_list:
            print(f"Scraping {len(url_list)} URLs from provided list")
            for url in url_list:
                page_data = self.scrape_page(url, check_robots=not ignore_robots)
                if page_data:
                    self.pages_data.append(page_data)
                # Rate limiting
                time.sleep(self.RATE_LIMIT)
            return
        
        # Otherwise use link-following crawl
        if start_url is None:
            start_url = f"{self.BASE_URL}/"
        
        start_url = self.normalize_url(start_url)
        if not start_url:
            return
        
        self.url_queue.append((start_url, 0))  # (url, depth)
        
        while self.url_queue:
            url, depth = self.url_queue.popleft()
            
            if depth > self.MAX_DEPTH:
                continue
            
            page_data = self.scrape_page(url)
            if page_data:
                self.pages_data.append(page_data)
                
                # Add new links to queue
                if depth < self.MAX_DEPTH:
                    links = [link["target"] for link in page_data.get("internalLinks", [])]
                    for link in links:
                        if link not in self.visited_urls and (link, depth + 1) not in self.url_queue:
                            self.url_queue.append((link, depth + 1))
            
            # Rate limiting
            time.sleep(self.RATE_LIMIT)
    
    def save(self):
        """Save all scraped data to JSON files."""
        # Save content.json
        content_file = self.output_dir / "content.json"
        with open(content_file, "w", encoding="utf-8") as f:
            json.dump({"pages": self.pages_data}, f, indent=2, ensure_ascii=False)
        
        # Save entities.json
        entities_file = self.output_dir / "entities.json"
        with open(entities_file, "w", encoding="utf-8") as f:
            json.dump(self.entities, f, indent=2, ensure_ascii=False)
        
        # Save assets.json
        assets_file = self.output_dir / "assets.json"
        with open(assets_file, "w", encoding="utf-8") as f:
            json.dump({"assets": self.assets}, f, indent=2, ensure_ascii=False)
        
        # Save sitemap.json
        sitemap_data = {
            "urls": [page["url"] for page in self.pages_data],
            "hierarchy": self._build_hierarchy(),
            "redirects": {}
        }
        sitemap_file = self.output_dir / "sitemap.json"
        with open(sitemap_file, "w", encoding="utf-8") as f:
            json.dump(sitemap_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nScraping complete!")
        print(f"  Pages scraped: {len(self.pages_data)}")
        print(f"  Assets found: {len(self.assets)}")
        print(f"  Tours: {len(self.entities['tours'])}")
        print(f"  FAQs: {len(self.entities['faqs'])}")
        print(f"  Testimonials: {len(self.entities['testimonials'])}")
        print(f"  Team members: {len(self.entities['team'])}")
    
    def _build_hierarchy(self) -> Dict:
        """Build URL hierarchy."""
        hierarchy = {}
        
        for page in self.pages_data:
            url = page["url"]
            parsed = urlparse(url)
            path_parts = [p for p in parsed.path.split("/") if p]
            
            current = hierarchy
            for part in path_parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current["_url"] = url
        
        return hierarchy


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Scrape motorover.in website")
    parser.add_argument(
        "--sitemap",
        type=str,
        default="sitemap.xml",
        help="Path to sitemap.xml file (default: sitemap.xml)"
    )
    parser.add_argument(
        "--use-sitemap",
        action="store_true",
        help="Use URLs from sitemap.xml instead of link-following crawl"
    )
    parser.add_argument(
        "--start-url",
        type=str,
        help="Start URL for link-following crawl (default: homepage)"
    )
    parser.add_argument(
        "--ignore-robots",
        action="store_true",
        help="Ignore robots.txt restrictions (use with caution)"
    )
    
    args = parser.parse_args()
    
    scraper = MotoRoverScraper()
    
    if args.use_sitemap:
        # Load URLs from sitemap and scrape them
        urls = scraper.load_urls_from_sitemap(args.sitemap)
        if urls:
            scraper.crawl(url_list=urls, ignore_robots=args.ignore_robots)
        else:
            print("No URLs found in sitemap. Exiting.")
            return
    else:
        # Use link-following crawl
        scraper.crawl(start_url=args.start_url, ignore_robots=args.ignore_robots)
    
    scraper.save()


if __name__ == "__main__":
    main()
