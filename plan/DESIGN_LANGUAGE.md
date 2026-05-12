# MotoRover Beta — Design Language
**By ProPage.in | 2026-03-29**

---

## Philosophy

> "Remove everything unnecessary. What remains must be perfect." — ProPage.in Mantra

We apply first-principles thinking to every design decision. Every color, every shadow, every spacing unit must earn its place.

---

## Color Tokens

```css
/* === BACKGROUNDS === */
--color-bg:          #080808;   /* Page background — near black */
--color-surface:     #111111;   /* Card/section backgrounds */
--color-surface-2:   #1A1A1A;   /* Elevated: modals, dropdowns */
--color-border:      #242424;   /* Subtle dividers */
--color-border-2:    #333333;   /* Visible dividers */

/* === ACCENT === */
--color-accent:      #E05A00;   /* Primary orange — adventure/fire */
--color-accent-light:#FF7A20;   /* Hover state / glow */
--color-accent-dim:  rgba(224, 90, 0, 0.12);  /* Accent background wash */

/* === TEXT === */
--color-text:        #F0EDE8;   /* Primary text (warm off-white) */
--color-text-muted:  #888880;   /* Secondary/caption text */
--color-text-faint:  #555550;   /* Placeholder / disabled */

/* === FIXED === */
--color-white:       #FFFFFF;
--color-black:       #000000;
```

---

## Typography

### Font Families
```css
--font-display: 'Playfair Display', Georgia, serif;   /* Headlines */
--font-body:    'Inter', system-ui, sans-serif;       /* Body/UI */
```

### Type Scale (fluid with clamp)
```css
--text-xs:   clamp(0.7rem,  1vw,   0.75rem);
--text-sm:   clamp(0.8rem,  1.2vw, 0.875rem);
--text-base: clamp(0.9rem,  1.4vw, 1rem);
--text-lg:   clamp(1rem,    1.6vw, 1.125rem);
--text-xl:   clamp(1.125rem,2vw,   1.25rem);
--text-2xl:  clamp(1.25rem, 2.5vw, 1.5rem);
--text-3xl:  clamp(1.5rem,  3vw,   2rem);
--text-4xl:  clamp(2rem,    4vw,   2.75rem);
--text-5xl:  clamp(2.5rem,  5vw,   3.5rem);
--text-hero: clamp(3rem,    7vw,   5.5rem);
```

### Font Weights
- Display headings: `700` (bold) or `800` (extrabold)
- Section headings: `600`
- Body: `400`
- Labels/caps: `500`
- UI buttons: `600`

---

## Spacing System

Base unit: `8px`

```css
--space-1:  8px;
--space-2:  16px;
--space-3:  24px;
--space-4:  32px;
--space-5:  40px;
--space-6:  48px;
--space-8:  64px;
--space-10: 80px;
--space-12: 96px;
--space-16: 128px;
--space-20: 160px;
```

---

## Layout

```css
--container-max: 1200px;
--container-padding: clamp(1rem, 5vw, 2rem);
--section-padding: clamp(60px, 10vw, 120px);
--border-radius-sm: 4px;
--border-radius: 8px;
--border-radius-lg: 16px;
--border-radius-xl: 24px;
--border-radius-pill: 9999px;
```

---

## Shadows & Depth

```css
--shadow-sm:  0 1px 3px rgba(0,0,0,0.4);
--shadow:     0 4px 16px rgba(0,0,0,0.5);
--shadow-lg:  0 8px 32px rgba(0,0,0,0.6);
--shadow-accent: 0 0 24px rgba(224, 90, 0, 0.25);
```

---

## Transitions

```css
--transition-fast:   150ms ease;
--transition:        250ms ease;
--transition-slow:   400ms ease;
--transition-spring: 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
```

---

## Component Patterns

### Navigation
- Height: 72px desktop, 60px mobile
- Transparent on hero scroll-top
- `--color-surface` + blur on scroll
- Logo: left, nav links: center/right, CTA button: far right

### Buttons
```
Primary:   bg accent, text white, border-radius pill, px 28 py 14, fw 600
Secondary: border 1px accent, text accent, transparent bg
Ghost:     text white, no border, underline on hover
```

### Tour Cards
- Background: `--color-surface`
- Border: `1px solid --color-border`
- Hover: `translateY(-4px)` + `--shadow-lg` + accent border-top
- Image: 240px height, object-fit cover
- Tag: accent bg pill label (dates / destination)

### Section Headers
- Eyebrow: `--text-sm`, uppercase, letter-spacing 0.12em, accent color
- Headline: `--font-display`, `--text-4xl`, text-primary
- Subtext: `--text-lg`, `--color-text-muted`, max-width 580px

---

## Motion

- Page load: opacity fade-in `0 → 1` over 600ms
- Sections: `IntersectionObserver` — fade + translateY(30px → 0)
- Nav: smooth scroll behavior
- Cards: hover lift + shadow transition
- Hero text: stagger reveal with delay

---

## Iconography

- Library: Font Awesome 6 Free (CDN)
- Style: `fa-solid` or `fa-regular`
- Size in text: `1em` (inherits)
- Standalone: 24px–48px
- Accent icons: wrapped in 48x48 circle with `--color-accent-dim` bg

---

## Images

All images reference parent directory: `../imgs/image-N.webp`
- Hero: full-bleed, `object-fit: cover`, overlay `linear-gradient`
- Cards: aspect-ratio `4/3`, `object-fit: cover`
- Team: aspect-ratio `1/1`, `border-radius` 50% or lg

---

## Responsive Breakpoints

```css
/* Mobile first */
@media (min-width: 480px)  { /* sm */ }
@media (min-width: 768px)  { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```
