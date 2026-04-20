/* ============================================================
   KAZI ONLINE v2 — UX Enhancements
   Loaded after page-specific JS
   ============================================================ */

(function() {
  'use strict';

  /* === 1. Keyboard Shortcut: "/" to open search === */
  document.addEventListener('keydown', function(e) {
    // Don't trigger if user is typing in an input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) return;

    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      var overlay = document.querySelector('.search-overlay');
      if (overlay) {
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        var input = overlay.querySelector('input[type="text"]');
        if (input) {
          setTimeout(function() { input.focus(); }, 100);
        }
      }
    }
  });

  /* === 2. SDC Popup: Delay + localStorage suppression === */
  (function() {
    var POPUP_KEY = 'sdc_popup_dismissed';
    var POPUP_DELAY = 60000; // 60 seconds
    var SUPPRESS_DAYS = 7;

    // Check if popup was recently dismissed
    var dismissed = localStorage.getItem(POPUP_KEY);
    if (dismissed) {
      var dismissedDate = new Date(parseInt(dismissed));
      var daysSince = (Date.now() - dismissedDate) / (1000 * 60 * 60 * 24);
      if (daysSince < SUPPRESS_DAYS) {
        // Prevent popup from showing
        var style = document.createElement('style');
        style.textContent = '.sdc-popup-overlay { display: none !important; }';
        document.head.appendChild(style);
        return;
      }
    }

    // Override popup trigger to use delay instead of scroll position
    var popupOverlay = document.querySelector('.sdc-popup-overlay');
    if (popupOverlay) {
      // Remove any existing scroll-based trigger
      popupOverlay.style.display = 'none';

      // Show popup after delay
      setTimeout(function() {
        // Only show if user hasn't dismissed
        if (!localStorage.getItem(POPUP_KEY)) {
          popupOverlay.style.display = '';
          popupOverlay.classList.add('active');
        }
      }, POPUP_DELAY);

      // Handle close button
      var closeBtn = popupOverlay.querySelector('.sdc-popup-close');
      if (closeBtn) {
        var originalClick = closeBtn.onclick;
        closeBtn.onclick = function(e) {
          localStorage.setItem(POPUP_KEY, Date.now().toString());
          if (originalClick) originalClick.call(this, e);
        };
      }
    }
  })();

  /* === 3. SDC Float Banner: Show once per session === */
  (function() {
    var BANNER_KEY = 'sdc_banner_closed';
    var banner = document.querySelector('.sdc-float-banner');
    if (!banner) return;

    if (sessionStorage.getItem(BANNER_KEY)) {
      banner.style.display = 'none';
      return;
    }

    var closeBtn = banner.querySelector('.sdc-float-banner-close');
    if (closeBtn) {
      var originalClick = closeBtn.onclick;
      closeBtn.addEventListener('click', function() {
        sessionStorage.setItem(BANNER_KEY, '1');
      });
    }
  })();

  /* === 4. Image lazy loading enhancement === */
  (function() {
    // Add loading="lazy" to images that don't have it
    var images = document.querySelectorAll('img:not([loading])');
    images.forEach(function(img) {
      // Don't lazy-load above-the-fold images
      var rect = img.getBoundingClientRect();
      if (rect.top > window.innerHeight) {
        img.setAttribute('loading', 'lazy');
      }
    });
  })();

  /* === 6. Smooth scroll for anchor links === */
  document.querySelectorAll('a[href^="#"]').forEach(function(link) {
    link.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

})();
