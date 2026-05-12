---
name: Adopt Airbnb Design Principles (Static Site)
overview: Enhance MotoRover's static homepage by adopting Airbnb's visual design principles, including image-heavy cards, horizontal carousels, enhanced hero section, social proof elements, and improved visual hierarchy. All interactions will use "Learn More" CTAs since this is a static site without search functionality.
todos:
  - id: enhance-hero
    content: Enhance hero section visually (no search) with better imagery and CTAs
    status: completed
  - id: image-cards
    content: Transform cards to image-heavy design with overlays, badges, and ratings
    status: completed
  - id: carousel
    content: Implement horizontal scrolling carousel for featured tours section
    status: completed
  - id: social-proof
    content: Add social proof elements (ratings, badges, reviews)
    status: completed
  - id: header-enhance
    content: Enhance header design visually (no search functionality)
    status: completed
  - id: pricing-display
    content: Add transparent pricing information to tour cards
    status: completed
  - id: hover-effects
    content: Enhance card hover states and interactions
    status: completed
  - id: visual-hierarchy
    content: Improve section hierarchy and spacing throughout the page
    status: completed
  - id: see-all-links
    content: Add 'See all tours' navigation links to sections
    status: completed
---

# Adopt Airbnb Design Principles for MotoRover Homepage (Static Site)

## Analysis Summary

After analyzing Airbnb's homepage design, here are the key **visual design principles** that can enhance MotoRover's user experience. Since MotoRover is a static site without search functionality, we'll focus on visual improvements and "Learn More" CTAs.

### Key Airbnb Design Principles to Adopt:

1. **Visual-First Card Design**: High-quality images as primary visual element with overlays for badges and actions
2. **Horizontal Scrolling Carousels**: For featured content sections with navigation arrows
3. **Enhanced Hero Section**: More visually engaging hero with clear value proposition and prominent CTAs
4. **Social Proof Elements**: Ratings, badges ("Guest favourite"), and transparent pricing
5. **Clear Section Hierarchy**: Section headings with navigation indicators and clear visual separation
6. **Card Interactions**: Wishlist/favorite icons, hover effects, and clear pricing display
7. **Transparent Information**: Clear pricing with "all fees included" messaging
8. **Content Organization**: Section-based layout with clear categorization

## Implementation Plan

### 1. Enhance Hero Section (`index.html` + `css/styles.css`)

**Current State**: Simple text-centered hero with two buttons

**Airbnb-Inspired Improvements**:

- Make hero more visually engaging with background imagery or gradient
- Larger, more prominent headline and value proposition
- Better visual hierarchy with subtitle and CTAs
- Add visual interest without search interface (focus on "Explore Tours" and "Contact Us" buttons)
- Consider adding a hero image or background pattern

**Files to Modify**:

- `index.html` (lines 97-106): Enhance hero section structure
- `css/styles.css`: Add hero visual enhancements

### 2. Transform Cards to Image-Heavy Design (`index.html` + `css/styles.css`)

**Current State**: Text-only cards with minimal visual appeal

**Airbnb-Inspired Improvements**:

- Add high-quality tour images to each card (from `/assets/` directory)
- Implement image-first card layout (image on top, content below)
- Add overlay badges (e.g., "Featured Tour", "Popular", "New")
- Include wishlist/favorite icon in top-right corner of images (visual only, can link to contact)
- Add rating display (stars + number) if available
- Show pricing information prominently (if available)
- Improve hover states with image zoom effects
- Make "Learn More" buttons more prominent

**Files to Modify**:

- `index.html` (lines 114-156): Update card structure with images
- `css/styles.css` (lines 541-568): Enhance card styles for image-heavy design

### 3. Implement Horizontal Scrolling Carousels (`index.html` + `css/styles.css` + `js/main.js`)

**Current State**: Static grid layout

**Airbnb-Inspired Improvements**:

- Convert "Featured Tours" section to horizontal scrolling carousel
- Add navigation arrows (left/right) for carousel control
- Add section heading with "See all" link pointing to `/tours.html`
- Implement smooth scrolling behavior
- Add touch/swipe support for mobile
- Show 3-4 cards at a time on desktop, 1-2 on mobile

**Files to Modify**:

- `index.html` (lines 109-158): Restructure featured tours as carousel
- `css/styles.css`: Add carousel container and navigation styles
- `js/main.js`: Add carousel functionality (check if exists, add if needed)

