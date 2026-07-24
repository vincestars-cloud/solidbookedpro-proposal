#!/usr/bin/env python3
# Replace the #offer section with the premium osaat-styled hub + checklist + investment.
# Scoped under #offer with so- prefixed classes so nothing leaks into/out of the page.
# Reuses .laptop-viewport/.laptop-iframe so the existing #laptop-fill JS auto-fits the live demo.
import re

DEMO = "https://demo.solidbookedpro.com/gihon-family-care-home/"

OFFER_CSS = """<style id="sbp-offer-css">
#offer.sbp-offer{--accent:#2563EB;--gold:#EEB644;--ink:#030303;--muted:rgba(3,3,3,.72);--gray:#7A7A7A;--cream:#FBF5E5;--line:rgba(0,0,0,.08);box-sizing:border-box;width:100%;padding:66px 60px 78px;overflow-x:hidden;font-family:'Open Sans',sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased;background:radial-gradient(720px 340px at 12% 6%,rgba(37,99,235,.07),transparent 62%),radial-gradient(760px 380px at 92% 26%,rgba(238,182,68,.09),transparent 62%),linear-gradient(180deg,#FFFDF9 0%,#FBF3E6 100%);}
#offer.sbp-offer *{box-sizing:border-box;}
#offer .so-inner{max-width:1180px;margin:0 auto;}
#offer .so-title{font-family:'Montserrat';font-weight:900;font-size:44px;line-height:1.14;letter-spacing:-1px;color:var(--ink);text-align:center;margin:0;}
#offer .so-title .so-acc{color:var(--accent);}
#offer .so-diagram{display:flex;flex-direction:column;align-items:center;margin-top:44px;}
#offer .so-hub{display:flex;align-items:center;justify-content:center;gap:18px;}
#offer .so-sys{width:270px;min-height:132px;background:linear-gradient(180deg,#fff,#FFFDF7);border:1px solid var(--line);border-left:5px solid var(--gold);border-radius:14px;padding:20px 22px;box-shadow:0 22px 48px rgba(15,20,40,.13),0 2px 6px rgba(15,20,40,.05);position:relative;display:flex;flex-direction:column;justify-content:center;}
#offer .so-sys .so-emoji{position:absolute;top:16px;right:18px;font-size:24px;line-height:1;}
#offer .so-sys .so-t{font-family:'Montserrat';font-weight:900;font-size:18px;letter-spacing:-.3px;color:var(--ink);padding-right:34px;line-height:1.2;}
#offer .so-sys .so-s{font-family:'Montserrat';font-weight:700;font-size:12.5px;letter-spacing:.6px;text-transform:uppercase;color:var(--accent);margin-top:9px;}
#offer .so-conn{flex:0 0 auto;width:44px;height:44px;border-radius:50%;background:linear-gradient(160deg,#3B7BF6,#2563EB);display:flex;align-items:center;justify-content:center;border:3px solid #fff;box-shadow:0 10px 22px rgba(37,99,235,.42);}
#offer .so-conn svg{width:22px;height:22px;fill:#fff;}
#offer .so-site{width:452px;border-radius:14px;overflow:hidden;background:#fff;border:1px solid var(--line);box-shadow:0 30px 66px rgba(15,15,15,.20);}
#offer .so-bbar{height:34px;background:#F1EEE7;display:flex;align-items:center;gap:7px;padding:0 13px;border-bottom:1px solid var(--line);}
#offer .so-bbar i{width:10px;height:10px;border-radius:50%;background:#CFC9BE;}
#offer .so-bbar .so-url{margin-left:10px;flex:1;height:20px;background:#fff;border-radius:10px;border:1px solid var(--line);display:flex;align-items:center;padding:0 11px;font-family:'Open Sans';font-size:11px;color:var(--gray);}
#offer .so-bbar .so-url:before{content:'';width:8px;height:8px;border:1.5px solid #B7B0A3;border-radius:50%;margin-right:7px;}
#offer .so-site .laptop-viewport.so-vp{width:100%;height:238px;border-radius:0;}
#offer .so-downcol{display:flex;flex-direction:column;align-items:center;}
#offer .so-conn.so-down{margin:14px 0;}
#offer .so-sys.so-bottom{width:400px;border-left:5px solid var(--accent);display:flex;align-items:center;gap:16px;}
#offer .so-sys.so-bottom .so-ico{flex:0 0 auto;width:46px;height:46px;border-radius:11px;background:rgba(37,99,235,.08);display:flex;align-items:center;justify-content:center;font-size:24px;}
#offer .so-sys.so-bottom .so-tx .so-t{padding-right:0;}
#offer .so-inc{margin-top:52px;background:#fff;border:1px solid var(--line);border-radius:20px;padding:36px 40px 38px;box-shadow:0 30px 66px rgba(15,20,40,.13),0 2px 8px rgba(15,20,40,.05);}
#offer .so-inc-h{display:flex;align-items:center;gap:34px;padding-bottom:24px;margin-bottom:24px;border-bottom:1px solid var(--line);}
#offer .so-inc-h .so-hd{flex:0 0 auto;max-width:230px;font-family:'Montserrat';font-weight:800;font-size:21px;line-height:1.25;letter-spacing:3px;text-transform:uppercase;color:var(--accent);}
#offer .so-inc-h .so-cover{flex:1;text-align:center;font-family:'Montserrat';font-weight:800;font-size:22px;color:var(--ink);letter-spacing:-.3px;}
#offer .so-rows{display:flex;flex-direction:column;gap:12px;}
#offer .so-crow{position:relative;background:linear-gradient(180deg,#FCF7EA,#FAF2DF);border:1px solid rgba(0,0,0,.06);border-radius:12px;padding:16px 58px;text-align:center;box-shadow:inset 0 1px 0 rgba(255,255,255,.6),0 1px 2px rgba(15,20,40,.03);}
#offer .so-crow .so-cbox{position:absolute;left:16px;top:50%;transform:translateY(-50%);width:30px;height:30px;border-radius:8px;background:linear-gradient(160deg,#3B7BF6,#2563EB);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 14px rgba(37,99,235,.4);}
#offer .so-crow .so-cbox svg{width:17px;height:17px;stroke:#fff;stroke-width:3.2;fill:none;}
#offer .so-crow .so-ctext{font-family:'Open Sans';font-size:16.5px;font-weight:600;color:var(--ink);line-height:1.35;}
#offer .so-crow .so-ctext b{font-weight:800;}
#offer .so-invest{margin-top:36px;padding:52px 40px 46px;border:1px solid rgba(255,255,255,.08);border-radius:22px;text-align:center;position:relative;overflow:hidden;color:#fff;background:radial-gradient(560px 320px at 84% -12%,rgba(238,182,68,.20),transparent 60%),radial-gradient(620px 380px at 8% 118%,rgba(37,99,235,.34),transparent 60%),linear-gradient(158deg,#14243F 0%,#0A1526 100%);box-shadow:0 40px 90px rgba(9,18,33,.5),inset 0 1px 0 rgba(255,255,255,.06);}
#offer .so-invest:before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,var(--accent),var(--gold));}
#offer .so-invest .so-crown{position:absolute;top:26px;right:32px;font-size:30px;line-height:1;filter:drop-shadow(0 6px 14px rgba(238,182,68,.55));}
#offer .so-invest .so-kick{display:flex;align-items:center;justify-content:center;gap:12px;color:var(--gold);font-family:'Montserrat';font-weight:800;font-size:14px;letter-spacing:3.5px;text-transform:uppercase;}
#offer .so-invest .so-kick:before,#offer .so-invest .so-kick:after{content:'';width:30px;height:2px;background:rgba(238,182,68,.55);border-radius:2px;}
#offer .so-invest .so-lbl{font-family:'Montserrat';font-weight:800;font-size:12.5px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,.55);margin-top:20px;}
#offer .so-invest .so-price{font-family:'Montserrat';font-weight:900;font-size:82px;line-height:1;letter-spacing:-2.5px;color:#fff;margin-top:12px;text-shadow:0 14px 44px rgba(37,99,235,.4);}
#offer .so-invest .so-price .so-to{font-size:30px;font-weight:700;color:rgba(255,255,255,.5);letter-spacing:0;margin:0 16px;vertical-align:middle;}
#offer .so-invest .so-dep{font-family:'Open Sans';font-size:17px;color:rgba(255,255,255,.62);margin-top:14px;}
#offer .so-invest .so-trust{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:30px;padding-top:30px;border-top:1px dashed rgba(255,255,255,.18);flex-wrap:wrap;}
#offer .so-invest .so-chip{display:inline-flex;align-items:center;gap:9px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.15);border-radius:30px;padding:11px 20px;font-family:'Montserrat';font-weight:700;font-size:14px;color:#fff;}
#offer .so-invest .so-chip .so-c{width:20px;height:20px;border-radius:50%;background:var(--gold);flex:0 0 auto;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 10px rgba(238,182,68,.4);}
#offer .so-invest .so-chip .so-c svg{width:12px;height:12px;stroke:#0A1526;stroke-width:3.6;fill:none;}
@media(max-width:820px){
#offer.sbp-offer{padding:46px 16px 56px;}
#offer .so-title{font-size:30px;}
#offer .so-hub{flex-direction:column;gap:14px;}
#offer .so-hub>.so-conn{display:none;}
#offer .so-sys,#offer .so-site,#offer .so-sys.so-bottom,#offer .so-downcol{width:100%;max-width:440px;}
#offer .so-inc{padding:24px 16px 26px;}
#offer .so-inc-h{flex-direction:column;gap:8px;text-align:center;}
#offer .so-inc-h .so-hd{max-width:none;}
#offer .so-crow{padding:14px 46px 14px 52px;text-align:left;}
#offer .so-invest{padding:34px 20px 30px;}
#offer .so-invest .so-price{font-size:52px;}
#offer .so-invest .so-price .so-to{font-size:22px;margin:0 8px;}
}
</style>"""

