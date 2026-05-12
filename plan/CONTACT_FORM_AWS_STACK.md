# MotoRover Contact Form — AWS Stack

**Philosophy:** Own your data. No 3rd-party SaaS. AWS free tier → paid without changing a line of code.

---

## Architecture Overview

```
Browser (contact.html)
        │
        │  POST /enquire  (JSON)
        ▼
  AWS API Gateway  ──────────────────────────────────────────┐
        │                                                     │
        ▼                                                     │
  AWS Lambda (Node.js)                                        │
        │                                                     │
        ├──► AWS SES ──► info@motorover.in (email notify)    │
        │                                                     │
        ├──► AWS S3  ──► enquiries/YYYY-MM/entry.json (log)  │
        │                                                     │
        └──► AWS DynamoDB (optional) ──► queryable records   │
                                                              │
  AWS CloudFront ◄──────────────────────────────────────────┘
  (CDN for static site + API cache headers)
```

---

## Services Used

| Service         | What it does                          | Free Tier                          | Paid (after free)                  |
|-----------------|---------------------------------------|------------------------------------|------------------------------------|
| API Gateway     | HTTPS endpoint for form POST          | 1M requests/month (12 months)      | $3.50 per million requests         |
| Lambda          | Runs form handler logic (Node.js)     | 1M requests + 400,000 GB-s/month   | $0.20 per million requests         |
| SES             | Sends email to info@motorover.in      | 62,000 emails/month (from Lambda)  | $0.10 per 1,000 emails             |
| S3              | Stores enquiry JSON files             | 5 GB storage + 20K GET + 2K PUT    | $0.023/GB/month                    |
| CloudFront      | CDN for static site + caching         | 1 TB transfer + 10M requests/month | $0.0085/GB (India edge)            |
| DynamoDB        | Optional: queryable enquiry database  | 25 GB + 200M requests/month        | $1.25 per million write units      |

> **Reality check:** At MotoRover's volume (est. <500 enquiries/month), this entire stack runs at **$0/month indefinitely** on AWS free tier. You pay only if you scale beyond millions of requests.

---

## Lambda Function (Node.js)

**File: `lambda/enquiry-handler.js`**

```javascript
const { SESClient, SendEmailCommand } = require('@aws-sdk/client-ses');
const { S3Client, PutObjectCommand }  = require('@aws-sdk/client-s3');

const ses = new SESClient({ region: 'ap-south-1' }); // Mumbai
const s3  = new S3Client({ region: 'ap-south-1' });

const BUCKET     = process.env.ENQUIRY_BUCKET;   // e.g. motorover-enquiries
const FROM_EMAIL = process.env.FROM_EMAIL;        // verified SES sender
const TO_EMAIL   = process.env.TO_EMAIL;          // info@motorover.in

exports.handler = async (event) => {
  // CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return cors(200, '');
  }

  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return cors(400, JSON.stringify({ error: 'Invalid JSON' }));
  }

  const { name, email, phone, tour, message, _honeypot } = body;

  // Honeypot spam check
  if (_honeypot) {
    return cors(200, JSON.stringify({ ok: true })); // silently discard
  }

  // Basic validation
  if (!name || !email || !message) {
    return cors(400, JSON.stringify({ error: 'Required fields missing' }));
  }

  const timestamp = new Date().toISOString();
  const id        = `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;

  // 1. Save to S3
  const entry = { id, timestamp, name, email, phone, tour, message };
  await s3.send(new PutObjectCommand({
    Bucket:      BUCKET,
    Key:         `enquiries/${timestamp.slice(0, 7)}/${id}.json`,
    Body:        JSON.stringify(entry, null, 2),
    ContentType: 'application/json',
  }));

  // 2. Send email via SES
  await ses.send(new SendEmailCommand({
    Source: FROM_EMAIL,
    Destination: { ToAddresses: [TO_EMAIL] },
    Message: {
      Subject: { Data: `New Enquiry — ${tour || 'General'} | MotoRover` },
      Body: {
        Html: {
          Data: `
            <h2 style="color:#D05200;">New MotoRover Enquiry</h2>
            <table style="border-collapse:collapse; width:100%; font-family:sans-serif;">
              <tr><td style="padding:8px; font-weight:600; color:#555;">Name</td><td style="padding:8px;">${name}</td></tr>
              <tr style="background:#f9f9f9;"><td style="padding:8px; font-weight:600; color:#555;">Email</td><td style="padding:8px;"><a href="mailto:${email}">${email}</a></td></tr>
              <tr><td style="padding:8px; font-weight:600; color:#555;">Phone</td><td style="padding:8px;">${phone || '—'}</td></tr>
              <tr style="background:#f9f9f9;"><td style="padding:8px; font-weight:600; color:#555;">Tour</td><td style="padding:8px;">${tour || '—'}</td></tr>
              <tr><td style="padding:8px; font-weight:600; color:#555;">Message</td><td style="padding:8px;">${message}</td></tr>
              <tr style="background:#f9f9f9;"><td style="padding:8px; font-weight:600; color:#555;">Submitted</td><td style="padding:8px;">${timestamp}</td></tr>
            </table>
            <p style="margin-top:24px; font-size:12px; color:#999;">Saved to S3: enquiries/${timestamp.slice(0,7)}/${id}.json</p>
          `
        }
      }
    }
  }));

  return cors(200, JSON.stringify({ ok: true, id }));
};

