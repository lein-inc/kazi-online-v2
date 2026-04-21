#!/usr/bin/env python3
"""「舵社出版物」のリンクを wireframe_publications.html から wireframe_top.html#publications へ変更。

ローカルメニュー（ハンバーガー OTHER、フッター local-nav）のリンクだけを置換。
"""

import os, glob

V2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(V2_DIR)

OLD = '<a href="wireframe_publications.html">舵社出版物</a>'
NEW = '<a href="wireframe_top.html#publications">舵社出版物</a>'


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    if OLD not in html:
        return False

    new_html = html.replace(OLD, NEW)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True


files = sorted(glob.glob('wireframe_*.html'))
count = 0
for f in files:
    if process_file(f):
        count += 1
print(f'Updated: {count} files')
