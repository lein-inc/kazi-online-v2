// URLパラメータから記事情報を取得
  const params = new URLSearchParams(window.location.search);
  const cat   = params.get('cat')   || 'フィッシング';
  const title = params.get('title') || '記事タイトルがここに入ります。SEOを意識したキーワードを含む詳細タイトル';

  document.getElementById('catBadge').textContent    = cat;
  document.getElementById('articleTitle').textContent = title;
  document.getElementById('breadCat').textContent    = cat;
  document.getElementById('breadTitle').textContent  = title.length > 30 ? title.slice(0,30)+'…' : title;
  document.getElementById('bodySubject').textContent  = cat;
  document.getElementById('bodySubject2').textContent = cat;
  ['relCat1','relCat2','relCat3','relCat4'].forEach(id => { var el = document.getElementById(id); if (el) el.textContent = cat; });
  document.title = title + ' - KAZI ONLINE';

  // タグをカテゴリーに合わせて更新
  const tagMap = {
    'フィッシング':      ['#ルアー', '#タックル', '#釣り入門', '#魚種別'],
    'ライフスタイル':    ['#マリンファッション', '#グルメ', '#リゾート', '#トラベル'],
    'ボート':            ['#ボートレビュー', '#2馬力', '#トレーラブル', '#購入ガイド'],
    'ヨット':            ['#ヨット', '#セーリング', '#レース', '#購入ガイド'],
    'マリングッズ・ギア':['#マリンウェア', '#ライフジャケット', '#パドルスポーツ', '#ギア'],
    'マリーナ':          ['#マリーナ', '#係留', '#エリア別', '#マリーナマップ'],
    'ニュース':          ['#新製品', '#イベント', '#ランキング', '#展示会'],
  };
  const tags = tagMap[cat] || ['#タグ1', '#タグ2', '#タグ3', '#タグ4'];
  const tagHtml = tags.map(t =>
    `<a class="article-tag" href="#" onclick="toast('${t}で絞り込み');return false;">${t}</a>`
  ).join('');
  document.getElementById('articleTags').innerHTML     = tagHtml;
  document.getElementById('articleTagsBottom').innerHTML = tagHtml;

  // 目次の開閉
  let tocOpen = true;
  function toggleToc() {
    tocOpen = !tocOpen;
    document.getElementById('tocContent').style.display = tocOpen ? '' : 'none';
    document.querySelector('.toc-toggle').textContent = tocOpen ? '[閉じる]' : '[開く]';
  }

  // 目次スクロール
  function scrollToSec(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  }

  // ページトップへ戻るボタン（スクロール量で表示）
  const backBtn = document.getElementById('backToTop');
  window.addEventListener('scroll', () => {
    backBtn.classList.toggle('show', window.scrollY > 400);
  });

  // SDC Scroll Popup（スクロール800pxで表示・ページ訪問中1回のみ）
  var sdcPopupDone = false;
  window.closeSdcPopup = function() {
    document.getElementById('sdcPopupOverlay').classList.remove('open');
    document.getElementById('sdcPopup').classList.remove('open');
    sdcPopupDone = true;
  };
  window.addEventListener('scroll', function() {
    if (sdcPopupDone) return;
    if (window.scrollY > 800) {
      sdcPopupDone = true;
      document.getElementById('sdcPopupOverlay').classList.add('open');
      document.getElementById('sdcPopup').classList.add('open');
    }
  });

  // 検索ポップアップ
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
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSearchBox();
  });

  // トースト
  let toastTimer;
  function toast(msg) {
    const el = document.getElementById('toast');
    el.textContent = '→ ' + msg;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2000);
  }

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

  // Scroll Reveal
  const revealElements = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
  revealElements.forEach(el => revealObserver.observe(el));

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
