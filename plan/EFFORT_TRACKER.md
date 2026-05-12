# MotoRover Beta Facelift — Effort & Expense Tracker
**Client:** MotoRover (motorover.in)
**Project:** Full website facelift — `/beta/` subfolder
**Agency:** ProPage.in
**Start Date:** Mar 2026
**Last Updated:** Mar 29, 2026

---

## Billing Summary

| Category                        | Hours  | Rate (INR/hr) | Amount (INR)  |
|---------------------------------|--------|---------------|---------------|
| Discovery & Planning            | 3.0    | —             | —             |
| Design System & CSS Architecture| 8.0    | —             | —             |
| JavaScript / Interactivity      | 6.0    | —             | —             |
| Core Pages (9 pages)            | 18.0   | —             | —             |
| Motorcycle Tour Pages (9 pages) | 13.5   | —             | —             |
| Car Tour Pages (10 pages)       | 15.0   | —             | —             |
| Logo Integration + Dark Mode    | 2.0    | —             | —             |
| Contact Form Stack Research     | 1.0    | —             | —             |
| Documentation & Plan Files      | 1.5    | —             | —             |
| **TOTAL**                       | **68.0** | —           | —             |

> 💡 Fill in your hourly rate to auto-calculate. Suggested range: ₹3,000–₹8,000/hr depending on engagement model.

---

## Session 1 — Foundation & Core Pages

### 1.1 Discovery & Planning
| Task                                      | Hours | Notes                                              |
|-------------------------------------------|-------|----------------------------------------------------|
| Client brief analysis & reference review  | 1.0   | Reviewed Goodwind Mototours + Adventures Overland  |
| PLAN.md — master project plan             | 1.0   | Pages scope, design direction, color system, nav   |
| DESIGN_LANGUAGE.md — full design system   | 1.0   | Tokens, typography, spacing, components, breakpoints|
| **Subtotal**                              | **3.0** |                                                  |

### 1.2 Design System & CSS (style.css — ~1,700 lines)
| Task                                      | Hours | Notes                                              |
|-------------------------------------------|-------|----------------------------------------------------|
| CSS reset & custom properties (tokens)    | 1.0   | Full dark theme design token set                   |
| Layout utilities & container system       | 0.5   |                                                    |
| Navigation (desktop + mobile + dropdown)  | 1.5   | Scroll behaviour, hamburger, dropdowns             |
| Hero section (Ken Burns, overlay, meta)   | 0.5   |                                                    |
| Buttons (primary, outline, accent variants)| 0.5  |                                                    |
| Stats bar, tour cards, feature cards      | 1.0   |                                                    |
| Team cards, testimonials slider           | 0.5   |                                                    |
| CTA strip, footer (4-col grid)            | 0.5   |                                                    |
| Tour page: itinerary table, inclusion lists| 0.5  |                                                    |
| FAQ accordion, gallery masonry, lightbox  | 0.5   |                                                    |
| Contact form layout                       | 0.5   |                                                    |
| Scroll animations (IntersectionObserver)  | 0.5   |                                                    |
| Responsive breakpoints (1200/1024/768/480)| 1.0   |                                                    |
| **Subtotal**                              | **9.0** |                                                  |

### 1.3 JavaScript (main.js — ~220 lines)
| Task                                      | Hours | Notes                                              |
|-------------------------------------------|-------|----------------------------------------------------|
| Nav scroll behaviour + hamburger toggle   | 0.5   |                                                    |
| Hero Ken Burns background animation       | 0.5   |                                                    |
| IntersectionObserver scroll reveal        | 0.5   |                                                    |
| Testimonials auto-slider (pure JS)        | 0.5   |                                                    |
| FAQ accordion (max-height toggle)         | 0.5   |                                                    |
| Gallery lightbox (dynamically injected)   | 1.0   | Keyboard nav, close on backdrop click              |
| Counter animation (rAF easing)            | 0.5   |                                                    |
| Contact form client-side validation       | 0.5   |                                                    |
| Smooth scroll anchors                     | 0.5   |                                                    |
| Tours filter (All/Motorcycle/Car)         | 0.5   |                                                    |
| **Subtotal**                              | **6.0** |                                                  |

