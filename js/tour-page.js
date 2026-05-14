/* ============================================================
   Tour detail pages — itinerary (non-table), tour types,
   booking-card INR estimate from live FX, responsive grid hints.
   ============================================================ */
(function () {
  'use strict';

  var ITINERARY_MONTH_INDEX = {
    jan: 0,
    feb: 1,
    mar: 2,
    apr: 3,
    may: 4,
    jun: 5,
    jul: 6,
    aug: 7,
    sep: 8,
    oct: 9,
    nov: 10,
    dec: 11
  };
  var ITINERARY_MONTH_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var ITINERARY_WEEKDAY_LONG = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  function parseItineraryMonthDayCell(raw) {
    var s = raw.trim();
    var m = s.match(/^([A-Za-z]{3})\s+(\d{1,2})$/);
    if (!m) {
      return null;
    }
    var monthIndex = ITINERARY_MONTH_INDEX[m[1].toLowerCase()];
    if (monthIndex === undefined) {
      return null;
    }
    var dayNum = parseInt(m[2], 10);
    if (dayNum < 1 || dayNum > 31) {
      return null;
    }
    return { monthIndex: monthIndex, day: dayNum };
  }

  function formatItineraryLongDate(d) {
    return (
      ITINERARY_WEEKDAY_LONG[d.getDay()] +
      ', ' +
      d.getDate() +
      ' ' +
      ITINERARY_MONTH_SHORT[d.getMonth()] +
      ' ' +
      d.getFullYear()
    );
  }

  function escapeHtmlText(s) {
    if (!s) {
      return '';
    }
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /** Formats "Jun 2" style cells to "Tuesday, 2 Jun 2026". Keeps TBA, em dash, etc. Handles year rollover (e.g. Dec → Jan). */
  function formatItineraryDateLabel(raw, state) {
    var parsed = parseItineraryMonthDayCell(raw);
    if (!parsed) {
      return raw;
    }
    var y = state.year;
    var d = new Date(y, parsed.monthIndex, parsed.day);
    var guard = 0;
    while (state.lastMs !== null && d.getTime() <= state.lastMs && guard < 4) {
      y += 1;
      d = new Date(y, parsed.monthIndex, parsed.day);
      guard += 1;
    }
    state.year = y;
    state.lastMs = d.getTime();
    return formatItineraryLongDate(d);
  }

  function enhanceItineraryTables() {
    document.querySelectorAll('table.itinerary-table').forEach(function (table) {
      if (table.dataset.itineraryEnhanced === '1') {
        return;
      }
      var thead = table.querySelector('thead');
      var tbody = table.querySelector('tbody');
      if (!thead || !tbody) {
        return;
      }
      var thEls = thead.querySelectorAll('th');
      if (!thEls.length) {
        return;
      }
      var col = {};
      for (var hi = 0; hi < thEls.length; hi++) {
        col[thEls[hi].textContent.trim().toLowerCase()] = hi;
      }
      function idx(name) {
        return col[name] !== undefined ? col[name] : -1;
      }
      var iDay = idx('day');
      var iDate = idx('date');
      var iRoute = idx('route');
      var iActivity = idx('activity');
      var iMeals = idx('meals');
      var iDist = idx('distance');
      if (iDay < 0 || iRoute < 0 || iActivity < 0 || iDist < 0) {
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
      var yearAttr = parseInt(table.getAttribute('data-itinerary-year'), 10);
      var dateState = {
        year: Number.isFinite(yearAttr) ? yearAttr : 2026,
        lastMs: null
      };
      rows.forEach(function (tr) {
        var tds = tr.querySelectorAll('td');
        if (tds.length < thEls.length) {
          return;
        }
        function cellAt(ix) {
          return ix >= 0 && ix < tds.length ? tds[ix] : null;
        }
        var dayTd = cellAt(iDay);
        var dateTd = cellAt(iDate);
        var routeTd = cellAt(iRoute);
        var activityTd = cellAt(iActivity);
        var mealsTd = cellAt(iMeals);
        var distTd = cellAt(iDist);
        if (!dayTd || !routeTd || !activityTd || !distTd) {
          return;
        }
        var rawDate = dateTd ? dateTd.textContent.trim() : '';
        var dateLabel = iDate >= 0 ? formatItineraryDateLabel(rawDate, dateState) : '';
        var mealsBlock = '';
        if (mealsTd) {
          mealsBlock = '<p class="itinerary-day__meals">' + mealsTd.innerHTML.trim() + '</p>';
        }
        var day = document.createElement('article');
        day.className = 'itinerary-day';
        day.setAttribute('role', 'article');
        day.innerHTML =
          '<div class="itinerary-day__head">' +
          '<span class="itinerary-day__badge-wrap">' +
          dayTd.innerHTML +
          '</span>' +
          '<span class="itinerary-day__date">' +
          escapeHtmlText(dateLabel) +
          '</span>' +
          '</div>' +
          '<p class="itinerary-day__route">' +
          routeTd.textContent.trim() +
          '</p>' +
          '<div class="itinerary-day__activity">' +
          activityTd.innerHTML +
          '</div>' +
          mealsBlock +
          '<p class="itinerary-day__km">' +
          distTd.textContent.trim() +
          '</p>';
        wrap.appendChild(day);
      });
      if (!wrap.children.length) {
        return;
      }
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
    el.setAttribute('aria-label', 'Three ways to do this tour');
    el.innerHTML =
      '<p class="tour-type-legend__title">Three ways to do this tour</p>' +
      '<ul class="tour-type-legend__list">' +
      '<li><span class="tour-type-legend__name">Guided Group Self-Drive Road Trips / Motorcycle Tour</span> ' +
      '<span class="tour-type-legend__desc">Fixed dates | Company of like-minded people | Support team | All related services</span></li>' +
      '<li><span class="tour-type-legend__name">Self Guided Road Trips / Motorcycle Tours</span> ' +
      '<span class="tour-type-legend__desc">Your dates | Your group | Vehicles | Hotels | Route | Transfers</span></li>' +
      '<li><span class="tour-type-legend__name">Bespoke Tours</span> ' +
      '<span class="tour-type-legend__desc">All the goodness of a Guided Tour but your dates, your group.</span></li>' +
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

  function formatTourCurrencyLead(parsed) {
    var num = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(parsed.amount);
    if (parsed.currency === 'USD') {
      return 'USD ' + num;
    }
    if (parsed.currency === 'EUR') {
      return 'Euro ' + num;
    }
    return '';
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
    foot.textContent =
      'Payments to be in Indian Rupees as per the Euro (or USD) exchange rate on the date of transfer.';
    var note = header.querySelector('.booking-card__price-note');
    if (note) {
      note.after(foot);
    } else {
      priceEl.after(foot);
    }

    fetchInrRate(parsed.currency)
      .then(function (rate) {
        var inr = Math.round(parsed.amount * rate);
        var inrFmt = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(inr);
        var lead = formatTourCurrencyLead(parsed);
        if (lead) {
          priceEl.textContent = lead + ' / Rs. ' + inrFmt + ' approx.';
        }
      })
      .catch(function () {
        foot.textContent =
          'Payments to be in Indian Rupees as per the Euro (or USD) exchange rate on the date of transfer. ' +
          'Live INR equivalent estimate is temporarily unavailable.';
      });
  }

  function init() {
    var main = document.querySelector('main');
    if (main) {
      main.classList.add('tour-page-main');
    }
    document.body.classList.add('is-tour-page');
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
