---
name: Remove i18n and templates
overview: Delete the i18n directory, templates directory, and i18n.js file to complete the transition to a fully static website. All HTML files are already generated and don't reference i18n functionality.
todos:
  - id: delete_i18n_dir
    content: Delete the i18n/ directory containing translation JSON files
    status: completed
  - id: delete_templates_dir
    content: Delete the templates/ directory containing all Jinja2 template files
    status: completed
  - id: delete_i18n_js
    content: Delete js/i18n.js file since it depends on i18n directory
    status: completed
---

## Plan: Remove i18n and Templates for Static Site

Since all HTML pages are already generated as static files, we can safely remove the template system and internationalization components.

### Files to Delete

1. **`i18n/` directory** - Contains translation JSON files (`en-IN.json`, `en-US.json`)
2. **`templates/` directory** - Contains 8 Jinja2 template files:

- `base.html`
- `home.html`
- `tour-detail.html`
- `about.html`
- `faq.html`
- `team.html`
- `contact.html`
- `media.html`

3. **`js/i18n.js`** - JavaScript file for internationalization (no longer needed)

### Verification

- ✅ Generated HTML files don't reference `i18n.js` (checked `car-balkan.html` and others)
- ✅ No `data-i18n` attributes found in generated HTML files
- ✅ The `i18n.js` script was conditionally included in templates but not in final HTML

### Notes

- The `scripts/generate_site.py` script will no longer work without templates, but this is fine since all pages are already generated
- Static HTML pages are better for SEO: faster load times, easier crawling, no JavaScript dependency for content
- All existing HTML files in the root directory will remain unchanged

### SEO Benefits of Static Pages

Static HTML pages provide:

- **Faster load times** - No server-side processing
- **Better crawlability** - Search engines can index content immediately
- **No JavaScript dependency** - Content is available without JS execution
- **Lower server costs** - Can be served from CDN
- **Better reliability** - Fewer moving parts means fewer failure points