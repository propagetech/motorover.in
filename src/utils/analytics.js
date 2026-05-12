/**
 * Analytics and Lead Tracking Utility
 * UTM parameter tracking, referral source tracking, CRM integration
 */

export function initAnalytics() {
  trackPageView();
  trackUTMParams();
  trackReferralSource();
}

function trackPageView() {
  if (window.gtag) {
    window.gtag('config', 'GA_MEASUREMENT_ID', {
      page_path: window.location.pathname,
      page_title: document.title,
    });
  }
}

function trackUTMParams() {
  const urlParams = new URLSearchParams(window.location.search);
  const utmParams = {
    utm_source: urlParams.get('utm_source'),
    utm_medium: urlParams.get('utm_medium'),
    utm_campaign: urlParams.get('utm_campaign'),
    utm_term: urlParams.get('utm_term'),
    utm_content: urlParams.get('utm_content'),
  };
  
  // Store in sessionStorage for form submissions
  if (Object.values(utmParams).some(v => v)) {
    sessionStorage.setItem('utmParams', JSON.stringify(utmParams));
  }
  
  // Track in analytics
  if (window.gtag && utmParams.utm_source) {
    window.gtag('event', 'page_view', {
      campaign_source: utmParams.utm_source,
      campaign_medium: utmParams.utm_medium,
      campaign_name: utmParams.utm_campaign,
    });
  }
}

function trackReferralSource() {
  const referrer = document.referrer;
  if (referrer) {
    sessionStorage.setItem('referrer', referrer);
    
    if (window.gtag) {
      window.gtag('event', 'referral', {
        referrer_url: referrer,
      });
    }
  }
}

export function trackEvent(eventName, eventData = {}) {
  if (window.gtag) {
    window.gtag('event', eventName, eventData);
  }
}

export function trackConversion(type, value, data = {}) {
  trackEvent(`${type}_conversion`, {
    value,
    currency: 'INR',
    ...data,
  });
}

export function getLeadSource() {
  const utmParams = JSON.parse(sessionStorage.getItem('utmParams') || '{}');
  const referrer = sessionStorage.getItem('referrer') || document.referrer;
  
  return {
    utm_source: utmParams.utm_source,
    utm_medium: utmParams.utm_medium,
    utm_campaign: utmParams.utm_campaign,
    referrer: referrer,
    direct: !referrer && !utmParams.utm_source,
  };
}

export default {
  initAnalytics,
  trackEvent,
  trackConversion,
  getLeadSource,
};
