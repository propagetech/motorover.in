# Dual-Email Notification System Implementation Plan

## 1. Executive Summary
This document outlines the architecture and implementation strategy for a high-performance, secure, and zero-cost dual-email notification system using Cloudflare Workers and Rust. The system replaces the legacy Node.js/Express backend with a serverless edge function that handles form submissions, validation, PDF distribution, and email notifications.

## 2. Architecture Design

### 2.1 Serverless Edge Compute (Cloudflare Workers)
- **Runtime**: Rust (compiled to WebAssembly) for memory safety and performance.
- **Framework**: `workers-rs` crate.
- **Deployment**: Global edge network (low latency).
- **Cost**: Zero-cost (Cloudflare Workers Free Tier includes 100k req/day).

### 2.2 External Integrations
- **Email Service**: SendGrid (Free Tier: 100 emails/day) or MailChannels (Free for Cloudflare Workers).
  - *Fallback*: Mailgun.
- **Bot Protection**: Google reCAPTCHA v3.
  - Score-based analysis (0.0 - 1.0).
  - Threshold: 0.5 for acceptance.
- **PDF Hosting**: Cloudflare CDN (Static assets).

### 2.3 Data Flow
1. **Visitor** submits form on website.
2. **Client-side JS** intercepts submit, executes reCAPTCHA v3, gets token.
3. **POST Request** sent to Worker (`/api/submit`) with payload + token.
4. **Worker** verifies token with Google API.
5. **Worker** validates input data (Sanitization).
6. **Worker** selects PDF link based on `form_type`.
7. **Worker** dispatches two emails in parallel (Visitor & Owner).
8. **Worker** returns JSON response to client.

## 3. Security & Compliance

### 3.1 Security Measures
- **Input Validation**: Strict typing with Rust structs.
- **CORS Policy**: Restricted to `motorover.in` domain (configured in code).
- **Rate Limiting**:
  - Implementation: Cloudflare WAF (IP blocking) + Worker-level checks.
- **Bot Detection**: reCAPTCHA v3 invisible badge.

### 3.2 Data Privacy (GDPR/CCPA/PIPEDA)
- **Data Minimization**: The Worker is stateless; it processes data in transit and does not persist PII to disk/database (unless logging is enabled, which should be anonymized).
- **Encryption**: All data in transit is encrypted via TLS 1.3.
- **Right to be Forgotten**: Since no data is stored in the Worker's database, this is compliant by design. Logs should be rotated/anonymized.

## 4. Implementation Details

### 4.1 Tech Stack
- **Language**: Rust (Edition 2021)
- **Dependencies**:
  - `worker`: Cloudflare Workers bindings.
  - `serde`: Serialization/Deserialization.
  - `serde_json`: JSON handling.

### 4.2 File Structure
```
email-worker/
├── Cargo.toml          # Dependencies
├── wrangler.toml       # Worker configuration
└── src/
    ├── lib.rs          # Main entry point & Router
    └── utils.rs        # Helper functions (Email, Recaptcha)
```

## 5. Deployment Pipeline

### 5.1 Infrastructure as Code (IaC)
- `wrangler.toml` defines the infrastructure configuration.
- Secrets are managed via `wrangler secret put`.

### 5.2 Deployment Steps
1. **Install Dependencies**: `npm install -g wrangler`, `cargo install worker-build`.
2. **Configure Secrets**:
   ```bash
   wrangler secret put SENDGRID_API_KEY
   wrangler secret put RECAPTCHA_SECRET_KEY
   wrangler secret put OWNER_EMAIL
   ```
3. **Deploy**:
   ```bash
   cd email-worker
   wrangler deploy
   ```

## 6. Testing Strategy
- **Unit Tests**: Test validation logic and PDF mapping in Rust.
- **Integration Tests**: Test the worker endpoint using `wrangler dev` (local simulation).
- **Security Scans**: `cargo audit` to check for vulnerabilities in dependencies.

## 7. Next Steps
1. Register for SendGrid and Google reCAPTCHA v3 keys.
2. Update `wrangler.toml` (vars) and secrets.
3. Deploy the worker.
4. Update frontend `form-handler.js` to point to the new Worker URL.