CK = '<svg viewBox="0 0 24 24"><path d="M4 12l5 5L20 6"/></svg>'
AR_R = '<svg viewBox="0 0 24 24"><path d="M4 11h12.2l-4.6-4.6L13 5l7 7-7 7-1.4-1.4 4.6-4.6H4z"/></svg>'
AR_L = '<svg viewBox="0 0 24 24"><path d="M20 11H7.8l4.6-4.6L11 5l-7 7 7 7 1.4-1.4L7.8 13H20z"/></svg>'
AR_D = '<svg viewBox="0 0 24 24"><path d="M11 4v12.2l-4.6-4.6L5 13l7 7 7-7-1.4-1.4-4.6 4.6V4z"/></svg>'

ITEMS = [
    'Full custom <b>Home Care</b> website built in 3 days',
    'Mobile-first design that converts on a 5-inch screen',
    'SEO + AEO foundation, indexed',
    'Google Business Profile, optimized &amp; syncing reviews',
    'Same-day consultation booking via the live form',
    'Hosting + SSL included',
    '5-Star Outreach System to grow reviews &amp; ranking',
    '24/7 missed-call &amp; follow-up receptionist',
]
rows = ''.join(
    '<div class="so-crow"><span class="so-cbox">%s</span><div class="so-ctext">%s</div></div>' % (CK, t)
    for t in ITEMS)

