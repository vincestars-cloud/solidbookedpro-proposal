# -*- coding: utf-8 -*-
"""Patch current index.html: inject the single-page-vs-multi-page section right
AFTER the forms section (.fp-section)."""
import re
from pages_section import PAGES_CSS, build_pages

doc = open('index.html', encoding='utf-8').read()
if 'id="pages-css"' in doc:
    print('pages section already present — skipping')
    raise SystemExit

doc = doc.replace('</head>', PAGES_CSS + '</head>')
doc, n = re.subn(r'(<section class="fp-section">.*?</section>)',
                 lambda m: m.group(1) + build_pages(), doc, count=1, flags=re.S)
open('index.html', 'w', encoding='utf-8').write(doc)
print(f'injected pages section after fp-section (n={n}, bytes={len(doc)})')
