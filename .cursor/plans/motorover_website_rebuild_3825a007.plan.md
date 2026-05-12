---
name: MotoRover Website Rebuild
overview: Comprehensive rebuild of MotoRover website with enhanced static site architecture, API integration capabilities, progressive booking flow, AI features, and all requested sections. Maintains current static site benefits while adding modern dynamic capabilities.
todos:
  - id: design-system
    content: Enhance CSS design system with new utilities, night mode toggle, and mobile optimizations
    status: completed
  - id: navigation
    content: Build new navigation structure with dropdowns for Motorcycle Tours, Car Tours, and About Us sections
    status: completed
  - id: home-page
    content: Create enhanced home page with hero, featured tours, testimonials, gallery, and newsletter
    status: completed
  - id: tours-listing
    content: Build tours listing page with filters (type, destination, date) and tour cards
    status: completed
  - id: tour-detail
    content: Create tour detail pages with highlights, interactive map, pricing, booking CTA, and gallery
    status: completed
  - id: about-section
    content: "Build About Us pages: Our Story, Team (Official Team, Guides/Tour Managers), Why Us"
    status: completed
  - id: contact-faq
    content: Enhance Contact and FAQ pages with forms, validation, and interactive elements
    status: completed
  - id: booking-flow
    content: "Implement progressive booking flow: tour selection → dates → travelers → add-ons → payment"
    status: completed
  - id: inquiry-system
    content: Build inquiry form with email automation, CRM integration, and lead tracking
    status: completed
  - id: api-backend
    content: Create API server with endpoints for inquiries, bookings, tours, and admin functions
    status: completed
  - id: email-automation
    content: Implement automated email system for inquiries, bookings, and notifications
    status: completed
  - id: currency-converter
    content: Build real-time currency converter component for tour pricing
    status: completed
  - id: interactive-maps
    content: Integrate interactive maps with destination pins and itinerary display
    status: completed
  - id: trip-comparison
    content: Create trip comparison tool for side-by-side tour comparison
    status: completed
  - id: tour-planner
    content: Build interactive tour planner with filters for dates, cost, terrain, support level
    status: completed
  - id: group-planner
    content: Create customized group tour planner with quote request system
    status: completed
  - id: motorcycle-selector
    content: Build motorcycle selection component with dynamic pricing
    status: completed
  - id: ai-assistant
    content: Implement AI travel assistant with chat interface and recommendation engine
    status: completed
  - id: tour-automation
    content: Create automated tour management system for date updates and status changes
    status: completed
  - id: blog-section
    content: Build blog section with listing, individual posts, categories, and SEO optimization
    status: completed
  - id: seo-enhancements
    content: "Implement comprehensive SEO: meta tags, structured data, sitemap, keyword optimization"
    status: completed
  - id: mobile-optimization
    content: Ensure full mobile compatibility with responsive design and PWA features
    status: completed
  - id: performance
    content: "Optimize performance: image optimization, code splitting, lazy loading, caching"
    status: completed
  - id: testing
    content: "Conduct comprehensive testing: cross-browser, mobile, forms, API, performance"
    status: completed
  - id: deployment
    content: "Set up deployment: static hosting, API server, database, CDN, SSL, domain config"
    status: completed
---

# MotoRover Website Rebuild Plan

## Architecture Overview

The new website will be an **enhanced static site** with hybrid content management:

- **Static Foundation**: HTML/CSS/JS for core pages (SEO-friendly, fast)
- **Dynamic Layer**: API endpoints for bookings, inquiries, admin functions
- **Content Management**: JSON files for static content + API/database for dynamic content
- **Progressive Enhancement**: Core functionality works without JS, enhanced with JS

## Technology Stack

### Frontend

- **Core**: HTML5, CSS3 (enhanced design system), Vanilla JavaScript (ES6+)
- **Build Tools**: Vite for development and bundling
- **Styling**: Enhanced CSS custom properties (current system) + utility classes
- **Components**: Modular JavaScript components
- **Forms**: Progressive enhancement with validation

