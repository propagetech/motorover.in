# MotoRover Website - Enhanced Static Site

Comprehensive rebuild of MotoRover website with enhanced static site architecture, API integration capabilities, progressive booking flow, AI features, and all requested sections.

## Features

### Core Features
- ✅ Enhanced CSS design system with utilities and mobile optimizations
- ✅ Navigation with dropdowns for Motorcycle Tours, Car Tours, and About Us
- ✅ Enhanced home page with hero, featured tours, testimonials, gallery, and newsletter
- ✅ Tours listing page with filters (type, destination, date)
- ✅ Tour detail pages with highlights, interactive map, pricing, booking CTA, and gallery

### Booking & Inquiry
- ✅ Progressive booking flow (tour → dates → travelers → add-ons → payment)
- ✅ Inquiry form with email automation, CRM integration, and lead tracking
- ✅ API backend with endpoints for inquiries, bookings, tours, and admin functions
- ✅ Automated email system for inquiries, bookings, and notifications

### Advanced Features
- ✅ Real-time currency converter for tour pricing
- ✅ Interactive maps with destination pins and itinerary display
- ✅ Trip comparison tool for side-by-side tour comparison
- ✅ Interactive tour planner with filters (dates, cost, terrain, support level)
- ✅ Customized group tour planner with quote request system
- ✅ Motorcycle selection component with dynamic pricing
- ✅ AI travel assistant with chat interface and recommendation engine
- ✅ Automated tour management system for date updates and status changes

### Content & SEO
- ✅ Blog section with listing, individual posts, categories, and SEO optimization
- ✅ Comprehensive SEO: meta tags, structured data, sitemap, keyword optimization
- ✅ Mobile optimization with responsive design and PWA features
- ✅ Performance optimization: image optimization, code splitting, lazy loading, caching

## Technology Stack

### Frontend
- HTML5, CSS3 (enhanced design system)
- Vanilla JavaScript (ES6+)
- Vite for development and bundling

### Backend/API
- Node.js/Express API server
- Database support (PostgreSQL/MongoDB)
- Email service integration (Nodemailer/SendGrid)
- Payment integration (Stripe/Razorpay/UPI)
- CRM integration for lead tracking

### Content Management
- Static content: JSON files in `content/` directory
- Dynamic content: Database/API for bookings and inquiries

## File Structure

```
motorover.in/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   ├── pages/              # Page components
│   ├── utils/              # Utility functions
│   ├── styles/             # CSS modules
│   └── scripts/            # JavaScript modules
├── content/                # Static content (JSON)
├── api/                    # API server
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   └── config/             # Configuration
└── scripts/                # Build & utility scripts
```

## Getting Started

### Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### API Server

```bash
# Start API server (requires Node.js)
cd api
node server.js
```

## Deployment

- Static site: Netlify/Vercel/GitHub Pages
- API server: Heroku/Railway/AWS
- Database: PostgreSQL/MongoDB Atlas
- CDN: For assets
- SSL: Required for production

## Features in Development

- About Us pages (Our Story, Team sections)
- Contact & FAQ enhancements
- Comprehensive testing
- Full deployment setup

## License

Copyright © 2026 MotoRover Tours. All Rights Reserved.
