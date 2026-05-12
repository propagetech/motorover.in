/**
 * Customized Group Tour Planner
 * Special section for group bookings with quote request
 */

export function initGroupTourPlanner() {
  const plannerContainer = document.querySelector('.group-tour-planner');
  if (!plannerContainer) return;
  
  setupGroupPlanner(plannerContainer);
}

function setupGroupPlanner(container) {
  container.innerHTML = `
    <div class="group-planner">
      <h2>Plan Your Group Tour</h2>
      <p>Customize a tour for your group with special dates and requirements.</p>
      
      <form class="group-planner-form form">
        <div class="form__group">
          <label for="group-tour" class="form__label form__label--required">Select Tour</label>
          <select id="group-tour" class="form__select" name="tour" required>
            <option value="">Choose a tour...</option>
            <!-- Tours will be populated dynamically -->
          </select>
        </div>
        
        <div class="form__group">
          <label for="group-dates" class="form__label form__label--required">Preferred Dates</label>
          <input type="date" id="group-dates" class="form__input" name="dates" required>
        </div>
        
        <div class="form__group">
          <label for="group-size" class="form__label form__label--required">Group Size</label>
          <input type="number" id="group-size" class="form__input" name="groupSize" min="1" max="50" required>
        </div>
        
        <div class="form__group">
          <label for="group-requirements" class="form__label">Special Requirements</label>
          <textarea id="group-requirements" class="form__textarea" name="requirements" rows="4" placeholder="Any special requirements, dietary restrictions, accommodation preferences, etc."></textarea>
        </div>
        
        <div class="form__group">
          <label for="group-name" class="form__label form__label--required">Your Name</label>
          <input type="text" id="group-name" class="form__input" name="name" required>
        </div>
        
        <div class="form__group">
          <label for="group-email" class="form__label form__label--required">Email</label>
          <input type="email" id="group-email" class="form__input" name="email" required>
        </div>
        
        <div class="form__group">
          <label for="group-phone" class="form__label form__label--required">Phone</label>
          <input type="tel" id="group-phone" class="form__input" name="phone" required>
        </div>
        
        <button type="submit" class="btn btn--primary">Request Quote</button>
      </form>
    </div>
  `;
  
  const form = container.querySelector('.group-planner-form');
  form.addEventListener('submit', handleGroupQuoteRequest);
}

async function handleGroupQuoteRequest(e) {
  e.preventDefault();
  
  const form = e.target;
  const formData = new FormData(form);
  const quoteData = {
    tour: formData.get('tour'),
    dates: formData.get('dates'),
    groupSize: formData.get('groupSize'),
    requirements: formData.get('requirements'),
    name: formData.get('name'),
    email: formData.get('email'),
    phone: formData.get('phone'),
  };
  
  // Submit quote request
  const submitButton = form.querySelector('button[type="submit"]');
  submitButton.disabled = true;
  submitButton.textContent = 'Submitting...';
  
  try {
    // In production, this would call an API
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    showSuccess(form, 'Quote request submitted! We will contact you within 24 hours.');
    form.reset();
  } catch (error) {
    showError(form, 'Failed to submit quote request. Please try again.');
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = 'Request Quote';
  }
}

function showSuccess(form, message) {
  const successEl = document.createElement('div');
  successEl.className = 'form__success';
  successEl.style.cssText = 'padding: var(--space-4); background: var(--success); color: white; border-radius: var(--border-radius); margin-top: var(--space-4);';
  successEl.textContent = message;
  form.appendChild(successEl);
  setTimeout(() => successEl.remove(), 5000);
}

function showError(form, message) {
  const errorEl = document.createElement('div');
  errorEl.className = 'form__error';
  errorEl.style.cssText = 'padding: var(--space-4); background: var(--error); color: white; border-radius: var(--border-radius); margin-top: var(--space-4);';
  errorEl.textContent = message;
  form.appendChild(errorEl);
  setTimeout(() => errorEl.remove(), 5000);
}

export default { initGroupTourPlanner };
