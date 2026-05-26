/* ============================================================
   site.js — universal nav + region-switcher behaviour
   Loaded by EVERY page (linked from the nav partial).
   Page-specific JS (hero scenes, marquee, reveal observer) stays
   inline in src/mockup-*-homepage.html.
   ============================================================ */
(function () {
  'use strict';

  /* ===== Region-switcher dropdown ===== */
  document.querySelectorAll('.region-switch').forEach(function (rs) {
    var trigger = rs.querySelector('.region-switch__trigger');
    if (!trigger) return;
    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = rs.getAttribute('data-open') === 'true';
      rs.setAttribute('data-open', String(!open));
      trigger.setAttribute('aria-expanded', String(!open));
    });
  });

  /* ===== Nav dropdown click-toggle (mobile / keyboard) =====
     On wide viewports the dropdowns open on :hover (pure CSS).
     On narrow viewports the chevron toggles aria-expanded. */
  document.querySelectorAll('.nav__item-group').forEach(function (grp) {
    var trigger = grp.querySelector('.nav__item-trigger');
    if (!trigger) return;
    trigger.addEventListener('click', function (e) {
      if (window.matchMedia('(min-width: 981px)').matches) return;
      e.stopPropagation();
      var open = grp.getAttribute('aria-expanded') === 'true';
      // Close any other open dropdown first
      document.querySelectorAll('.nav__item-group[aria-expanded="true"]').forEach(function (g) {
        if (g !== grp) {
          g.setAttribute('aria-expanded', 'false');
          var t = g.querySelector('.nav__item-trigger');
          if (t) t.setAttribute('aria-expanded', 'false');
        }
      });
      grp.setAttribute('aria-expanded', String(!open));
      trigger.setAttribute('aria-expanded', String(!open));
    });
  });

  /* ===== Close any open dropdown on outside-click ===== */
  document.addEventListener('click', function (e) {
    document.querySelectorAll('.region-switch[data-open="true"]').forEach(function (rs) {
      if (!rs.contains(e.target)) {
        rs.setAttribute('data-open', 'false');
        var t = rs.querySelector('.region-switch__trigger');
        if (t) t.setAttribute('aria-expanded', 'false');
      }
    });
    document.querySelectorAll('.nav__item-group[aria-expanded="true"]').forEach(function (g) {
      if (!g.contains(e.target)) {
        g.setAttribute('aria-expanded', 'false');
        var t = g.querySelector('.nav__item-trigger');
        if (t) t.setAttribute('aria-expanded', 'false');
      }
    });
  });

  /* ===== Close any open dropdown on Escape ===== */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('.region-switch[data-open="true"]').forEach(function (rs) {
      rs.setAttribute('data-open', 'false');
      var t = rs.querySelector('.region-switch__trigger');
      if (t) { t.setAttribute('aria-expanded', 'false'); t.focus(); }
    });
    document.querySelectorAll('.nav__item-group[aria-expanded="true"]').forEach(function (g) {
      g.setAttribute('aria-expanded', 'false');
      var t = g.querySelector('.nav__item-trigger');
      if (t) { t.setAttribute('aria-expanded', 'false'); t.focus(); }
    });
  });

  /* ===== Auto-mark the current page in the nav =====
     Adds aria-current="page" to whichever nav link's href matches
     the current pathname. Lets the active-state CSS take over. */
  (function highlightCurrent() {
    var path = window.location.pathname.replace(/\/+$/, '') || '/';
    document.querySelectorAll('.nav a[href]').forEach(function (a) {
      var hrefPath = a.getAttribute('href').split('#')[0].split('?')[0].replace(/\/+$/, '') || '/';
      if (hrefPath === path) a.setAttribute('aria-current', 'page');
    });
  })();

  /* ===== Count-up animation for [data-count] elements =====
     Animates 0 → target value when the element enters viewport.
     data-count="N"        target value
     data-decimals="0"     decimal places to show
     data-suffix="%"       appended after number
     data-prefix=""        prepended before number
     ===================================================== */
  function animateCount(el) {
    var target   = parseFloat(el.dataset.count);
    var decimals = parseInt(el.dataset.decimals || '0', 10);
    var suffix   = el.dataset.suffix || '';
    var prefix   = el.dataset.prefix || '';
    var duration = 1400;
    var start    = performance.now();
    el.classList.add('counting');

    function tick(now) {
      var t = Math.min(1, (now - start) / duration);
      var eased = 1 - Math.pow(1 - t, 3);
      var value = target * eased;
      el.textContent = prefix
        + value.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
        + suffix;
      if (t < 1) {
        requestAnimationFrame(tick);
      } else {
        el.classList.remove('counting');
        el.classList.add('counted');
      }
    }
    requestAnimationFrame(tick);
  }

  if ('IntersectionObserver' in window) {
    var countObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          animateCount(en.target);
          countObs.unobserve(en.target);
        }
      });
    }, { threshold: 0.45 });
    document.querySelectorAll('[data-count]').forEach(function (el) {
      countObs.observe(el);
    });

    /* ===== Section threads ===== */
    var threadObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('in-view');
          threadObs.unobserve(en.target);
        }
      });
    }, { threshold: 0.4 });
    document.querySelectorAll('[data-thread]').forEach(function (el) {
      threadObs.observe(el);
    });
  } else {
    document.querySelectorAll('[data-count]').forEach(animateCount);
    document.querySelectorAll('[data-thread]').forEach(function (el) {
      el.classList.add('in-view');
    });
  }

  /* ===== Custom cursor follow =====
     Tiny Matcha-bordered dot that follows the cursor with ease-out lag.
     Auto-disables on touch + reduced motion (handled in CSS).
     ===================================================== */
  (function cursorFollow() {
    if (window.matchMedia('(hover: none), (pointer: coarse), (prefers-reduced-motion: reduce)').matches) {
      return;
    }
    var dot = document.createElement('div');
    dot.className = 'cursor-follow';
    dot.setAttribute('aria-hidden', 'true');
    document.body.appendChild(dot);

    var targetX = window.innerWidth / 2;
    var targetY = window.innerHeight / 2;
    var x = targetX;
    var y = targetY;
    var rafId = null;
    var firstMove = true;

    function render() {
      x += (targetX - x) * 0.18;
      y += (targetY - y) * 0.18;
      dot.style.transform = 'translate(' + x + 'px, ' + y + 'px) translate(-50%, -50%)';
      rafId = requestAnimationFrame(render);
    }

    document.addEventListener('mousemove', function (e) {
      targetX = e.clientX;
      targetY = e.clientY;
      if (firstMove) {
        firstMove = false;
        dot.classList.add('is-active');
        rafId = requestAnimationFrame(render);
      }
    });

    document.addEventListener('mouseleave', function () { dot.classList.remove('is-active'); });
    document.addEventListener('mouseenter', function () { dot.classList.add('is-active'); });

    /* Grow on hover over interactive elements */
    var hoverSelector = 'a, button, [role="button"], .btn, .bcard, .pcard, .acard, .proof-tile, .nav__item-trigger';
    document.addEventListener('mouseover', function (e) {
      if (e.target.closest && e.target.closest(hoverSelector)) {
        dot.classList.add('is-hovering');
      }
    });
    document.addEventListener('mouseout', function (e) {
      if (e.target.closest && e.target.closest(hoverSelector)) {
        dot.classList.remove('is-hovering');
      }
    });
  })();

  /* ===== Reimbursement / capacity calculator =====
     Two formulas, picked by which inputs exist inside .calc__widget:
       US: stores × encounters/wk × 3,867 → "$NNN,NNN" annual unlock
       CA: stores × hours       × 11    → "+ N,NNN" consults/month
     Both formulas tuned to match the original static defaults
     ($487,200 for 3×42, +1,840 for 12×14). */
  document.querySelectorAll('[data-calc-widget]').forEach(function (widget) {
    var storesEl     = widget.querySelector('[data-calc-stores]');
    var encountersEl = widget.querySelector('[data-calc-encounters]');
    var hoursEl      = widget.querySelector('[data-calc-hours]');
    var resultEl     = widget.querySelector('[data-calc-result]');
    if (!storesEl || !resultEl) return;

    function clampInt(el) {
      var n = parseInt(el.value, 10);
      if (isNaN(n) || n < 0) n = 0;
      var max = parseInt(el.getAttribute('max') || '999999', 10);
      if (n > max) n = max;
      return n;
    }

    function recalc() {
      var s = clampInt(storesEl);
      var value;
      if (encountersEl) {
        var enc = clampInt(encountersEl);
        value = s * enc * 3867;
        resultEl.textContent = '$' + value.toLocaleString();
      } else if (hoursEl) {
        var hrs = clampInt(hoursEl);
        value = s * hrs * 11;
        resultEl.textContent = '+ ' + value.toLocaleString();
      }
    }

    [storesEl, encountersEl, hoursEl].forEach(function (el) {
      if (el) el.addEventListener('input', recalc);
    });
    recalc();
  });

  /* ===== Cookie consent management =====
     Reads/writes consent state in localStorage. Shows the banner if no
     consent has been recorded; lets users accept all / reject non-essential
     / customize via the modal. Exposes window.MedMeConsent + dispatches
     a `medme:consent-changed` event so any future analytics/marketing
     tools can gate themselves on user choice.

     Compliance approach (strictest superset across GDPR / CCPA / PIPEDA /
     Quebec Law 25): non-essential cookies OFF by default; "reject" has
     equal visual weight to "accept"; granular per-category control;
     re-access via footer "Cookie preferences" link. */
  (function cookieConsent() {
    var STORAGE_KEY = 'medme_consent_v1';
    var banner = document.getElementById('cookieBanner');
    var modal = document.getElementById('cookieModal');
    if (!banner) return;  /* no banner partial on this page (e.g. region picker) */

    function readConsent() {
      try {
        var raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : null;
      } catch (e) { return null; }
    }

    function writeConsent(consent) {
      consent.timestamp = Date.now();
      consent.version = 1;
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(consent)); } catch (e) {}
      window.MedMeConsent = consent;
      document.dispatchEvent(new CustomEvent('medme:consent-changed', { detail: consent }));
    }

    function showBanner() { banner.removeAttribute('hidden'); }
    function hideBanner() { banner.setAttribute('hidden', ''); }
    function showModal() {
      if (!modal) return;
      modal.removeAttribute('hidden');
      var current = readConsent() || { functional: false, analytics: false, marketing: false };
      ['functional', 'analytics', 'marketing'].forEach(function (cat) {
        var box = modal.querySelector('[data-consent-cat="' + cat + '"]');
        if (box) box.checked = !!current[cat];
      });
      var firstFocus = modal.querySelector('.cookie-modal__close');
      if (firstFocus) firstFocus.focus();
    }
    function hideModal() { if (modal) modal.setAttribute('hidden', ''); }

    /* Initial state */
    var existing = readConsent();
    if (!existing) {
      showBanner();
    } else {
      window.MedMeConsent = existing;
    }

    /* Event delegation — works regardless of when banner/modal mounts */
    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-consent-accept]')) {
        writeConsent({ functional: true, analytics: true, marketing: true });
        hideBanner(); hideModal();
      } else if (e.target.closest('[data-consent-reject]')) {
        writeConsent({ functional: false, analytics: false, marketing: false });
        hideBanner(); hideModal();
      } else if (e.target.closest('[data-consent-customize]')) {
        hideBanner();
        showModal();
      } else if (e.target.closest('[data-consent-save]')) {
        var consent = {};
        modal.querySelectorAll('[data-consent-cat]').forEach(function (box) {
          consent[box.dataset.consentCat] = box.checked;
        });
        writeConsent(consent);
        hideModal();
      } else if (e.target.closest('[data-consent-close]')) {
        hideModal();
        /* If user never recorded consent, re-show banner so they can't skip */
        if (!readConsent()) showBanner();
      } else if (e.target.closest('[data-consent-reopen]')) {
        e.preventDefault();
        hideBanner();
        showModal();
      }
    });

    /* Escape closes modal */
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal && !modal.hasAttribute('hidden')) {
        hideModal();
        if (!readConsent()) showBanner();
      }
    });
  })();

  /* ===== Sticky nav pill-shape on scroll =====
     When the user scrolls past ~40px, add `.is-scrolled` to the nav so
     CSS transitions it into a floating rounded-pill panel. Toggle only
     on state change (not on every scroll tick) to keep style-recalc cheap.
     Passive listener so we don't block the scroll thread. */
  (function navPillOnScroll() {
    var nav = document.querySelector('.nav');
    if (!nav) return;
    var threshold = 40;
    var scrolled = false;
    function update() {
      var nowScrolled = window.scrollY > threshold;
      if (nowScrolled !== scrolled) {
        scrolled = nowScrolled;
        nav.classList.toggle('is-scrolled', scrolled);
      }
    }
    update();
    window.addEventListener('scroll', update, { passive: true });
  })();

  /* ===== Mobile hamburger drawer =====
     The .nav__hamburger button toggles the .nav-drawer panel and its
     own aria-expanded state. Closes if the user clicks a drawer link
     or resizes back to desktop. */
  (function navDrawerToggle() {
    var btn = document.querySelector('.nav__hamburger');
    var drawer = document.getElementById('mobile-drawer');
    if (!btn || !drawer) return;
    function setOpen(open) {
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
      document.body.style.overflow = open ? 'hidden' : '';
    }
    btn.addEventListener('click', function () {
      var willOpen = btn.getAttribute('aria-expanded') !== 'true';
      setOpen(willOpen);
    });
    drawer.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
    /* Auto-close when crossing back into desktop layout */
    var mql = matchMedia('(min-width: 769px)');
    function onChange(e) { if (e.matches) setOpen(false); }
    if (mql.addEventListener) mql.addEventListener('change', onChange);
    else if (mql.addListener) mql.addListener(onChange);
  })();

  /* ===== Proof dashboard build-up animation =====
     When the .proof__dashboard enters viewport:
       1. Each <polyline> in .proof-chart "draws" via
          stroke-dasharray + stroke-dashoffset animation
       2. .proof-heatmap cells fade in with stagger (top-left → bottom-right)
       Existing [data-count] handles the 34% / 3.8× count-up. */
  if ('IntersectionObserver' in window) {
    var dashObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;

        /* Line draw: stroke-dashoffset N → 0 */
        var lines = en.target.querySelectorAll('.proof-chart polyline');
        lines.forEach(function (line, i) {
          var len;
          try { len = line.getTotalLength(); } catch (e) { len = 320; }
          line.style.strokeDasharray = len + ' ' + len;
          line.style.strokeDashoffset = len;
          line.getBoundingClientRect(); /* force reflow */
          line.style.transition = 'stroke-dashoffset 1.6s cubic-bezier(0.2, 0.8, 0.2, 1)';
          line.style.transitionDelay = (i * 200) + 'ms';
          line.style.strokeDashoffset = '0';
        });

        /* Heatmap stagger fade — preserve each cell's original opacity */
        var cells = en.target.querySelectorAll('.proof-heatmap span');
        cells.forEach(function (cell, i) {
          var saved = cell.style.opacity || '1';
          cell.style.opacity = '0';
          cell.style.transition = 'opacity 0.4s ease-out';
          setTimeout(function () { cell.style.opacity = saved; }, 600 + i * 22);
        });

        dashObs.unobserve(en.target);
      });
    }, { threshold: 0.4 });
    document.querySelectorAll('.proof__dashboard').forEach(function (d) {
      dashObs.observe(d);
    });
  }
})();
