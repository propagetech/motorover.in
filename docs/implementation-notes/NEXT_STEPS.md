# Next Steps for Deployment

Your dual-email notification system is implemented in the `email-worker` directory. To go live, follow these steps:

## 1. Prerequisites
Ensure you have the following tools installed:
- [Node.js & npm](https://nodejs.org/)
- [Rust & Cargo](https://rustup.rs/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/): `npm install -g wrangler`

## 2. API Keys
You need to obtain the following keys:
1. **SendGrid API Key**: Sign up at [SendGrid](https://sendgrid.com/) (Free Tier) and create an API Key.
2. **Google reCAPTCHA v3**: Sign up at [Google reCAPTCHA](https://www.google.com/recaptcha/admin) and get a **Site Key** and **Secret Key**.

## 3. Configuration
1. **Frontend**:
   - Open `assets/js/form-handler.js`.
   - Replace `PLACEHOLDER_SITE_KEY` with your actual Google reCAPTCHA **Site Key**.
   - Add `<script src="assets/js/form-handler.js"></script>` to your HTML pages (e.g., `contactus.html`, `about.html`).

2. **Worker Secrets**:
   Run the following commands in your terminal (inside `email-worker` directory):
   ```bash
   cd email-worker
   wrangler secret put SENDGRID_API_KEY
   # Paste your SendGrid key when prompted

   wrangler secret put RECAPTCHA_SECRET_KEY
   # Paste your Google reCAPTCHA Secret Key when prompted
   ```

## 4. Deploy
Deploy the worker to Cloudflare's edge network:
```bash
cd email-worker
wrangler deploy
```

## 5. Update Frontend URL
After deployment, Wrangler will output your Worker's URL (e.g., `https://email-worker.your-subdomain.workers.dev`).
1. Copy this URL.
2. Open `assets/js/form-handler.js`.
3. Update `API_URL` with your new Worker URL.
4. Deploy your static website (commit and push).

## 6. Verification
- Submit a form on your website.
- Check the browser console for "Submission successful".
- Check your email (visitor and owner) for the notifications.
- Check Cloudflare Dashboard > Workers > Logs to see the structured logs.
