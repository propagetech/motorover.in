/**
 * Trip Comparison Tool
 * Side-by-side comparison of tours
 */

export function initTripComparison() {
  const comparisonContainer = document.querySelector('.trip-comparison');
  if (!comparisonContainer) return;
  
  let selectedTours = [];
  
  setupComparisonUI(comparisonContainer, selectedTours);
}

function setupComparisonUI(container, selectedTours) {
  container.innerHTML = `
    <div class="comparison-controls">
      <h3>Compare Tours</h3>
      <button class="btn btn--primary" onclick="window.tripComparison?.addTour()">Add Tour to Compare</button>
      <button class="btn btn--secondary" onclick="window.tripComparison?.clearComparison()">Clear</button>
    </div>
    <div class="comparison-table" id="comparison-table"></div>
  `;
  
  window.tripComparison = {
    addTour: () => {
      // Show tour selection modal
      showTourSelectionModal(selectedTours);
    },
    clearComparison: () => {
      selectedTours = [];
      renderComparison(container, selectedTours);
    },
    removeTour: (tourId) => {
      selectedTours = selectedTours.filter(t => t.id !== tourId);
      renderComparison(container, selectedTours);
    },
  };
}

function renderComparison(container, tours) {
  const table = container.querySelector('#comparison-table');
  if (!table) return;
  
  if (tours.length === 0) {
    table.innerHTML = '<p>No tours selected for comparison. Click "Add Tour to Compare" to get started.</p>';
    return;
  }
  
  const comparisonFields = [
    { key: 'name', label: 'Tour Name' },
    { key: 'price', label: 'Price' },
    { key: 'duration', label: 'Duration' },
    { key: 'difficulty', label: 'Difficulty' },
    { key: 'highlights', label: 'Key Highlights' },
    { key: 'destinations', label: 'Destinations' },
  ];
  
  table.innerHTML = `
    <table class="comparison-table__table">
      <thead>
        <tr>
          <th>Feature</th>
          ${tours.map(tour => `
            <th>
              ${tour.name}
              <button onclick="window.tripComparison?.removeTour('${tour.id}')" class="btn btn--text">Remove</button>
            </th>
          `).join('')}
        </tr>
      </thead>
      <tbody>
        ${comparisonFields.map(field => `
          <tr>
            <td><strong>${field.label}</strong></td>
            ${tours.map(tour => `
              <td>${formatFieldValue(tour[field.key], field.key)}</td>
            `).join('')}
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

function formatFieldValue(value, fieldKey) {
  if (Array.isArray(value)) {
    return value.join(', ');
  }
  if (fieldKey === 'price') {
    return `₹${value?.toLocaleString() || 'N/A'}`;
  }
  return value || 'N/A';
}

function showTourSelectionModal(selectedTours) {
  // Placeholder for tour selection modal
  alert('Tour selection modal - would show list of available tours');
}

export default { initTripComparison };