OFFER_HTML = (
'<section id="offer" class="sbp-offer"><div class="so-inner">'
'<h2 class="so-title">The Site That Only Costs You Something<br><span class="so-acc">If It Works.</span></h2>'
'<div class="so-diagram"><div class="so-hub">'
'<div class="so-sys"><div class="so-emoji">&#11088;</div><div class="so-t">5-Star Outreach System</div><div class="so-s">More reviews, higher ranking</div></div>'
'<div class="so-conn">' + AR_R + '</div>'
'<div class="so-site"><div class="so-bbar"><i></i><i></i><i></i><div class="so-url">gihonfamilycare.com</div></div>'
'<div class="laptop-viewport so-vp"><iframe class="laptop-iframe" src="' + DEMO + '" style="pointer-events:none" tabindex="-1" loading="lazy" title="Gihon Family Care Home live preview"></iframe></div></div>'
'<div class="so-conn">' + AR_L + '</div>'
'<div class="so-sys"><div class="so-emoji">&#128737;&#65039;</div><div class="so-t">Monthly Qualified Prospect Guarantee</div><div class="so-s">Guaranteed senior leads</div></div>'
'</div>'
'<div class="so-downcol"><div class="so-conn so-down">' + AR_D + '</div>'
'<div class="so-sys so-bottom"><div class="so-ico">&#128222;</div><div class="so-tx"><div class="so-t">24/7 Receptionist Follow-Up</div><div class="so-s">Never miss a family&rsquo;s call</div></div></div>'
'</div></div>'
'<div class="so-inc"><div class="so-inc-h"><div class="so-hd">Everything you need to see success</div><div class="so-cover">100% of what we covered on the call.</div></div>'
'<div class="so-rows">' + rows + '</div></div>'
'<div class="so-invest"><div class="so-crown">&#128081;</div><div class="so-kick">Your Investment</div><div class="so-lbl">One-Time Payment</div>'
'<div class="so-price">$297<span class="so-to">to</span>$997</div><div class="so-dep">Depending on your need</div>'
'<div class="so-trust">'
'<span class="so-chip"><span class="so-c">' + CK + '</span>One Payment</span>'
'<span class="so-chip"><span class="so-c">' + CK + '</span>You Own It</span>'
'<span class="so-chip"><span class="so-c">' + CK + '</span>Money-Back Guarantee</span>'
'</div></div>'
'</div></section>')

doc = open('index.html', encoding='utf-8').read()

# 1) inject CSS once
if 'id="sbp-offer-css"' not in doc:
    doc = doc.replace('</head>', OFFER_CSS + '</head>', 1)
    print('CSS injected')
else:
    doc = re.sub(r'<style id="sbp-offer-css">.*?</style>', OFFER_CSS, doc, count=1, flags=re.S)
    print('CSS updated')

# 2) replace the offer section in place
doc, n = re.subn(r'<section id="offer".*?</section>', lambda m: OFFER_HTML, doc, count=1, flags=re.S)
print('offer section replaced:', n)
assert n == 1, 'offer section not found/replaced'

open('index.html', 'w', encoding='utf-8').write(doc)
print('written; markers:',
      'sbp-offer' in doc, 'so-invest' in doc, '$297' in doc, 'If It Works' in doc)
