#!/usr/bin/env python3
"""全ページから「新着順 / 人気順」ソートボタン (.list-sort) を削除。"""

import os, glob, re

V2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(V2_DIR)


def process(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # <div class="list-sort"> ... </div> を丸ごと削除（直前の空白改行も吸収）
    pattern = re.compile(
        r'\s*<div class="list-sort">.*?</div>',
        re.DOTALL
    )
    new_html = pattern.sub('', html)

    if new_html != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return True
    return False


files = sorted(glob.glob('wireframe_*.html'))
count = 0
for f in files:
    if process(f):
        count += 1
print(f'Updated: {count} files')
