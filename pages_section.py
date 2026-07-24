# -*- coding: utf-8 -*-
"""
pages_section.py — "A page for every service — not just a list."
Side-by-side: a basic site (one page, a plain bulleted list) vs ours (the real
multi-page services grid). RIGHT side = the client's actual services image,
used as-is (home-care-multipage.png shipped in repo). Scoped .mp-* classes.
"""

PAGES_CSS = """<style id="pages-css">
.mp-section{width:100%;background:linear-gradient(180deg,#FFFFFF 0%,#F1F6FF 100%);padding:62px 24px 70px;font-family:'Open Sans',sans-serif;color:#0F1E35}
.mp-inner{max-width:1120px;margin:0 auto}
.mp-kicker{display:flex;align-items:center;justify-content:center;gap:12px;color:#C8A84B;font-family:'Montserrat',sans-serif;font-weight:800;font-size:14px;letter-spacing:2.5px;text-transform:uppercase}
.mp-kicker:before,.mp-kicker:after{content:'';width:30px;height:3px;background:#C8A84B;border-radius:2px}
.mp-head{font-family:'Montserrat',sans-serif;font-weight:900;font-size:38px;line-height:1.12;letter-spacing:-1px;color:#0F1E35;text-align:center;margin-top:14px}
.mp-head em{color:#2563EB;font-style:normal}
.mp-lead{font-size:18px;line-height:1.5;color:#4A5568;text-align:center;max-width:800px;margin:13px auto 40px}
.mp-cols{display:flex;align-items:flex-start;justify-content:center;gap:0}
.mp-mid{flex:0 0 64px;display:flex;align-items:center;justify-content:center;align-self:center}
.mp-vs{width:52px;height:52px;border-radius:50%;background:#0F1E35;color:#fff;font-family:'Montserrat',sans-serif;font-weight:900;font-size:16px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 22px rgba(15,20,40,.2)}
.mp-col{display:flex;flex-direction:column}
.mp-col.bad{flex:0 0 340px}
.mp-col.good{flex:1;max-width:620px}
.mp-lab{font-family:'Montserrat',sans-serif;font-weight:800;font-size:13px;letter-spacing:.4px;text-transform:uppercase;display:flex;align-items:center;gap:8px;margin-bottom:14px}
.mp-lab .b{width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;font-weight:900}
.mp-col.bad .mp-lab{color:#D2402E}.mp-col.bad .mp-lab .b{background:#D2402E}
.mp-col.good .mp-lab{color:#1F8F55}.mp-col.good .mp-lab .b{background:#1F8F55}
.mp-win{background:#fff;border:1px solid #E6ECF3;border-radius:13px;overflow:hidden;box-shadow:0 16px 40px rgba(15,20,40,.1)}
.mp-col.good .mp-win{box-shadow:0 18px 46px rgba(37,99,235,.16);border-color:rgba(37,99,235,.24)}
.mp-bar{height:32px;background:#EEF2F7;display:flex;align-items:center;gap:6px;padding:0 12px;border-bottom:1px solid #E6ECF3}
.mp-bar i{width:9px;height:9px;border-radius:50%;background:#CBD5E1}
.mp-bar u{margin-left:9px;font-style:normal;font-size:11px;color:#7C8697}
.mp-lp{padding:26px 28px 34px}
.mp-lp h4{font-family:'Montserrat',sans-serif;font-weight:800;font-size:20px;color:#0F1E35;margin-bottom:18px}
.mp-lp ul{list-style:none;margin:0;padding:0}
.mp-lp li{font-size:16px;color:#3a4658;padding:11px 0;border-bottom:1px solid #eef1f5;display:flex;align-items:center;gap:11px}
.mp-lp li:before{content:'';width:7px;height:7px;border-radius:50%;background:#9aa7ba;flex:0 0 auto}
.mp-shot{width:100%;display:block}
@media(max-width:760px){.mp-cols{flex-direction:column;align-items:center}.mp-col.bad,.mp-col.good{flex:none;max-width:100%;width:100%}.mp-mid{padding:14px 0}.mp-head{font-size:29px}}
</style>"""


def build_pages(cfg=None):
    return (
        '<section class="mp-section"><div class="mp-inner">'
        '<div class="mp-kicker">Built to be found</div>'
        '<h2 class="mp-head">A page for every service &mdash; <em>not just a list.</em></h2>'
        '<p class="mp-lead">People scan. If they don&rsquo;t see the exact service they searched, they hit back. A page for each one means they always land on it &mdash; and Google has far more to rank.</p>'
        '<div class="mp-cols">'
          '<div class="mp-col bad">'
            '<div class="mp-lab"><span class="b">&times;</span> A basic site &mdash; one page, a list</div>'
            '<div class="mp-win"><div class="mp-bar"><i></i><i></i><i></i><u>generichomecare.com</u></div>'
              '<div class="mp-lp"><h4>Our Services</h4><ul>'
                '<li>Personal Care</li><li>Companionship</li><li>Respite Care</li>'
                '<li>24-Hour &amp; Live-In Care</li><li>Dementia &amp; Alzheimer&rsquo;s Care</li><li>Post-Operative Care</li>'
              '</ul></div></div>'
          '</div>'
          '<div class="mp-mid"><div class="mp-vs">VS</div></div>'
          '<div class="mp-col good">'
            '<div class="mp-lab"><span class="b">&#10003;</span> Ours &mdash; a page for each</div>'
            '<div class="mp-win"><div class="mp-bar"><i></i><i></i><i></i><u>gihonfamilycare.com/services</u></div>'
              '<img class="mp-shot" src="home-care-multipage.png" alt="A dedicated page for every service"></div>'
          '</div>'
        '</div>'
        '</div></section>'
    )