### Backend/API

- **API Server**: Node.js/Express or Python/Flask (for booking, inquiries, admin)
- **Database**: PostgreSQL or MongoDB (for bookings, inquiries, user data)
- **Email**: Nodemailer/SendGrid for automated emails
- **Payment**: Stripe/Razorpay/UPI integration
- **CRM Integration**: REST API endpoints for lead tracking

### Content Management

- **Static Content**: JSON files in `content/` directory (tours, pages, team)
- **Dynamic Content**: Database/API for bookings, inquiries, user data
- **Admin Panel**: Simple web interface for content updates (future)

## File Structure

```
motorover.in/
├── public/                 # Static assets
│   ├── assets/
│   │   ├── img/
│   │   ├── icons/
│   │   └── videos/
│   └── manifest.webmanifest
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── Header.js
│   │   ├── Footer.js
│   │   ├── TourCard.js
│   │   ├── BookingFlow.js
│   │   ├── CurrencyConverter.js
│   │   ├── InteractiveMap.js
│   │   └── AITravelAssistant.js
│   ├── pages/              # Page components
│   │   ├── Home.js
│   │   ├── Tours.js
│   │   ├── TourDetail.js
│   │   ├── About.js
│   │   ├── Team.js
│   │   ├── Contact.js
│   │   ├── FAQ.js
│   │   └── Blog.js
│   ├── utils/              # Utility functions
│   │   ├── api.js          # API client
│   │   ├── currency.js    # Currency conversion
│   │   ├── validation.js  # Form validation
│   │   └── seo.js         # SEO helpers
│   ├── styles/
│   │   ├── base.css       # Enhanced from current styles.css
│   │   ├── components.css
│   │   └── utilities.css
│   └── scripts/
│       ├── main.js        # Enhanced main.js
│       ├── booking.js     # Booking flow logic
│       └── analytics.js   # Tracking & analytics
├── content/                # Static content (JSON)
│   ├── pages.json
│   ├── tours.json
│   ├── team.json
│   ├── faqs.json
│   └── blog.json
├── api/                    # API server (Node.js/Python)
│   ├── routes/
│   │   ├── inquiries.js
│   │   ├── bookings.js
│   │   ├── tours.js
│   │   └── admin.js
│   ├── services/
│   │   ├── email.js
│   │   ├── crm.js
│   │   └── payment.js
│   └── config/
│       └── database.js
├── admin/                  # Admin panel (future)
├── scripts/                # Build & utility scripts
│   ├── generate_site.py   # Enhanced site generator
│   └── build.js           # Vite build config
└── package.json
```

## Implementation Phases

### Phase 1: Core Structure & Current Requirements

#### 1.1 Enhanced Design System

- **File**: `src/styles/base.css`
- Extend current CSS variables system
- Add utility classes for common patterns
- Enhance mobile responsiveness
- Implement night mode toggle (already has dark mode support)
- Add animation utilities

#### 1.2 Navigation & Header

- **File**: `src/components/Header.js`
- Implement new navigation structure:
  - Home
  - Motorcycle Tours (dropdown: all tours)
  - Car Tours (dropdown: all tours)
  - About Us (dropdown: Our Story, Team, Official Team, Guides/Tour Managers)
  - Contact Us
  - Why Us
  - FAQ
- Add night mode toggle button
- Mobile-responsive hamburger menu
- Sticky header with smooth transitions

#### 1.3 Home Page

- **File**: `src/pages/Home.js`
- Hero section with tour carousel
- Featured tours section (motorcycle & car)
- Why Choose MotoRover section
- Testimonials section
- Gallery section (new)
- Newsletter subscription
- SEO-optimized content

#### 1.4 Tours Pages

- **Files**: `src/pages/Tours.js`, `src/pages/TourDetail.js`
- Tour listing page with filters:
  - Tour type (Motorcycle/Car)
  - Budget tier (Budget/Classic/Luxury) - future ready
  - Destination
  - Date range