const cors = (statusCode, body) => ({
  statusCode,
  headers: {
    'Content-Type':                'application/json',
    'Access-Control-Allow-Origin': 'https://www.motorover.in',
    'Access-Control-Allow-Headers':'Content-Type',
    'Access-Control-Allow-Methods':'POST, OPTIONS',
  },
  body,
});
```

---

## contact.html — Form Update

Replace the existing `<form>` submit handler in `main.js`:

```javascript
const ENQUIRY_API = 'https://YOUR_API_ID.execute-api.ap-south-1.amazonaws.com/prod/enquire';

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
          name:       form.name.value.trim(),
          email:      form.email.value.trim(),
          phone:      form.phone?.value.trim(),
          tour:       form.tour?.value,
          message:    form.message.value.trim(),
          _honeypot:  form._honeypot?.value, // bot trap
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
        throw new Error('API error');
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

### Step 1 — Verify SES sender domain
```bash
# In AWS Console → SES → Verified Identities
# Add: motorover.in  (domain verification via DNS TXT record)
# Add: info@motorover.in
```

### Step 2 — Create S3 bucket
```bash
aws s3 mb s3://motorover-enquiries --region ap-south-1

# Block all public access (private data bucket)
aws s3api put-public-access-block \
  --bucket motorover-enquiries \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### Step 3 — Create Lambda function
```bash
# Zip and deploy
zip -r enquiry.zip lambda/
aws lambda create-function \
  --function-name motorover-enquiry \
  --runtime nodejs20.x \
  --handler enquiry-handler.handler \
  --zip-file fileb://enquiry.zip \
  --role arn:aws:iam::ACCOUNT_ID:role/motorover-lambda-role \
  --environment Variables="{
    ENQUIRY_BUCKET=motorover-enquiries,
    FROM_EMAIL=noreply@motorover.in,
    TO_EMAIL=info@motorover.in
  }" \
  --region ap-south-1
```

### Step 4 — Create API Gateway + route
```bash
# Via AWS Console: API Gateway → HTTP API → Create
# Route: POST /enquire → Lambda motorover-enquiry
# Enable CORS: origin https://www.motorover.in
# Stage: prod
# Deploy → note your endpoint URL
```

### Step 5 — IAM Role for Lambda
Lambda needs these permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": ["ses:SendEmail"], "Resource": "*" },
    { "Effect": "Allow", "Action": ["s3:PutObject"],  "Resource": "arn:aws:s3:::motorover-enquiries/*" }
  ]
}
```

### Step 6 — CloudFront (optional — for static site CDN)
```bash
# Create CloudFront distribution
# Origin: motorover.in S3 bucket (static site)
# Cache behaviour: /enquire → No-cache (API passthrough)
# Price class: PriceClass_200 (includes India edge locations)
```

---

## Scaling Path

```
0–1M req/month      → AWS Free Tier ($0)
1M–10M req/month    → ~$5–15/month (Lambda + API GW)
10M+ req/month      → ~$50–150/month (scale up Lambda memory/concurrency)
```

The API endpoint URL **never changes**. No code deploys on scale — AWS scales Lambda automatically.

---

## Data Ownership & Privacy

- All enquiry data lives in **your own S3 bucket** — no 3rd party ever sees it
- S3 bucket is private (no public access)
- SES sends from your verified domain — professional, not `no-reply@formspree.io`
- Enquiries are stored as JSON files: easy to export, query with AWS Athena, or build a simple admin dashboard later
- GDPR compliant: you control data retention (set S3 lifecycle policy to delete after N years)

---

## S3 Enquiry Structure

```
motorover-enquiries/
  enquiries/
    2026-03/
      1743200000000-ab3x9.json
      1743200001234-cd7y2.json
    2026-04/
      ...
```

Each file:
```json
{
  "id": "1743200000000-ab3x9",
  "timestamp": "2026-03-29T08:32:10.000Z",
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "phone": "+91 98765 43210",
  "tour": "Ultimate Alps Motorcycle Tour",
  "message": "Interested in July 2026 batch, need single room."
}
```

---

## Summary

| Aspect         | Detail                                      |
|----------------|---------------------------------------------|
| Cost           | $0/month (free tier, MotoRover volume)      |
| Latency        | ~100–300ms (Lambda cold start first call)   |
| Reliability    | 99.95% SLA (API Gateway + Lambda)           |
| Data ownership | 100% yours — private S3 bucket              |
| Vendor lock-in | Low — standard Node.js, easy to migrate     |
| Complexity     | Medium — one-time setup, zero maintenance   |
| Email provider | AWS SES — your domain, professional         |
