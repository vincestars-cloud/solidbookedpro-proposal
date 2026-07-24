#!/usr/bin/env python3
# SolidBooked Pro proposal-page builder.
# Reads the reference layout, applies SBP branding + section edits + GHL/industry
# tokens, and writes a rendered instance. The GHL automation calls the equivalent:
#   webhook(contact) -> CFG below -> substitute -> deploy to proposal.solidbookedpro.com/{slug}
import re, sys

# ---------- PER-CLIENT CONFIG (the automation fills this from the GHL webhook) ----------
# GHL merge fields: company_name={{contact.company_name}}, industry={{contact.industry}},
# city={{contact.city}}, state={{contact.state}}
CFG = {
    'company_name': 'Gihon Family Care Home',
    'industry_raw': 'roofing',                 # source industry token in the layout
    'industry':     'Home Care',               # humanized {{contact.industry}}, first letter cap
    'industry_lc':  'home care',
    'city':  'Palm Coast',                     # <- from GHL {{contact.city}} / their Google page
    'state': 'Florida',                        # <- from GHL {{contact.state}}
    'slug':  'gihon-family-care-home',
    'preview_domain': 'gihonfamilycare.com',   # shown in laptop chrome (not the real/openable url)
    'demo_url': 'https://demo.scalingsos.com/gihon-family-care-home/',  # real demo shown in laptop
    'phone':   '(470) 918-0516',   # <- GHL {{contact.phone}}
    'address': 'Palm Coast, FL',   # <- GHL {{contact.address}}
    'first_name': '[First Name]',  # <- GHL {{contact.first_name}}
    # ----- industry-derived terms (INDUSTRY_TERMS['home care']) -----
    'customer_noun':   'seniors',              # HOMEOWNERS ->
    'service_term':    'consultation',         # estimate / inspection ->
    'provider_term':   'care provider',        # contractor ->
    'outcome_upper':   'SERVE MORE SENIORS',   # SELL MORE ROOFS ->
    'founder_name':    '[Your Founder]',       # Dean White -> (needs SBP info)
}

# Term map the automation (n8n) keys on {{contact.industry}} — all 23 target verticals.
INDUSTRY_TERMS = {
    'cleaning':           {'customer_noun':'homeowners',  'service_term':'quote',        'provider_term':'cleaning company',    'outcome_upper':'BOOK MORE CLEANINGS'},
    'diesel mechanic':    {'customer_noun':'fleet owners','service_term':'estimate',     'provider_term':'shop',                'outcome_upper':'FIX MORE TRUCKS'},
    'electrical':         {'customer_noun':'homeowners',  'service_term':'estimate',     'provider_term':'electrician',         'outcome_upper':'BOOK MORE JOBS'},
    'fencing':            {'customer_noun':'homeowners',  'service_term':'quote',        'provider_term':'fence company',       'outcome_upper':'BUILD MORE FENCES'},
    'flooring':           {'customer_noun':'homeowners',  'service_term':'quote',        'provider_term':'flooring company',    'outcome_upper':'INSTALL MORE FLOORS'},
    'funeral home':       {'customer_noun':'families',    'service_term':'consultation', 'provider_term':'funeral home',        'outcome_upper':'SERVE MORE FAMILIES'},
    'home care':          {'customer_noun':'seniors',     'service_term':'consultation', 'provider_term':'care provider',       'outcome_upper':'SERVE MORE SENIORS'},
    'hvac':               {'customer_noun':'homeowners',  'service_term':'estimate',     'provider_term':'HVAC company',        'outcome_upper':'BOOK MORE JOBS'},
    'landscaping':        {'customer_noun':'homeowners',  'service_term':'quote',        'provider_term':'landscaper',          'outcome_upper':'BOOK MORE PROJECTS'},
    'mobile mechanic':    {'customer_noun':'drivers',     'service_term':'quote',        'provider_term':'mobile mechanic',     'outcome_upper':'FIX MORE CARS'},
    'mobile truck repair':{'customer_noun':'fleet owners','service_term':'estimate',     'provider_term':'repair shop',         'outcome_upper':'FIX MORE TRUCKS'},
    'mold remediation':   {'customer_noun':'homeowners',  'service_term':'inspection',   'provider_term':'remediation company', 'outcome_upper':'BOOK MORE JOBS'},
    'moving':             {'customer_noun':'homeowners',  'service_term':'quote',        'provider_term':'moving company',      'outcome_upper':'BOOK MORE MOVES'},
    'painting':           {'customer_noun':'homeowners',  'service_term':'quote',        'provider_term':'painting company',    'outcome_upper':'BOOK MORE JOBS'},
    'pest control':       {'customer_noun':'homeowners',  'service_term':'inspection',   'provider_term':'pest control company','outcome_upper':'BOOK MORE TREATMENTS'},
    'plumbing':           {'customer_noun':'homeowners',  'service_term':'estimate',     'provider_term':'plumber',             'outcome_upper':'BOOK MORE JOBS'},
    'remodeling':         {'customer_noun':'homeowners',  'service_term':'consultation', 'provider_term':'remodeler',           'outcome_upper':'BOOK MORE PROJECTS'},
    'roofing':            {'customer_noun':'homeowners',  'service_term':'inspection',   'provider_term':'contractor',          'outcome_upper':'SELL MORE ROOFS'},
    'septic tank':        {'customer_noun':'homeowners',  'service_term':'quote',        'provider_term':'septic company',      'outcome_upper':'BOOK MORE JOBS'},
    'solar':              {'customer_noun':'homeowners',  'service_term':'consultation', 'provider_term':'solar company',       'outcome_upper':'CLOSE MORE INSTALLS'},
    'therapy/counseling': {'customer_noun':'clients',     'service_term':'consultation', 'provider_term':'practice',            'outcome_upper':'BOOK MORE CLIENTS'},
    'tree repair':        {'customer_noun':'homeowners',  'service_term':'quote',        'provider_term':'tree service',        'outcome_upper':'BOOK MORE JOBS'},
    'tree service':       {'customer_noun':'homeowners',  'service_term':'quote',        'provider_term':'tree service',        'outcome_upper':'BOOK MORE JOBS'},
}

