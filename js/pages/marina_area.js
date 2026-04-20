let toastTimer;
  function toast(msg) { const el = document.getElementById('toast'); el.textContent = '→ ' + msg; el.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('show'), 2000); }
  document.querySelectorAll('.sort-btn').forEach(btn => { btn.addEventListener('click', e => { e.preventDefault(); document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active')); btn.classList.add('active'); }); });
  document.querySelectorAll('.region-btn').forEach(btn => { btn.addEventListener('click', e => { e.preventDefault(); document.querySelectorAll('.region-btn').forEach(b => b.classList.remove('active')); btn.classList.add('active'); }); });

  // ドロップダウン クリック開閉
  document.querySelectorAll('.nav-item > a.has-sub').forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      var item = this.closest('.nav-item');
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.nav-item').forEach(function(i) { i.classList.remove('open'); });
      if (!isOpen) item.classList.add('open');
    });
  });
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.nav-item')) {
      document.querySelectorAll('.nav-item').forEach(function(i) { i.classList.remove('open'); });
    }
  });

  // ===== 検索ポップアップ =====
  function openSearch() { document.getElementById('searchOverlay').classList.add('open'); }
  function closeSearchBox() { document.getElementById('searchOverlay').classList.remove('open'); }
  function closeSearch(e) { if (e.target === document.getElementById('searchOverlay')) closeSearchBox(); }
  function fillSearch(kw) { var el = document.getElementById('searchInput'); if(el){ el.value = kw; el.focus(); } }
  
  // ===== Mega Menu =====
  const megaMap = {
    'ニュース': 'mega-news', 'フィッシング': 'mega-fishing',
    'マリングッズ・ギア': 'mega-gear', 'ヨット': 'mega-yacht',
    'ボート': 'mega-boat', 'マリーナ': 'mega-marina',
    'ライフスタイル': 'mega-lifestyle'
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

  // ===== Scrolled Header =====
  (function() {
    var header = document.querySelector('header');
    var threshold = 80;
    window.addEventListener('scroll', function() {
      if (window.scrollY > threshold) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  })();

  function toggleHamburger() {
    var panel = document.getElementById('hamburgerPanel');
    var backdrop = document.getElementById('hamburgerBackdrop');
    if (panel.classList.contains('open')) { closeHamburger(); } else {
      panel.classList.add('open'); backdrop.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }
  function closeHamburger() {
    document.getElementById('hamburgerPanel').classList.remove('open');
    document.getElementById('hamburgerBackdrop').classList.remove('open');
    document.body.style.overflow = '';
  }


  // ===== Background Diagonal Stripe Animation =====
  (function() {
    var bgc = document.getElementById('bgCanvas');
    if (!bgc) return;
    var bgctx = bgc.getContext('2d');
    bgc.width = window.innerWidth; bgc.height = window.innerHeight;
    window.addEventListener('resize', function() {
      bgc.width = window.innerWidth; bgc.height = window.innerHeight;
      stripeRender();
    });
    var ANGLE = 35 * Math.PI / 180;
    var stripes = [
      [-0.05, 1, 0.15, 180, 0.012],
      [ 0.30,-1, 0.25,  60, 0.035],
      [ 0.50, 1, 0.18,   4, 0.12],
      [ 0.60, 1, 0.12, 140, 0.01],
      [ 0.90,-1, 0.30,  45, 0.04],
    ];
    var sPos=[],sWm=[]; for(var i=0;i<stripes.length;i++){sPos.push(0);sWm.push(1);}
    var sVel=0, sSmooth=0, sRaf=null, sLastY=0;
    window.addEventListener('scroll', function() {
      var y=window.scrollY, dy=y-sLastY; sLastY=y;
      sVel += dy * 0.6;
      if (!sRaf) sRaf = requestAnimationFrame(stripeLoop);
    });
    function stripeLoop() {
      sRaf=null;
      sSmooth += (sVel-sSmooth)*0.3; sVel *= 0.5;
      for(var i=0;i<stripes.length;i++){
        sPos[i]+=sSmooth*stripes[i][2]*stripes[i][1]*0.3;
        var tw=1+Math.abs(sSmooth)*0.003; sWm[i]+=(tw-sWm[i])*0.1;
      }
      stripeRender();
      if(Math.abs(sSmooth)>1.0||Math.abs(sVel)>1.0){
        sRaf=requestAnimationFrame(stripeLoop);
      } else {
        sSmooth=0;sVel=0;
        for(var i=0;i<stripes.length;i++) sWm[i]=1;
        stripeRender(); bgc.style.opacity=0;
      }
    }
    function stripeRender() {
      var W=bgc.width,H=bgc.height,d=Math.sqrt(W*W+H*H)*1.4;
      bgctx.clearRect(0,0,W,H);
      for(var i=0;i<stripes.length;i++){
        var cx=stripes[i][0]*W+sPos[i]; cx=((cx%W)+W)%W;
        var w=Math.max(4,stripes[i][3]*sWm[i]);
        bgctx.save(); bgctx.translate(cx,H/2); bgctx.rotate(ANGLE);
        bgctx.fillStyle="rgba(44,95,138,"+stripes[i][4]+")";
        bgctx.fillRect(-w/2,-d/2,w,d); bgctx.restore();
      }
    }
    stripeRender();
  })();
  // ===== Scroll Reveal =====
  var revEls = document.querySelectorAll('.reveal');
  var revObs = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
  revEls.forEach(function(el) { revObs.observe(el); });
