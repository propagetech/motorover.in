/**
 * Tour Card Component
 * Reusable tour card with image, title, price, and CTA
 */

export function createTourCard(tour) {
  const card = document.createElement('article');
  card.className = 'card card--simple tour-card';
  card.dataset.tourType = tour.type || 'motorcycle';
  card.dataset.destination = tour.destination || '';
  card.dataset.date = tour.date || '';
  
  card.innerHTML = `
    <div class="card__image-wrapper">
      <img 
        src="${tour.image || '/assets/img/tour-placeholder.jpg'}" 
        alt="${tour.name}" 
        class="card__image" 
        loading="lazy"
        onerror="this.src='/assets/img/tour-placeholder.jpg'"
      >
      ${tour.badge ? `<span class="card__badge card__badge--${tour.badge}">${tour.badge}</span>` : ''}
    </div>
    <div class="card__body">
      <h3 class="card__title">${tour.name}</h3>
      ${tour.description ? `<p class="card__content">${tour.description}</p>` : ''}
      ${tour.price ? `
        <div class="card__price">
          <span class="card__price-label">Starting from</span>
          <span class="card__price-amount">${tour.price}</span>
        </div>
      ` : ''}
      <a href="${tour.url}" class="btn btn--know-more">KNOW MORE</a>
    </div>
  `;
  
  return card;
}

export function renderTourCards(container, tours) {
  if (!container) return;
  
  container.innerHTML = '';
  tours.forEach(tour => {
    const card = createTourCard(tour);
    container.appendChild(card);
  });
}

export default { createTourCard, renderTourCards };
