#!/usr/bin/env python3
"""
Static Site Generator
Generates HTML pages from JSON content using Jinja2 templates.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape


class SiteGenerator:
    """Generate static HTML site from JSON content."""
    
    def __init__(self, content_dir: str = "content", output_dir: str = ".", templates_dir: str = "templates"):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.templates_dir = Path(templates_dir)
        
        # Setup Jinja2
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Load content
        self.content = self._load_json("content.json")
        self.entities = self._load_json("entities.json")
        self.sitemap_data = self._load_json("sitemap.json")
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
    
    def _load_json(self, filename: str) -> Dict:
        """Load JSON file."""
        filepath = self.content_dir / filename
        if not filepath.exists():
            return {}
        
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _get_page_by_url(self, url: str) -> Optional[Dict]:
        """Get page data by URL."""
        pages = self.content.get("pages", [])
        for page in pages:
            if page.get("url") == url:
                return page
        return None
    
    def _get_tour_by_url(self, url: str) -> Optional[Dict]:
        """Get tour entity by URL."""
        tours = self.entities.get("tours", [])
        for tour in tours:
            if tour.get("url") == url:
                return tour
        return None
    
    def _build_breadcrumbs(self, page: Dict) -> List[Dict]:
        """Build breadcrumb trail for a page."""
        url = page.get("url", "")
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split("/") if p]
        
        breadcrumbs = [{"name": "Home", "url": "/"}]
        
        current_path = ""
        for i, part in enumerate(path_parts):
            current_path += f"/{part}"
            # Try to find page title
            page_data = self._get_page_by_url(f"https://www.motorover.in{current_path}")
            name = part.replace("-", " ").title()
            if page_data and page_data.get("title"):
                name = page_data["title"]
            
            breadcrumbs.append({
                "name": name,
                "url": current_path if current_path != "/" else "/"
            })
        
        return breadcrumbs
    
    def _determine_template(self, page: Dict) -> str:
        """Determine which template to use for a page."""
        url = page.get("url", "").lower()
        slug = page.get("slug", "").lower()
        
        if slug == "index" or url.endswith("/") or url.endswith("/index.html"):
            return "home.html"
        elif "tour" in url or "motorcycle" in url or "self-drive" in url:
            return "tour-detail.html"
        elif "about" in url or "why" in url:
            return "about.html"
        elif "faq" in url:
            return "faq.html"
        elif "team" in url:
            return "team.html"
        elif "contact" in url:
            return "contact.html"
        elif "media" in url or "press" in url:
            return "media.html"
        else:
            return "base.html"
    
    def _get_template_context(self, page: Dict) -> Dict:
        """Build template context for a page."""
        url = page.get("url", "")
        slug = page.get("slug", "")
        
        context = {
            "url": url,
            "slug": slug,
            "title": page.get("title", ""),
            "metaDescription": page.get("metaDescription", ""),
            "canonical": page.get("canonical", url),
            "lang": page.get("lang", "en-IN"),
            "headings": page.get("headings", {}),
            "contentBlocks": page.get("contentBlocks", []),
            "images": page.get("images", []),
            "forms": page.get("forms", []),
            "currentYear": "2024"
        }
        
        # Add breadcrumbs for non-home pages
        if slug != "index":
            context["breadcrumbs"] = self._build_breadcrumbs(page)
        
        # Add tour data if applicable
        tour = self._get_tour_by_url(url)
        if tour:
            context["tour"] = tour
        
        # Add FAQs if FAQ page
        if "faq" in url.lower():
            context["faqs"] = self.entities.get("faqs", [])
        
        # Add team if team page
        if "team" in url.lower():
            context["team"] = self.entities.get("team", [])
        
        # Add contact info if contact page
        if "contact" in url.lower():
            contact_list = self.entities.get("contact", [])
            if contact_list:
                context["contactInfo"] = contact_list[0]
        
        # Add featured tours for homepage
        if slug == "index":
            context["featuredTours"] = self.entities.get("tours", [])[:6]
            context["testimonials"] = self.entities.get("testimonials", [])[:4]
            # Add why us section
            context["whyUs"] = [
                {"title": "Expert Guides", "description": "Experienced local guides who know every route."},
                {"title": "Quality Equipment", "description": "Well-maintained motorcycles and vehicles."},
                {"title": "Small Groups", "description": "Intimate group sizes for better experiences."},
                {"title": "24/7 Support", "description": "Round-the-clock assistance during your journey."}
            ]
        
        return context
    
    def generate_page(self, page: Dict) -> str:
        """Generate HTML for a single page."""
        template_name = self._determine_template(page)
        template = self.env.get_template(template_name)
        
        context = self._get_template_context(page)
        html = template.render(**context)
        
        return html
    
    def _get_output_path(self, page: Dict) -> Path:
        """Determine output file path for a page."""
        slug = page.get("slug", "index")
        url = page.get("url", "")
        
        # All HTML files go to root directory
        if slug == "index" or url.endswith("/") or url.endswith("/index.html"):
            return self.output_dir / "index.html"
        else:
            filename = f"{slug}.html"
            return self.output_dir / filename
    
    def generate_all(self):
        """Generate all pages."""
        pages = self.content.get("pages", [])
        
        print(f"Generating {len(pages)} pages...")
        
        for i, page in enumerate(pages, 1):
            print(f"[{i}/{len(pages)}] Generating: {page.get('slug', 'unknown')}")
            
            try:
                html = self.generate_page(page)
                output_path = self._get_output_path(page)
                
                # Ensure parent directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write file
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(html)
                
            except Exception as e:
                print(f"  Error generating {page.get('slug')}: {e}")
        
        print(f"\nSite generation complete!")
        print(f"  Pages generated: {len(pages)}")
    
    def generate_sitemap_xml(self):
        """Generate sitemap.xml."""
        urls = self.sitemap_data.get("urls", [])
        
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url in urls:
            # Convert to relative path
            parsed = urlparse(url)
            path = parsed.path
            if not path or path == "/":
                path = "/index.html"
            elif not path.endswith(".html"):
                path = path.rstrip("/") + ".html"
            
            sitemap += f'  <url>\n'
            sitemap += f'    <loc>https://www.motorover.in{path}</loc>\n'
            sitemap += f'    <changefreq>monthly</changefreq>\n'
            sitemap += f'    <priority>0.8</priority>\n'
            sitemap += f'  </url>\n'
        
        sitemap += '</urlset>\n'
        
        sitemap_path = self.output_dir / "sitemap.xml"
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(sitemap)
        
        print(f"Generated sitemap.xml with {len(urls)} URLs")
    
    def generate_robots_txt(self):
        """Generate robots.txt."""
        robots = "User-agent: *\n"
        robots += "Allow: /\n"
        robots += "\n"
        robots += "Sitemap: https://www.motorover.in/sitemap.xml\n"
        
        robots_path = self.output_dir / "robots.txt"
        with open(robots_path, "w", encoding="utf-8") as f:
            f.write(robots)
        
        print("Generated robots.txt")


def main():
    """Main entry point."""
    generator = SiteGenerator()
    generator.generate_all()
    generator.generate_sitemap_xml()
    generator.generate_robots_txt()


if __name__ == "__main__":
    main()
