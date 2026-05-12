/**
 * API Client Utility
 * Handles all API communication
 */

const API_BASE_URL = process.env.API_BASE_URL || '/api';

export async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };
  
  if (config.body && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body);
  }
  
  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    return { data, error: null };
  } catch (error) {
    console.error('API Request failed:', error);
    return { data: null, error: error.message };
  }
}

// Inquiry API
export async function submitInquiry(inquiryData) {
  return apiRequest('/inquiries', {
    method: 'POST',
    body: inquiryData,
  });
}

// Booking API
export async function createBooking(bookingData) {
  return apiRequest('/bookings', {
    method: 'POST',
    body: bookingData,
  });
}

// Tours API
export async function getTours(filters = {}) {
  const queryParams = new URLSearchParams(filters);
  return apiRequest(`/tours?${queryParams}`);
}

export async function getTour(id) {
  return apiRequest(`/tours/${id}`);
}

export default {
  apiRequest,
  submitInquiry,
  createBooking,
  getTours,
  getTour,
};
