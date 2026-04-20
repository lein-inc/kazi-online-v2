#!/usr/bin/env python3
"""Update mega menus, hamburger nav, and footer sitemap to match new subcategory structure.

Subcategories (from spreadsheet):
- ヨット: ヨットの紹介、レース、ハウツー
- ボート: ボートの紹介、エンジン、ハウツー
- フィッシング: ルアー、船釣り、釣り入門 (dummy)
- クルージング: 国内クルーズ、海外クルーズ、クルージング入門 (dummy)
- ライフスタイル: ファッション、グルメ、時計、クルマ、客船、リゾート
- グッズ＆ギア: マリンウェア、安全装備、パドルスポーツ (dummy)
- トピックス: ニュース、イベント、ランキング (dummy)
"""

import os, re, glob

V2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(V2_DIR)

# ============================================================
# NEW MEGA MENUS (flat subcategories only, no sub-sub)
# ============================================================
NEW_MEGA_MENUS = '''<!-- Mega Menu: ヨット -->
<div class="mega-menu" id="mega-yacht">
  <div class="mega-menu-header"><a href="wireframe_yacht.html" class="mega-title" style="text-decoration:none;color:inherit">ヨット</a></div>
  <div class="mega-menu-body">
    <a href="wireframe_yacht_review.html">ヨットの紹介</a>
    <a href="wireframe_yacht_race.html">レース</a>
    <a href="wireframe_yacht_technique.html">ハウツー</a>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: ボート -->
<div class="mega-menu" id="mega-boat">
  <div class="mega-menu-header"><a href="wireframe_boat.html" class="mega-title" style="text-decoration:none;color:inherit">ボート</a></div>
  <div class="mega-menu-body">
    <a href="wireframe_boat_review.html">ボートの紹介</a>
    <a href="wireframe_boat_technique.html">エンジン</a>
    <a href="wireframe_boat_guide.html">ハウツー</a>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: フィッシング -->
<div class="mega-menu" id="mega-fishing">
  <div class="mega-menu-header"><a href="wireframe_fishing.html" class="mega-title" style="text-decoration:none;color:inherit">フィッシング</a></div>
  <div class="mega-menu-body">
    <a href="wireframe_fishing_lure.html">ルアー</a>
    <a href="wireframe_fishing_species.html">船釣り</a>
    <a href="wireframe_fishing_beginner.html">釣り入門</a>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: クルージング -->
<div class="mega-menu" id="mega-cruising">
  <div class="mega-menu-header"><a href="#" class="mega-title" style="text-decoration:none;color:inherit" onclick="toast('クルージング');return false;">クルージング</a></div>
  <div class="mega-menu-body">
    <a href="#" onclick="toast('国内クルーズ');return false;">国内クルーズ</a>
    <a href="#" onclick="toast('海外クルーズ');return false;">海外クルーズ</a>
    <a href="#" onclick="toast('クルージング入門');return false;">クルージング入門</a>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: ライフスタイル -->
<div class="mega-menu" id="mega-lifestyle">
  <div class="mega-menu-header"><a href="wireframe_lifestyle.html" class="mega-title" style="text-decoration:none;color:inherit">ライフスタイル</a></div>
  <div class="mega-menu-body">
    <a href="wireframe_lifestyle_fashion.html">ファッション</a>
    <a href="wireframe_lifestyle_gourmet.html">グルメ</a>
    <a href="#" onclick="toast('時計');return false;">時計</a>
    <a href="#" onclick="toast('クルマ');return false;">クルマ</a>
    <a href="#" onclick="toast('客船');return false;">客船</a>
    <a href="wireframe_lifestyle_hotel.html">リゾート</a>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: グッズ＆ギア -->
<div class="mega-menu" id="mega-gear">
  <div class="mega-menu-header"><a href="wireframe_gear.html" class="mega-title" style="text-decoration:none;color:inherit">グッズ＆ギア</a></div>
  <div class="mega-menu-body">
    <a href="wireframe_gear_wear.html">マリンウェア</a>
    <a href="wireframe_gear_lifejacket.html">安全装備</a>
    <a href="wireframe_gear_paddle.html">パドルスポーツ</a>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: トピックス -->
<div class="mega-menu" id="mega-news">
  <div class="mega-menu-header"><a href="wireframe_news.html" class="mega-title" style="text-decoration:none;color:inherit">トピックス</a></div>
  <div class="mega-menu-body">
    <a href="wireframe_news.html">ニュース</a>
    <a href="wireframe_news_events.html">イベント</a>
    <a href="wireframe_news_ranking.html">ランキング</a>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>'''

