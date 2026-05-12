/**
 * Currency Converter Component
 * Real-time currency conversion for tour pricing
 */

const SUPPORTED_CURRENCIES = ['INR', 'USD', 'EUR', 'GBP'];
const DEFAULT_CURRENCY = 'INR';
const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours

let exchangeRates = {};
let lastUpdate = 0;

export async function initCurrencyConverter() {
  await loadExchangeRates();
  setupCurrencySelector();
  updateAllPrices();
}

async function loadExchangeRates() {
  const cached = getCachedRates();
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    exchangeRates = cached.rates;
    return;
  }
  
  try {
    // Use exchangerate-api.com or similar
    const response = await fetch('https://api.exchangerate-api.com/v4/latest/INR');
    const data = await response.json();
    
    exchangeRates = {
      INR: 1,
      USD: data.rates.USD || 0.012,
      EUR: data.rates.EUR || 0.011,
      GBP: data.rates.GBP || 0.0095,
    };
    
    cacheRates(exchangeRates);
  } catch (error) {
    console.error('Failed to load exchange rates:', error);
    // Use fallback rates
    exchangeRates = {
      INR: 1,
      USD: 0.012,
      EUR: 0.011,
      GBP: 0.0095,
    };
  }
}

function getCachedRates() {
  try {
    const cached = localStorage.getItem('exchangeRates');
    return cached ? JSON.parse(cached) : null;
  } catch {
    return null;
  }
}

function cacheRates(rates) {
  try {
    localStorage.setItem('exchangeRates', JSON.stringify({
      rates,
      timestamp: Date.now(),
    }));
  } catch (error) {
    console.error('Failed to cache rates:', error);
  }
}

function setupCurrencySelector() {
  const selector = document.querySelector('.currency-selector');
  if (!selector) return;
  
  // Create currency selector if it doesn't exist
  if (!selector.innerHTML) {
    selector.innerHTML = `
      <label for="currency" class="form__label">Currency</label>
      <select id="currency" class="form__select">
        ${SUPPORTED_CURRENCIES.map(currency => `
          <option value="${currency}" ${currency === getSelectedCurrency() ? 'selected' : ''}>
            ${currency}
          </option>
        `).join('')}
      </select>
    `;
  }
  
  const select = selector.querySelector('#currency');
  select.addEventListener('change', (e) => {
    setSelectedCurrency(e.target.value);
    updateAllPrices();
  });
}

function getSelectedCurrency() {
  return localStorage.getItem('preferredCurrency') || DEFAULT_CURRENCY;
}

function setSelectedCurrency(currency) {
  localStorage.setItem('preferredCurrency', currency);
}

export function convertPrice(priceInINR, targetCurrency) {
  if (!exchangeRates[targetCurrency]) {
    return priceInINR;
  }
  
  const rate = exchangeRates[targetCurrency];
  return priceInINR * rate;
}

export function formatPrice(price, currency) {
  const converted = convertPrice(price, currency);
  
  const formatters = {
    INR: new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }),
    USD: new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }),
    EUR: new Intl.NumberFormat('en-EU', { style: 'currency', currency: 'EUR' }),
    GBP: new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' }),
  };
  
  const formatter = formatters[currency] || formatters[DEFAULT_CURRENCY];
  return formatter.format(converted);
}

function updateAllPrices() {
  const currency = getSelectedCurrency();
  const priceElements = document.querySelectorAll('[data-price-inr]');
  
  priceElements.forEach(element => {
    const priceInINR = parseFloat(element.dataset.priceInr);
    if (!isNaN(priceInINR)) {
      element.textContent = formatPrice(priceInINR, currency);
    }
  });
}

export default {
  initCurrencyConverter,
  convertPrice,
  formatPrice,
};
