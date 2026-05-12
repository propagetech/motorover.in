# MotoRover Contact Form — Cloudflare Stack

**Philosophy:** Own your data. Edge-first, serverless, global. Cloudflare free tier → paid without a single code change.

---

## Architecture Overview

```
Browser (contact.html)
        │
        │  POST /enquire  (JSON)
        ▼
  Cloudflare Worker  (runs at edge, <1ms cold start)
        │
        ├──► Cloudflare Email Routing ──► info@motorover.in
        │    (or MailChannels — free transactional email)
        │
        ├──► Cloudflare KV ──► enquiries:ID → JSON (fast key-value log)
        │
        ├──► Cloudflare D1 ──► SQLite database (queryable, structured)
        │
        └──► Cloudflare R2 ──► enquiries/YYYY-MM/ID.json (object storage)

  Cloudflare Pages ◄── Static site (motorover.in/beta/)
  (CDN + automatic HTTPS + global edge)
```

> **Key advantage over AWS:** Cloudflare Workers have **zero cold start** (runs at edge, not a container). Response time < 50ms globally, including from India.

---

## Services Used

| Service                 | What it does                            | Free Tier                              | Paid (Workers Paid $5/mo)              |
|-------------------------|-----------------------------------------|----------------------------------------|----------------------------------------|
| Cloudflare Workers      | Runs form handler at edge               | 100K req/day, 10ms CPU/req             | 10M req/month included                 |
| Cloudflare KV           | Key-value store for enquiry logs        | 100K reads/day, 1K writes/day, 1GB     | $0.50/million reads                    |
| Cloudflare D1           | SQLite database (queryable)             | 5M rows read/day, 100K writes/day, 1GB | $0.001 per 100K rows read              |
| Cloudflare R2           | Object storage (like S3, zero egress)   | 10 GB/month, 1M Class-A ops            | $0.015/GB/month (no egress fee!)       |
| Cloudflare Email Routing| Forward email to info@motorover.in      | Free, unlimited                        | Free                                   |
| Cloudflare Pages        | Static site hosting + CDN               | Unlimited bandwidth, unlimited sites   | Free                                   |
| MailChannels (via Worker)| Transactional email sending            | Free (from Cloudflare Workers)         | Free                                   |

> **Reality check:** At MotoRover's volume, this entire stack runs at **$0/month forever** on Cloudflare's free tier. Even at 100K enquiries/month you'd stay free.

---

## Worker Code

**File: `workers/enquiry-worker.js`**

```javascript
export default {
  async fetch(request, env, ctx) {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return corsResponse(200, null);
    }

    if (request.method !== 'POST') {
      return corsResponse(405, { error: 'Method not allowed' });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return corsResponse(400, { error: 'Invalid JSON' });
    }

    const { name, email, phone, tour, message, _honeypot } = body;

    // Honeypot spam check
    if (_honeypot) {
      return corsResponse(200, { ok: true }); // silently discard bots
    }

    // Basic validation
    if (!name || !email || !message) {
      return corsResponse(400, { error: 'Required fields missing' });
    }

    const timestamp = new Date().toISOString();
    const id        = `${Date.now()}-${crypto.randomUUID().slice(0, 8)}`;
    const entry     = { id, timestamp, name, email, phone: phone || '', tour: tour || '', message };

    // Run all 3 storage/email ops in parallel
    await Promise.all([
      // 1. Save to KV (fast lookup, 30-day TTL)
      env.ENQUIRIES_KV.put(
        `enquiry:${id}`,
        JSON.stringify(entry),
        { expirationTtl: 60 * 60 * 24 * 365 } // 1 year
      ),

      // 2. Save to D1 (queryable SQLite)
      env.DB.prepare(
        `INSERT INTO enquiries (id, timestamp, name, email, phone, tour, message)
         VALUES (?, ?, ?, ?, ?, ?, ?)`
      ).bind(id, timestamp, name, email, phone || '', tour || '', message).run(),

      // 3. Save to R2 (permanent JSON file archive)
      env.ENQUIRIES_R2.put(
        `enquiries/${timestamp.slice(0, 7)}/${id}.json`,
        JSON.stringify(entry, null, 2),
        { httpMetadata: { contentType: 'application/json' } }
      ),

      // 4. Send email via MailChannels
      sendEmail(name, email, phone, tour, message, timestamp, id),
    ]);

    return corsResponse(200, { ok: true, id });
  }
};

async function sendEmail(name, email, phone, tour, message, timestamp, id) {
  const res = await fetch('https://api.mailchannels.net/tx/v1/send', {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      personalizations: [{
        to: [{ email: 'info@motorover.in', name: 'MotoRover' }],
      }],
      from: { email: 'noreply@motorover.in', name: 'MotoRover Enquiries' },
      subject: `New Enquiry — ${tour || 'General'} | MotoRover`,
      content: [{
        type: 'text/html',
        value: `
          <h2 style="color:#D05200; font-family:sans-serif;">New MotoRover Enquiry</h2>
          <table style="border-collapse:collapse; width:100%; font-family:sans-serif; font-size:14px;">
            <tr><td style="padding:10px; font-weight:600; color:#555; width:120px;">Name</td><td style="padding:10px;">${name}</td></tr>
            <tr style="background:#f9f9f9;"><td style="padding:10px; font-weight:600; color:#555;">Email</td><td style="padding:10px;"><a href="mailto:${email}">${email}</a></td></tr>
            <tr><td style="padding:10px; font-weight:600; color:#555;">Phone</td><td style="padding:10px;">${phone || '—'}</td></tr>
            <tr style="background:#f9f9f9;"><td style="padding:10px; font-weight:600; color:#555;">Tour</td><td style="padding:10px;">${tour || '—'}</td></tr>
            <tr><td style="padding:10px; font-weight:600; color:#555;">Message</td><td style="padding:10px;">${message}</td></tr>
            <tr style="background:#f9f9f9;"><td style="padding:10px; font-weight:600; color:#555;">Submitted</td><td style="padding:10px;">${timestamp}</td></tr>
          </table>
          <p style="margin-top:24px; font-size:11px; color:#999; font-family:sans-serif;">
            Ref ID: ${id} · Saved to KV, D1, and R2
          </p>
        `
      }]
    })
  });
  return res;
}

function corsResponse(status, data) {
  return new Response(
    data ? JSON.stringify(data) : null,
    {
      status,
      headers: {
        'Content-Type':                'application/json',
        'Access-Control-Allow-Origin': 'https://www.motorover.in',
        'Access-Control-Allow-Headers':'Content-Type',
        'Access-Control-Allow-Methods':'POST, OPTIONS',
      }
    }
  );
}
```

