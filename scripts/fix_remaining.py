#!/usr/bin/env python3
"""Fix remaining old category references: search overlay, mega menus, and any other spots."""

import os, re, glob

V2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(V2_DIR)

# New search category buttons (replaces old 7-button block)
NEW_SEARCH_CATS = '''    <div class="search-cats">
      <a class="search-cat-btn" href="wireframe_yacht.html" onclick="closeSearchBox()">
        <span class="search-cat-symbol">[ Y ]</span>ヨット
      </a>
      <a class="search-cat-btn" href="wireframe_boat.html" onclick="closeSearchBox()">
        <span class="search-cat-symbol">[ B ]</span>ボート
      </a>
      <a class="search-cat-btn" href="wireframe_fishing.html" onclick="closeSearchBox()">
        <span class="search-cat-symbol">[ F ]</span>フィッシング
      </a>
      <a class="search-cat-btn" href="#" onclick="toast('クルージング');closeSearchBox();return false;">
        <span class="search-cat-symbol">[ C ]</span>クルージング
      </a>
      <a class="search-cat-btn" href="wireframe_lifestyle.html" onclick="closeSearchBox()">
        <span class="search-cat-symbol">[ L ]</span>ライフスタイル
      </a>
      <a class="search-cat-btn" href="wireframe_gear.html" onclick="closeSearchBox()">
        <span class="search-cat-symbol">[ G ]</span>グッズ＆ギア
      </a>
      <a class="search-cat-btn" href="wireframe_news.html" onclick="closeSearchBox()">
        <span class="search-cat-symbol">[ T ]</span>トピックス
      </a>
    </div>'''

# New mega menus for files that have mega-menu-footer style
NEW_MEGA_MENUS_WITH_FOOTER = '''<!-- Mega Menu: ヨット -->
<div class="mega-menu" id="mega-yacht">
  <div class="mega-menu-header"><a href="wireframe_yacht.html" class="mega-title" style="text-decoration:none;color:inherit">ヨット トップ</a></div>
  <div class="mega-menu-body">
    <div class="mega-col">
      <div class="mega-col-title">ヨット紹介</div>
      <a href="wireframe_yacht_review.html">最新ヨットレビュー</a>
      <a href="wireframe_yacht_guide.html">購入ガイド</a>
    </div>
    <div class="mega-col">
      <div class="mega-col-title">レース・ハウツー</div>
      <a href="wireframe_yacht_race.html">レース情報</a>
      <a href="wireframe_yacht_technique.html">セーリング技術</a>
    </div>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: ボート -->
<div class="mega-menu" id="mega-boat">
  <div class="mega-menu-header"><a href="wireframe_boat.html" class="mega-title" style="text-decoration:none;color:inherit">ボート トップ</a></div>
  <div class="mega-menu-body">
    <div class="mega-col">
      <div class="mega-col-title">ボート紹介</div>
      <a href="wireframe_boat_review.html">ボートレビュー</a>
      <a href="wireframe_boat_2hp.html">2馬力ボート特集</a>
      <a href="wireframe_boat_trailable.html">トレーラブルボート</a>
    </div>
    <div class="mega-col">
      <div class="mega-col-title">エンジン・ハウツー</div>
      <a href="wireframe_boat_technique.html">操縦テクニック</a>
      <a href="wireframe_boat_guide.html">購入ガイド</a>
    </div>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: フィッシング -->
<div class="mega-menu" id="mega-fishing">
  <div class="mega-menu-header"><a href="wireframe_fishing.html" class="mega-title" style="text-decoration:none;color:inherit">フィッシング トップ</a></div>
  <div class="mega-menu-body">
    <div class="mega-col">
      <div class="mega-col-title">カテゴリー</div>
      <a href="wireframe_fishing_lure.html">ルアーフィッシング</a>
      <a href="wireframe_fishing_species.html">魚種別ガイド</a>
    </div>
    <div class="mega-col">
      <div class="mega-col-title">ギア・入門</div>
      <a href="wireframe_fishing_tackle.html">タックル・ギア</a>
      <a href="wireframe_fishing_beginner.html">フィッシング入門</a>
    </div>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: クルージング -->
<div class="mega-menu" id="mega-cruising">
  <div class="mega-menu-header"><a href="#" class="mega-title" style="text-decoration:none;color:inherit" onclick="toast('クルージング');return false;">クルージング トップ</a></div>
  <div class="mega-menu-body">
    <div class="mega-col">
      <div class="mega-col-title">クルージング</div>
      <a href="#" onclick="toast('国内クルーズ');return false;">国内クルーズ</a>
      <a href="#" onclick="toast('海外クルーズ');return false;">海外クルーズ</a>
    </div>
    <div class="mega-col">
      <div class="mega-col-title">ガイド</div>
      <a href="#" onclick="toast('クルージング入門');return false;">クルージング入門</a>
      <a href="wireframe_marina_list.html">マリーナ一覧</a>
    </div>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: ライフスタイル -->
<div class="mega-menu" id="mega-lifestyle">
  <div class="mega-menu-header"><a href="wireframe_lifestyle.html" class="mega-title" style="text-decoration:none;color:inherit">ライフスタイル トップ</a></div>
  <div class="mega-menu-body">
    <div class="mega-col">
      <div class="mega-col-title">ファッション・グルメ</div>
      <a href="wireframe_lifestyle_fashion.html">ファッション</a>
      <a href="wireframe_lifestyle_gourmet.html">グルメ</a>
    </div>
    <div class="mega-col">
      <div class="mega-col-title">ラグジュアリー</div>
      <a href="#" onclick="toast('時計');return false;">時計</a>
      <a href="#" onclick="toast('クルマ');return false;">クルマ</a>
    </div>
    <div class="mega-col">
      <div class="mega-col-title">トラベル</div>
      <a href="#" onclick="toast('客船');return false;">客船</a>
      <a href="wireframe_lifestyle_hotel.html">リゾート</a>
    </div>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: グッズ＆ギア -->
<div class="mega-menu" id="mega-gear">
  <div class="mega-menu-header"><a href="wireframe_gear.html" class="mega-title" style="text-decoration:none;color:inherit">グッズ＆ギア トップ</a></div>
  <div class="mega-menu-body">
    <div class="mega-col">
      <div class="mega-col-title">ウェア・安全</div>
      <a href="wireframe_gear_wear.html">マリンウェア</a>
      <a href="wireframe_gear_lifejacket.html">ライフジャケット・安全器具</a>
    </div>
    <div class="mega-col">
      <div class="mega-col-title">用品</div>
      <a href="wireframe_gear_paddle.html">パドルスポーツ用品</a>
      <a href="wireframe_gear_list.html">グッズ一覧</a>
    </div>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>

<!-- Mega Menu: トピックス -->
<div class="mega-menu" id="mega-news">
  <div class="mega-menu-header"><a href="wireframe_news.html" class="mega-title" style="text-decoration:none;color:inherit">トピックス トップ</a></div>
  <div class="mega-menu-body">
    <div class="mega-col">
      <div class="mega-col-title">ニュース</div>
      <a href="wireframe_news.html">新着ニュース一覧</a>
      <a href="wireframe_news_products.html">新製品・新着</a>
    </div>
    <div class="mega-col">
      <div class="mega-col-title">イベント</div>
      <a href="wireframe_news_events.html">イベント情報</a>
      <a href="wireframe_news_exhibition.html">展示会</a>
    </div>
    <div class="mega-col">
      <div class="mega-col-title">ランキング</div>
      <a href="wireframe_news_ranking.html">人気ランキング</a>
    </div>
  </div>
  <div class="mega-menu-footer" onclick="closeMega()">閉じる &times;</div>
</div>'''