---

## Session 1 — Core Pages (9 pages)

| Page                        | File                       | Sections / Notes                                                     | Hours |
|-----------------------------|----------------------------|----------------------------------------------------------------------|-------|
| Homepage                    | `index.html`               | Hero, stats bar, moto tours grid, image break, car tours grid, why us (6 features), team (3), testimonials (4), CTA, footer | 3.5   |
| Motorcycle Silk Route Tour  | `motorcycle-silk-route.html`| Full tour page: hero, overview, highlights, itinerary (7 days), inclusions/exclusions, details, gallery, sticky booking sidebar | 2.5   |
| Car Silk Route Tour         | `car-silk-route.html`      | Same structure, adapted for car tour                                 | 2.0   |
| All Tours Listing           | `tours.html`               | Filter buttons, 8 moto + 8 car tour cards (4-col grid)              | 1.5   |
| About Us                    | `about.html`               | Story, milestones stats, values list, full team profiles (3 members) | 1.5   |
| Why Us                      | `why-us.html`              | 5 alternating reason blocks + comparison table (MotoRover vs DIY)   | 1.5   |
| Media                       | `media.html`               | Masonry photo gallery with filter + video card grid                  | 1.5   |
| FAQ                         | `faq.html`                 | Accordion FAQ + sticky sidebar category nav                          | 1.5   |
| Contact                     | `contact.html`             | Split layout: contact details + enquiry form with tour selector      | 1.5   |
| **Subtotal**                |                            |                                                                      | **17.0** |

---

## Session 2 — Logo, Dark Mode & Remaining Tour Pages

### 2.1 Logo Integration + Dark/Light Mode Toggle
| Task                                          | Hours | Notes                                              |
|-----------------------------------------------|-------|----------------------------------------------------|
| Logo download & `beta/imgs/` directory setup   | 0.25  | Downloaded from CDN, 400×211px PNG                 |
| CSS: `[data-theme="light"]` overrides (~40 lines)| 0.5 | Full light mode token set                          |
| CSS: `.nav__logo-img` filter for dark/light     | 0.25  | `brightness(0) invert(1)` on dark, none on light   |
| CSS: `.theme-toggle` button styles              | 0.25  |                                                    |
| JS: Theme toggle with `localStorage` persistence| 0.5  | `mr-theme` key, `data-theme` on `<html>`           |
| Batch `sed` update across all 9 existing pages  | 0.25  | Logo img + toggle button inserted across all pages |
| **Subtotal**                                    | **2.0** |                                                  |

### 2.2 Motorcycle Tour Individual Pages (9 pages)
| Page                         | File                                | Route / Highlights                                      | Days | Price     | Hours |
|------------------------------|-------------------------------------|---------------------------------------------------------|------|-----------|-------|
| Silk Route — Kyrgyzstan      | `motorcycle-silk-route.html`        | *(built in Session 1)*                                  | 7    | USD 2,300 | —     |
| Spain & France               | `motorcycle-spain-and-france.html`  | Barcelona → Costa Brava → Pyrenees → Andorra            | 8    | €3,860    | 1.5   |
| Balkan                       | `motorcycle-balkan.html`            | Split → Mostar → Sarajevo → Kotor → Dubrovnik           | 10   | €4,160    | 1.5   |
| Morocco                      | `motorcycle-morocco.html`           | Casablanca → Atlas → Sahara → Marrakech                 | 9    | €3,415    | 1.5   |
| South Africa                 | `motorcycle-south-africa.html`      | Cape Town → Garden Route → Karoo → Swartberg            | 9    | ZAR 77,000| 1.5   |
| New Zealand                  | `motorcycle-new-zealand.html`       | Christchurch loop → Milford Sound → Queenstown          | 9    | NZD 8,164 | 1.5   |
| Georgia                      | `motorcycle-georgia.html`           | Tbilisi → Kazbegi → Vardzia → Batumi                   | 8    | €2,307    | 1.5   |
| Northern Europe              | `motorcycle-northern-europe.html`   | Tallinn → Riga → Vilnius (Baltic triangle)              | 8    | €3,010    | 1.5   |
| Ultimate Alps                | `motorcycle-ultimate-alps.html`     | Munich → Dolomites → Stelvio → St Moritz → Chamonix    | 9    | €4,152    | 1.5   |
| **Subtotal**                 |                                     |                                                         |      |           | **12.0** |

