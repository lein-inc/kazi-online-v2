#!/usr/bin/env python3
"""
KAZI ONLINE v2 — Inject design system CSS and UX enhancement JS into all HTML files.

This script:
1. Adds <link> tags for variables.css and v2-overrides.css after responsive.css
2. Adds <script src> for v2-enhancements.js before </body>
3. Extracts inline <style> blocks to external CSS files in css/pages/
4. Extracts inline <script> blocks to external JS files in js/pages/
5. Replaces inline blocks with <link>/<script src> references
6. Updates hamburger menu CSS to always show on mobile (UX improvement)
"""

import os
import re
import sys

V2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_DIR = V2_DIR
CSS_PAGES_DIR = os.path.join(V2_DIR, 'css', 'pages')
JS_PAGES_DIR = os.path.join(V2_DIR, 'js', 'pages')

os.makedirs(CSS_PAGES_DIR, exist_ok=True)
os.makedirs(JS_PAGES_DIR, exist_ok=True)

# CSS link tags to inject
V2_CSS_LINKS = '''<link rel="stylesheet" href="css/variables.css">
<link rel="stylesheet" href="css/v2-overrides.css">'''

# JS script tag to inject
V2_JS_SCRIPT = '<script src="js/v2-enhancements.js"></script>'


def get_page_name(filename):
    """Convert filename to a clean page name for CSS/JS files."""
    name = filename.replace('.html', '').replace('wireframe_', '')
    return name


def extract_and_replace_style(html, page_name):
    """Extract <style>...</style> block, save to external CSS, replace with <link>."""
    style_pattern = re.compile(r'<style>(.*?)</style>', re.DOTALL)
    match = style_pattern.search(html)

    if not match:
        return html

    css_content = match.group(1)
    css_filename = f'{page_name}.css'
    css_filepath = os.path.join(CSS_PAGES_DIR, css_filename)

    # Save CSS to external file
    with open(css_filepath, 'w', encoding='utf-8') as f:
        f.write(css_content.strip() + '\n')

    # Replace inline <style> with <link> to external CSS
    css_link = f'<link rel="stylesheet" href="css/pages/{css_filename}">'
    html = style_pattern.sub(css_link, html, count=1)

    return html


def extract_and_replace_script(html, page_name):
    """Extract the main inline <script>...</script> block (not auth.js ref), save externally."""
    # Find all script blocks that are inline (not src references)
    # Skip the auth.js script tag and any small inline scripts
    script_pattern = re.compile(r'<script>(.*?)</script>', re.DOTALL)
    matches = list(script_pattern.finditer(html))

    if not matches:
        return html

    # Find the largest inline script block (the main page script)
    largest = max(matches, key=lambda m: len(m.group(1)))

    if len(largest.group(1).strip()) < 50:
        # Too small, probably not the main script
        return html

    js_content = largest.group(1)
    js_filename = f'{page_name}.js'
    js_filepath = os.path.join(JS_PAGES_DIR, js_filename)

    # Save JS to external file
    with open(js_filepath, 'w', encoding='utf-8') as f:
        f.write(js_content.strip() + '\n')

    # Replace inline <script> with <script src>
    js_link = f'<script src="js/pages/{js_filename}"></script>'
    html = html.replace(largest.group(0), js_link, 1)

    return html


def inject_v2_assets(html):
    """Inject v2 CSS links and JS script into the HTML."""
    # Inject CSS: after responsive.css link
    responsive_pattern = re.compile(r'(<link\s+rel="stylesheet"\s+href="responsive\.css"\s*/?>)')
    match = responsive_pattern.search(html)
    if match:
        html = html.replace(match.group(0), match.group(0) + '\n' + V2_CSS_LINKS)
    else:
        # Fallback: inject before </head>
        html = html.replace('</head>', V2_CSS_LINKS + '\n</head>')

    # Inject JS: before </body>
    html = html.replace('</body>', V2_JS_SCRIPT + '\n</body>')

    return html


def fix_hamburger_mobile(html):
    """
    UX fix: Make hamburger button always visible on mobile (<=1024px).
    Modify inline CSS or add override.
    """
    # This is handled by v2-overrides.css, but we need to ensure
    # the hamburger button exists even when not scrolled.
    # The JS scroll handler hides it by default — we'll fix this via CSS override.
    return html


def process_file(filepath):
    """Process a single HTML file."""
    filename = os.path.basename(filepath)
    page_name = get_page_name(filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # Step 1: Extract inline CSS to external file
    html = extract_and_replace_style(html, page_name)

    # Step 2: Extract inline JS to external file
    html = extract_and_replace_script(html, page_name)

    # Step 3: Inject v2 assets
    html = inject_v2_assets(html)

    # Step 4: UX fixes
    html = fix_hamburger_mobile(html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def main():
    """Process all HTML files in the v2 directory."""
    html_files = sorted([
        f for f in os.listdir(HTML_DIR)
        if f.endswith('.html') and (f.startswith('wireframe_') or f == 'index.html')
    ])

    print(f'Processing {len(html_files)} HTML files...')

    processed = 0
    for filename in html_files:
        filepath = os.path.join(HTML_DIR, filename)
        if process_file(filepath):
            processed += 1
            print(f'  [OK] {filename}')
        else:
            print(f'  [--] {filename} (no changes)')

    print(f'\nDone: {processed} files updated')
    print(f'CSS pages: {len(os.listdir(CSS_PAGES_DIR))} files created in css/pages/')
    print(f'JS pages: {len(os.listdir(JS_PAGES_DIR))} files created in js/pages/')


if __name__ == '__main__':
    main()