def titlecap(s): return s[:1].upper()+s[1:]
def UP(s): return s.upper()

doc = open('../osaat-proposal/page.html', encoding='utf-8').read()

# ============ 1. SECTION REMOVALS ============
# 1a. $1M proof + case-study videos -> replaced by a slim risk-reversal promise band
promise = ('<section class="sbp-promise-band"><div class="sbp-promise-inner">'
           'Cancel any time after month 3 &middot; no long-term contracts &middot; '
           '<span class="sbp-promise-hl">the risk is on us.</span>'
           '</div></section>')
doc, n_proof = re.subn(r'<section\b[^>]*section-proof[^>]*>.*?</section>', promise, doc, flags=re.S)
# 1b. e-signature acceptance section -> removed
doc, n_accept = re.subn(r'<section\b[^>]*id="accept"[^>]*>.*?</section>', '', doc, flags=re.S)
# 1c. Open Live Site button -> removed
doc, n_live = re.subn(r'<a\b[^>]*cover-open-live[^>]*>.*?</a>', '', doc, flags=re.S)
# 1d. ROI calculator + client-builds carousel sections + footer tagline -> removed
doc, n_roi = re.subn(r'<section\b[^>]*section-roi[^>]*>.*?</section>', '', doc, flags=re.S)
doc, n_car = re.subn(r'<section\b[^>]*section-client-builds[^>]*>.*?</section>', '', doc, flags=re.S)
doc, n_ftag = re.subn(r'<p\b[^>]*footer-tag[^>]*>.*?</p>', '', doc, flags=re.S)
# 1e. Traffic & Conversion "How?" panels -> strip screenshot figures [2026-07-24]
# NOTE (2026-07-25): those cards are now HAND-ENRICHED to Trust's full anatomy (emoji + bullets +
# "Why this works" callout + CTA) directly in index.html. This strip only yields sparse cards; if
# this generator is revived, templatize the 5 traffic/conversion cards with INDUSTRY_TERMS to match.
doc, n_fig = re.subn(r'<figure class="fhow-card-img">.*?</figure>', '', doc, flags=re.S)
# 1g. Before/After heading -> osaat "Setting industry standards" treatment (accent word + bold sub)
doc = doc.replace('<h2 class="rv">Before and After</h2>', '<h2 class="rv ba-title">Before and <span class="ba-accent">After</span></h2>')
doc = doc.replace('<p class="lede rv">Same business, same services, same owner. Only the first impression changed.</p>', '<p class="lede rv ba-sub">Same business, same services, same owner. <strong>Only the first impression changed.</strong></p>')
# 1f. real branded reel thumbnails (remote poster jpgs -> local pngs shipped in repo)
doc = doc.replace('poster="https://prep.solidbookedpro.com/assets/img/poster-reel-deonco.jpg"', 'poster="poster-reel-deonco.png"')
doc = doc.replace('poster="https://prep.solidbookedpro.com/assets/img/poster-reel-ijeoma.jpg"', 'poster="poster-reel-ijeoma.png"')

