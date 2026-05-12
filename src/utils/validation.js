/**
 * Form Validation Utility
 */

export function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

export function validatePhone(phone) {
  const re = /^[\d\s\-\+\(\)]+$/;
  return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

export function validateRequired(value) {
  return value && value.trim().length > 0;
}

export function validateMinLength(value, minLength) {
  return value && value.trim().length >= minLength;
}

export function validateMaxLength(value, maxLength) {
  return value && value.trim().length <= maxLength;
}

export function validateDate(date) {
  return date && !isNaN(Date.parse(date));
}

export function validateDateRange(startDate, endDate) {
  if (!startDate || !endDate) return true;
  return new Date(startDate) <= new Date(endDate);
}

export function validateForm(form) {
  const errors = {};
  const inputs = form.querySelectorAll('[required], [data-validate]');
  
  inputs.forEach(input => {
    const value = input.value.trim();
    const validations = input.dataset.validate?.split(',') || [];
    const fieldErrors = [];
    
    // Required validation
    if (input.hasAttribute('required') && !validateRequired(value)) {
      fieldErrors.push(`${getFieldLabel(input)} is required`);
    }
    
    // Email validation
    if (input.type === 'email' && value && !validateEmail(value)) {
      fieldErrors.push('Please enter a valid email address');
    }
    
    // Phone validation
    if (input.type === 'tel' && value && !validatePhone(value)) {
      fieldErrors.push('Please enter a valid phone number');
    }
    
    // Custom validations
    validations.forEach(validation => {
      const [type, param] = validation.split(':');
      
      switch (type) {
        case 'minLength':
          if (value && !validateMinLength(value, parseInt(param))) {
            fieldErrors.push(`${getFieldLabel(input)} must be at least ${param} characters`);
          }
          break;
        case 'maxLength':
          if (value && !validateMaxLength(value, parseInt(param))) {
            fieldErrors.push(`${getFieldLabel(input)} must be no more than ${param} characters`);
          }
          break;
      }
    });
    
    if (fieldErrors.length > 0) {
      errors[input.name || input.id] = fieldErrors;
    }
  });
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
}

function getFieldLabel(input) {
  const label = input.closest('.form__group')?.querySelector('.form__label');
  return label?.textContent.replace('*', '').trim() || input.name || 'This field';
}

export function showFieldError(input, message) {
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
    errorEl.remove();
  }, { once: true });
}

export function clearFieldError(input) {
  const group = input.closest('.form__group');
  if (group) {
    group.classList.remove('form__group--error');
    const errorEl = group.querySelector('.form__error');
    if (errorEl) {
      errorEl.remove();
    }
  }
}

export default {
  validateEmail,
  validatePhone,
  validateRequired,
  validateMinLength,
  validateMaxLength,
  validateDate,
  validateDateRange,
  validateForm,
  showFieldError,
  clearFieldError,
};