- Tour detail pages with:
  - Key highlights section
  - Interactive itinerary map
  - Pricing with currency converter
  - Booking CTA
  - Gallery
  - Testimonials
  - FAQ section

#### 1.5 About Us Section

- **Files**: `src/pages/About.js`, `src/pages/Team.js`
- Our Story page
- Team page with:
  - Official Team section
  - Guides/Tour Managers section
  - Team member profiles with photos
- Why Us page (enhanced)

#### 1.6 Contact & FAQ

- **Files**: `src/pages/Contact.js`, `src/pages/FAQ.js`
- Contact form with validation
- FAQ page with accordion (enhance current)
- Interactive map for office location

### Phase 2: Booking & Inquiry System

#### 2.1 Progressive Booking Flow

- **File**: `src/components/BookingFlow.js`
- Multi-step booking process:

  1. Choose tour
  2. Enter travel dates
  3. Add travelers (number, details)
  4. Choose add-ons (room upgrades, extra nights, motorcycle selection)
  5. Final price calculation
  6. Pay deposit online (Stripe/Razorpay/UPI)

- Real-time price updates
- Form validation
- Progress indicator

#### 2.2 Inquiry System

- **File**: `src/components/InquiryForm.js`
- Tour inquiry form
- Automated email on submission
- Email notification to support team
- CRM integration for lead tracking
- Trackable links for lead source attribution

#### 2.3 API Backend

- **Files**: `api/routes/inquiries.js`, `api/routes/bookings.js`
- RESTful API endpoints:
  - `POST /api/inquiries` - Submit inquiry
  - `POST /api/bookings` - Create booking
  - `GET /api/tours` - Get tour data
  - `GET /api/tours/:id` - Get tour details
- Database schema for inquiries and bookings
- Email service integration

#### 2.4 Email Automation

- **File**: `api/services/email.js`
- Automated emails:
  - Inquiry confirmation to customer
  - Inquiry notification to support team
  - Booking confirmation
  - Payment receipt
- Email templates
- Support for multiple email providers

### Phase 3: Advanced Features

#### 3.1 Currency Converter

- **File**: `src/components/CurrencyConverter.js`
- Real-time currency conversion for all tours
- Support for INR, USD, EUR, GBP
- API integration with currency exchange service
- Persistent user preference (localStorage)

#### 3.2 Interactive Maps

- **File**: `src/components/InteractiveMap.js`
- Map integration (Google Maps/Mapbox)
- Destination pins for each tour
- Clickable pins showing day's itinerary
- Route visualization
- Embedded in tour detail pages

#### 3.3 Trip Comparison Tool

- **File**: `src/components/TripComparison.js`
- Side-by-side comparison of tours
- Compare: price, duration, difficulty, highlights
- Export comparison
- Share comparison link

#### 3.4 Interactive Tour Planner

- **File**: `src/components/TourPlanner.js`
- Filter tours by:
  - Dates
  - Cost range
  - Terrain type
  - Support level
  - Off-roading level
- Real-time filtering
- Save preferences

#### 3.5 Customized Group Tour Planner

- **File**: `src/components/GroupTourPlanner.js`
- Special section for group bookings
- Custom date selection
- Group size input
- Special requirements form
- Quote request system

#### 3.6 Motorcycle Selection & Pricing

- **File**: `src/components/MotorcycleSelector.js`
- Motorcycle selection dropdown on tour pages
- Dynamic pricing based on selection
- Motorcycle specifications
- Availability check

### Phase 4: AI & Automation

#### 4.1 AI Travel Assistant

- **File**: `src/components/AITravelAssistant.js`
- Chat interface for tour recommendations
- AI integration (OpenAI API or similar)
- Preference-based suggestions:
  - Budget
  - Experience level
  - Preferred destinations
  - Travel dates
  - Group size
- Natural language processing

#### 4.2 Automated Tour Management

- **File**: `api/services/tourManagement.js`
- Automatic date updates (TBA when tour finished)
- Tour status management
- Availability updates
- Scheduled tasks for tour lifecycle

