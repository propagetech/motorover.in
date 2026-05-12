/* ============================================================
   Tour detail pages — itinerary (non-table), tour types, INR toggle,
   responsive grid hints. Frankfurter API (no key) for FX.
   ============================================================ */
(function () {
  'use strict';

  function enhanceItineraryTables() {
    document.querySelectorAll('table.itinerary-table').forEach(function (table) {
      if (table.dataset.itineraryEnhanced === '1') {
        return;
      }
      var tbody = table.querySelector('tbody');
      if (!tbody) {
        return;
      }
      var rows = tbody.querySelectorAll('tr');
      if (!rows.length) {
        return;
      }
      var wrap = document.createElement('div');
      wrap.className = 'itinerary-scroll';
      wrap.setAttribute('role', 'region');
      wrap.setAttribute('aria-label', 'Day by day itinerary');
      rows.forEach(function (tr) {
        var tds = tr.querySelectorAll('td');
        if (tds.length < 5) {
          return;
        }
        var day = document.createElement('article');
        day.className = 'itinerary-day';
        day.setAttribute('role', 'article');
        day.innerHTML =
          '<div class="itinerary-day__head">' +
          '<span class="itinerary-day__badge-wrap">' + tds[0].innerHTML + '</span>' +
          '<span class="itinerary-day__date">' + tds[1].textContent.trim() + '</span>' +
          '</div>' +
          '<p class="itinerary-day__route">' + tds[2].textContent.trim() + '</p>' +
          '<div class="itinerary-day__activity">' + tds[3].innerHTML + '</div>' +
          '<p class="itinerary-day__km">' + tds[4].textContent.trim() + '</p>';
        wrap.appendChild(day);
      });
      table.setAttribute('hidden', '');
      table.setAttribute('aria-hidden', 'true');
      table.dataset.itineraryEnhanced = '1';
      table.parentNode.insertBefore(wrap, table);
    });
  }

  function injectTourTypes() {
    var facts = document.querySelector('.booking-card__facts');
    if (!facts || document.querySelector('.tour-type-legend')) {
      return;
    }
    var el = document.createElement('div');
    el.className = 'tour-type-legend';
    el.setAttribute('aria-label', 'Tour formats we offer');
    el.innerHTML =
      '<p class="tour-type-legend__title">Types of tours</p>' +
      '<ul class="tour-type-legend__list">' +
      '<li><span class="tour-type-legend__name">Bespoke tours</span> ' +
      '<span class="tour-type-legend__desc">Private groups, custom dates &amp; routing.</span></li>' +
      '<li><span class="tour-type-legend__name">Self-drive tours</span> ' +
      '<span class="tour-type-legend__desc">Guided convoy self-drive road trips in our SUV programmes.</span></li>' +
      '<li><span class="tour-type-legend__name">Fixed departure guided road trips</span> ' +
      '<span class="tour-type-legend__desc">Scheduled group departures &mdash; dates as listed in this tour.</span></li>' +
      '</ul>';
    facts.parentNode.insertBefore(el, facts.nextSibling);
  }

  function markResponsiveGrids() {
    var root = document.querySelector('.tour-main') || document.querySelector('main');
    if (!root) {
      return;
    }
    root.querySelectorAll('[style*="repeat(2"]').forEach(function (el) {
      var s = el.getAttribute('style');
      if (s && s.indexOf('1fr') !== -1) {
        el.classList.add('tour-grid--2');
      }
    });
    root.querySelectorAll('[style*="repeat(3"]').forEach(function (el) {
      var s = el.getAttribute('style');
      if (s && s.indexOf('1fr') !== -1) {
        el.classList.add('tour-grid--3');
      }
    });
  }

  function parsePriceFromText(text) {
    if (!text || /on request/i.test(text)) {
      return null;
    }
    var usd = text.match(/USD\s*([\d,]+)/i);
    if (usd) {
      return { amount: parseFloat(usd[1].replace(/,/g, '')), currency: 'USD' };
    }
    var eur1 = text.match(/€\s*([\d.,]+)/);
    if (eur1) {
      return { amount: parseFloat(eur1[1].replace(/,/g, '')), currency: 'EUR' };
    }
    var eur2 = text.match(/([\d,]+)\s*EUR/i);
    if (eur2) {
      return { amount: parseFloat(eur2[1].replace(/,/g, '')), currency: 'EUR' };
    }
    return null;
  }

  function fetchInrRate(baseCurrency) {
    var sources = [
      function () {
        return fetch('https://open.er-api.com/v6/latest/' + encodeURIComponent(baseCurrency))
          .then(function (r) {
            if (!r.ok) {
              throw new Error('rate');
            }
            return r.json();
          })
          .then(function (d) {
            var rate = d && d.rates && d.rates.INR;
            if (typeof rate !== 'number') {
              throw new Error('rate');
            }
            return rate;
          });
      },
      function () {
        return fetch('https://api.exchangerate-api.com/v4/latest/' + encodeURIComponent(baseCurrency))
          .then(function (r) {
            if (!r.ok) {
              throw new Error('rate');
            }
            return r.json();
          })
          .then(function (d) {
            var rate = d && d.rates && d.rates.INR;
            if (typeof rate !== 'number') {
              throw new Error('rate');
            }
            return rate;
          });
      }
    ];
    var index = 0;

    function tryNext() {
      var source = sources[index];
      if (!source) {
        return Promise.reject(new Error('rate'));
      }
      index += 1;
      return source().catch(function () {
        return tryNext();
      });
    }

    return tryNext();
  }

  function buildCurrencyUI(priceEl) {
    if (priceEl.dataset.currencyBind === '1') {
      return;
    }
    var raw = priceEl.textContent.trim();
    var parsed = parsePriceFromText(raw);
    if (!parsed) {
      return;
    }
    priceEl.dataset.currencyBind = '1';
    priceEl.dataset.priceOriginal = raw;
    var header = priceEl.closest('.booking-card__header');
    if (!header) {
      return;
    }
    var foot = document.createElement('p');
    foot.className = 'tour-currency-foot';
    foot.textContent = 'Live FX estimate. You pay in INR at the rate on the date of transfer.';

    var group = document.createElement('div');
    group.className = 'tour-currency-toggle';
    group.setAttribute('role', 'group');
    group.setAttribute('aria-label', 'Display price in tour currency or INR');
    var btnTour = document.createElement('button');
    btnTour.type = 'button';
    btnTour.className = 'tour-currency-btn is-active';
    btnTour.setAttribute('aria-pressed', 'true');
    btnTour.textContent = parsed.currency;
    var btnInr = document.createElement('button');
    btnInr.type = 'button';
    btnInr.className = 'tour-currency-btn';
    btnInr.setAttribute('aria-pressed', 'false');
    btnInr.textContent = 'INR (live est.)';
    group.appendChild(btnTour);
    group.appendChild(btnInr);
    var note = header.querySelector('.booking-card__price-note');
    if (note) {
      note.after(foot);
    } else {
      priceEl.after(foot);
    }
    foot.after(group);

    var inrText = null;
    btnTour.setAttribute('disabled', '');
    btnInr.setAttribute('disabled', '');

    function showTour() {
      priceEl.textContent = priceEl.dataset.priceOriginal || raw;
      btnTour.classList.add('is-active');
      btnInr.classList.remove('is-active');
      btnTour.setAttribute('aria-pressed', 'true');
      btnInr.setAttribute('aria-pressed', 'false');
    }
    function showInr() {
      if (!inrText) {
        return;
      }
      priceEl.textContent = inrText;
      btnInr.classList.add('is-active');
      btnTour.classList.remove('is-active');
      btnInr.setAttribute('aria-pressed', 'true');
      btnTour.setAttribute('aria-pressed', 'false');
    }

    fetchInrRate(parsed.currency)
      .then(function (rate) {
        var inr = Math.round(parsed.amount * rate);
        var fmt = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(inr);
        inrText = '≈ ₹ ' + fmt;
        btnTour.removeAttribute('disabled');
        btnInr.removeAttribute('disabled');
        btnTour.addEventListener('click', showTour);
        btnInr.addEventListener('click', showInr);
      })
      .catch(function () {
        foot.textContent = 'INR live estimate unavailable. Prices shown in ' + parsed.currency + ' only.';
        group.setAttribute('hidden', '');
      });
  }

  function init() {
    var main = document.querySelector('main');
    if (main) {
      main.classList.add('tour-page-main');
    }
    enhanceItineraryTables();
    injectTourTypes();
    markResponsiveGrids();
    var priceEl = document.querySelector('.booking-card__header .booking-card__price');
    if (priceEl) {
      buildCurrencyUI(priceEl);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
