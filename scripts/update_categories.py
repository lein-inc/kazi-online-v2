#!/usr/bin/env python3
"""
KAZI ONLINE v2 — Update navigation categories across all HTML files.

New category order:
1. ヨット (yacht)
2. ボート (boat)
3. フィッシング (fishing)
4. クルージング (cruising) — NEW
5. ライフスタイル (lifestyle) — subcategories changed
6. グッズ＆ギア (gear) — renamed from マリングッズ・ギア
7. トピックス (topics) — renamed from ニュース
マリーナ — removed from main nav (pages still exist)
"""

import os
import re
import glob

V2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# New navigation HTML blocks
# ============================================================

NEW_GLOBAL_NAV = '''<nav class="global-nav">
      <div class="nav-item">
        <a href="wireframe_yacht.html" class="has-sub" onclick="toggleMega(event,'mega-yacht')">ヨット</a>
      </div>
      <div class="nav-item">
        <a href="wireframe_boat.html" class="has-sub" onclick="toggleMega(event,'mega-boat')">ボート</a>
      </div>
      <div class="nav-item">
        <a href="wireframe_fishing.html" class="has-sub" onclick="toggleMega(event,'mega-fishing')">フィッシング</a>
      </div>
      <div class="nav-item">
        <a href="#" class="has-sub" onclick="toggleMega(event,'mega-cruising')">クルージング</a>
      </div>
      <div class="nav-item">
        <a href="wireframe_lifestyle.html" class="has-sub" onclick="toggleMega(event,'mega-lifestyle')">ライフスタイル</a>
      </div>
      <div class="nav-item">
        <a href="wireframe_gear.html" class="has-sub" onclick="toggleMega(event,'mega-gear')">グッズ＆ギア</a>
      </div>
      <div class="nav-item">
        <a href="wireframe_news.html" class="has-sub" onclick="toggleMega(event,'mega-news')">トピックス</a>
      </div>
    </nav>'''

NEW_MEGA_MENUS = '''<!-- Mega Menu: ヨット -->
<div class="mega-menu" id="mega-yacht">
  <div class="mega-menu-header"><a href="wireframe_yacht.html" class="mega-title">ヨット トップ ›</a></div>
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
</div>
<div class="mega-overlay" onclick="closeMega()"></div>

<!-- Mega Menu: ボート -->
<div class="mega-menu" id="mega-boat">
  <div class="mega-menu-header"><a href="wireframe_boat.html" class="mega-title">ボート トップ ›</a></div>
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
</div>
<div class="mega-overlay" onclick="closeMega()"></div>

<!-- Mega Menu: フィッシング -->
<div class="mega-menu" id="mega-fishing">
  <div class="mega-menu-header"><a href="wireframe_fishing.html" class="mega-title">フィッシング トップ ›</a></div>
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
</div>
<div class="mega-overlay" onclick="closeMega()"></div>

<!-- Mega Menu: クルージング -->
<div class="mega-menu" id="mega-cruising">
  <div class="mega-menu-header"><a href="#" class="mega-title" onclick="toast('クルージング');return false;">クルージング トップ ›</a></div>
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
</div>
<div class="mega-overlay" onclick="closeMega()"></div>

<!-- Mega Menu: ライフスタイル -->
<div class="mega-menu" id="mega-lifestyle">
  <div class="mega-menu-header"><a href="wireframe_lifestyle.html" class="mega-title">ライフスタイル トップ ›</a></div>
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
</div>
<div class="mega-overlay" onclick="closeMega()"></div>

<!-- Mega Menu: グッズ＆ギア -->
<div class="mega-menu" id="mega-gear">
  <div class="mega-menu-header"><a href="wireframe_gear.html" class="mega-title">グッズ＆ギア トップ ›</a></div>
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
</div>
<div class="mega-overlay" onclick="closeMega()"></div>

<!-- Mega Menu: トピックス -->
<div class="mega-menu" id="mega-news">
  <div class="mega-menu-header"><a href="wireframe_news.html" class="mega-title">トピックス トップ ›</a></div>
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
</div>
<div class="mega-overlay" onclick="closeMega()"></div>'''

