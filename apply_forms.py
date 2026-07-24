# -*- coding: utf-8 -*-
"""Patch the current index.html: inject the forms comparison section right AFTER
the 'How we write your site' (cmp-section) block. Same logic build_proposal.py uses."""
import re
from forms_section import FORMS_CSS, build_forms

doc = open('index.html', encoding='utf-8').read()
if 'fp-section' in doc:
    print('forms section already present — skipping')
    raise SystemExit

doc = doc.replace('</head>', FORMS_CSS + '</head>')
doc, n = re.subn(r'(<section class="cmp-section">.*?</section>)',
                 lambda m: m.group(1) + build_forms(), doc, count=1, flags=re.S)
open('index.html', 'w', encoding='utf-8').write(doc)
print(f'injected forms after cmp-section (n={n}, bytes={len(doc)})')
