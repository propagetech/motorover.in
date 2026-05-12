/**
 * Newsletter Subscription Component
 */

export function initNewsletter() {
  const form = document.querySelector('.newsletter-form');
  if (!form) return;
  
  form.addEventListener('submit', handleNewsletterSubmit);
}

function handleNewsletterSubmit(e) {
  e.preventDefault();
  
  const form = e.target;
  const emailInput = form.querySelector('input[type="email"]');
  const email = emailInput.value.trim();
  
  if (!email || !isValidEmail(email)) {
    showError(emailInput, 'Please enter a valid email address');
    return;
  }
  
  // Show loading state
  const submitButton = form.querySelector('button[type="submit"]');
  const originalText = submitButton.textContent;
  submitButton.disabled = true;
  submitButton.textContent = 'Subscribing...';
  
  // In a real implementation, this would call an API
  setTimeout(() => {
    showSuccess(form, 'Thank you for subscribing!');
    form.reset();
    submitButton.disabled = false;
    submitButton.textContent = originalText;
  }, 1000);
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showError(input, message) {
  const group = input.closest('.form__group');
  if (!group) return;
  
  group.classList.add('form__group--error');
  let errorEl = group.querySelector('.form__error');
  
  if (!errorEl) {
    errorEl = document.createElement('div');
    errorEl.className = 'form__error';
    group.appendChild(errorEl);
  }
  
  errorEl.textContent = message;
  
  input.addEventListener('input', () => {
    group.classList.remove('form__group--error');
  }, { once: true });
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

export default { initNewsletter };
