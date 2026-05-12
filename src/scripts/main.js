/**
 * Main JavaScript - Enhanced
 * Initializes all components and features
 */

import { initHeader } from '../components/Header.js';
import { initNewsletter } from '../components/Newsletter.js';
import { initInquiryForm } from '../components/InquiryForm.js';
import { initBookingFlow } from '../components/BookingFlow.js';
import { initCurrencyConverter } from '../components/CurrencyConverter.js';
import { initMotorcycleSelector } from '../components/MotorcycleSelector.js';
import { initAITravelAssistant } from '../components/AITravelAssistant.js';
import { initToursPage } from '../pages/Tours.js';
import { initBlogPage } from '../pages/Blog.js';
import { initAnalytics } from '../utils/analytics.js';

(function() {
  'use strict';
  
  // Initialize when DOM is ready
  function init() {
    // Core components
    initHeader();
    initNewsletter();
    initInquiryForm();
    initAnalytics();
    
    // Page-specific components
    if (document.querySelector('.booking-flow')) {
      initBookingFlow();
    }
    
    if (document.querySelector('.currency-selector')) {
      initCurrencyConverter();
    }
    
    if (document.querySelector('.motorcycle-selector')) {
      initMotorcycleSelector();
    }
    
    if (document.querySelector('.ai-assistant')) {
      initAITravelAssistant();
    }
    
    if (document.querySelector('.tours-page')) {
      initToursPage();
    }
    
    if (document.querySelector('.blog-page')) {
      initBlogPage();
    }
    
    // Initialize existing features from original main.js
    initMobileNav();
    initFAQAccordion();
    initLightbox();
    initSmoothScroll();
    initCarousel();
  }
  
  // Mobile Navigation (from original main.js)
  function initMobileNav() {
    const navToggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('.nav');
    
    if (!navToggle || !nav) return;
    
    navToggle.addEventListener('click', function() {
      const isExpanded = nav.getAttribute('aria-expanded') === 'true';
      nav.setAttribute('aria-expanded', !isExpanded);
      navToggle.setAttribute('aria-expanded', !isExpanded);
    });
  }
  
  // FAQ Accordion (from original main.js)
  function initFAQAccordion() {
    const faqs = document.querySelectorAll('.faq');
    faqs.forEach(function(faq) {
      const summary = faq.querySelector('.faq__question');
      if (!summary || faq.tagName === 'DETAILS') return;
      
      summary.setAttribute('role', 'button');
      summary.setAttribute('aria-expanded', 'false');
      
      summary.addEventListener('click', function(event) {
        event.preventDefault();
        const isExpanded = summary.getAttribute('aria-expanded') === 'true';
        summary.setAttribute('aria-expanded', !isExpanded);
        faq.classList.toggle('faq--open');
      });
    });
  }
  
  // Lightbox (from original main.js)
  function initLightbox() {
    const galleryItems = document.querySelectorAll('.gallery__item img');
    galleryItems.forEach(function(img) {
      img.style.cursor = 'pointer';
      img.addEventListener('click', function() {
        // Simple lightbox implementation
        const overlay = document.createElement('div');
        overlay.style.cssText = `
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.9);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 10000;
          cursor: pointer;
        `;
        
        const lightboxImg = document.createElement('img');
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt;
        lightboxImg.style.cssText = 'max-width: 90%; max-height: 90%; object-fit: contain;';
        
        overlay.appendChild(lightboxImg);
        document.body.appendChild(overlay);
        document.body.style.overflow = 'hidden';
        
        overlay.addEventListener('click', function() {
          document.body.removeChild(overlay);
          document.body.style.overflow = '';
        });
      });
    });
  }
  
  // Smooth Scroll (from original main.js)
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
      anchor.addEventListener('click', function(event) {
        const href = this.getAttribute('href');
        if (href === '#' || href === '#main-content') return;
        
        const target = document.querySelector(href);
        if (target) {
          event.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }
  
  // Carousel (from original main.js)
  function initCarousel() {
    const carousel = document.querySelector('.carousel');
    if (!carousel) return;
    
    const track = carousel.querySelector('.carousel__track');
    const prevButton = carousel.querySelector('.carousel__button--prev');
    const nextButton = carousel.querySelector('.carousel__button--next');
    const cards = carousel.querySelectorAll('.card--tour');
    
    if (!track || !prevButton || !nextButton || cards.length === 0) return;
    
    let currentIndex = 0;
    
    function updateCarousel() {
      const cardWidth = cards[0].offsetWidth;
      const gap = parseInt(getComputedStyle(track).gap) || 24;
      const translateX = -currentIndex * (cardWidth + gap);
      track.style.transform = `translateX(${translateX}px)`;
    }
    
    prevButton.addEventListener('click', () => {
      if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
      }
    });
    
    nextButton.addEventListener('click', () => {
      if (currentIndex < cards.length - 1) {
        currentIndex++;
        updateCarousel();
      }
    });
    
    updateCarousel();
  }
  
  // Initialize
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
