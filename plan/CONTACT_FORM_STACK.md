# MotoRover Contact Form — Tech & Infra Stack Recommendation

**Requirement:** Cost-effective (free to start), scales to paid without changing the stack or codebase.

---

## Recommended Stack

### Form Backend: **Formspree**
> https://formspree.io

| Tier       | Price         | Submissions/month | Features                                      |
|------------|---------------|-------------------|-----------------------------------------------|
| Free       | $0            | 50                | Email notifications, spam filter, file upload |
| Basic      | $10/mo        | 1,000             | Custom redirect, webhooks                     |
| Business   | $40/mo        | 10,000            | Team access, Zapier integration, priority support |
| Gold       | $99/mo        | Unlimited         | Full feature set                              |

**Why Formspree:**
- Zero backend code — just a `<form action="https://formspree.io/f/YOUR_ID">` attribute swap
- Works with plain HTML forms — no JS required (but optional AJAX for a smoother UX)
- Built-in spam protection (reCAPTCHA + honeypot)
- Email notifications to `info@motorover.in` on every submission
- Dashboard to view all submissions
- One `action=` attribute URL — the free → paid upgrade happens entirely on Formspree's dashboard, **no code changes ever**
- GDPR compliant, data stored in EU/US

---

## Implementation (Current contact.html)

### Step 1 — Sign up at formspree.io, create a new form, get your endpoint ID

The endpoint looks like: `https://formspree.io/f/xpzgkwrd`

### Step 2 — Update the `<form>` tag in `contact.html`:

```html
<form
  id="enquiry-form"
  action="https://formspree.io/f/YOUR_FORM_ID"
  method="POST"
  novalidate
>
```

Add a hidden field for the tour name (auto-populates from URL parameter or dropdown):

```html
<input type="hidden" name="_subject" value="New Enquiry — MotoRover" />
<input type="hidden" name="_next" value="https://www.motorover.in/beta/contact.html?sent=1" />
```

### Step 3 — Optional: AJAX submission (no page reload)

Replace the default form submit with a `fetch()` call for a smoother UX. The existing `main.js` contact form handler can be updated:

```javascript
// In main.js — replace the form submit handler:
const form = document.getElementById('enquiry-form');
if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    // ... existing client-side validation ...

    const data = new FormData(form);
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json' }
      });
      if (res.ok) {
        // Show success message
        form.innerHTML = `<div class="form-success">
          <i class="fa-solid fa-circle-check" style="color:#4CAF50; font-size:3rem;"></i>
          <h3>Message Sent!</h3>
          <p>We'll get back to you within 24 hours.</p>
        </div>`;
      } else {
        // Show error
        alert('Something went wrong. Please try WhatsApp instead.');
      }
    } catch {
      alert('Network error. Please try WhatsApp instead.');
    }
  });
}
```

---

## Scaling Path (same stack, zero code changes)

```
0–50 submissions/month  → Formspree Free ($0)
51–1,000/month          → Formspree Basic ($10/mo) — just upgrade in dashboard
1,001–10,000/month      → Formspree Business ($40/mo) — same
High volume             → Formspree Gold ($99/mo) or custom plan
```

The form `action` URL **never changes**. No code deploys needed on upgrade.

---

## Spam Protection

Formspree's free tier includes:
- reCAPTCHA v3 (invisible, no user friction)
- Honeypot field (auto-inserted)

For the contact.html form, also add a honeypot field manually:

```html
<!-- Honeypot: hidden from users, bots fill it in -->
<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off" />
```

---

## WhatsApp as Primary (Backup Always Works)

Since MotoRover's primary conversion path is WhatsApp (`+91 83903 45646`), the contact form is a secondary channel. Even if Formspree has downtime, users can always reach the team via WhatsApp. This makes the form a "nice to have" rather than mission-critical, making Formspree's free tier perfectly adequate for early stage.

---

## Alternative Options Considered

| Option         | Free Tier     | Code Change on Scale | Notes                                     |
|----------------|---------------|---------------------|-------------------------------------------|
| **Formspree**  | 50/mo         | None                | ✅ Best fit for this use case              |
| Netlify Forms  | 100/mo        | None (if on Netlify) | Tied to Netlify hosting                  |
| EmailJS        | 200/mo        | None                | Client-side only, exposes API key         |
| Basin          | 100/mo        | None                | Good but less known                       |
| Self-hosted    | Free          | Full dev work        | Requires email worker / Node.js backend  |
| Getform        | 50/mo         | None                | Similar to Formspree, slightly less mature |

---

## Notification Routing

Set Formspree to notify: `info@motorover.in`

In Formspree dashboard, you can also set:
- CC to a team member (e.g. `piyush@motorover.in`)
- Auto-reply email to the enquirer (available on Basic+)
- Webhook to Slack/Zapier for instant team alerts

---

## Summary

**Use Formspree.** One attribute change in `contact.html`, zero server maintenance, free to start, upgrade in-dashboard. No new infra, no email worker, no Node.js. Works forever with plain HTML.

Action item: Sign up at formspree.io → create form → replace `YOUR_FORM_ID` in `contact.html`.