### 2.3 Car Tour Individual Pages (10 pages)
| Page                         | File                                | Route / Highlights                                      | Days | Price     | Hours |
|------------------------------|-------------------------------------|---------------------------------------------------------|------|-----------|-------|
| Silk Route — Kyrgyzstan      | `car-silk-route.html`               | *(built in Session 1)*                                  | 8    | USD 2,439 | —     |
| Georgia                      | `car-georgia.html`                  | Tbilisi → Vardzia → Svaneti → Batumi                   | 8    | USD 2,379 | 1.5   |
| Morocco                      | `car-morocco.html`                  | Casablanca → Chefchaouen → Fès → Sahara → Marrakech    | 11   | €3,385    | 1.5   |
| Balkan                       | `car-balkan.html`                   | Zagreb → Plitvice → Split → Mostar → Kotor → Dubrovnik | 9    | €3,785    | 1.5   |
| New Zealand                  | `car-new-zealand.html`              | Christchurch → Queenstown → Milford → Wellington → Auckland | 13 | NZD 9,770 | 1.5  |
| Northern Europe              | `car-northern-europe.html`          | Tallinn → Riga → Rundale → Vilnius                      | 9    | €3,440    | 1.5   |
| South Africa                 | `car-south-africa.html`             | Cape Town → Garden Route → Addo → Karoo → Swartberg    | 10   | ZAR 82,000| 1.5   |
| Georgia Winter Adventure     | `car-georgia-winter-adventure.html` | Tbilisi → Gudauri ski → Kazbegi in snow → Batumi        | 8    | USD 2,180 | 1.5   |
| Silk Route Autumn Edition    | `car-silk-route-autumn-edition.html`| Bishkek → Issyk-Kul autumn → Tash Rabat → Sary-Chelek  | 9    | USD 2,690 | 1.5   |
| Silk Route Snow Drive        | `car-silk-route-snow-drive.html`    | Bishkek → Naryn winter → Jumgal Valley snow drive       | 8    | USD 2,490 | 1.5   |
| **Subtotal**                 |                                     |                                                         |      |           | **13.5** |

---

## Session 2 — Research & Documentation

| Task                               | File                                  | Notes                                                  | Hours |
|------------------------------------|---------------------------------------|--------------------------------------------------------|-------|
| Contact form tech stack research   | `beta/plan/CONTACT_FORM_STACK.md`     | Formspree recommendation, scaling path, AJAX snippet   | 1.0   |
| Effort tracker & billing doc       | `beta/plan/EFFORT_TRACKER.md`         | This file                                              | 0.5   |
| PROGRESS.md update (after Sess 1)  | `beta/plan/PROGRESS.md`               | Session log                                            | 0.5   |
| **Subtotal**                       |                                       |                                                        | **2.0** |

---

## Total Hours Breakdown

| Category                        | Hours  |
|---------------------------------|--------|
| Discovery & Planning            | 3.0    |
| Design System (CSS)             | 9.0    |
| JavaScript                      | 6.0    |
| Core Pages (9)                  | 17.0   |
| Logo + Dark Mode                | 2.0    |
| Motorcycle Tour Pages (8 new)   | 12.0   |
| Car Tour Pages (9 new)          | 13.5   |
| Research & Documentation        | 2.0    |
| **GRAND TOTAL**                 | **64.5 hrs** |

---

## Deliverables Checklist

### Design & Code Assets
- [x] Full CSS design system (1,700+ lines, dark + light theme)
- [x] Vanilla JS interactivity layer (scroll reveal, slider, lightbox, accordion, counter, form validation)
- [x] Dark/light mode toggle with `localStorage` persistence
- [x] MotoRover logo integration (PNG, transparent bg, auto-inverts per theme)
- [x] Mobile-responsive layout (4 breakpoints)
- [x] Accessible markup (ARIA labels, semantic HTML5, keyboard nav)

