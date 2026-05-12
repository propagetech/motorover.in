# Deployment Guide

## Overview

This guide covers deployment of the MotoRover website including static site, API server, database, and related services.

## Static Site Deployment

### Option 1: Netlify (Recommended)

1. **Connect Repository**
   - Push code to GitHub/GitLab
   - Connect repository to Netlify
   - Set build command: `npm run build`
   - Set publish directory: `dist`
   - The static site HTML, CSS, and assets live at the repository root; `vite.config.js` builds from `index.html`

2. **Environment Variables**
   - Add any required environment variables in Netlify dashboard

3. **Custom Domain**
   - Add custom domain: motorover.in
   - Configure DNS records as per Netlify instructions
   - Enable SSL (automatic)

### Option 2: Vercel

1. **Deploy**
   ```bash
   npm install -g vercel
   vercel
   ```

2. **Production Deployment**
   ```bash
   vercel --prod
   ```
3. **Build Output**
   - Keep build command as `npm run build`
   - Keep output directory as `dist`
   - Vite is configured to build from the repository root (`index.html`)

### Option 3: GitHub Pages

1. **Build and Deploy**
   ```bash
   npm run build
   # Push dist/ to gh-pages branch
   ```

## API Server Deployment

### Option 1: Railway

1. **Create New Project**
   - Connect GitHub repository
   - Select `api/` directory as root
   - Railway will auto-detect Node.js

2. **Environment Variables**
   - Add required environment variables:
     - `PORT=3001`
     - `DATABASE_URL=...`
     - `EMAIL_SERVICE_KEY=...`
     - `STRIPE_SECRET_KEY=...`
     - `RAZORPAY_KEY=...`

3. **Custom Domain**
   - Add custom domain: api.motorover.in
   - Configure DNS

### Option 2: Heroku

1. **Create Heroku App**
   ```bash
   cd api
   heroku create motorover-api
   ```

2. **Deploy**
   ```bash
   git push heroku main
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set DATABASE_URL=...
   heroku config:set EMAIL_SERVICE_KEY=...
   ```

### Option 3: AWS/EC2

1. **Setup EC2 Instance**
   - Launch Ubuntu instance
   - Install Node.js and PM2

2. **Deploy**
   ```bash
   git clone <repository>
   cd api
   npm install
   pm2 start server.js --name motorover-api
   ```

## Database Setup

### PostgreSQL (Recommended)

1. **Option 1: Supabase**
   - Create free account
   - Create new project
   - Get connection string
   - Update `api/config/database.js`

2. **Option 2: AWS RDS**
   - Create PostgreSQL instance
   - Configure security groups
   - Get connection endpoint

3. **Option 2: Railway/Heroku Postgres**
   - Add PostgreSQL addon
   - Connection string provided automatically

### MongoDB (Alternative)

1. **MongoDB Atlas**
   - Create free cluster
   - Get connection string
   - Update database config

## Email Service Setup

### SendGrid

1. **Create Account**
   - Sign up at sendgrid.com
   - Verify sender email
   - Generate API key

2. **Configure**
   - Add API key to environment variables
   - Update `api/services/email.js`

### Nodemailer (Alternative)

1. **SMTP Configuration**
   - Use Gmail, Outlook, or custom SMTP
   - Add credentials to environment variables

## Payment Gateway Setup

### Stripe

1. **Create Account**
   - Sign up at stripe.com
   - Get API keys
   - Add to environment variables

### Razorpay

1. **Create Account**
   - Sign up at razorpay.com
   - Get API keys
   - Add to environment variables

## CDN Setup

### Cloudflare

1. **Add Site**
   - Add motorover.in to Cloudflare
   - Update nameservers
   - Enable CDN and caching

2. **Optimization**
   - Enable Auto Minify
   - Enable Brotli compression
   - Configure caching rules

## SSL Certificate

- **Automatic**: Netlify, Vercel, Railway provide free SSL
- **Manual**: Use Let's Encrypt for custom setups

## DNS Configuration

### Required Records

```
A Record: @ → Static site IP (Netlify/Vercel)
CNAME: www → Static site domain
CNAME: api → API server domain
```

## Environment Variables Checklist

### API Server
- `PORT=3001`
- `DATABASE_URL=...`
- `EMAIL_SERVICE_KEY=...`
- `STRIPE_SECRET_KEY=...`
- `RAZORPAY_KEY_ID=...`
- `RAZORPAY_KEY_SECRET=...`
- `CRM_API_KEY=...`
- `MAPBOX_TOKEN=...`
- `OPENAI_API_KEY=...` (for AI assistant)

### Frontend
- `API_BASE_URL=https://api.motorover.in`
- `GA_MEASUREMENT_ID=...`

## Monitoring & Analytics

1. **Google Analytics**
   - Create GA4 property
   - Add tracking ID to environment variables

2. **Error Tracking**
   - Consider Sentry for error monitoring
   - Add Sentry DSN to environment variables

## Backup Strategy

1. **Database Backups**
   - Automated daily backups (most providers include this)
   - Manual backup before major updates

2. **Content Backups**
   - Git repository serves as backup
   - Regular exports of JSON content files

## Performance Optimization

1. **Image Optimization**
   - Use WebP/AVIF formats
   - Implement lazy loading
   - Use CDN for image delivery

2. **Caching**
   - Static assets: Long-term caching
   - API responses: Appropriate cache headers
   - CDN caching for static content

## Security Checklist

- [ ] SSL certificates installed
- [ ] Environment variables secured
- [ ] API rate limiting configured
- [ ] CORS properly configured
- [ ] Input validation on all forms
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF protection for forms

## Post-Deployment

1. **Testing**
   - Test all forms
   - Test booking flow
   - Test payment integration
   - Test email delivery
   - Test mobile responsiveness

2. **SEO**
   - Submit sitemap to Google Search Console
   - Verify structured data
   - Check mobile-friendliness

3. **Monitoring**
   - Set up uptime monitoring
   - Configure error alerts
   - Monitor API performance