NEW_HAMBURGER_NAV = '''<div class="hamburger-nav">
          <div class="hamburger-nav-grid">
            <div class="hamburger-nav-group">
              <a href="wireframe_yacht.html">ヨット</a>
              <div class="ham-sub">
                <a href="wireframe_yacht_review.html">最新ヨットレビュー</a>
                <a href="wireframe_yacht_technique.html">セーリング技術</a>
                <a href="wireframe_yacht_race.html">レース情報</a>
                <a href="wireframe_yacht_guide.html">購入ガイド</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="wireframe_boat.html">ボート</a>
              <div class="ham-sub">
                <a href="wireframe_boat_review.html">ボートレビュー</a>
                <a href="wireframe_boat_technique.html">操縦テクニック</a>
                <a href="wireframe_boat_2hp.html">2馬力ボート特集</a>
                <a href="wireframe_boat_trailable.html">トレーラブルボート</a>
                <a href="wireframe_boat_guide.html">購入ガイド</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="wireframe_fishing.html">フィッシング</a>
              <div class="ham-sub">
                <a href="wireframe_fishing_lure.html">ルアーフィッシング</a>
                <a href="wireframe_fishing_tackle.html">タックル・ギア</a>
                <a href="wireframe_fishing_species.html">魚種別ガイド</a>
                <a href="wireframe_fishing_beginner.html">フィッシング入門</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="#" onclick="toast('クルージング');return false;">クルージング</a>
              <div class="ham-sub">
                <a href="#" onclick="toast('国内クルーズ');return false;">国内クルーズ</a>
                <a href="#" onclick="toast('海外クルーズ');return false;">海外クルーズ</a>
                <a href="#" onclick="toast('クルージング入門');return false;">クルージング入門</a>
                <a href="wireframe_marina_list.html">マリーナ一覧</a>
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
                <a href="wireframe_gear_lifejacket.html">ライフジャケット</a>
                <a href="wireframe_gear_paddle.html">パドルスポーツ用品</a>
                <a href="wireframe_gear_list.html">グッズ一覧</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="wireframe_news.html">トピックス</a>
              <div class="ham-sub">
                <a href="wireframe_news.html">新着ニュース</a>
                <a href="wireframe_news_products.html">新製品・新着</a>
                <a href="wireframe_news_events.html">イベント情報</a>
                <a href="wireframe_news_ranking.html">人気ランキング</a>
                <a href="wireframe_news_exhibition.html">展示会</a>
              </div>
            </div>
            <div class="hamburger-nav-group">
              <a href="#" onclick="toast('マガジン');return false;">マガジン</a>
              <div class="ham-sub">
                <a href="#">KAZI</a>
                <a href="#">Boat CLUB</a>
                <a href="#">Sea Dream</a>
                <a href="#">CANOE WORLD</a>
                <a href="#">書籍</a>
              </div>
            </div>
          </div>
        </div>'''

NEW_FOOTER_SITEMAP = '''<div class="footer-sitemap">
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_yacht.html">ヨット</a></div>
        <ul>
          <li><a href="wireframe_yacht_review.html">最新ヨットレビュー</a></li>
          <li><a href="wireframe_yacht_technique.html">セーリング技術</a></li>
          <li><a href="wireframe_yacht_race.html">レース情報</a></li>
          <li><a href="wireframe_yacht_guide.html">購入ガイド</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_boat.html">ボート</a></div>
        <ul>
          <li><a href="wireframe_boat_review.html">ボートレビュー</a></li>
          <li><a href="wireframe_boat_technique.html">操縦テクニック</a></li>
          <li><a href="wireframe_boat_2hp.html">2馬力ボート特集</a></li>
          <li><a href="wireframe_boat_trailable.html">トレーラブルボート</a></li>
          <li><a href="wireframe_boat_guide.html">購入ガイド</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_fishing.html">フィッシング</a></div>
        <ul>
          <li><a href="wireframe_fishing_lure.html">ルアーフィッシング</a></li>
          <li><a href="wireframe_fishing_tackle.html">タックル・ギア</a></li>
          <li><a href="wireframe_fishing_species.html">魚種別ガイド</a></li>
          <li><a href="wireframe_fishing_beginner.html">フィッシング入門</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="#" onclick="toast('クルージング');return false;">クルージング</a></div>
        <ul>
          <li><a href="#" onclick="toast('国内クルーズ');return false;">国内クルーズ</a></li>
          <li><a href="#" onclick="toast('海外クルーズ');return false;">海外クルーズ</a></li>
          <li><a href="#" onclick="toast('クルージング入門');return false;">クルージング入門</a></li>
          <li><a href="wireframe_marina_list.html">マリーナ一覧</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_lifestyle.html">ライフスタイル</a></div>
        <ul>
          <li><a href="wireframe_lifestyle_fashion.html">ファッション</a></li>
          <li><a href="wireframe_lifestyle_gourmet.html">グルメ</a></li>
          <li><a href="#" onclick="toast('時計');return false;">時計</a></li>
          <li><a href="#" onclick="toast('クルマ');return false;">クルマ</a></li>
          <li><a href="#" onclick="toast('客船');return false;">客船</a></li>
          <li><a href="wireframe_lifestyle_hotel.html">リゾート</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_gear.html">グッズ＆ギア</a></div>
        <ul>
          <li><a href="wireframe_gear_wear.html">マリンウェア</a></li>
          <li><a href="wireframe_gear_lifejacket.html">ライフジャケット</a></li>
          <li><a href="wireframe_gear_paddle.html">パドルスポーツ用品</a></li>
          <li><a href="wireframe_gear_list.html">グッズ一覧</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title"><a href="wireframe_news.html">トピックス</a></div>
        <ul>
          <li><a href="wireframe_news.html">新着ニュース</a></li>
          <li><a href="wireframe_news_products.html">新製品・新着</a></li>
          <li><a href="wireframe_news_events.html">イベント情報</a></li>
          <li><a href="wireframe_news_ranking.html">人気ランキング</a></li>
          <li><a href="wireframe_news_exhibition.html">展示会</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">サービス</div>
        <ul>
          <li><a href="wireframe_sdclub.html">KAZI SeaDream Club</a></li>
          <li><a href="wireframe_entry.html">エントリーガイド</a></li>
          <li><a href="wireframe_maker.html">メーカー&amp;ビルダー</a></li>
          <li><a href="wireframe_company.html">会社概要</a></li>
          <li><a href="wireframe_contact.html">お問い合わせ</a></li>
          <li><a href="wireframe_privacy.html">プライバシーポリシー</a></li>
        </ul>
      </div>
    </div>'''