---

## D1 Database Schema

```sql
-- Run once via Wrangler CLI
CREATE TABLE IF NOT EXISTS enquiries (
  id        TEXT PRIMARY KEY,
  timestamp TEXT NOT NULL,
  name      TEXT NOT NULL,
  email     TEXT NOT NULL,
  phone     TEXT,
  tour      TEXT,
  message   TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_timestamp ON enquiries(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_tour      ON enquiries(tour);
```

---

## wrangler.toml (Worker Config)

```toml
name       = "motorover-enquiry"
main       = "workers/enquiry-worker.js"
compatibility_date = "2024-01-01"

[[kv_namespaces]]
binding  = "ENQUIRIES_KV"
id       = "YOUR_KV_NAMESPACE_ID"

[[d1_databases]]
binding  = "DB"
database_name = "motorover-enquiries"
database_id   = "YOUR_D1_DATABASE_ID"

[[r2_buckets]]
binding = "ENQUIRIES_R2"
bucket_name = "motorover-enquiries"

[vars]
ENVIRONMENT = "production"

[[routes]]
pattern = "motorover.in/enquire"
zone_name = "motorover.in"
```

---

## contact.html — Form Update

Same as the AWS version — just swap the endpoint URL:

```javascript
const ENQUIRY_API = 'https://motorover.in/enquire'; // or your worker URL

const form = document.getElementById('enquiry-form');
if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    // ... existing client-side validation ...

    const btn = form.querySelector('[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Sending…';

    try {
      const res = await fetch(ENQUIRY_API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name:      form.name.value.trim(),
          email:     form.email.value.trim(),
          phone:     form.phone?.value.trim(),
          tour:      form.tour?.value,
          message:   form.message.value.trim(),
          _honeypot: form._honeypot?.value,
        }),
      });

      const data = await res.json();
      if (data.ok) {
        form.innerHTML = `
          <div style="text-align:center; padding:var(--sp-8);">
            <i class="fa-solid fa-circle-check" style="color:#4CAF50; font-size:3rem;"></i>
            <h3 style="margin-top:var(--sp-3);">Enquiry Received!</h3>
            <p style="color:var(--text-muted);">We'll reply within 24 hours. Ref: ${data.id}</p>
          </div>`;
      } else {
        throw new Error('Worker error');
      }
    } catch {
      btn.disabled = false;
      btn.textContent = 'Send Enquiry';
      alert('Something went wrong. Please WhatsApp us directly.');
    }
  });
}
```

---

## Deployment Steps

### Step 1 — Install Wrangler CLI
```bash
npm install -g wrangler
wrangler login
```

