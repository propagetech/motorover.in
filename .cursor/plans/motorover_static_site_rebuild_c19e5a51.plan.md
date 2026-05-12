---
name: MotoRover Static Site Rebuild
overview: Scrape all content from motorover.in, normalize into JSON content model, and rebuild as pure static HTML/CSS/JS site achieving Lighthouse 100s across all categories with a minimal LoveFrom/Jony Ive aesthetic.
todos:
  - id: setup_scraping
    content: Create Python scraping infrastructure (scripts/scraper.py) with BeautifulSoup4 and Selenium/Playwright for JS rendering
    status: completed
  - id: scrape_content
    content: Scrape all pages from motorover.in, extract content, forms, images, metadata, and build sitemap
    status: completed
    dependencies:
      - setup_scraping
  - id: normalize_data
    content: Create JSON content model (content.json, entities.json, assets.json, sitemap.json) with normalized tour, team, FAQ, testimonial data
    status: completed
    dependencies:
      - scrape_content
  - id: download_images
    content: Download all images, optimize with Pillow (WebP/AVIF), generate responsive srcset data, store in assets/img/
    status: completed
    dependencies:
      - normalize_data
  - id: design_system
    content: Create CSS design system (css/styles.css) with variables, base styles, components, utilities, and light/dark theme support
    status: completed
  - id: create_templates
    content: Design HTML templates (base, home, tour-detail, about, FAQ, team, contact, media) with semantic structure
    status: completed
    dependencies:
      - design_system
  - id: generate_pages
    content: Create Python script (scripts/generate_site.py) to generate static HTML pages from JSON content using templates
    status: completed
    dependencies:
      - create_templates
      - normalize_data
  - id: implement_js
    content: Create minimal JavaScript (main.js, theme.js, i18n.js) for nav toggle, theme switching, i18n, and progressive enhancements
    status: completed
  - id: seo_structured_data
    content: Implement SEO meta tags, OpenGraph, Twitter cards, and JSON-LD structured data (Organization, BreadcrumbList, FAQPage, TouristTrip, Person)
    status: completed
    dependencies:
      - generate_pages
  - id: accessibility_pass
    content: Ensure semantic HTML, proper labels, keyboard navigation, focus states, ARIA attributes, color contrast, and reduced motion support
    status: completed
    dependencies:
      - generate_pages
      - implement_js
  - id: performance_optimization
    content: Optimize images, inline critical CSS, lazy load images, minimize JS, ensure zero CLS, achieve Lighthouse 100 performance
    status: completed
    dependencies:
      - download_images
      - generate_pages
  - id: i18n_implementation
    content: Create translation files (i18n/en-IN.json, en-US.json) and implement i18n.js for locale switching
    status: completed
    dependencies:
      - generate_pages
  - id: generate_sitemap_robots
    content: Generate sitemap.xml and robots.txt from scraped URL data
    status: completed
    dependencies:
      - normalize_data
  - id: qa_testing
    content: Run HTML validation, Lighthouse audits (target 100/100/100/100), browser testing, link checking, and accessibility audit
    status: completed
    dependencies:
      - accessibility_pass
      - performance_optimization
      - seo_structured_data
  - id: documentation
    content: Create README.md with local serving instructions, Lighthouse testing steps, image optimization notes, and URL redirects map
    status: completed
    dependencies:
      - qa_testing
---

# MotoRover Static Site Rebuild - Complete Implementation Plan

## Phase 1: Scraping & Content Extraction

### 1.1 Python Scraping Infrastructure

Create `scripts/scraper.py` using:

- `requests` + `BeautifulSoup4` for HTML parsing
- `selenium` or `playwright` for JavaScript-rendered content if needed
- `urllib.parse` for URL normalization
- Respect `robots.txt` and rate limiting

**Scraping Strategy:**

- Start from `https://www.motorover.in/`
- Extract all internal links (same domain only)
- Build URL queue with deduplication
- Crawl breadth-first, respecting depth limits
- Extract per-page data according to schema below

### 1.2 Content Schema Design

Create JSON schemas in `content/schemas/`:

**`content.json` structure:**

```json
{
  "pages": [
    {
      "url": "https://www.motorover.in/",
      "slug": "index",
      "title": "...",
      "metaDescription": "...",
      "canonical": "...",
      "lang": "en-IN",
      "headings": {"h1": [...], "h2": [...], ...},
      "contentBlocks": [
        {"type": "hero", "content": {...}},
        {"type": "text", "content": {...}},
        {"type": "itinerary-day", "content": {...}}
      ],
      "images": [...],
      "forms": [...],
      "internalLinks": [...],
      "structuredDataHints": [...]
    }
  ]
}
```

**`entities.json` structure:**