### 4. Add Social Proof Elements (`index.html` + `css/styles.css`)

**Current State**: No ratings, badges, or social proof

**Airbnb-Inspired Improvements**:

- Add star ratings to tour cards (if review data exists, otherwise use placeholder)
- Include badges like "Popular", "Featured", "New", "Best Seller"
- Add testimonial snippets or review counts if available
- Show trust indicators like "Guest favourite" or "Highly Rated"

**Files to Modify**:

- `index.html`: Add rating and badge elements to cards
- `css/styles.css`: Style badges and rating displays

### 5. Enhance Header Design (`index.html` + `css/styles.css`)

**Current State**: Simple header with logo, nav, and theme toggle

**Airbnb-Inspired Improvements**:

- Keep header clean but make it more visually appealing
- Add subtle background or border effects
- Improve navigation link styling
- Consider adding a "Book Now" or "Contact" CTA button in header
- Maintain sticky header behavior

**Files to Modify**:

- `index.html` (lines 62-93): Enhance header structure (no search, just visual improvements)
- `css/styles.css` (lines 333-450): Update header styles

### 6. Improve Visual Hierarchy and Spacing (`css/styles.css`)

**Current State**: Good spacing but could be more section-focused

**Airbnb-Inspired Improvements**:

- Add clear section separators or background variations
- Improve section heading styles with better typography
- Add "See all" or "View all tours" links to section headings
- Better use of white space between sections
- Add section numbers or icons for visual interest

**Files to Modify**:

- `css/styles.css`: Enhance section styling and typography

### 7. Add Transparent Pricing Display (`index.html` + `css/styles.css`)

**Current State**: No pricing information visible

**Airbnb-Inspired Improvements**:

- Display pricing on tour cards (if pricing data is available)
- Add "Starting from" or "All fees included" messaging
- Show pricing tooltip or info icon
- If no pricing available, show "Contact for pricing" or "Request quote"

**Files to Modify**:

- `index.html`: Add pricing elements to cards
- `css/styles.css`: Style pricing displays

### 8. Enhance Card Hover States and Interactions (`css/styles.css`)

**Current State**: Basic border color change on hover

**Airbnb-Inspired Improvements**:

- Image zoom effect on hover (scale transform)
- Smooth transitions for all interactions
- Shadow elevation changes on hover
- Better visual feedback for "Learn More" buttons
- Card lift effect on hover

**Files to Modify**:

- `css/styles.css` (lines 541-568): Enhance card hover effects

### 9. Add "See All" Navigation Pattern (`index.html` + `css/styles.css`)

**Airbnb-Inspired Improvements**:

- Add "See all tours →" links to section headings
- Make it easy to navigate to full tour listings
- Use arrow icons or chevrons for visual indication

**Files to Modify**:

- `index.html`: Add "See all" links to sections
- `css/styles.css`: Style navigation links

## Technical Considerations

1. **Image Assets**: Use existing tour images from `/assets/` directory (check available formats: webp, avif, jpg)
2. **JavaScript**: Add carousel functionality if not already present in `js/main.js`
3. **Responsive Design**: Ensure all new elements work on mobile devices
4. **Performance**: Optimize image loading (lazy loading, proper formats like webp/avif)
5. **Accessibility**: Maintain ARIA labels and keyboard navigation
6. **Static Site**: All interactions use links/CTAs - no dynamic search or filtering

## Priority Implementation Order

1. **High Priority**: Image-heavy cards, horizontal carousels, enhanced hero (visual only)
2. **Medium Priority**: Social proof elements, pricing display, header enhancements
3. **Low Priority**: Advanced interactions, additional badges, section navigation

## Key Differences from Original Plan

- ❌ **Removed**: Search interface in hero section
- ❌ **Removed**: Header search integration
- ✅ **Kept**: All visual design improvements
- ✅ **Kept**: Image-heavy cards, carousels, social proof
- ✅ **Enhanced**: "Learn More" and "See all" CTAs throughout

## Questions to Consider

1. Do you have tour images available in the `/assets/` directory that we should use for the cards?
2. Do you have rating/review data to display, or should we use placeholder content?
3. Should the carousel be auto-scrolling or only manual navigation?
4. What pricing information should be displayed (starting prices, full prices, or "Contact for pricing")?
5. Should we add a prominent "Contact Us" or "Book Now" button in the header?