# ============ 2. LAPTOP PREVIEW: non-interactive home-care mock (no live URL) ============
MOCK = ('<div style=\'font-family:Open Sans,sans-serif;color:#0F172A;background:#fff\'>'
        '<div style=\'display:flex;align-items:center;justify-content:space-between;padding:14px 24px;background:#0F172A;color:#fff\'>'
        '<b style=\'font-family:Montserrat;letter-spacing:.3px\'>' + CFG['company_name'] + '</b>'
        '<span style=\'font-size:12px;opacity:.85\'>Home &nbsp; Services &nbsp; About &nbsp; Contact</span></div>'
        '<div style=\'position:relative;padding:52px 40px;background:linear-gradient(120deg,#1D4ED8,#2563EB);color:#fff\'>'
        '<div style=\'font-size:11px;letter-spacing:2px;font-weight:700;color:#BFDBFE;margin-bottom:12px\'>COMPASSIONATE HOME CARE &middot; ' + UP(CFG['city']) + ' &amp; ' + UP(CFG['state']) + '</div>'
        '<div style=\'font-family:Montserrat;font-weight:800;font-size:30px;line-height:1.1;max-width:560px\'>Trusted, compassionate care for the ' + CFG['customer_noun'] + ' you love.</div>'
        '<div style=\'margin:14px 0 22px;font-size:14px;color:#E0EAFF;max-width:460px\'>Personal care, companion care, and respite &mdash; right at home.</div>'
        '<span style=\'display:inline-block;background:#fff;color:#1D4ED8;font-weight:800;padding:12px 22px;border-radius:8px;font-size:13px\'>Schedule a Free ' + titlecap(CFG['service_term']) + ' &rarr;</span></div>'
        '<div style=\'display:flex;gap:12px;padding:20px 40px;background:#EAF1FE\'>'
        '<div style=\'flex:1;background:#fff;border:1px solid #DBEAFE;border-radius:10px;padding:14px;font-size:12px;color:#475569\'>Personal Care</div>'
        '<div style=\'flex:1;background:#fff;border:1px solid #DBEAFE;border-radius:10px;padding:14px;font-size:12px;color:#475569\'>Companion Care</div>'
        '<div style=\'flex:1;background:#fff;border:1px solid #DBEAFE;border-radius:10px;padding:14px;font-size:12px;color:#475569\'>Respite Care</div></div></div>')
MOCK_ATTR = MOCK.replace('"', '&quot;')
# swap both laptop iframes to the REAL demo we built for them, non-interactive (no way to open live)
doc = re.sub(r'src="https://osaat-roofing-construction\.vercel\.app[^"]*"',
             'src="' + CFG['demo_url'] + '" style="pointer-events:none" tabindex="-1"', doc)

# ============ 3. BRANDING: logo, client wordmark, color remap ============
# 3a. agency logo (top-left) -> SBP white logo; hide the KCA text wordmark
doc = doc.replace('kca-logo.svg', 'sbp-logo-white.png')
# 3b. client logo (top-right) -> typed company name from GHL
doc = re.sub(r'<img\b[^>]*client-logo[^>]*>',
             '<span class="topbar-client-text">' + CFG['company_name'] + '</span>', doc)
# 3c. color remap: reference red+gold-on-black -> SBP blue system
COLOR_MAP = {
    '#eeb644':'#2563EB', '#ae312d':'#2563EB',      # gold + red -> primary blue
    '#7a1f1c':'#1D4ED8', '#c9941f':'#1D4ED8',      # dark red/gold -> blue-dark
    '#ffcb58':'#60A5FA', '#ffd700':'#60A5FA', '#ffe9a7':'#BFDBFE', '#ffc857':'#93C5FD',
    '#7a5a0a':'#1E40AF', '#fbf5e5':'#EAF1FE', '#faf8f1':'#F6F9FF', '#fbf5e5':'#EAF1FE',
    '#ffcb58':'#60A5FA',
}
for a, b in COLOR_MAP.items():
    doc = re.sub(re.escape(a), b, doc, flags=re.I)