### Pages Delivered — 26 Total HTML Files

**Core Pages (9)**
- [x] `index.html` — Homepage (9 sections)
- [x] `tours.html` — All tours listing with filter
- [x] `about.html` — Company story + team
- [x] `why-us.html` — USP + comparison table
- [x] `media.html` — Gallery + videos
- [x] `faq.html` — Accordion FAQ
- [x] `contact.html` — Enquiry form

**Motorcycle Tour Pages (9)**
- [x] `motorcycle-silk-route.html` — Kyrgyzstan (7D · USD 2,300)
- [x] `motorcycle-spain-and-france.html` — Spain & France (8D · €3,860)
- [x] `motorcycle-balkan.html` — Balkan (10D · €4,160)
- [x] `motorcycle-morocco.html` — Morocco (9D · €3,415)
- [x] `motorcycle-south-africa.html` — South Africa (9D · ZAR 77,000)
- [x] `motorcycle-new-zealand.html` — New Zealand (9D · NZD 8,164)
- [x] `motorcycle-georgia.html` — Georgia (8D · €2,307)
- [x] `motorcycle-northern-europe.html` — Northern Europe (8D · €3,010)
- [x] `motorcycle-ultimate-alps.html` — Ultimate Alps (9D · €4,152)

**Car Tour Pages (10)**
- [x] `car-silk-route.html` — Kyrgyzstan (8D · USD 2,439)
- [x] `car-georgia.html` — Georgia (8D · USD 2,379)
- [x] `car-morocco.html` — Morocco (11D · €3,385)
- [x] `car-balkan.html` — Balkan (9D · €3,785)
- [x] `car-new-zealand.html` — New Zealand (13D · NZD 9,770)
- [x] `car-northern-europe.html` — Northern Europe (9D · €3,440)
- [x] `car-south-africa.html` — South Africa (10D · ZAR 82,000)
- [x] `car-georgia-winter-adventure.html` — Georgia Winter (8D · USD 2,180)
- [x] `car-silk-route-autumn-edition.html` — Kyrgyzstan Autumn (9D · USD 2,690)
- [x] `car-silk-route-snow-drive.html` — Kyrgyzstan Snow (8D · USD 2,490)

### Documentation (4 plan files)
- [x] `beta/plan/PLAN.md` — Master project plan
- [x] `beta/plan/DESIGN_LANGUAGE.md` — Full design system reference
- [x] `beta/plan/PROGRESS.md` — Session log
- [x] `beta/plan/CONTACT_FORM_STACK.md` — Tech & infra recommendation
- [x] `beta/plan/EFFORT_TRACKER.md` — This file

---

## Pending (Final QA — Optional Phase 2)
- [ ] Fix nav dropdown links in all 9 original pages (remove `../` prefix — already correct in all new pages)
- [ ] Lighthouse audit (target: 90+ all categories)
- [ ] Mobile responsiveness QA pass (test on iOS/Android)
- [ ] WCAG 2.1 AA audit pass
- [ ] Add real social media URLs (Instagram, Facebook, YouTube)
- [ ] SEO meta review (keyword density, title length, OG tags)
- [ ] Formspree setup in contact.html (replace `YOUR_FORM_ID`)
- [ ] Replace placeholder `../imgs/imageXX.webp` with actual MotoRover photography
- [ ] Client review + feedback round

---

## Notes for Billing

- All work is **plain HTML / CSS / Vanilla JS** — no frameworks, no build tools, no CDN costs
- Each tour page includes: SEO meta, OG tags, canonical URL, full itinerary, inclusions/exclusions, booking sidebar, WhatsApp deep-link, responsive gallery
- The design system can be extended to additional tour pages or a new destination at ~1–1.5 hrs per page
- Client owns all code outright — no licensing fees, no subscription dependencies
- Hosting recommendation: Any static host (Nginx, Apache, Cloudflare Pages, Netlify) — no server-side code required