def fix_search_cats(html):
    """Replace search category buttons."""
    pattern = re.compile(
        r'<div class="search-cats">.*?</div>\s*(?=<div class="search-sdc)',
        re.DOTALL
    )
    if pattern.search(html):
        html = pattern.sub(NEW_SEARCH_CATS + '\n    ', html)
    return html


def fix_mega_menus(html):
    """Remove ALL old mega menus and replace with new ones."""
    # Find the first mega-menu comment or div
    patterns_to_find = [
        '<!-- Mega Menu Overlay -->',
        '<!-- Mega Menu:',
        '<div class="mega-menu" id="mega-',
    ]

    first_pos = len(html)
    for p in patterns_to_find:
        idx = html.find(p)
        if idx != -1 and idx < first_pos:
            first_pos = idx

    if first_pos == len(html):
        return html

    # Find the last mega-menu-footer or mega-overlay closing div
    last_pos = first_pos

    # Search for all mega-menu-footer divs
    for m in re.finditer(r'<div class="mega-menu-footer"[^>]*>.*?</div>', html):
        if m.end() > last_pos:
            last_pos = m.end()

    # Also search for mega-overlay divs
    for m in re.finditer(r'<div class="mega-overlay"[^>]*>.*?</div>', html):
        if m.end() > last_pos:
            last_pos = m.end()

    if last_pos <= first_pos:
        return html

    # Skip whitespace after last element
    while last_pos < len(html) and html[last_pos] in '\n\r\t ':
        last_pos += 1

    # Check if there's a megaOverlay div nearby
    overlay_match = re.search(r'<div id="megaOverlay"[^>]*></div>', html[first_pos:last_pos+200])
    if overlay_match:
        overlay_end = first_pos + overlay_match.end()
        if overlay_end > last_pos:
            last_pos = overlay_end
            while last_pos < len(html) and html[last_pos] in '\n\r\t ':
                last_pos += 1

    # Replace entire mega menu section
    html = html[:first_pos] + NEW_MEGA_MENUS_WITH_FOOTER + '\n<div id="megaOverlay" class="mega-overlay" onclick="closeMega()"></div>\n\n' + html[last_pos:]

    return html


def fix_search_placeholder(html):
    """Update search placeholder text."""
    html = html.replace(
        'キーワードを入力してください（例：ルアー釣り、ボート免許、マリーナ）',
        'キーワードを入力してください（例：ルアー釣り、ボート免許、クルージング）'
    )
    return html


def fix_search_tags(html):
    """Update search keyword tags."""
    html = html.replace(
        "fillSearch('マリーナ 関東')",
        "fillSearch('クルージング 関東')"
    )
    html = html.replace('>マリーナ 関東</a>', '>クルージング 関東</a>')
    return html


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html

    html = fix_search_cats(html)
    html = fix_mega_menus(html)
    html = fix_search_placeholder(html)
    html = fix_search_tags(html)

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
print(f'\nDone: {count} files fixed')
