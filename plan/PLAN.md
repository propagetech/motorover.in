# MotoRover.in — Beta Facelift Plan
**Agency:** ProPage.in
**Project Start:** 2026-03-29
**Status:** In Progress

---

## Project Brief

MotoRover.in is a 12-year-old adventure travel website offering international motorcycle tours and self-drive car road trips. The client wants a complete visual facelift while preserving all existing content, routes, and brand identity.

### Client Reference Websites
1. **Goodwind Mototours** — www.goodwindmototours.com
   *What we take:* Energetic typography, strong CTAs, tour card grid, feature highlights*
2. **Adventures Overland** — www.adventuresoverland.com
   *What we take:* Dark cinematic aesthetic, luxury feel, full-screen hero, stats section*

### Our Recent Work (Benchmark)
- **Law Park Educational Trust** — journey.lawparkeducationaltrust.org
  *What we apply:* Gold accent restraint, fluid typography (clamp), warm section separators, serif + sans pairing*

---

## Tech Stack
- **Strictly:** Plain HTML5, CSS3, Vanilla JavaScript only
- No frameworks, no build tools, no npm
- All assets reference `../imgs/` and `../assets/` (existing site files)
- Google Fonts via CDN (Playfair Display + Inter)
- Font Awesome 6 via CDN (icons)

---

## Pages Scope

| # | Page | File | Status |
|---|------|------|--------|
| 1 | Homepage | `index.html` | Pending |
| 2 | Motorcycle Tour — Silk Route Kyrgyzstan | `motorcycle-silk-route.html` | Pending |
| 3 | Car Tour — Silk Route Kyrgyzstan | `car-silk-route.html` | Pending |
| 4 | All Tours Listing | `tours.html` | Pending |
| 5 | About & Team | `about.html` | Pending |
| 6 | Why Us | `why-us.html` | Pending |
| 7 | Media Gallery | `media.html` | Pending |
| 8 | FAQ | `faq.html` | Pending |
| 9 | Contact | `contact.html` | Pending |

---

## Design Direction

### Aesthetic: Dark Cinematic Adventure
- Full-screen heroes with overlay gradients
- Warm orange accent (`#E05A00`) — fire, adventure, energy
- Near-black backgrounds (`#080808`) with subtle surface layers
- Serif display headlines (Playfair Display) + clean body (Inter)
- Generous whitespace, grid-based layouts
- Smooth hover/transition animations

### Color System
```
--bg:          #080808   (page background)
--surface:     #111111   (cards, sections)
--surface-2:   #1A1A1A   (elevated elements)
--border:      #242424   (subtle dividers)
--accent:      #E05A00   (primary orange)
--accent-light:#FF7A20   (hover/glow state)
--text:        #F0EDE8   (primary text)
--text-muted:  #888880   (secondary text)
--white:       #FFFFFF
```

### Typography
- **Display:** Playfair Display — hero titles, section headers
- **Body:** Inter — nav, body copy, labels, CTAs
- **Scale:** Fluid using `clamp()` for all major sizes

### Layout Principles
1. Max container: 1200px centered
2. Section padding: 80px–120px vertical
3. Grid: 12-column flex/grid system
4. Hero: 100vh full-bleed with image/overlay
5. Cards: Subtle border + hover lift + accent detail

---

## Navigation Structure

```
Logo [MotoRover]          [Motorcycle Tours] [Car Tours] [About] [Media] [FAQ]  [WhatsApp CTA]
```

- Transparent on hero, dark on scroll
- Dropdown for tour categories
- Sticky mobile hamburger menu

---

## Key Sections (Homepage)

1. **Hero** — Full viewport, dramatic headline, dual CTAs
2. **Stats Bar** — 15+ years, 50+ tours, 1000+ travellers, 30+ countries
3. **Motorcycle Tours Grid** — Featured upcoming tours
4. **Car Tours Grid** — Featured upcoming tours
5. **Why MotoRover** — 6 value props with icons
6. **The Team** — 3 team member cards
7. **Testimonials** — Carousel of customer quotes
8. **Newsletter + Social** — CTA strip
9. **Footer** — Full links, contact, social

---

## ProPage.in Quality Gates
- [ ] Lighthouse Performance 90+
- [ ] Lighthouse SEO 90+
- [ ] Lighthouse Accessibility 90+
- [ ] WCAG 2.1 AA compliance
- [ ] All images have alt attributes
- [ ] Semantic HTML5 elements
- [ ] Open Graph meta tags
- [ ] Canonical URLs
- [ ] Mobile-first responsive
- [ ] No console errors

---

## Prompting Strategy

Each page follows this build sequence:
1. Research existing content (WebFetch)
2. Define section structure
3. Write HTML semantics-first
4. Write CSS with design tokens
5. Add JavaScript interactions
6. Review against quality gates

All sessions documented in `PROGRESS.md`.
