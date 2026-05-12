/**
 * Navigation Utility
 * Generates navigation structure from tour data
 */

export function getNavigationData() {
  // This will be populated from content/entities.json
  // For now, return static structure
  return {
    motorcycleTours: [
      { name: 'Kyrgyzstan - July/August 2025', url: '/motorcycle-silk-route.html' },
      { name: 'Spain & France - September 2025', url: '/motorcycle-spain-and-france.html' },
      { name: 'South Africa - Oct/Nov 2025', url: '/motorcycle-south-africa.html' },
      { name: 'New Zealand - Feb/Mar 2026', url: '/motorcycle-new-zealand.html' },
      { name: 'Spain & Portugal - Mar 2026', url: '/motorcycle-andalucia.html' },
      { name: 'Balkan - April 2026', url: '/motorcycle-balkan.html' },
      { name: 'Morocco - May 2026', url: '/motorcycle-morocco.html' },
      { name: 'Ultimate Alps - July 2026', url: '/motorcycle-ultimate-alps.html' },
      { name: 'Northern Europe - Aug 2026', url: '/motorcycle-northern-europe.html' },
    ],
    carTours: [
      { name: 'Kyrgyzstan Spring Edition - June 2025', url: '/car-kyrgyzstan-spring-edition.html' },
      { name: 'Kyrgyzstan Summer Edition - August 2025', url: '/car-silk-route.html' },
      { name: 'Georgia - Sept 2025', url: '/car-georgia.html' },
      { name: 'Kyrgyzstan Autumn Edition - Oct 2025', url: '/car-silk-route-autumn-edition.html' },
      { name: 'South Africa - Nov 2025', url: '/car-south-africa.html' },
      { name: 'Kyrgyzstan Winter Edition - Dec 2025', url: '/car-silk-route-snow-drive.html' },
      { name: 'Georgia Snow Drive - Feb 2026', url: '/car-georgia-winter-adventure.html' },
      { name: 'NewZealand - Feb 2026', url: '/car-new-zealand.html' },
      { name: 'Russia Winter Edition - Feb/Mar 2026', url: '/russia-winter-adventure.html' },
      { name: 'Balkan Self-Drive Road Trip - April 2026', url: '/car-balkan.html' },
      { name: 'Morocco - Apr/May 2026', url: '/car-morocco.html' },
      { name: 'Kyrgyzstan Spring Edition - May 2026', url: '/car-kyrgyzstan-spring-edition.html' },
      { name: 'Northern Europe - Sept 2026', url: '/car-northern-europe.html' },
    ],
  };
}

export function renderNavigation(navData) {
  const motorcycleTours = navData.motorcycleTours || [];
  const carTours = navData.carTours || [];
  
  return `
    <ul class="nav__list">
      <li class="nav__item">
        <a href="/" class="nav__link" aria-current="${window.location.pathname === '/' ? 'page' : 'false'}">Home</a>
      </li>
      
      <li class="nav__item nav__dropdown" aria-expanded="false">
        <a href="/tours.html" class="nav__link nav__dropdown-toggle">
          Motorcycle Tours
          <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6" />
          </svg>
        </a>
        <ul class="nav__dropdown-menu">
          ${motorcycleTours.map(tour => `
            <li class="nav__dropdown-item">
              <a href="${tour.url}" class="nav__link">${tour.name}</a>
            </li>
          `).join('')}
        </ul>
      </li>
      
      <li class="nav__item nav__dropdown" aria-expanded="false">
        <a href="/tours.html" class="nav__link nav__dropdown-toggle">
          Car Tours
          <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6" />
          </svg>
        </a>
        <ul class="nav__dropdown-menu">
          ${carTours.map(tour => `
            <li class="nav__dropdown-item">
              <a href="${tour.url}" class="nav__link">${tour.name}</a>
            </li>
          `).join('')}
        </ul>
      </li>
      
      <li class="nav__item nav__dropdown" aria-expanded="false">
        <a href="/about.html" class="nav__link nav__dropdown-toggle">
          About Us
          <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6" />
          </svg>
        </a>
        <ul class="nav__dropdown-menu">
          <li class="nav__dropdown-item">
            <a href="/about.html" class="nav__link">Our Story</a>
          </li>
          <li class="nav__dropdown-item">
            <a href="/the-team.html" class="nav__link">Team</a>
          </li>
          <li class="nav__dropdown-item">
            <a href="/the-team.html#official-team" class="nav__link">Official Team</a>
          </li>
          <li class="nav__dropdown-item">
            <a href="/the-team.html#guides" class="nav__link">Guides / Tour Managers</a>
          </li>
        </ul>
      </li>
      
      <li class="nav__item">
        <a href="/contactus.html" class="nav__link" aria-current="${window.location.pathname.includes('contact') ? 'page' : 'false'}">Contact Us</a>
      </li>
      
      <li class="nav__item">
        <a href="/why-us.html" class="nav__link" aria-current="${window.location.pathname.includes('why-us') ? 'page' : 'false'}">Why Us</a>
      </li>
      
      <li class="nav__item">
        <a href="/faq.html" class="nav__link" aria-current="${window.location.pathname.includes('FAQ') ? 'page' : 'false'}">FAQ</a>
      </li>
    </ul>
  `;
}