- `tours[]` - normalized tour data
- `team[]` - team member profiles
- `faqs[]` - FAQ entries
- `testimonials[]` - customer testimonials
- `payments[]` - payment information
- `contact[]` - contact details

**`assets.json` structure:**

- Image references with metadata
- Download locations
- Usage mapping (which pages use which assets)

**`sitemap.json` structure:**

- Complete URL list
- URL hierarchy
- Redirect mappings

### 1.3 Image Download & Optimization

Create `scripts/download_images.py`:

- Download all referenced images
- Use `Pillow` + `pillow-simd` or `sharp` (via subprocess) for optimization
- Generate WebP/AVIF versions with fallbacks
- Store in `assets/img/` with organized naming
- Update JSON to reference local paths
- Generate responsive srcset data

## Phase 2: Information Architecture & Templates

### 2.1 Route Analysis

Analyze scraped `sitemap.json` to:

- Identify all page types
- Map URL patterns to templates
- Create `redirects.json` if URLs change
- Preserve SEO-friendly URLs where possible

### 2.2 Template Design

Define template structure:

- `templates/base.html` - Base layout with header/nav/footer
- `templates/home.html` - Homepage template
- `templates/tour-detail.html` - Tour pages (motorcycle/car)
- `templates/about.html` - About/Why Us pages
- `templates/faq.html` - FAQ pages
- `templates/team.html` - Team pages
- `templates/contact.html` - Contact pages
- `templates/media.html` - Media/Press pages

## Phase 3: Design System Implementation

### 3.1 CSS Architecture

Create `css/styles.css` with sections:

1. **CSS Variables** (`:root` for light/dark themes)
2. **Base/Reset** (minimal normalize, system font stack)
3. **Layout** (grid, flexbox utilities)
4. **Components** (BEM-style: `.card`, `.card__title`, `.card--featured`)
5. **Utilities** (minimal, consistent)
6. **Theme** (light/dark mode variables)

**Design Tokens:**

- Typography: system font stack, generous line-height, clear hierarchy
- Spacing: consistent scale (4px base unit)
- Colors: minimal palette, high contrast
- Motion: subtle transitions, respect `prefers-reduced-motion`

### 3.2 Component Library

Build reusable components:

- Buttons (primary, secondary, text)
- Cards (tour cards, testimonial cards)
- Itinerary timeline
- FAQ accordion (using `<details>` with JS enhancement)
- Gallery grid
- Form inputs (with proper labels)
- Navigation (mobile-friendly, keyboard accessible)

## Phase 4: Static Site Generation

### 4.1 HTML Generation Script

Create `scripts/generate_site.py`:

- Read `content/content.json` and `content/entities.json`
- Apply templates to generate static HTML files
- Inject JSON-LD structured data
- Generate `sitemap.xml` and `robots.txt`
- Create redirect pages if needed

### 4.2 Page Implementation

Generate all pages:

- `/index.html` - Homepage
- `/tours/*.html` - Individual tour pages
- `/about/*.html` - About/Why Us pages
- `/contact.html` - Contact page
- `/faq.html` - FAQ page
- `/team.html` - Team page
- `/media.html` - Media page

Each page includes:

- Semantic HTML5 structure
- Unique `<title>` and meta description
- OpenGraph + Twitter cards
- Canonical URL
- JSON-LD structured data
- Proper heading hierarchy (one H1)
- Breadcrumbs for deep pages

## Phase 5: JavaScript Enhancements

### 5.1 Core JavaScript Files

Create minimal JS files:

**`js/main.js`:**

- Mobile navigation toggle
- FAQ accordion enhancement (if not using native `<details>`)
- Lightbox for galleries (if needed)
- Progressive enhancement patterns

**`js/theme.js`:**

- Theme toggle functionality
- `localStorage` persistence
- Respect `prefers-color-scheme`
- Update CSS variables

**`js/i18n.js`:**

- Translation loading
- Text swapping for `data-i18n` attributes
- Locale persistence
- `<html lang>` updates

### 5.2 Performance Optimization

- Lazy load images with `loading="lazy"`
- Defer non-critical JS
- Inline critical CSS for above-the-fold
- Minimize JS bundle size

## Phase 6: SEO & Structured Data

### 6.1 Meta Tags

Every page includes:

- Unique `<title>` (50-60 chars)
- Meta description (150-160 chars)
- Canonical URL
- OpenGraph tags (og:title, og:description, og:image, og:url)
- Twitter Card tags
- Language declaration

### 6.2 JSON-LD Structured Data

Implement schema.org types:

- `Organization` + `WebSite` (homepage)
- `BreadcrumbList` (all pages with depth > 1)
- `FAQPage` (FAQ pages)
- `TouristTrip` or `Product`/`Offer` (tour pages)
- `Person` (team pages)
- `Article` (if blog/media content exists)

