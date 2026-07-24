# -*- coding: utf-8 -*-
"""Patch the current (already-built) index.html with the comparison section,
using the same logic build_proposal.py will use on future regens.
CFG mirrors build_proposal.py's CFG for the current client (Gihon / home care)."""
import re
from cmp_section import CMP_CSS, build_cmp

CFG = {
    'industry_lc': 'home care',
    'provider_term': 'care provider',
    'service_term': 'consultation',
    'preview_domain': 'gihonfamilycare.com',
}

doc = open('index.html', encoding='utf-8').read()
if 'cmp-section' in doc:
    print('cmp-section already present — skipping')
    raise SystemExit

doc = doc.replace('</head>', CMP_CSS + '</head>')
doc, n = re.subn(r'(<section\b[^>]*section-three-reasons[^>]*>.*?</section>)',
                 lambda m: m.group(1) + build_cmp(CFG), doc, count=1, flags=re.S)
open('index.html', 'w', encoding='utf-8').write(doc)
print(f'injected cmp into index.html (n={n}, bytes={len(doc)})')