def replace_global_nav(html):
    """Replace the global-nav block."""
    pattern = re.compile(
        r'<nav class="global-nav">.*?</nav>',
        re.DOTALL
    )
    if pattern.search(html):
        html = pattern.sub(NEW_GLOBAL_NAV, html)
    return html


def replace_mega_menus(html):
    """Replace all mega-menu blocks."""
    # Remove all existing mega-menu blocks and their overlays
    # Find the first mega-menu and last mega-overlay, replace entire range
    pattern = re.compile(
        r'<!-- Mega Menu.*?<div class="mega-menu" id="mega-\w+".*?'
        r'(?:<div class="mega-overlay"[^>]*></div>\s*)+',
        re.DOTALL
    )

    # Simpler approach: find first mega-menu, find last mega-overlay after it
    first_mega = html.find('<div class="mega-menu" id="mega-')
    if first_mega == -1:
        return html

    # Find comment before first mega menu
    comment_start = html.rfind('<!-- Mega Menu', 0, first_mega)
    if comment_start == -1:
        comment_start = first_mega

    # Find last mega-overlay
    last_pos = first_mega
    while True:
        next_overlay = html.find('<div class="mega-overlay"', last_pos)
        if next_overlay == -1:
            break
        end_of_overlay = html.find('</div>', next_overlay) + len('</div>')
        last_pos = end_of_overlay

    if last_pos > first_mega:
        # Skip any trailing whitespace
        while last_pos < len(html) and html[last_pos] in '\n\r\t ':
            last_pos += 1
        html = html[:comment_start] + NEW_MEGA_MENUS + '\n' + html[last_pos:]

    return html


def replace_hamburger_nav(html):
    """Replace the hamburger-nav block."""
    pattern = re.compile(
        r'<div class="hamburger-nav">.*?</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    match = pattern.search(html)
    if match:
        # Find the exact hamburger-nav block (ends with 3 closing divs for nav-grid, nav, and beyond)
        start = html.find('<div class="hamburger-nav">')
        if start == -1:
            return html

        # Count nested divs to find the correct end
        depth = 0
        pos = start
        end = start
        while pos < len(html):
            if html[pos:pos+4] == '<div':
                depth += 1
            elif html[pos:pos+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end = pos + 6
                    break
            pos += 1

        if end > start:
            html = html[:start] + NEW_HAMBURGER_NAV + html[end:]

    return html


def replace_footer_sitemap(html):
    """Replace the footer-sitemap block."""
    start = html.find('<div class="footer-sitemap">')
    if start == -1:
        return html

    # Count nested divs to find the correct end
    depth = 0
    pos = start
    end = start
    while pos < len(html):
        if html[pos:pos+4] == '<div':
            depth += 1
        elif html[pos:pos+6] == '</div>':
            depth -= 1
            if depth == 0:
                end = pos + 6
                break
        pos += 1

    if end > start:
        html = html[:start] + NEW_FOOTER_SITEMAP + html[end:]

    return html


def update_mega_js_mapping(html):
    """Update the mega menu JS mapping for category names."""
    # Replace category label mappings in JS
    replacements = [
        ("'ニュース'", "'トピックス'"),
        ("'マリングッズ・ギア'", "'グッズ＆ギア'"),
        ('"ニュース"', '"トピックス"'),
        ('"マリングッズ・ギア"', '"グッズ＆ギア"'),
    ]
    for old, new in replacements:
        html = html.replace(old, new)

    # Add cruising mapping if mega menu JS mapping exists
    if "'mega-yacht'" in html and "'mega-cruising'" not in html:
        html = html.replace(
            "'ヨット':'mega-yacht'",
            "'ヨット':'mega-yacht','クルージング':'mega-cruising'"
        )

    return html


def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    html = replace_global_nav(html)
    html = replace_mega_menus(html)
    html = replace_hamburger_nav(html)
    html = replace_footer_sitemap(html)
    html = update_mega_js_mapping(html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def main():
    html_files = sorted(glob.glob(os.path.join(V2_DIR, 'wireframe_*.html')))
    print(f'Processing {len(html_files)} wireframe files...')

    processed = 0
    for filepath in html_files:
        filename = os.path.basename(filepath)
        if process_file(filepath):
            processed += 1
            print(f'  [OK] {filename}')
        else:
            print(f'  [--] {filename} (no changes)')

    print(f'\nDone: {processed}/{len(html_files)} files updated')


if __name__ == '__main__':
    main()
