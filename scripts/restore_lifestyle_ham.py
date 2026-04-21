#!/usr/bin/env python3
"""スクリプト2回実行で誤って削除されたライフスタイルの ham-sub を復元。"""

import os, glob, re

V2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(V2_DIR)

LIFESTYLE_HAM_SUB = '''              <div class="ham-sub">
                <a href="wireframe_lifestyle_fashion.html">ファッション</a>
                <a href="wireframe_lifestyle_gourmet.html">グルメ</a>
                <a href="wireframe_lifestyle_watch.html">時計</a>
                <a href="wireframe_lifestyle_car.html">クルマ</a>
                <a href="wireframe_lifestyle_cruise_ship.html">客船</a>
                <a href="wireframe_lifestyle_hotel.html">リゾート</a>
              </div>
'''


def restore(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # hamburger-nav-group 内のライフスタイルリンクだけを特定
    # パターン: <div class="hamburger-nav-group">\n ... <a href="wireframe_lifestyle.html">ライフスタイル</a>\n            </div>
    pattern = re.compile(
        r'(<div class="hamburger-nav-group">\s*<a href="wireframe_lifestyle\.html">ライフスタイル</a>)\s*(</div>)',
        re.DOTALL
    )
    if not pattern.search(html):
        return False

    replacement = r'\1\n' + LIFESTYLE_HAM_SUB + r'            \2'
    new_html = pattern.sub(replacement, html, count=1)

    if new_html != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return True
    return False


files = sorted(glob.glob('wireframe_*.html'))
count = 0
for f in files:
    if restore(f):
        count += 1
        print(f'  [OK] {f}')
print(f'\nRestored: {count} files')