# ============ 4. TEXT / INDUSTRY / LOCATION SWAPS (ordered) ============
company = CFG['company_name']
reps = [
    # brand
    ('King Contractor Agency LLC','SolidBooked Pro'), ('King Contractor Agency','SolidBooked Pro'),
    ('King Contractor','SolidBooked Pro'), ('KingContractor.com','solidbookedpro.com'),
    ('kingcontractor.com','solidbookedpro.com'),
    # founder = Vince (his name; bio stays roofing = his real track record, restored below)
    ('Dean White', 'Vince Stars'), ('Dean', 'Vince'),
    # client company
    ('OSAAT Roofing &amp; Construction, LLC', company), ('OSAAT Roofing & Construction, LLC', company),
    ('OSAAT Roofing &amp; Construction', company), ('OSAAT Roofing & Construction', company), ('OSAAT', company),
    # product name
    ('AI Smart Website','Smart Website'),
    # outcome (Title-case in source, uppercased via CSS) -> home-care outcome
    ('Sell More Roofs','Serve More Seniors'), ('More Roofs Sold','More Seniors Served'),
    ('SELL MORE ROOFS', CFG['outcome_upper']),
    # laptop chrome + serp (not clickable)
    ('osaatconstruction.com', CFG['preview_domain']), ('(your live preview)','(preview only)'),
    ('houston', CFG['city']),
    # roofing-scenario prose -> home-care equivalents (flagged for copy review)
    ('Roof Replacement','Home Care'), ('Roof-curious','Care-curious'), ('roof-curious','care-curious'),
    ('crew walks the roof same week','caregiver visits that week'),
    ('walks the roof','visits the home'), ('walk the roof','visit the home'),
    ('person on the roof','caregiver at the door'),
    ('Roofs','Seniors'),
    # industry
    ('ROOFING', UP(CFG['industry'])), ('Roofing', CFG['industry']), ('roofing', CFG['industry_lc']),
    ('Roofers', titlecap(CFG['provider_term'])+'s'), ('roofers', CFG['provider_term']+'s'),
    ('Roofer', titlecap(CFG['provider_term'])), ('roofer', CFG['provider_term']),
    ('roofs', CFG['customer_noun']),
    # provider / contractor
    ('CONTRACTOR', UP(CFG['provider_term'])), ('Contractor', titlecap(CFG['provider_term'])), ('contractor', CFG['provider_term']),
    # customer noun
    ('HOMEOWNERS', UP(CFG['customer_noun'])), ('Homeowners', titlecap(CFG['customer_noun'])),
    ('homeowners', CFG['customer_noun']), ('homeowner', CFG['customer_noun'].rstrip('s')),
    # service term
    ('INSPECTION', UP(CFG['service_term'])), ('Inspection', titlecap(CFG['service_term'])), ('inspection', CFG['service_term']),
    ('ESTIMATE', UP(CFG['service_term'])), ('Estimate', titlecap(CFG['service_term'])), ('estimate', CFG['service_term']),
    # location
    ('Central Texas', 'Central ' + CFG['state']), ('Texas', CFG['state']),
    ('Houston', CFG['city']), ('Killeen', CFG['city']),
    # client DATA pulled from GHL (factual merge fields) + removals
    ('(512) 791-5774', CFG['phone']),
    ('8376 Davis Blvd, Suite 249, Spring, TX', CFG['address']),
    ('Licensed (TX #03-0235)', ''),
    ('Chris', CFG['first_name']),
    ('Founder of KCA', 'Founder of SolidBooked Pro'),
    # ---- POST-SWAP fixes: MUST run after the industry swaps above ----
    # founder bio stays Vince's real roofing track record (restore after roofing->home care)
    ('home care companies','roofing companies'), ('in seniors sold','in roofs sold'),
    ('the home care community','the roofing community'),
    # promise + wording polish
    ('My priority is to help you','My only priority is to help you'),
    ('sell more seniors','serve more seniors'), ('help you sell','help you serve'),
    ('average ticket','average client value'), ('Average ticket','Average client value'), ('per job','per client'),
]
for a, b in reps:
    doc = doc.replace(a, b)

