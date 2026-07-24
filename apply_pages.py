# -*- coding: utf-8 -*-
"""Patch current index.html with the single-page-vs-multi-page section.
Replaces an existing one (updates in place) or injects after the forms section."""
import re
from pages_section import PAGES_CSS, build_pages

doc = open('index.html', encoding='utf-8').read()

if 'id="pages-css"' in doc:
    # update in place
    doc = re.sub(r'<style id="pages-css">.*?</style>', lambda m: PAGES_CSS, doc, count=1, flags=re.S)
    doc, n = re.subn(r'<section class="mp-section">.*?</section>', lambda m: build_pages(), doc, count=1, flags=re.S)
    print(f'replaced existing pages section (n={n})')
else:
    doc = doc.replace('</head>', PAGES_CSS + '</head>')
    doc, n = re.subn(r'(<section class="fp-section">.*?</section>)',
                     lambda m: m.group(1) + build_pages(), doc, count=1, flags=re.S)
    print(f'injected pages section after fp-section (n={n})')

open('index.html', 'w', encoding='utf-8').write(doc)
print(f'bytes={len(doc)}')
