/**
 * Motorcycle Selection Component
 * Dynamic pricing based on motorcycle selection
 */

export function initMotorcycleSelector() {
  const selectors = document.querySelectorAll('.motorcycle-selector');
  selectors.forEach(selector => {
    setupSelector(selector);
  });
}

function setupSelector(container) {
  const basePrice = parseFloat(container.dataset.basePrice) || 0;
  const motorcycles = JSON.parse(container.dataset.motorcycles || '[]');
  
  if (motorcycles.length === 0) return;
  
  container.innerHTML = `
    <div class="form__group">
      <label for="motorcycle-select" class="form__label">Select Motorcycle</label>
      <select id="motorcycle-select" class="form__select" name="motorcycle">
        ${motorcycles.map((bike, index) => `
          <option value="${bike.id}" data-price="${bike.price || 0}" ${index === 0 ? 'selected' : ''}>
            ${bike.name} ${bike.price ? `(+₹${bike.price.toLocaleString()})` : ''}
          </option>
        `).join('')}
      </select>
    </div>
    <div class="motorcycle-price-display">
      <strong>Total Price: </strong>
      <span class="price-display" data-base-price="${basePrice}">₹${basePrice.toLocaleString()}</span>
    </div>
  `;
  
  const select = container.querySelector('#motorcycle-select');
  const priceDisplay = container.querySelector('.price-display');
  
  select.addEventListener('change', (e) => {
    const selectedOption = e.target.options[e.target.selectedIndex];
    const additionalPrice = parseFloat(selectedOption.dataset.price) || 0;
    const totalPrice = basePrice + additionalPrice;
    
    if (priceDisplay) {
      priceDisplay.textContent = `₹${totalPrice.toLocaleString()}`;
    }
    
    // Update any other price displays on the page
    updateTourPrice(totalPrice);
  });
}

function updateTourPrice(newPrice) {
  const priceElements = document.querySelectorAll('[data-tour-price]');
  priceElements.forEach(el => {
    el.textContent = `₹${newPrice.toLocaleString()}`;
  });
}

export default { initMotorcycleSelector };