# ============ 5. HIDE review block + append SBP brand + mobile-first CSS ============
BRAND_CSS = '''
<style id="sbp-brand">
:root{--sbp-blue:#2563EB;--sbp-blue-dark:#1D4ED8;--sbp-navy:#0F172A;--sbp-bg-blue:#EAF1FE;}
/* logo top-left */
.kca-mark img{height:40px!important;width:auto!important}
.kca-mark .kca-name{display:none!important}
@media(max-width:768px){.kca-mark img{height:32px!important}}
/* client wordmark top-right */
.topbar-client-mark .topbar-client-text{font-family:'Montserrat',sans-serif;font-weight:800;font-size:16px;color:#fff;text-transform:none;letter-spacing:.2px;text-align:right;line-height:1.15}
@media(max-width:768px){.topbar-client-mark .topbar-client-text{font-size:12px}}
/* removed review block + off-brand gold crown artifacts */
.dean-reviews-block{display:none!important}
.cover-laptop-crown,.pricing-hero-crown,.kca-crown::before{display:none!important}
/* remove agency-side edit controls (edit pricing / undo / edit proposal / checklist edit) */
.setup-fee-edit,.footer-undo-btn,.addon-footer-btn,#kcaUndo,[class*="pencil"],[onclick*="openEditModal"],[onclick*="EditModal"],[onclick*="toggleSuccessChecklistEdit"]{display:none!important}
/* plus signs between Traffic/Trust/Conversion were blue-on-blue -> make them white */
.formula-op{color:#fff!important}
/* make the 'Tap to expand' reputation pill stand out (was blending in) */
.ai-rep-hint{background:#2563EB!important;color:#fff!important;padding:5px 14px!important;border-radius:100px!important;font-weight:800!important;font-size:11px!important;letter-spacing:.05em!important;text-transform:uppercase!important;box-shadow:0 4px 12px rgba(37,99,235,.35)!important}
/* risk-reversal promise band (replaces $1M proof) */
.sbp-promise-band{background:#030303;padding:clamp(48px,7vw,84px) 0}
.sbp-promise-inner{max-width:960px;margin:0 auto;padding:0 24px;text-align:center;font-family:'Montserrat',sans-serif;font-weight:800;font-size:clamp(19px,2.6vw,30px);line-height:1.35;color:#fff}
.sbp-promise-hl{color:#3B82F6}
/* wordmark font per SBP brand */
.cover h1,.section-title,.kca-name{font-family:'Montserrat',sans-serif}
</style>
'''
MOBILE_CSS = '''
<style id="sbp-mobile">
html,body{max-width:100%;overflow-x:hidden}
img,video,iframe,svg{max-width:100%}
@media(max-width:768px){
  .topbar-inner{padding:0 16px;gap:10px}
  .cover{padding:56px 0 44px}
  .cover-inner{padding:0 18px}
  .cover-grid{grid-template-columns:1fr!important;gap:32px}
  .cover h1{font-size:clamp(32px,8vw,44px)!important}
  .cover-bullets .cb-label{font-size:16px!important}
  .section-inner,.cover-inner{padding-left:18px;padding-right:18px}
  .formula-horizontal{flex-direction:column;gap:14px}
  .formula-op{transform:rotate(90deg)}
  .section-three-reasons .reasons{grid-template-columns:1fr!important}
  .wid-bullets{grid-template-columns:1fr!important}
  .dean-intro-grid,.frustration-grid{grid-template-columns:1fr!important}
  /* prevent horizontal overflow: let flex/grid children shrink */
  *{min-width:0}
  .cover-laptop{max-width:100%!important}
  .formula-pillar,.formula-result-pill{padding:16px 14px!important}
  .formula-pillar-term,.formula-result-text{font-size:19px!important}
}
/* AI section: keep website + chat + call on one line and shrink together (no phone drop) */
.ai-row,.ai-row-mock{min-width:0}
.ai-row-mock{flex-wrap:nowrap!important}
.ai-row-mock > *{min-width:0;flex:0 1 auto}
@media(max-width:1024px){ .ai-row{gap:12px} .ai-row > *{min-width:0;flex-shrink:1} }
@media(max-width:860px){ .ai-row-mock{transform:scale(.82);transform-origin:top center} }
@media(max-width:620px){ .ai-row-mock{transform:scale(.66)} }
</style>
'''
# Consolidated responsive + polish fixes (2026-07-24 per Vince) — appended LAST so it wins the cascade.
FIXES_CSS = '''<style id="sbp-fixes">
/* Formula: below 3-across, stack to a centered single column; operators centered (not floating right) */
@media(max-width:1024px){
  .formula-horizontal{flex-direction:column!important;align-items:stretch!important;gap:16px!important}
  .formula-pillar,.formula-result-pill{width:100%!important;flex:1 1 auto!important;min-width:0!important}
  .formula-op{align-self:center!important;margin:2px auto!important;transform:none!important}
}
/* AI journey: keep website + chat + call on ONE line (1x3); scale as a unit; phone keeps aspect (no stretch) */
.ai-journey{flex-wrap:nowrap!important}
.ai-journey-arrow{transform:none!important;flex:0 0 auto}
.ai-journey .ai-phone{width:300px!important;max-width:300px!important;flex:0 0 auto}
@media(max-width:1080px){.ai-journey{zoom:.86}}
@media(max-width:940px){.ai-journey{zoom:.72}}
@media(max-width:760px){.ai-journey{zoom:.60}}
@media(max-width:600px){.ai-journey{zoom:.48}}
@media(max-width:470px){.ai-journey{zoom:.38}}
@media(max-width:400px){.ai-journey{zoom:.30}}
/* Founder: portrait stays on the RIGHT on resize; stack only on true mobile */
@media(min-width:561px){.dean-intro-grid{grid-template-columns:1.05fr .95fr!important;gap:clamp(28px,4vw,56px)!important;align-items:center!important}}
@media(max-width:560px){.dean-intro-grid{grid-template-columns:1fr!important}}
.dean-portrait-wrap{min-width:0}
/* Timeline: keep Day 1/2/3 as 1x3; stack only on true mobile */
.timeline{grid-template-columns:repeat(3,minmax(0,1fr))!important;max-width:920px;margin-left:auto;margin-right:auto}
@media(max-width:640px){.timeline{grid-template-columns:1fr!important}}
/* Answers deck (prep-ported): kill leftover Playfair serif + gold; use page Montserrat + SBP blue */
.prep-ported-block{--serif:'Montserrat',sans-serif;--sans:'Open Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;--gold:#2563EB;--gold-l:#60A5FA;--navy:#0F172A}
.prep-ported-block .slide .big{font-family:'Montserrat',sans-serif!important;letter-spacing:-0.01em}
.prep-ported-block .slide .pop,.prep-ported-block .gold,.prep-ported-block .eyebrow{color:#2563EB!important}
.prep-ported-block .eyebrow:before,.prep-ported-block .eyebrow:after{background:#2563EB!important}
/* Before/After: full-image landscape-width cards (no portrait crop) + osaat "Setting industry standards" type scale */
.bagrid .bacard{flex:0 0 clamp(280px,38vw,360px)!important;height:auto!important}
.bagrid .bacard img{height:auto!important;object-fit:contain!important}
.bagrid{align-items:flex-start}
.prep-ported-block .ba-title{font-weight:900!important;font-size:clamp(26px,3.4vw,34px)!important;letter-spacing:-0.012em!important}
.prep-ported-block .ba-title .ba-accent{color:#2563EB}
.prep-ported-block .ba-sub{font-family:'Open Sans',sans-serif;font-size:clamp(15px,1.9vw,19px)}
.prep-ported-block .ba-sub strong{color:#0F172A;font-weight:700}
/* Before/After carousel dots (autoplay JS lives in index.html #ba-scroll: setInterval 4.5s + dot nav + left-align) */
.ba-dots{display:flex;justify-content:center;flex-wrap:wrap;gap:9px;margin-top:22px}
.ba-dot{width:9px;height:9px;border-radius:50%;border:0;background:#CBD5E1;cursor:pointer;padding:0;-webkit-appearance:none;transition:background .25s,transform .25s}
.ba-dot:hover{background:#93C5FD}
.ba-dot.active{background:#2563EB;transform:scale(1.3)}
/* In their words: keep the 2 testimonial videos 2-up from tablet down (was 820px) */
@media(min-width:560px){.reels{grid-template-columns:1fr 1fr!important}}
/* In their words: center the testimonial quote + caption */
.reel .meta{text-align:center}
</style>
'''
doc = doc.replace('</head>', BRAND_CSS + MOBILE_CSS + '</head>')