### 6.3 Sitemap & Robots

- Generate `sitemap.xml` from scraped URLs
- Create `robots.txt` with proper directives
- Ensure all pages are discoverable

## Phase 7: Accessibility Implementation

### 7.1 Semantic HTML

- Use proper landmarks (`<header>`, `<nav>`, `<main>`, `<footer>`)
- Skip-to-content link
- Proper heading hierarchy
- List structures for navigation

### 7.2 Form Accessibility

- All inputs have `<label>` elements
- No placeholder-only labels
- Required field indicators
- Error message associations
- Keyboard navigation support

### 7.3 Interactive Elements

- Focus states clearly visible (2px+ outline)
- Keyboard navigable menus
- ARIA attributes only when needed
- Native HTML5 elements preferred

### 7.4 Visual Accessibility

- Color contrast AA/AAA compliant
- No color-only information
- Respect `prefers-reduced-motion`
- Scalable text (no fixed px for body)

## Phase 8: Performance Optimization

### 8.1 Image Optimization

- All images optimized (WebP/AVIF with fallbacks)
- Responsive images with `srcset` and `sizes`
- Explicit `width` and `height` to prevent CLS
- Lazy loading for below-fold images
- Proper aspect ratios maintained

### 8.2 CSS Optimization

- Inline critical CSS (above-the-fold)
- Single small CSS file for rest (or split if needed)
- No unused CSS
- Use CSS variables efficiently
- Minimize specificity

### 8.3 JavaScript Optimization

- Minimal JS (only enhancements)
- Defer non-critical scripts
- No third-party trackers
- Efficient event delegation

### 8.4 Caching & Headers

- Document cache headers for static hosting
- Proper `Cache-Control` directives
- `manifest.webmanifest` if beneficial

## Phase 9: i18n Implementation

### 9.1 Translation Files

Create `i18n/en-IN.json` (default) and `i18n/en-US.json` (stub):

- All translatable strings
- Organized by page/section
- Include placeholders for dynamic content

### 9.2 i18n JavaScript

- Load translation files
- Swap text for `data-i18n` attributes
- Update `<html lang>` attribute
- Persist preference in `localStorage`

## Phase 10: Quality Assurance

### 10.1 Validation Checklist

- [ ] HTML validation (W3C validator)
- [ ] All images have alt text (or empty alt for decorative)
- [ ] No console errors
- [ ] All internal links work
- [ ] Forms are accessible and functional
- [ ] Sitemap and robots.txt correct
- [ ] Mobile responsive (test on multiple devices)

### 10.2 Lighthouse Audit

Run Lighthouse for each page type:

- Performance: 100
- Accessibility: 100
- Best Practices: 100
- SEO: 100

Document exact steps to reproduce scores.

### 10.3 Browser Testing

Test in:

- Chrome (latest)
- Safari (latest)
- Firefox (latest)
- Edge (latest)
- Graceful degradation for older browsers

## File Structure

```
motorover.in/
├── index.html
├── robots.txt
├── sitemap.xml
├── manifest.webmanifest (optional)
├── redirects.json (if needed)
├── assets/
│   ├── img/ (optimized images)
│   └── icons/ (SVG icons)
├── css/
│   └── styles.css
├── js/
│   ├── main.js
│   ├── theme.js
│   └── i18n.js
├── content/
│   ├── sitemap.json
│   ├── content.json
│   ├── entities.json
│   ├── assets.json
│   └── schemas/ (JSON schemas)
├── tours/ (static tour pages)
├── about/ (about pages)
├── contact.html
├── faq.html
├── team.html
├── media.html
├── i18n/
│   ├── en-IN.json
│   └── en-US.json
├── scripts/
│   ├── scraper.py
│   ├── download_images.py
│   └── generate_site.py
└── README.md
```

## Implementation Notes

1. **Scraping**: Use Python with BeautifulSoup4 + Selenium/Playwright for JS-heavy pages. Respect rate limits and robots.txt.

2. **Image Handling**: Download all images, optimize with Pillow, generate WebP/AVIF versions, store locally in organized structure.

3. **Templates**: Use Python Jinja2 or simple string templating to generate HTML from JSON content.

4. **Performance**: Inline critical CSS, lazy load images, minimize JS, use system fonts, optimize all assets.

5. **Accessibility**: Semantic HTML, proper labels, keyboard navigation, focus states, ARIA only when needed.

6. **SEO**: Unique titles/descriptions, structured data, sitemap, robots.txt, proper heading hierarchy.

7. **Design**: Minimal, premium aesthetic with generous whitespace, clear typography, subtle motion.