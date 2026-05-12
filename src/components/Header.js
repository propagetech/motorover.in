/**
 * Header Component with Enhanced Navigation
 * Includes dropdowns for Motorcycle Tours, Car Tours, and About Us
 */

export function initHeader() {
  const header = document.querySelector('.header');
  if (!header) return;

  // Initialize mobile navigation
  initMobileNav();
  
  // Initialize dropdowns
  initDropdowns();
  
  // Initialize theme toggle (if not already initialized)
  if (!document.getElementById('theme-toggle')) {
    initThemeToggle();
  }
}

function initMobileNav() {
  const navToggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.nav');
  
  if (!navToggle || !nav) return;
  
  navToggle.addEventListener('click', function() {
    const isExpanded = nav.getAttribute('aria-expanded') === 'true';
    nav.setAttribute('aria-expanded', !isExpanded);
    navToggle.setAttribute('aria-expanded', !isExpanded);
    
    // Prevent body scroll when menu is open
    if (!isExpanded) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  });
  
  // Close nav when clicking outside
  document.addEventListener('click', function(event) {
    if (!nav.contains(event.target) && !navToggle.contains(event.target)) {
      nav.setAttribute('aria-expanded', 'false');
      navToggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
  });
  
  // Close nav on escape key
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && nav.getAttribute('aria-expanded') === 'true') {
      nav.setAttribute('aria-expanded', 'false');
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.focus();
      document.body.style.overflow = '';
    }
  });
}

function initDropdowns() {
  const dropdowns = document.querySelectorAll('.nav__dropdown');
  
  dropdowns.forEach(dropdown => {
    const toggle = dropdown.querySelector('.nav__dropdown-toggle');
    const menu = dropdown.querySelector('.nav__dropdown-menu');
    
    if (!toggle || !menu) return;
    
    // Desktop: hover to open
    if (window.innerWidth > 768) {
      dropdown.addEventListener('mouseenter', () => {
        dropdown.setAttribute('aria-expanded', 'true');
      });
      
      dropdown.addEventListener('mouseleave', () => {
        dropdown.setAttribute('aria-expanded', 'false');
      });
    }
    
    // Mobile: click to toggle
    if (window.innerWidth <= 768) {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const isExpanded = dropdown.getAttribute('aria-expanded') === 'true';
        dropdown.setAttribute('aria-expanded', !isExpanded);
      });
    }
    
    // Keyboard navigation
    toggle.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const isExpanded = dropdown.getAttribute('aria-expanded') === 'true';
        dropdown.setAttribute('aria-expanded', !isExpanded);
      }
    });
  });
  
  // Handle window resize
  let resizeTimeout;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      dropdowns.forEach(dropdown => {
        dropdown.setAttribute('aria-expanded', 'false');
      });
    }, 250);
  });
}

function initThemeToggle() {
  // Theme toggle is handled by theme.js
  // This is just a placeholder if needed
}

// Export for use in other modules
export default { initHeader };