### Step 2 — Create KV namespace
```bash
wrangler kv:namespace create ENQUIRIES_KV
# Copy the ID into wrangler.toml
```

### Step 3 — Create D1 database
```bash
wrangler d1 create motorover-enquiries
# Copy the database_id into wrangler.toml

# Run schema migration
wrangler d1 execute motorover-enquiries --file=./schema.sql
```

### Step 4 — Create R2 bucket
```bash
wrangler r2 bucket create motorover-enquiries
```

### Step 5 — Set up Cloudflare Email Routing
```bash
# In Cloudflare Dashboard → motorover.in → Email Routing
# Add catch-all or specific:  noreply@motorover.in → info@motorover.in
# This verifies your domain as a sender for MailChannels
```

### Step 6 — Deploy Worker
```bash
wrangler deploy
# Output: https://motorover-enquiry.YOUR_SUBDOMAIN.workers.dev
# Or route it to: motorover.in/enquire
```

### Step 7 — Deploy static site to Cloudflare Pages
```bash
# In Cloudflare Dashboard → Pages → Connect to Git
# Or direct upload:
wrangler pages deploy ./beta --project-name=motorover-beta
# Auto HTTPS, global CDN, custom domain: beta.motorover.in
```

---

## Scaling Path

```
0–100K req/day          → Cloudflare Workers Free ($0)
100K–10M req/month      → Workers Paid ($5/month flat — includes 10M req)
10M+ req/month          → Workers Paid + usage ($0.30 per million over)
```

The Worker URL **never changes**. Cloudflare handles all scaling automatically at the edge.

---

## Cloudflare vs AWS — Quick Comparison

| Aspect              | Cloudflare                           | AWS                                    |
|---------------------|--------------------------------------|----------------------------------------|
| Cold start          | ~0ms (V8 isolate, not container)     | ~100–300ms (Lambda container)          |
| Global edge nodes   | 310+ cities incl. Mumbai, Chennai    | 30+ regions (closer to 100 edge nodes) |
| Free tier requests  | 100K/day (Workers Free)              | 1M/month (12 months only)              |
| Free tier — forever | ✅ Yes (Workers Free never expires)   | ⚠️ 12-month free tier, then pay         |
| Email               | MailChannels (free from Workers)     | SES (free from Lambda up to 62K/mo)    |
| Object storage      | R2 — zero egress fee                 | S3 — egress charged per GB             |
| SQL database        | D1 (SQLite at edge)                  | DynamoDB or RDS                        |
| Static site CDN     | Cloudflare Pages — free, unlimited BW| CloudFront — 1TB free then $0.0085/GB  |
| Setup complexity    | Low (Wrangler CLI, ~30 min)          | Medium (IAM roles, multi-service setup)|
| Vendor lock-in      | Low (standard JS, Worker API)        | Medium (AWS SDK specifics)             |
| India latency       | ~10–30ms (Mumbai/Chennai PoPs)       | ~50–150ms (ap-south-1 Mumbai)          |

---

## Data Ownership & Privacy

- All enquiry data lives in **your own Cloudflare account** — KV, D1, and R2 are private by default
- R2 has **zero egress fees** (unlike S3 — great for downloading backups)
- Email sent from `noreply@motorover.in` — your domain, your identity
- GDPR: you control data retention — D1 rows and R2 files deleteable at will
- No 3rd-party SaaS ever handles your leads

---

## Bonus — Simple Admin View (optional)

Since enquiries are in D1, you can query them any time:
```bash
# View last 10 enquiries
wrangler d1 execute motorover-enquiries \
  --command "SELECT id, timestamp, name, email, tour FROM enquiries ORDER BY timestamp DESC LIMIT 10;"

# Count by tour
wrangler d1 execute motorover-enquiries \
  --command "SELECT tour, COUNT(*) as count FROM enquiries GROUP BY tour ORDER BY count DESC;"
```

Or build a simple password-protected admin page on Cloudflare Pages that queries D1 via Workers — zero additional cost.

---

## Summary

| Aspect         | Detail                                                |
|----------------|-------------------------------------------------------|
| Cost           | $0/month forever (free tier never expires)            |
| Latency        | ~10–30ms from India (edge node in Mumbai/Chennai)     |
| Reliability    | 99.99% uptime SLA, 310+ global edge nodes             |
| Data ownership | 100% yours — private KV + D1 + R2                    |
| Vendor lock-in | Very low — standard JS, portable data                 |
| Complexity     | Low — one CLI tool (Wrangler), 30-min setup           |
| Email provider | MailChannels via Worker — your domain, free           |
| Bonus          | Static site on Cloudflare Pages = free CDN for beta/  |
