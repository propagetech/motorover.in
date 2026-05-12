/**
 * SEO Utilities
 * Enhanced meta tags, structured data, sitemap generation
 */

export function updateMetaTags(data) {
  // Update title
  if (data.title) {
    document.title = data.title;
  }
  
  // Update meta description
  updateMetaTag('description', data.description);
  
  // Update Open Graph tags
  if (data.openGraph) {
    updateMetaTag('og:title', data.openGraph.title || data.title);
    updateMetaTag('og:description', data.openGraph.description || data.description);
    updateMetaTag('og:image', data.openGraph.image);
    updateMetaTag('og:url', data.openGraph.url || window.location.href);
    updateMetaTag('og:type', data.openGraph.type || 'website');
  }
  
  // Update Twitter Card tags
  if (data.twitterCard) {
    updateMetaTag('twitter:card', data.twitterCard.card || 'summary_large_image');
    updateMetaTag('twitter:title', data.twitterCard.title || data.title);
    updateMetaTag('twitter:description', data.twitterCard.description || data.description);
    updateMetaTag('twitter:image', data.twitterCard.image);
  }
  
  // Update canonical URL
  updateCanonical(data.canonical || window.location.href);
}

function updateMetaTag(name, content) {
  if (!content) return;
  
  let meta = document.querySelector(`meta[name="${name}"]`) || 
             document.querySelector(`meta[property="${name}"]`);
  
  if (!meta) {
    meta = document.createElement('meta');
    if (name.startsWith('og:') || name.startsWith('twitter:')) {
      meta.setAttribute('property', name);
    } else {
      meta.setAttribute('name', name);
    }
    document.head.appendChild(meta);
  }
  
  meta.setAttribute('content', content);
}

function updateCanonical(url) {
  let link = document.querySelector('link[rel="canonical"]');
  if (!link) {
    link = document.createElement('link');
    link.setAttribute('rel', 'canonical');
    document.head.appendChild(link);
  }
  link.setAttribute('href', url);
}

export function addStructuredData(data) {
  const script = document.createElement('script');
  script.type = 'application/ld+json';
  script.textContent = JSON.stringify(data);
  document.head.appendChild(script);
}

export function generateTourStructuredData(tour) {
  return {
    '@context': 'https://schema.org',
    '@type': 'TouristTrip',
    name: tour.name,
    description: tour.description,
    url: tour.url,
    provider: {
      '@type': 'Organization',
      name: 'MotoRover',
      url: 'https://www.motorover.in',
    },
    offers: {
      '@type': 'Offer',
      price: tour.price,
      priceCurrency: 'INR',
    },
    itinerary: tour.itinerary?.map(day => ({
      '@type': 'TouristDestination',
      name: day.location,
      description: day.description,
    })),
  };
}

export function generateBreadcrumbStructuredData(items) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

export default {
  updateMetaTags,
  addStructuredData,
  generateTourStructuredData,
  generateBreadcrumbStructuredData,
};