#### 4.3 Lead Source Tracking

- **File**: `src/utils/analytics.js`
- UTM parameter tracking
- Referral source tracking
- CRM integration for lead attribution
- Analytics dashboard (future)

### Phase 5: Content & SEO

#### 5.1 Blog Section

- **Files**: `src/pages/Blog.js`, `src/pages/BlogPost.js`
- Blog listing page
- Individual blog post pages
- SEO-optimized structure
- Categories and tags
- Related posts
- Social sharing

#### 5.2 SEO Enhancements

- **File**: `src/utils/seo.js`
- Enhanced meta tags
- Structured data (Schema.org)
- Open Graph tags
- Twitter Cards
- Sitemap generation
- robots.txt optimization
- Keyword optimization in content

#### 5.3 Content Management

- Enhanced JSON structure for easy updates
- Scripts for content migration
- Validation for content structure

### Phase 6: Future-Ready Sections

#### 6.1 Additional Navigation Items

- Group Tours section
- Budget/Classic/Luxury tier pages
- Expeditions section
- Lifestyle Trips section
- Merchandise section
- Careers page
- Partners page

#### 6.2 Additional Features

- Client Login & Referral system
- Admin Panel with hierarchy-based access
- Rentals section
- Club MotoRover section
- Video gallery tab
- Training section
- FIT (Free Independent Traveler) section
- Unique Adventures section
- Media section (enhanced)
- Events section
- Corporate section
- Cycle Tours section
- Unique Stays section

## Key Features Implementation Details

### Progressive Booking Flow

```javascript
// Booking flow state management
const bookingSteps = [
  { id: 'tour', title: 'Choose Tour' },
  { id: 'dates', title: 'Select Dates' },
  { id: 'travelers', title: 'Add Travelers' },
  { id: 'addons', title: 'Choose Add-ons' },
  { id: 'review', title: 'Review & Pay' }
];
```

### Currency Converter

- Use exchange rate API (e.g., exchangerate-api.com)
- Cache rates for performance
- Update rates daily
- Fallback to static rates if API fails

### Interactive Map

- Use Mapbox GL JS or Google Maps API
- Store tour coordinates in JSON
- Generate map markers from tour data
- Show itinerary on marker click

### AI Travel Assistant

- Integrate with OpenAI GPT API
- Context about all tours
- User preference collection
- Recommendation engine

### Email System

- Template-based emails
- HTML and plain text versions
- Support for multiple languages (future)
- Email queue for reliability

### CRM Integration

- REST API endpoints for CRM
- Lead data structure
- Webhook support
- Error handling and retries

## Mobile Optimization

- Responsive design (mobile-first)
- Touch-friendly interactions
- Optimized images (WebP, lazy loading)
- Progressive Web App (PWA) features
- Fast loading times
- Mobile menu optimization

## Performance Optimization

- Image optimization (WebP, AVIF)
- Code splitting
- Lazy loading
- Caching strategies
- CDN integration
- Minification and compression

## Testing & Quality Assurance

- Cross-browser testing
- Mobile device testing
- Form validation testing
- API endpoint testing
- Performance testing
- SEO audit

## Deployment

- Static site hosting (Netlify/Vercel/GitHub Pages)
- API server hosting (Heroku/Railway/AWS)
- Database hosting (PostgreSQL/MongoDB Atlas)
- CDN for assets
- SSL certificates
- Domain configuration

## Migration Strategy

1. Keep current site live during development
2. Develop new site in parallel
3. Content migration from current JSON files
4. Test thoroughly
5. Gradual rollout or big bang launch
6. Redirect old URLs to new structure

## Future Enhancements

- Admin panel for content management
- Multi-language support
- Advanced analytics dashboard
- Customer portal
- Referral program
- Loyalty program
- Integration with travel booking platforms
- Social media integration
- Live chat support

## Success Metrics

- Page load time < 3 seconds
- Mobile-friendly score > 95
- SEO score > 90
- Conversion rate tracking
- Lead source attribution
- User engagement metrics