# meta title cleanup
doc = re.sub(r'<title>.*?</title>', '<title>Your Custom ' + CFG['industry'] + ' Website Is Ready &middot; ' + company + ' &middot; SolidBooked Pro</title>', doc, flags=re.S)

# ============ PLAN PICKER: interactive 3-tier pricing (replaces section-grey listed view) ============
_chk = '<span class="pp-check"><svg viewBox="0 0 24 24"><path d="M4 12l5 5L20 6"/></svg></span>'
PP_CSS = '''<style id="sbp-plan-picker">
.plan-picker{background:#F6F9FF;color:#0F172A;font-family:'Open Sans',sans-serif;padding:clamp(48px,7vw,84px) 20px}
.pp-inner{max-width:940px;margin:0 auto}
.pp-h2{font-family:'Montserrat',sans-serif;text-align:center;font-size:clamp(24px,3.4vw,36px);font-weight:800;line-height:1.15;max-width:20ch;margin:0 auto 40px;letter-spacing:-0.01em}
.pp-diagram{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:clamp(10px,2vw,28px);max-width:840px;margin:0 auto}
.pp-side{display:flex;align-items:center;gap:12px;transition:opacity .25s}
.pp-left{justify-content:flex-end;text-align:right}.pp-right{justify-content:flex-start;text-align:left}
.pp-side-label{font-family:'Montserrat',sans-serif;font-weight:700;font-size:clamp(13px,1.5vw,15px);max-width:150px;line-height:1.25}
.pp-arrow{color:#2563EB;font-size:30px;font-weight:900;flex-shrink:0;line-height:1}
.pp-center{display:flex;flex-direction:column;align-items:center;gap:10px}
.pp-preview{width:clamp(160px,27vw,232px);border-radius:12px;border:1px solid #dbe4f3;background:#fff;box-shadow:0 14px 34px rgba(15,23,42,.14);overflow:hidden}
.pp-preview-bar{background:#e6edf9;padding:7px 10px;display:flex;gap:5px}
.pp-preview-bar i{width:8px;height:8px;border-radius:50%;background:#b9c6de;display:block}
.pp-preview-body{aspect-ratio:16/10;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:6px;background:linear-gradient(160deg,#eaf1fe,#fff)}
.pp-preview-body b{font-family:'Montserrat',sans-serif;font-size:14px;color:#1D4ED8;font-weight:800}
.pp-preview-body span{font-size:11px;color:#64748b}
.pp-down{display:flex;flex-direction:column;align-items:center;gap:5px;margin-top:4px;transition:opacity .25s}
.pp-arrow-down{font-size:26px}.pp-down .pp-side-label{text-align:center;max-width:190px}
.pp-included{margin:46px auto 0;max-width:560px}
.pp-included h3{font-family:'Montserrat',sans-serif;font-weight:800;font-size:18px;margin-bottom:16px}
.pp-list{list-style:none;padding:0;display:flex;flex-direction:column;gap:12px}
.pp-item{display:flex;align-items:flex-start;gap:12px;font-size:15.5px;line-height:1.4;transition:opacity .25s}
.pp-check{width:22px;height:22px;border-radius:50%;background:#16A34A;color:#fff;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}
.pp-check svg{width:12px;height:12px;fill:none;stroke:#fff;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.pp-off{opacity:.42}
.pp-item.pp-off{color:#64748b}.pp-item.pp-off .pp-check{background:#cbd5e1}
.pp-item.pp-off .pp-item-text{text-decoration:line-through;text-decoration-color:rgba(100,116,139,.55)}
.pp-side.pp-off .pp-arrow,.pp-down.pp-off .pp-arrow{color:#cbd5e1}
.pp-side.pp-off .pp-side-label,.pp-down.pp-off .pp-side-label{color:#64748b;text-decoration:line-through;text-decoration-color:rgba(100,116,139,.5)}
.pp-q{font-family:'Montserrat',sans-serif;text-align:center;font-weight:800;margin:48px 0 22px;font-size:clamp(21px,2.7vw,28px)}
.pp-plans{display:flex;gap:16px;justify-content:center;flex-wrap:wrap}
.pp-plan{cursor:pointer;border:2px solid #EAB308;background:#FEF9C3;color:#0F172A;border-radius:14px;padding:18px 28px;min-width:148px;display:flex;flex-direction:column;align-items:center;gap:3px;font-family:'Montserrat',sans-serif;transition:transform .12s,box-shadow .2s,background .2s,border-color .2s,color .2s}
.pp-plan span{font-size:12.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;opacity:.82}
.pp-plan b{font-size:27px;font-weight:800}
.pp-plan:hover{transform:translateY(-2px)}
.pp-plan.pp-selected{background:#16A34A;border-color:#15803D;color:#fff;box-shadow:0 14px 28px rgba(22,163,74,.35)}
@media(max-width:640px){.pp-diagram{grid-template-columns:1fr;gap:18px}.pp-left,.pp-right{justify-content:center;text-align:center}.pp-side .pp-arrow{transform:rotate(90deg)}.pp-plan{min-width:104px;padding:15px 18px}.pp-plan b{font-size:23px}}
</style>'''
PP_HTML = ('<section class="plan-picker"><div class="pp-inner">'
  '<h2 class="pp-h2">The Site That Only Costs You Something If It Works</h2>'
  '<div class="pp-diagram">'
  '<div class="pp-side pp-left" data-tier="2"><span class="pp-side-label">5-Star Outreach System</span><span class="pp-arrow">&#8594;</span></div>'
  '<div class="pp-center"><div class="pp-preview"><div class="pp-preview-bar"><i></i><i></i><i></i></div>'
  '<div class="pp-preview-body"><b>Site Preview</b><span>Your live demo</span></div></div>'
  '<div class="pp-down" data-tier="3"><span class="pp-arrow pp-arrow-down">&#8595;</span><span class="pp-side-label">24/7 Receptionist Follow&#8209;Up</span></div></div>'
  '<div class="pp-side pp-right" data-tier="3"><span class="pp-arrow">&#8592;</span><span class="pp-side-label">Monthly Qualified Prospect Guarantee</span></div>'
  '</div>'
  '<div class="pp-included"><h3>What&rsquo;s included:</h3><ul class="pp-list">'
  '<li class="pp-item" data-tier="1">'+_chk+'<span class="pp-item-text">Full custom '+CFG['industry']+' website built in 3 days</span></li>'
  '<li class="pp-item" data-tier="1">'+_chk+'<span class="pp-item-text">SEO + AEO foundation indexed</span></li>'
  '<li class="pp-item" data-tier="1">'+_chk+'<span class="pp-item-text">Hosting + SSL</span></li>'
  '<li class="pp-item" data-tier="1">'+_chk+'<span class="pp-item-text">Google Business Profile, optimized, syncing reviews</span></li>'
  '<li class="pp-item" data-tier="1">'+_chk+'<span class="pp-item-text">Mobile-first design that converts on a 5-inch screen</span></li>'
  '<li class="pp-item" data-tier="1">'+_chk+'<span class="pp-item-text">Same-day '+CFG['service_term']+' booking via live form</span></li>'
  '<li class="pp-item" data-tier="2">'+_chk+'<span class="pp-item-text">5-Star Outreach System to increase reviews &amp; ranking</span></li>'
  '<li class="pp-item" data-tier="3">'+_chk+'<span class="pp-item-text">24/7 Missed Call &amp; Follow-Up Receptionist</span></li>'
  '</ul></div>'
  '<h3 class="pp-q">Which option will be right for you?</h3>'
  '<div class="pp-plans">'
  '<button class="pp-plan" data-plan="1"><span>One Time</span><b>$297</b></button>'
  '<button class="pp-plan" data-plan="2"><span>One Time</span><b>$497</b></button>'
  '<button class="pp-plan" data-plan="3"><span>One Time</span><b>$997</b></button>'
  '</div></div></section>')
