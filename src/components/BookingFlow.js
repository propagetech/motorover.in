/**
 * Progressive Booking Flow Component
 * Multi-step booking: tour → dates → travelers → add-ons → payment
 */

const BOOKING_STEPS = [
  { id: 'tour', title: 'Choose Tour' },
  { id: 'dates', title: 'Select Dates' },
  { id: 'travelers', title: 'Add Travelers' },
  { id: 'addons', title: 'Choose Add-ons' },
  { id: 'review', title: 'Review & Pay' },
];

export function initBookingFlow() {
  const bookingContainer = document.querySelector('.booking-flow');
  if (!bookingContainer) return;
  
  let currentStep = 0;
  const bookingData = {
    tour: null,
    dates: { start: null, end: null },
    travelers: [],
    addons: [],
    totalPrice: 0,
  };
  
  renderBookingFlow(bookingContainer, currentStep, bookingData);
  attachEventListeners(bookingContainer, currentStep, bookingData);
}

function renderBookingFlow(container, stepIndex, data) {
  container.innerHTML = `
    <div class="booking-flow__progress">
      ${BOOKING_STEPS.map((step, index) => `
        <div class="booking-flow__step ${index === stepIndex ? 'booking-flow__step--active' : ''} ${index < stepIndex ? 'booking-flow__step--completed' : ''}">
          <div class="booking-flow__step-number">${index + 1}</div>
          <div class="booking-flow__step-title">${step.title}</div>
        </div>
      `).join('')}
    </div>
    
    <div class="booking-flow__content">
      ${renderStepContent(stepIndex, data)}
    </div>
  `;
}

function renderStepContent(stepIndex, data) {
  const step = BOOKING_STEPS[stepIndex];
  
  switch (step.id) {
    case 'tour':
      return renderTourSelection(data);
    case 'dates':
      return renderDateSelection(data);
    case 'travelers':
      return renderTravelersForm(data);
    case 'addons':
      return renderAddonsSelection(data);
    case 'review':
      return renderReview(data);
    default:
      return '';
  }
}

function renderTourSelection(data) {
  return `
    <div class="booking-step">
      <h3>Select Your Tour</h3>
      <div class="tours-selection">
        <!-- Tours will be loaded dynamically -->
      </div>
      <div class="booking-flow__actions">
        <button type="button" class="btn btn--primary" onclick="window.bookingFlow?.nextStep()">Continue</button>
      </div>
    </div>
  `;
}

function renderDateSelection(data) {
  return `
    <div class="booking-step">
      <h3>Select Travel Dates</h3>
      <div class="form__group">
        <label for="start-date" class="form__label form__label--required">Start Date</label>
        <input type="date" id="start-date" class="form__input" required>
      </div>
      <div class="form__group">
        <label for="end-date" class="form__label form__label--required">End Date</label>
        <input type="date" id="end-date" class="form__input" required>
      </div>
      <div class="booking-flow__actions">
        <button type="button" class="btn btn--secondary" onclick="window.bookingFlow?.prevStep()">Back</button>
        <button type="button" class="btn btn--primary" onclick="window.bookingFlow?.nextStep()">Continue</button>
      </div>
    </div>
  `;
}

function renderTravelersForm(data) {
  return `
    <div class="booking-step">
      <h3>Traveler Information</h3>
      <div class="form__group">
        <label for="traveler-count" class="form__label form__label--required">Number of Travelers</label>
        <input type="number" id="traveler-count" class="form__input" min="1" max="10" value="1" required>
      </div>
      <div id="travelers-details"></div>
      <div class="booking-flow__actions">
        <button type="button" class="btn btn--secondary" onclick="window.bookingFlow?.prevStep()">Back</button>
        <button type="button" class="btn btn--primary" onclick="window.bookingFlow?.nextStep()">Continue</button>
      </div>
    </div>
  `;
}

function renderAddonsSelection(data) {
  return `
    <div class="booking-step">
      <h3>Add-ons & Extras</h3>
      <div class="addons-selection">
        <div class="addon-item">
          <input type="checkbox" id="room-upgrade" class="addon-checkbox">
          <label for="room-upgrade">Room Upgrade (+₹5,000)</label>
        </div>
        <div class="addon-item">
          <input type="checkbox" id="extra-nights" class="addon-checkbox">
          <label for="extra-nights">Extra Nights (+₹3,000/night)</label>
        </div>
      </div>
      <div class="booking-flow__actions">
        <button type="button" class="btn btn--secondary" onclick="window.bookingFlow?.prevStep()">Back</button>
        <button type="button" class="btn btn--primary" onclick="window.bookingFlow?.nextStep()">Continue</button>
      </div>
    </div>
  `;
}

function renderReview(data) {
  const totalPrice = calculateTotalPrice(data);
  
  return `
    <div class="booking-step">
      <h3>Review Your Booking</h3>
      <div class="booking-summary">
        <div class="summary-item">
          <strong>Tour:</strong> ${data.tour?.name || 'Not selected'}
        </div>
        <div class="summary-item">
          <strong>Dates:</strong> ${data.dates.start || 'Not selected'} to ${data.dates.end || 'Not selected'}
        </div>
        <div class="summary-item">
          <strong>Travelers:</strong> ${data.travelers.length}
        </div>
        <div class="summary-item">
          <strong>Total Price:</strong> ₹${totalPrice.toLocaleString()}
        </div>
      </div>
      <div class="booking-flow__actions">
        <button type="button" class="btn btn--secondary" onclick="window.bookingFlow?.prevStep()">Back</button>
        <button type="button" class="btn btn--primary" onclick="window.bookingFlow?.proceedToPayment()">Proceed to Payment</button>
      </div>
    </div>
  `;
}

function calculateTotalPrice(data) {
  let total = data.tour?.basePrice || 0;
  data.addons.forEach(addon => {
    total += addon.price || 0;
  });
  return total * (data.travelers.length || 1);
}

function attachEventListeners(container, stepIndex, data) {
  // Event listeners will be attached here
  window.bookingFlow = {
    nextStep: () => {
      if (stepIndex < BOOKING_STEPS.length - 1) {
        currentStep = stepIndex + 1;
        renderBookingFlow(container, currentStep, data);
      }
    },
    prevStep: () => {
      if (stepIndex > 0) {
        currentStep = stepIndex - 1;
        renderBookingFlow(container, currentStep, data);
      }
    },
    proceedToPayment: () => {
      // Handle payment
      console.log('Proceeding to payment...', data);
    },
  };
}

export default { initBookingFlow };