# ============================================================
# NEW HAMBURGER NAV
# ============================================================
NEW_HAMBURGER_NAV = '''          <div class="hamburger-nav-grid">
            <div class="hamburger-nav-group">
              <a href="wireframe_yacht.html">ヨット</a>
              <div class="ham-sub">
                <a href="wireframe_yacht_review.html">ヨットの紹介</a>
                <a href="wireframe_yacht_race.html">レース</a>
                <a href="wireframe_yacht_technique.html">ハウツー</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="wireframe_boat.html">ボート</a>
              <div class="ham-sub">
                <a href="wireframe_boat_review.html">ボートの紹介</a>
                <a href="wireframe_boat_technique.html">エンジン</a>
                <a href="wireframe_boat_guide.html">ハウツー</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="wireframe_fishing.html">フィッシング</a>
              <div class="ham-sub">
                <a href="wireframe_fishing_lure.html">ルアー</a>
                <a href="wireframe_fishing_species.html">船釣り</a>
                <a href="wireframe_fishing_beginner.html">釣り入門</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="#" onclick="toast('クルージング');return false;">クルージング</a>
              <div class="ham-sub">
                <a href="#" onclick="toast('国内クルーズ');return false;">国内クルーズ</a>
                <a href="#" onclick="toast('海外クルーズ');return false;">海外クルーズ</a>
                <a href="#" onclick="toast('クルージング入門');return false;">クルージング入門</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="wireframe_lifestyle.html">ライフスタイル</a>
              <div class="ham-sub">
                <a href="wireframe_lifestyle_fashion.html">ファッション</a>
                <a href="wireframe_lifestyle_gourmet.html">グルメ</a>
                <a href="#" onclick="toast('時計');return false;">時計</a>
                <a href="#" onclick="toast('クルマ');return false;">クルマ</a>
                <a href="#" onclick="toast('客船');return false;">客船</a>
                <a href="wireframe_lifestyle_hotel.html">リゾート</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="wireframe_gear.html">グッズ＆ギア</a>
              <div class="ham-sub">
                <a href="wireframe_gear_wear.html">マリンウェア</a>
                <a href="wireframe_gear_lifejacket.html">安全装備</a>
                <a href="wireframe_gear_paddle.html">パドルスポーツ</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="wireframe_news.html">トピックス</a>
              <div class="ham-sub">
                <a href="wireframe_news.html">ニュース</a>
                <a href="wireframe_news_events.html">イベント</a>
                <a href="wireframe_news_ranking.html">ランキング</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="#" onclick="toast('マガジン');return false;">マガジン</a>
              <div class="ham-sub">
                <a href="#">KAZI</a>
                <a href="#">Boat CLUB</a>
                <a href="#">Sea Dream</a>
              </div>
            </div>
          </div>'''

