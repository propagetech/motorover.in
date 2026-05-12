/**
 * Tours Listing Page Component
 * Includes filters for tour type, destination, and date
 */

export function initToursPage() {
  initFilters();
  initTourCards();
}

function initFilters() {
  const filterForm = document.querySelector('.tours-filters');
  if (!filterForm) return;
  
  const filters = filterForm.querySelectorAll('input, select');
  filters.forEach(filter => {
    filter.addEventListener('change', handleFilterChange);
  });
}

function handleFilterChange() {
  const tours = document.querySelectorAll('.tour-card');
  const activeFilters = getActiveFilters();
  
  tours.forEach(tour => {
    const shouldShow = matchesFilters(tour, activeFilters);
    tour.style.display = shouldShow ? '' : 'none';
  });
  
  updateResultsCount();
}

function getActiveFilters() {
  const filterForm = document.querySelector('.tours-filters');
  if (!filterForm) return {};
  
  return {
    type: filterForm.querySelector('[name="tour-type"]:checked')?.value || 'all',
    destination: filterForm.querySelector('[name="destination"]')?.value || 'all',
    dateFrom: filterForm.querySelector('[name="date-from"]')?.value || '',
    dateTo: filterForm.querySelector('[name="date-to"]')?.value || '',
  };
}

function matchesFilters(tour, filters) {
  const tourType = tour.dataset.tourType;
  const tourDestination = tour.dataset.destination;
  const tourDate = tour.dataset.date;
  
  if (filters.type !== 'all' && tourType !== filters.type) {
    return false;
  }
  
  if (filters.destination !== 'all' && tourDestination !== filters.destination) {
    return false;
  }
  
  if (filters.dateFrom && tourDate && new Date(tourDate) < new Date(filters.dateFrom)) {
    return false;
  }
  
  if (filters.dateTo && tourDate && new Date(tourDate) > new Date(filters.dateTo)) {
    return false;
  }
  
  return true;
}

function updateResultsCount() {
  const visibleTours = document.querySelectorAll('.tour-card:not([style*="display: none"])').length;
  const countEl = document.querySelector('.tours-results-count');
  if (countEl) {
    countEl.textContent = `${visibleTours} tour${visibleTours !== 1 ? 's' : ''} found`;
  }
}

function initTourCards() {
  const cards = document.querySelectorAll('.tour-card');
  cards.forEach(card => {
    // Add any card-specific interactions here
  });
}

export default { initToursPage };
