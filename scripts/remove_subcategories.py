#!/usr/bin/env python3
"""フィッシング、クルージング、グッズ&ギア、トピックスをサブカテゴリーなしに変更。

対象:
- 全 wireframe_*.html の
  1) ヘッダーグローバルナビ: has-sub クラス除去
  2) メガメニュー: 該当4カテゴリの <div class="mega-menu" id="mega-xxx"> ブロック削除
  3) ハンバーガーナビ: 該当4カテゴリの <div class="ham-sub">...</div> 削除
  4) フッターサイトマップ: 該当4カテゴリのサブリンク削除
- 一覧ページ (wireframe_fishing/cruising/gear/news.html):
  5) <div class="subcat-wrap">...</div> ブロック削除
"""

import os, re, glob

V2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(V2_DIR)

# 削除対象カテゴリ（ホーム一覧ページのファイル名プレフィックス）
TARGETS = ['fishing', 'cruising', 'gear', 'news']
TARGET_LABELS = ['フィッシング', 'クルージング', 'グッズ＆ギア', 'トピックス']

# ------------------------------------------------------------
# 1) グローバルナビ: has-sub クラス除去
# ------------------------------------------------------------
def remove_has_sub(html):
    for t in TARGETS:
        # <a href="wireframe_fishing.html" class="has-sub">フィッシング</a>
        pattern = rf'(<a href="wireframe_{t}\.html")\s+class="has-sub"(>)'
        html = re.sub(pattern, r'\1\2', html)
    return html


# ------------------------------------------------------------
# 2) メガメニュー: 該当4カテゴリの <div class="mega-menu" id="mega-xxx"> ブロック削除
# ------------------------------------------------------------
def remove_mega_blocks(html):
    for t in TARGETS:
        # マッチ: <!-- Mega Menu: XXX --> を含む可能性のある行〜</div>(menu-footer)までのブロック
        # より安全に: <div class="mega-menu" id="mega-{t}"> から対応する </div> まで削除
        marker = f'<div class="mega-menu" id="mega-{t}">'
        idx = html.find(marker)
        if idx == -1:
            continue

        # コメントも含めて削除するため、コメント行を遡って探す
        comment_marker = f'<!-- Mega Menu: '
        # marker直前の行を見る
        before = html.rfind(comment_marker, max(0, idx - 200), idx)
        start = before if before != -1 else idx

        # 対応する </div> を探す (div 深さをカウント)
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
            continue

        # 末尾の改行/空白も取り込む
        while end < len(html) and html[end] in '\n\r\t ':
            end += 1

        html = html[:start] + html[end:]
    return html


# ------------------------------------------------------------
# 3) ハンバーガー: 該当4カテゴリの ham-sub ブロック削除
# ------------------------------------------------------------
def remove_ham_sub(html):
    for t in TARGETS:
        # <a href="wireframe_{t}.html">LABEL</a>
        #   <div class="ham-sub">
        #     ...
        #   </div>
        # の ham-sub ブロックだけ削除
        marker = f'<a href="wireframe_{t}.html">'
        idx = html.find(marker)
        while idx != -1:
            # この位置が hamburger-nav-group 内かどうか確認（簡易: 直近に hamburger-nav-group があるか）
            parent_start = html.rfind('<div class="hamburger-nav-group">', max(0, idx - 300), idx)
            if parent_start == -1:
                idx = html.find(marker, idx + 1)
                continue

            # marker直後の <div class="ham-sub"> を探す
            ham_sub_start = html.find('<div class="ham-sub">', idx, idx + 500)
            if ham_sub_start == -1:
                idx = html.find(marker, idx + 1)
                continue

            # 対応する </div> を探す
            depth = 0
            i = ham_sub_start
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
                idx = html.find(marker, idx + 1)
                continue

            # ham-sub直前の空白も取り込む
            sub_start = ham_sub_start
            while sub_start > 0 and html[sub_start - 1] in '\n\r\t ':
                sub_start -= 1

            html = html[:sub_start] + html[end:]
            # 次の検索はこのカテゴリ内では不要なので次の target へ
            break
    return html


# ------------------------------------------------------------
# 4) フッター: 該当4カテゴリの .footer-col 内サブリンクを削除（タイトルだけ残す）
# ------------------------------------------------------------
def simplify_footer_cols(html):
    for t, label in zip(TARGETS, TARGET_LABELS):
        # <div class="footer-col">
        #   <div class="footer-col-title"><a href="wireframe_{t}.html">LABEL</a></div>
        #   <a href="...">sub1</a>
        #   ...
        # </div>
        pattern = re.compile(
            rf'(<div class="footer-col">\s*<div class="footer-col-title"><a href="wireframe_{t}\.html">[^<]+</a></div>)'
            rf'(.*?)(</div>)',
            re.DOTALL
        )
        def repl(m):
            return m.group(1) + '\n      ' + m.group(3)
        html = pattern.sub(repl, html, count=1)
    return html


# ------------------------------------------------------------
# 5) 一覧ページの subcat-wrap を削除
# ------------------------------------------------------------
def remove_subcat_wrap(html):
    # <div class="subcat-wrap">...</div> ブロック削除（複数行対応）
    marker = '<div class="subcat-wrap">'
    idx = html.find(marker)
    if idx == -1:
        return html

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

    # 前後の空白改行
    start = idx
    while start > 0 and html[start - 1] in '\n\r\t ':
        start -= 1
    while end < len(html) and html[end] in '\n\r\t ':
        end += 1

    html = html[:start] + '\n\n' + html[end:]
    return html


# ------------------------------------------------------------
# 処理
# ------------------------------------------------------------
def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html

    html = remove_has_sub(html)
    html = remove_mega_blocks(html)
    html = remove_ham_sub(html)
    html = simplify_footer_cols(html)

    # 該当4カテゴリの一覧ページ + サブカテゴリページから subcat-wrap 削除
    basename = os.path.basename(filepath)
    remove_wrap = False
    for t in TARGETS:
        if basename == f'wireframe_{t}.html' or basename.startswith(f'wireframe_{t}_'):
            remove_wrap = True
            break
    if remove_wrap:
        html = remove_subcat_wrap(html)

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
print(f'\nDone: {count} files updated')
