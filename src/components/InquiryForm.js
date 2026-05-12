/**
 * Inquiry Form Component
 * Handles tour inquiries with email automation and CRM integration
 */

import { validateForm, showFieldError } from '../utils/validation.js';
import { submitInquiry } from '../utils/api.js';

export function initInquiryForm() {
  const forms = document.querySelectorAll('.inquiry-form');
  forms.forEach(form => {
    form.addEventListener('submit', handleInquirySubmit);
    
    // Real-time validation
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
      input.addEventListener('blur', () => validateField(input));
    });
  });
}

async function handleInquirySubmit(e) {
  e.preventDefault();
  
  const form = e.target;
  const validation = validateForm(form);
  
  if (!validation.isValid) {
    Object.entries(validation.errors).forEach(([field, errors]) => {
      const input = form.querySelector(`[name="${field}"]`) || form.querySelector(`#${field}`);
      if (input && errors.length > 0) {
        showFieldError(input, errors[0]);
      }
    });
    return;
  }
  
  const formData = new FormData(form);
  const inquiryData = {
    tour: formData.get('tour') || form.dataset.tourId,
    name: formData.get('name'),
    email: formData.get('email'),
    phone: formData.get('phone'),
    message: formData.get('message'),
    travelDates: formData.get('travel-dates'),
    travelers: formData.get('travelers'),
    source: getLeadSource(),
    utmParams: getUTMParams(),
  };
  
  // Show loading state
  const submitButton = form.querySelector('button[type="submit"]');
  const originalText = submitButton.textContent;
  submitButton.disabled = true;
  submitButton.textContent = 'Submitting...';
  
  try {
    const { data, error } = await submitInquiry(inquiryData);
    
    if (error) {
      throw new Error(error);
    }
    
    showSuccess(form, 'Thank you for your inquiry! We will contact you soon.');
    form.reset();
    
    // Track conversion
    trackInquiryConversion(inquiryData);
  } catch (error) {
    showError(form, 'Something went wrong. Please try again or contact us directly.');
    console.error('Inquiry submission error:', error);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = originalText;
  }
}

function validateField(input) {
  const value = input.value.trim();
  
  if (input.hasAttribute('required') && !value) {
    showFieldError(input, 'This field is required');
    return false;
  }
  
  if (input.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    showFieldError(input, 'Please enter a valid email address');
    return false;
  }
  
  return true;
}

function getLeadSource() {
  return document.referrer || 'direct';
}

function getUTMParams() {
  const urlParams = new URLSearchParams(window.location.search);
  return {
    utm_source: urlParams.get('utm_source'),
    utm_medium: urlParams.get('utm_medium'),
    utm_campaign: urlParams.get('utm_campaign'),
    utm_term: urlParams.get('utm_term'),
    utm_content: urlParams.get('utm_content'),
  };
}

function trackInquiryConversion(data) {
  // Track in analytics
  if (window.gtag) {
    window.gtag('event', 'inquiry_submitted', {
      tour: data.tour,
      value: 1,
    });
  }
}

function showSuccess(form, message) {
  const successEl = document.createElement('div');
  successEl.className = 'form__success';
  successEl.style.cssText = 'padding: var(--space-4); background: var(--success); color: white; border-radius: var(--border-radius); margin-top: var(--space-4);';
  successEl.textContent = message;
  
  form.appendChild(successEl);
  
  setTimeout(() => {
    successEl.remove();
  }, 5000);
}

function showError(form, message) {
  const errorEl = document.createElement('div');
  errorEl.className = 'form__error';
  errorEl.style.cssText = 'padding: var(--space-4); background: var(--error); color: white; border-radius: var(--border-radius); margin-top: var(--space-4);';
  errorEl.textContent = message;
  
  form.appendChild(errorEl);
  
  setTimeout(() => {
    errorEl.remove();
  }, 5000);
}

export default { initInquiryForm };
