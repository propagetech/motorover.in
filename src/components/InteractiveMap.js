/**
 * Interactive Map Component
 * Map integration with destination pins and itinerary display
 */

export function initInteractiveMap(containerId, tourData) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  // Check if Mapbox or Google Maps is available
  if (window.mapboxgl) {
    initMapboxMap(container, tourData);
  } else if (window.google && window.google.maps) {
    initGoogleMap(container, tourData);
  } else {
    // Fallback: show static map or message
    container.innerHTML = '<p>Map loading...</p>';
    loadMapLibrary(tourData);
  }
}

function initMapboxMap(container, tourData) {
  mapboxgl.accessToken = process.env.MAPBOX_TOKEN || '';
  
  const map = new mapboxgl.Map({
    container: containerId,
    style: 'mapbox://styles/mapbox/streets-v11',
    center: tourData.center || [0, 0],
    zoom: tourData.zoom || 5,
  });
  
  // Add markers for each destination
  tourData.destinations?.forEach((dest, index) => {
    const marker = new mapboxgl.Marker()
      .setLngLat([dest.lng, dest.lat])
      .setPopup(new mapboxgl.Popup().setHTML(`
        <div class="map-popup">
          <h4>Day ${index + 1}: ${dest.name}</h4>
          <p>${dest.description || ''}</p>
        </div>
      `))
      .addTo(map);
  });
  
  // Draw route if coordinates provided
  if (tourData.route) {
    map.on('load', () => {
      map.addSource('route', {
        type: 'geojson',
        data: {
          type: 'Feature',
          properties: {},
          geometry: {
            type: 'LineString',
            coordinates: tourData.route,
          },
        },
      });
      
      map.addLayer({
        id: 'route',
        type: 'line',
        source: 'route',
        layout: {
          'line-join': 'round',
          'line-cap': 'round',
        },
        paint: {
          'line-color': '#2563eb',
          'line-width': 3,
        },
      });
    });
  }
}

function initGoogleMap(container, tourData) {
  const map = new google.maps.Map(container, {
    center: tourData.center || { lat: 0, lng: 0 },
    zoom: tourData.zoom || 5,
  });
  
  // Add markers
  tourData.destinations?.forEach((dest, index) => {
    const marker = new google.maps.Marker({
      position: { lat: dest.lat, lng: dest.lng },
      map,
      title: `Day ${index + 1}: ${dest.name}`,
    });
    
    const infoWindow = new google.maps.InfoWindow({
      content: `
        <div class="map-popup">
          <h4>Day ${index + 1}: ${dest.name}</h4>
          <p>${dest.description || ''}</p>
        </div>
      `,
    });
    
    marker.addListener('click', () => {
      infoWindow.open(map, marker);
    });
  });
  
  // Draw route
  if (tourData.route) {
    const routePath = new google.maps.Polyline({
      path: tourData.route.map(coord => ({ lat: coord[1], lng: coord[0] })),
      geodesic: true,
      strokeColor: '#2563eb',
      strokeOpacity: 1.0,
      strokeWeight: 3,
    });
    
    routePath.setMap(map);
  }
}

function loadMapLibrary(tourData) {
  // Load Mapbox by default (can be changed to Google Maps)
  const script = document.createElement('script');
  script.src = 'https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js';
  script.onload = () => {
    initMapboxMap(document.getElementById(containerId), tourData);
  };
  document.head.appendChild(script);
  
  const link = document.createElement('link');
  link.href = 'https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css';
  link.rel = 'stylesheet';
  document.head.appendChild(link);
}

export default { initInteractiveMap };