PP_JS = "<script>(function(){var p=document.querySelector('.plan-picker');if(!p)return;var P=p.querySelectorAll('.pp-plan'),I=p.querySelectorAll('[data-tier]');function s(n){n=+n;P.forEach(function(b){b.classList.toggle('pp-selected',+b.dataset.plan===n)});I.forEach(function(e){e.classList.toggle('pp-off',+e.getAttribute('data-tier')>n)})}P.forEach(function(b){b.addEventListener('click',function(){s(b.dataset.plan)})});s(3);})();</script>"
doc, n_pp = re.subn(r'<section\b[^>]*section-grey[^>]*>.*?</section>', lambda m: PP_HTML, doc, count=1, flags=re.S)
doc = doc.replace('</head>', PP_CSS + '</head>')
doc = doc.replace('</body>', PP_JS + '</body>')
doc = doc.replace('</head>', FIXES_CSS + '</head>')   # append LAST so responsive fixes win the cascade

# ---- "How we write your site" comparison section (injected AFTER Three reasons) ----
# Per-industry copy in cmp_section.INDUSTRY_COMPARE (23 verticals, keyed on industry_lc —
# the same key n8n passes). Mirror into the n8n wrapper when built, like INDUSTRY_TERMS.
from cmp_section import CMP_CSS, build_cmp
from forms_section import FORMS_CSS, build_forms   # form comparison + book-online proof, sits under cmp
doc = doc.replace('</head>', CMP_CSS + FORMS_CSS + '</head>')
doc, n_cmp = re.subn(r'(<section\b[^>]*section-three-reasons[^>]*>.*?</section>)',
                     lambda m: m.group(1) + build_cmp(CFG) + build_forms(CFG), doc, count=1, flags=re.S)

# strip dev/pipeline HTML comments (non-visible, keeps template clean)
doc = re.sub(r'<!--.*?-->', '', doc, flags=re.S)
open('index.html','w',encoding='utf-8').write(doc)
print(f"built index.html {len(doc)} bytes | removed: proof={n_proof} accept={n_accept} openlive={n_live} roi={n_roi} carousel={n_car} footertag={n_ftag} | added cmp={n_cmp}")
for chk in ['OSAAT','Roofing','roofing','HOMEOWNERS','King Contractor','#eeb644','#ae312d','Texas','Killeen','Dean White']:
    c = doc.count(chk) if chk not in ('#eeb644','#ae312d') else len(re.findall(chk, doc, re.I))
    if c: print(f"  residual '{chk}': {c}")
