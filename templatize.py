#!/usr/bin/env python3
"""Turn the rendered Gihon proposal into an industry-agnostic template.

  index.html  ->  proposal.template.html

Two layers of tokens:
  1. word-level  {{COMPANY_NAME}} {{CITY}} {{CUSTOMER_NOUN}} ...
  2. content blocks {{JARGON_*}} {{CUSTOMER_*}} {{SERVICES_LIST}} ...
     (things too industry-specific to derive from a word swap)
"""
import re, sys, json

SRC = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'proposal.template.html'
h = open(SRC, encoding='utf-8').read()
orig_len = len(h)
report = []

def sub(old, new, label=None, required=True):
    global h
    n = h.count(old)
    if n == 0:
        if required:
            report.append(('MISS', label or old[:60], 0))
        return
    h = h.replace(old, new)
    report.append(('ok', label or (old[:52] + ('…' if len(old) > 52 else '')), n))

# ---------------------------------------------------------------- 0. structured content blocks
# The jargon-vs-customer comparison: every piece is industry-specific copy.
sub('In-Home Non-Medical ADL Assistance &amp; Care Coordination', '{{JARGON_HEADLINE}}', 'jargon headline')
sub('<li>Activities of daily living (ADL) support</li><li>Care-plan management &amp; coordination</li><li>HIPAA-compliant caregiver matching</li>',
    '{{JARGON_BULLETS}}', 'jargon bullets')
sub('<span class="cmp-cta">Request Consultation</span>', '<span class="cmp-cta">{{JARGON_CTA}}</span>', 'jargon cta')
sub('searches/mo for &ldquo;non-medical ADL assistance&rdquo;', 'searches/mo for &ldquo;{{JARGON_QUERY}}&rdquo;', 'jargon query')
sub('Worried About Mom Living Alone? Trusted Caregivers, a Few Hours a Day.', '{{CUSTOMER_HEADLINE}}', 'customer headline')
sub('<li>Help with bathing, meals &amp; medication reminders</li><li>Background-checked caregivers you can trust</li><li>Start with a free in-home visit</li>',
    '{{CUSTOMER_BULLETS}}', 'customer bullets')
sub('<span class="cmp-cta">Get a Free Consultation</span>', '<span class="cmp-cta">{{CUSTOMER_CTA}}</span>', 'customer cta')
sub('searches/mo for &ldquo;home care for elderly parent&rdquo;', 'searches/mo for &ldquo;{{CUSTOMER_QUERY}}&rdquo;', 'customer query')
sub('<div class="n">~40</div>', '<div class="n">{{JARGON_VOLUME}}</div>', 'jargon volume')
sub('<div class="n">~2,900</div>', '<div class="n">{{CUSTOMER_VOLUME}}</div>', 'customer volume')
# service list on the multi-page comparison
sub('<li>Personal Care</li><li>Companionship</li><li>Respite Care</li><li>24-Hour &amp; Live-In Care</li><li>Dementia &amp; Alzheimer&rsquo;s Care</li><li>Post-Operative Care</li>',
    '{{SERVICES_LIST}}', 'services list')
# reason #3 body (why-us copy is vertical-specific)
sub('We build for home care and nothing else, so we know what makes seniors and their families in Palm Coast pick one provider and skip the rest. Every page is written to earn that call. Generic agencies just guess.',
    '{{REASON_SPECIALIST_BODY}}', 'reason #3 body')

# ---------------------------------------------------------------- 1. industry-specific assets
sub('kca-assets/ultimate-home care-website-blueprint.pdf', '{{BLUEPRINT_PDF}}', 'blueprint pdf', required=False)
sub('home-care-multipage.png', '{{ASSET_MULTIPAGE}}', 'multipage asset')
sub('home-care-proof-layered.png', '{{ASSET_PROOF}}', 'proof asset')

# ---------------------------------------------------------------- 2. client identity (longest first)
sub('Gihon Family Care Home', '{{COMPANY_NAME}}', 'company name')
sub('gihon-family-care-home', '{{COMPANY_SLUG}}', 'company slug')
sub('gihonfamilycare.com', '{{PREVIEW_DOMAIN}}', 'preview domain')
sub('Palm Coast, FL', '{{CITY}}, {{STATE_ABBR}}', 'city, state')
sub('Palm Coast', '{{CITY}}', 'city')
sub('(470) 918-0516', '{{PHONE}}', 'phone')

# ---------------------------------------------------------------- 3. industry terms (longest / most-cased first)
sub('SERVE MORE SENIORS', '{{OUTCOME_UPPER}}', 'outcome upper', required=False)
sub('Serve More Seniors', '{{OUTCOME_TC}}', 'outcome title', required=False)
sub('serve more seniors', '{{OUTCOME_LC}}', 'outcome lower', required=False)
sub('More Seniors Served', '{{OUTCOME_RESULT}}', 'outcome result', required=False)
sub('More Seniors See You', '{{OUTCOME_SEEN}}', 'outcome seen', required=False)
sub('More Seniors', '{{CUSTOMER_NOUN_TC_MORE}}', 'more + customers', required=False)

sub('HOME CARE', '{{INDUSTRY_UC}}', 'industry UC', required=False)
sub('Home Care', '{{INDUSTRY}}', 'industry TC')
sub('home care', '{{INDUSTRY_LC}}', 'industry lc')

sub('care providers', '{{PROVIDER_TERM_PL}}', 'provider plural', required=False)
sub('Care Providers', '{{PROVIDER_TERM_PL_TC}}', 'provider plural TC', required=False)
sub('care provider', '{{PROVIDER_TERM}}', 'provider', required=False)

sub('SENIORS', '{{CUSTOMER_NOUN_UC}}', 'customers UC', required=False)
sub('Seniors', '{{CUSTOMER_NOUN_TC}}', 'customers TC', required=False)
sub('seniors', '{{CUSTOMER_NOUN}}', 'customers')
sub('senior', '{{CUSTOMER_NOUN_S}}', 'customer singular', required=False)

sub('consultations', '{{SERVICE_TERM_PL}}', 'service plural', required=False)
sub('Consultations', '{{SERVICE_TERM_PL_TC}}', 'service plural TC', required=False)
sub('Consultation', '{{SERVICE_TERM_TC}}', 'service TC', required=False)
sub('consultation', '{{SERVICE_TERM}}', 'service term')

sub('families', '{{BUYER_NOUN}}', 'families -> buyer', required=False)
sub('caregiver at the door', '{{WORKER_TERM}} at the door', 'worker at the door', required=False)

open(OUT, 'w', encoding='utf-8').write(h)

# ---------------------------------------------------------------- report
print(f'{SRC} ({orig_len:,}) -> {OUT} ({len(h):,})')
print('\nreplacements:')
for status, label, n in report:
    print(f'  {"·" if status=="ok" else "!!"} {label:<46} x{n}')

leftovers = {}
stripped = re.sub(r'\{\{[A-Z_]+\}\}', '', h)   # ignore token names (HEADLINE contains 'ADL')
for w in ['Gihon', 'gihonfamilycare', 'Palm Coast', 'home care', 'Home Care',
          'senior', 'Senior', 'caregiver', 'consultation', 'elderly', 'ADL']:
    c = stripped.count(w)
    if c:
        leftovers[w] = c
print('\nresidual industry/client words (should be empty):')
print('  ' + (json.dumps(leftovers) if leftovers else 'none — clean'))

toks = sorted(set(re.findall(r'\{\{([A-Z_]+)\}\}', h)))
print(f'\ntokens in template ({len(toks)}):\n  ' + ', '.join(toks))
