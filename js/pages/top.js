// ===== Random Photo Assignment =====
  (function() {
    function shuffle(arr) {
      const a = arr.slice();
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    }
    function pick(arr, n) { return shuffle(arr).slice(0, n); }

    const heroPool = [
      'hero_01.jpg','hero_02.jpg','hero_03.jpg','hero_04.jpg','hero_05.jpg',
      'jclass_01.jpg','jclass_02.jpg','jclass_03.jpg',
      'tp52_02.jpg','tp52_03.jpg',
      'endeavour_01.jpg','endeavour_02.jpg','endeavour_03.jpg',
      'classic_01.jpg','classic_02.jpg','classic_03.jpg',
      'silolona_01.jpg','transpac_01.jpg','transpac_02.jpg',
      'hobart_01.jpg','hobart_02.jpg','hobart_03.jpg',
      'arctic_01.jpg','arctic_02.jpg','arctic_03.jpg'
    ];
    const cardPool = [
      'news_main.jpg','news_01.jpg','news_02.jpg','news_03.jpg',
      'fishing_main.jpg','fishing_01.jpg','fishing_02.jpg','fishing_03.jpg',
      'lifestyle_main.jpg','lifestyle_01.jpg','lifestyle_02.jpg','lifestyle_03.jpg',
      'boat_main.jpg','boat_01.jpg','boat_02.jpg','boat_03.jpg',
      'gear_main.jpg','gear_01.jpg','gear_02.jpg','gear_03.jpg',
      'marina_main.jpg','marina_01.jpg','marina_02.jpg','marina_03.jpg',
      'jclass_01.jpg','jclass_02.jpg','jclass_03.jpg',
      'tp52_02.jpg','tp52_03.jpg',
      'imperia_01.jpg','imperia_02.jpg',
      'dragon_01.jpg','dragon_02.jpg',
      'sttropez_01.jpg','sttropez_02.jpg','sttropez_03.jpg',
      'hobart_01.jpg','hobart_02.jpg','hobart_03.jpg',
      'silolona_01.jpg','classic_01.jpg','classic_02.jpg','classic_03.jpg',
      'eilean_01.jpg','eilean_02.jpg',
      'endeavour_01.jpg','endeavour_02.jpg','endeavour_03.jpg',
      'marquesas_01.jpg','marquesas_02.jpg',
      'ponam_01.jpg','transpac_01.jpg','transpac_02.jpg',
      'karakuwa_01.jpg','arctic_01.jpg','arctic_02.jpg','arctic_03.jpg',
      'portugal_01.jpg','portugal_02.jpg'
    ];

    // Hero slides
    const heroPhotos = pick(heroPool, 5);
    document.querySelectorAll('.slide').forEach(function(slide, i) {
      slide.style.backgroundImage = "url('photos/" + heroPhotos[i] + "')";
    });

    // Card images (featured + small)
    const allCards = shuffle(cardPool);
    let idx = 0;
    document.querySelectorAll('.card-img img, .card-img-sm img').forEach(function(img) {
      img.src = 'photos/' + allCards[idx % allCards.length];
      idx++;
    });
  })();

  // ===== Infinite Carousel Slider =====
  (function() {
    const track = document.getElementById('slidesTrack');
    const origSlides = Array.from(document.querySelectorAll('.slide'));
    const TOTAL = origSlides.length;
    const dots = document.querySelectorAll('.dot');

    // Clone all slides and append for seamless loop
    origSlides.forEach(s => {
      const clone = s.cloneNode(true);
      clone.classList.remove('active');
      track.appendChild(clone);
    });
    // Also prepend clones for backward loop
    for (let i = TOTAL - 1; i >= 0; i--) {
      const clone = origSlides[i].cloneNode(true);
      clone.classList.remove('active');
      track.insertBefore(clone, track.firstChild);
    }

    const allSlides = Array.from(track.querySelectorAll('.slide'));
    let current = TOTAL; // start at first real slide (after prepended clones)

    function getSlotW() {
      return document.getElementById('heroSlider').offsetWidth * 0.80;
    }
    function getOffset(idx) {
      const containerW = document.getElementById('heroSlider').offsetWidth;
      const slotW = containerW * 0.80;
      const initOff = containerW * 0.10;
      return initOff - idx * slotW;
    }

    function render(animate) {
      track.style.transition = animate ? 'transform 0.6s cubic-bezier(0.25,0.46,0.45,0.94)' : 'none';
      track.style.transform = 'translateX(' + getOffset(current) + 'px)';
      allSlides.forEach((s, i) => s.classList.toggle('active', i === current));
      const dotIdx = ((current - TOTAL) % TOTAL + TOTAL) % TOTAL;
      dots.forEach((d, i) => d.classList.toggle('active', i === dotIdx));
    }

    function jumpIfNeeded() {
      if (current >= TOTAL * 2) {
        current -= TOTAL;
        render(false);
      } else if (current < TOTAL) {
        current += TOTAL;
        render(false);
      }
    }

    track.addEventListener('transitionend', function(e) {
      if (e.target === track && e.propertyName === 'transform') jumpIfNeeded();
    });

    window.slideTo = function(n) {
      current = TOTAL + n;
      render(true);
      resetTimer();
    };
    window.slideMove = function(dir) {
      current += dir;
      render(true);
      resetTimer();
    };

    let timer = setInterval(function() { window.slideMove(1); }, 6000);
    window.resetTimer = function() {
      clearInterval(timer);
      timer = setInterval(function() { window.slideMove(1); }, 6000);
    };

    window.addEventListener('resize', function() { render(false); });

    // Initial: hidden behind blue overlay, then slide in when overlay reveals
    track.style.transition = 'none';
    track.style.transform = 'translateX(' + (-document.getElementById('heroSlider').offsetWidth) + 'px)';
    allSlides.forEach(s => s.classList.remove('active'));
    setTimeout(function() {
      track.style.transition = 'transform 1.2s cubic-bezier(0.25,0.46,0.45,0.94)';
      track.style.transform = 'translateX(' + getOffset(current) + 'px)';
      allSlides[current].classList.add('active');
      dots.forEach((d, i) => d.classList.toggle('active', i === 0));
    }, 300);
  })();

  // ===== Article navigation =====
  function openArticle(cat, title) {
    const url = 'wireframe_article.html?cat=' + encodeURIComponent(cat) + '&title=' + encodeURIComponent(title);
    window.location.href = url;
  }

  // ===== Smooth scroll =====
  function navClick(e, id) {
    e.preventDefault();
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  }
  function smoothTo(e, id) {
    if (e) e.preventDefault();
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  }

  // ===== Search Overlay =====
  function openSearch() {
    document.getElementById('searchOverlay').classList.add('open');
    setTimeout(() => document.getElementById('searchInput').focus(), 100);
  }
  function closeSearchBox() {
    document.getElementById('searchOverlay').classList.remove('open');
  }
  function closeSearch(e) {
    if (e.target === document.getElementById('searchOverlay')) closeSearchBox();
  }
  function fillSearch(word) {
    document.getElementById('searchInput').value = word;
    document.getElementById('searchInput').focus();
  }

  // ===== ESC key =====
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      closeSearchBox();
      closeMega();
      closeArticle();
    }
  });

  // ===== Toast =====
  let toastTimer;
  function toast(msg) {
    const el = document.getElementById('toast');
    el.textContent = '\u2192 ' + msg;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2000);
  }

  // ===== Mega Menu =====
  const megaMap = {
    'ヨット': 'mega-yacht', 'ボート': 'mega-boat',
    'フィッシング': 'mega-fishing', 'クルージング': 'mega-cruising',
    'ライフスタイル': 'mega-lifestyle', 'グッズ＆ギア': 'mega-gear',
    'トピックス': 'mega-news'
  };
  let activeMega = null;

  function closeMega() {
    document.querySelectorAll('.mega-menu').forEach(m => m.classList.remove('open'));
    document.getElementById('megaOverlay').classList.remove('open');
    document.querySelectorAll('.nav-item > a.has-sub').forEach(a => a.classList.remove('active'));
    activeMega = null;
  }

  document.querySelectorAll('.nav-item > a.has-sub').forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const label = this.textContent.trim();
      const megaId = megaMap[label];
      if (!megaId) return;
      if (activeMega === megaId) { closeMega(); return; }
      closeMega();
      document.getElementById(megaId).classList.add('open');
      document.getElementById('megaOverlay').classList.add('open');
      this.classList.add('active');
      activeMega = megaId;
    });
  });

  // ===== Scrolled Header (compact + hamburger) =====
  (function() {
    var header = document.querySelector('header');
    var threshold = 80;
    var captionWraps = document.querySelectorAll('.slide-caption-wrap');
    window.addEventListener('scroll', function() {
      var y = window.scrollY;
      if (y > threshold) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
      // Hero caption moves up on scroll
      captionWraps.forEach(function(w) {
        w.style.transform = 'translateY(' + (-y * 0.4) + 'px)';
      });
      // Parallax banners
      document.querySelectorAll('.parallax-banner').forEach(function(b) {
        var rect = b.getBoundingClientRect();
        var viewH = window.innerHeight;
        if (rect.bottom > 0 && rect.top < viewH) {
          var ratio = (rect.top + rect.height) / (viewH + rect.height);
          var offset = (ratio - 0.5) * 80;
          b.querySelector('.parallax-banner-img').style.transform = 'translateY(' + offset + 'px)';
        }
      });
    });
  })();

  // Parallax banner random images
  (function() {
    var bannerPhotos = [
      'hero_01.jpg','hero_02.jpg','hero_03.jpg','hero_04.jpg','hero_05.jpg',
      'silolona_01.jpg','sttropez_01.jpg','sttropez_02.jpg',
      'jclass_01.jpg','jclass_02.jpg','transpac_01.jpg',
      'portugal_01.jpg','portugal_02.jpg','arctic_01.jpg','arctic_02.jpg',
      'marquesas_01.jpg','marquesas_02.jpg','eilean_01.jpg'
    ];
    document.querySelectorAll('.parallax-banner-img').forEach(function(img) {
      var photo = bannerPhotos[Math.floor(Math.random() * bannerPhotos.length)];
      img.style.backgroundImage = "url('photos/" + photo + "')";
    });
  })();

  function toggleHamburger() {
    var panel = document.getElementById('hamburgerPanel');
    var backdrop = document.getElementById('hamburgerBackdrop');
    if (panel.classList.contains('open')) {
      closeHamburger();
    } else {
      panel.classList.add('open');
      backdrop.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }
  function closeHamburger() {
    var panel = document.getElementById('hamburgerPanel');
    var backdrop = document.getElementById('hamburgerBackdrop');
    panel.classList.remove('open');
    backdrop.classList.remove('open');
    document.body.style.overflow = '';
  }

  // ===== SDC 右下追従バナー（スクロール600pxで表示） =====
  var floatBannerClosed = false;
  var floatBanner = document.getElementById('sdcFloatBanner');
  window.closeFloatBanner = function() {
    floatBanner.classList.remove('show');
    floatBannerClosed = true;
  };
  window.addEventListener('scroll', function() {
    if (floatBannerClosed) return;
    floatBanner.classList.toggle('show', window.scrollY > 600);
  });

  // ===== Scroll Reveal with IntersectionObserver =====
  (function() {
    const revealElements = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
      revealElements.forEach(function(el) {
        observer.observe(el);
      });
    } else {
      // Fallback for older browsers
      revealElements.forEach(function(el) {
        el.classList.add('visible');
      });
    }
  })();

  // ===== Background Diagonal Stripe Animation =====
  (function() {
    var bgc   = document.getElementById('bgCanvas');
    if (!bgc) return;
    var bgctx = bgc.getContext('2d');

    bgc.width  = window.innerWidth;
    bgc.height = window.innerHeight;
    window.addEventListener('resize', function() {
      bgc.width  = window.innerWidth;
      bgc.height = window.innerHeight;
      stripeRender();
    });

    var ANGLE = 35 * Math.PI / 180;
    var stripes = [
      [-0.05,  1, 0.15, 180, 0.012],
      [ 0.30, -1, 0.25,  60, 0.035],
      [ 0.50,  1, 0.18,   4, 0.12],
      [ 0.60,  1, 0.12, 140, 0.01],
      [ 0.90, -1, 0.30,  45, 0.04],
    ];
    var sPos   = []; for(var i=0;i<stripes.length;i++) sPos.push(0);
    var sWm    = []; for(var i=0;i<stripes.length;i++) sWm.push(1);
    var sVel   = 0;
    var sSmooth= 0;
    var sRaf   = null;
    var sLastY = 0;

    window.addEventListener('scroll', function() {
      var y  = window.scrollY;
      var dy = y - sLastY;
      sLastY = y;
      sVel  += dy * 0.6;
      if (!sRaf) sRaf = requestAnimationFrame(stripeLoop);

      // Hide during hero, show after
      var hero = document.getElementById('heroSlider');
      var heroBottom = hero ? hero.offsetTop + hero.offsetHeight : 0;
      if (y < heroBottom) { bgc.style.opacity = 0; } else { bgc.style.opacity = 1; }
    });

    function stripeLoop() {
      sRaf = null;
      sSmooth += (sVel - sSmooth) * 0.3;
      sVel    *= 0.5;
      for (var i = 0; i < stripes.length; i++) {
        sPos[i] += sSmooth * stripes[i][2] * stripes[i][1] * 0.3;
        var tw   = 1 + Math.abs(sSmooth) * 0.003;
        sWm[i]  += (tw - sWm[i]) * 0.1;
      }
      stripeRender();
      if (Math.abs(sSmooth) > 1.0 || Math.abs(sVel) > 1.0) {
        sRaf = requestAnimationFrame(stripeLoop);
      } else {
        sSmooth = 0; sVel = 0;
        for (var i = 0; i < stripes.length; i++) sWm[i] = 1;
        stripeRender();
        bgc.style.opacity = 0;
      }
    }

    function stripeRender() {
      var W = bgc.width, H = bgc.height;
      var d = Math.sqrt(W * W + H * H) * 1.4;
      bgctx.clearRect(0, 0, W, H);
      for (var i = 0; i < stripes.length; i++) {
        var cx = stripes[i][0] * W + sPos[i];
        // Loop position within screen bounds
        cx = ((cx % W) + W) % W;
        var w  = Math.max(4, stripes[i][3] * sWm[i]);
        bgctx.save();
        bgctx.translate(cx, H / 2);
        bgctx.rotate(ANGLE);
        bgctx.fillStyle = 'rgba(44,95,138,' + stripes[i][4] + ')';
        bgctx.fillRect(-w / 2, -d / 2, w, d);
        bgctx.restore();
      }
    }

    stripeRender();
  })();