# ============================================================
# NEW FOOTER SITEMAP
# ============================================================
NEW_FOOTER_SITEMAP = '''<div class="footer-sitemap">
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_yacht.html">ヨット</a></div>
        <a href="wireframe_yacht_review.html">ヨットの紹介</a>
        <a href="wireframe_yacht_race.html">レース</a>
        <a href="wireframe_yacht_technique.html">ハウツー</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_boat.html">ボート</a></div>
        <a href="wireframe_boat_review.html">ボートの紹介</a>
        <a href="wireframe_boat_technique.html">エンジン</a>
        <a href="wireframe_boat_guide.html">ハウツー</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_fishing.html">フィッシング</a></div>
        <a href="wireframe_fishing_lure.html">ルアー</a>
        <a href="wireframe_fishing_species.html">船釣り</a>
        <a href="wireframe_fishing_beginner.html">釣り入門</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="#" onclick="toast('クルージング');return false;">クルージング</a></div>
        <a href="#" onclick="toast('国内クルーズ');return false;">国内クルーズ</a>
        <a href="#" onclick="toast('海外クルーズ');return false;">海外クルーズ</a>
        <a href="#" onclick="toast('クルージング入門');return false;">クルージング入門</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_lifestyle.html">ライフスタイル</a></div>
        <a href="wireframe_lifestyle_fashion.html">ファッション</a>
        <a href="wireframe_lifestyle_gourmet.html">グルメ</a>
        <a href="#" onclick="toast('時計');return false;">時計</a>
        <a href="#" onclick="toast('クルマ');return false;">クルマ</a>
        <a href="#" onclick="toast('客船');return false;">客船</a>
        <a href="wireframe_lifestyle_hotel.html">リゾート</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_gear.html">グッズ＆ギア</a></div>
        <a href="wireframe_gear_wear.html">マリンウェア</a>
        <a href="wireframe_gear_lifejacket.html">安全装備</a>
        <a href="wireframe_gear_paddle.html">パドルスポーツ</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_news.html">トピックス</a></div>
        <a href="wireframe_news.html">ニュース</a>
        <a href="wireframe_news_events.html">イベント</a>
        <a href="wireframe_news_ranking.html">ランキング</a>
      </div>
    </div>'''


def replace_mega_menus(html):
    """Replace all mega menus between first <!-- Mega Menu: and last mega-menu-footer."""
    # Find first mega menu
    patterns = ['<!-- Mega Menu: ', '<div class="mega-menu" id="mega-']
    first_pos = len(html)
    for p in patterns:
        idx = html.find(p)
        if idx != -1 and idx < first_pos:
            first_pos = idx

    if first_pos == len(html):
        return html

    # Find megaOverlay
    overlay_pat = '<div id="megaOverlay" class="mega-overlay" onclick="closeMega()"></div>'
    overlay_idx = html.find(overlay_pat, first_pos)
    if overlay_idx == -1:
        return html

    last_pos = overlay_idx + len(overlay_pat)
    # Skip trailing whitespace
    while last_pos < len(html) and html[last_pos] in '\n\r\t ':
        last_pos += 1

    html = html[:first_pos] + NEW_MEGA_MENUS + '\n' + overlay_pat + '\n\n' + html[last_pos:]
    return html


def replace_hamburger_nav(html):
    """Replace hamburger-nav-grid block."""
    pat = re.compile(
        r'<div class="hamburger-nav-grid">.*?</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    # We need to find the hamburger-nav-grid and replace up to its proper closing
    start_marker = '<div class="hamburger-nav-grid">'
    idx = html.find(start_marker)
    if idx == -1:
        return html

    # Find the closing: we need to count divs
    depth = 0
    i = idx
    end = -1
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                end = i + 6
                break
        i += 1

    if end == -1:
        return html

    html = html[:idx] + NEW_HAMBURGER_NAV + html[end:]
    return html


def replace_footer_sitemap(html):
    """Replace footer-sitemap block."""
    start_marker = '<div class="footer-sitemap">'
    idx = html.find(start_marker)
    if idx == -1:
        return html

    # Find closing by counting divs
    depth = 0
    i = idx
    end = -1
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                end = i + 6
                break
        i += 1

    if end == -1:
        return html

    html = html[:idx] + NEW_FOOTER_SITEMAP + html[end:]
    return html


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html

    html = replace_mega_menus(html)
    html = replace_hamburger_nav(html)
    html = replace_footer_sitemap(html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


files = sorted(glob.glob('wireframe_*.html'))
print(f'Processing {len(files)} files...')
count = 0
for f in files:
    if process_file(f):
        count += 1
        print(f'  [OK] {f}')
    else:
        print(f'  [--] {f}')
print(f'\nDone: {count} files updated')
