# Testing Guide

## Overview

Comprehensive testing guide for the MotoRover website covering all aspects of functionality, performance, and user experience.

## Testing Checklist

### Functional Testing

#### Navigation
- [ ] Desktop navigation works correctly
- [ ] Mobile hamburger menu opens/closes
- [ ] Dropdown menus function on hover (desktop) and click (mobile)
- [ ] All navigation links work
- [ ] Active page highlighting works
- [ ] Theme toggle functions correctly

#### Forms
- [ ] Contact form validation works
- [ ] Inquiry form validation works
- [ ] Newsletter subscription works
- [ ] Booking flow validation at each step
- [ ] Error messages display correctly
- [ ] Success messages display correctly
- [ ] Form submissions work (test with API)

#### Booking Flow
- [ ] All 5 steps of booking flow work
- [ ] Can navigate forward and backward
- [ ] Price calculations update correctly
- [ ] Add-ons selection works
- [ ] Payment integration works (test mode)

#### Interactive Features
- [ ] Currency converter updates prices
- [ ] Interactive map loads and displays markers
- [ ] Trip comparison tool works
- [ ] Tour planner filters work
- [ ] Motorcycle selector updates pricing
- [ ] AI assistant chat interface works

### Cross-Browser Testing

Test in the following browsers:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

### Mobile Testing

#### Responsive Design
- [ ] Layout adapts correctly on mobile (< 768px)
- [ ] Navigation menu works on mobile
- [ ] Forms are usable on mobile
- [ ] Images scale correctly
- [ ] Touch targets are adequate size (min 44x44px)
- [ ] Text is readable without zooming

#### Device Testing
- [ ] iPhone (various sizes)
- [ ] Android phones (various sizes)
- [ ] Tablets (iPad, Android tablets)

### Performance Testing

#### Page Load Times
- [ ] Homepage loads in < 3 seconds
- [ ] Tour pages load in < 3 seconds
- [ ] Images lazy load correctly
- [ ] No layout shift (CLS)

#### Lighthouse Scores
- [ ] Performance: > 90
- [ ] Accessibility: > 95
- [ ] Best Practices: > 90
- [ ] SEO: > 90

#### Core Web Vitals
- [ ] LCP (Largest Contentful Paint): < 2.5s
- [ ] FID (First Input Delay): < 100ms
- [ ] CLS (Cumulative Layout Shift): < 0.1

### Accessibility Testing

- [ ] All images have alt text
- [ ] Form labels are properly associated
- [ ] Keyboard navigation works throughout
- [ ] Focus indicators are visible
- [ ] Color contrast meets WCAG AA standards
- [ ] Screen reader compatibility
- [ ] ARIA labels used where appropriate

### SEO Testing

- [ ] All pages have unique titles
- [ ] All pages have meta descriptions
- [ ] Open Graph tags present
- [ ] Twitter Card tags present
- [ ] Structured data (JSON-LD) present
- [ ] Canonical URLs set correctly
- [ ] Sitemap.xml is valid
- [ ] Robots.txt is configured correctly

### API Testing

#### Endpoints
- [ ] POST /api/inquiries - Creates inquiry
- [ ] POST /api/bookings - Creates booking
- [ ] GET /api/tours - Returns tours list
- [ ] GET /api/tours/:id - Returns tour details
- [ ] GET /api/health - Health check

#### Error Handling
- [ ] Invalid data returns appropriate errors
- [ ] Missing required fields handled
- [ ] Rate limiting works (if implemented)
- [ ] CORS configured correctly

### Email Testing

- [ ] Inquiry confirmation emails sent
- [ ] Notification emails sent to support
- [ ] Booking confirmation emails sent
- [ ] Email templates render correctly
- [ ] Email links work correctly

### Payment Testing

- [ ] Stripe test mode works
- [ ] Razorpay test mode works
- [ ] Payment success handling
- [ ] Payment failure handling
- [ ] Receipt generation

### Security Testing

- [ ] XSS prevention (test with script injection)
- [ ] SQL injection prevention (if applicable)
- [ ] CSRF protection on forms
- [ ] Input sanitization
- [ ] Secure headers configured
- [ ] HTTPS enforced

## Automated Testing

### Setup

```bash
# Install testing dependencies
npm install --save-dev @testing-library/dom @testing-library/jest-dom jest
```

### Example Test

```javascript
// tests/navigation.test.js
import { initHeader } from '../src/components/Header.js';

describe('Navigation', () => {
  test('mobile menu toggles correctly', () => {
    // Test implementation
  });
});
```

## Manual Testing Scenarios

### Scenario 1: User Books a Tour

1. Navigate to tours page
2. Select a tour
3. Click "Book Now"
4. Complete booking flow:
   - Select dates
   - Add traveler information
   - Select add-ons
   - Review and pay
5. Verify booking confirmation

### Scenario 2: User Submits Inquiry

1. Navigate to tour detail page
2. Fill inquiry form
3. Submit form
4. Verify confirmation message
5. Check email received

### Scenario 3: User Compares Tours

1. Navigate to tours page
2. Select multiple tours to compare
3. View comparison table
4. Verify all data displays correctly

## Performance Testing Tools

- **Lighthouse**: Built into Chrome DevTools
- **WebPageTest**: https://www.webpagetest.org/
- **GTmetrix**: https://gtmetrix.com/
- **PageSpeed Insights**: https://pagespeed.web.dev/

## Accessibility Testing Tools

- **WAVE**: https://wave.webaim.org/
- **axe DevTools**: Browser extension
- **Lighthouse**: Accessibility audit
- **Screen Reader**: NVDA (Windows) or VoiceOver (Mac)

## Browser Testing Tools

- **BrowserStack**: Cross-browser testing
- **Sauce Labs**: Automated testing
- **Local Testing**: Use browser dev tools device emulation

## Test Data

Create test data for:
- Tours (various types, dates, prices)
- Team members
- FAQs
- Testimonials
- Blog posts

## Reporting Issues

When reporting issues, include:
- Browser and version
- Device and OS
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Console errors if any
