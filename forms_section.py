# -*- coding: utf-8 -*-
"""
forms_section.py — "A contact form makes them work. Ours does the work for them."
A prospect-education section that sits under the "How we write your site" comparison:
a static Contact-Us form vs the interactive multi-step form (real animated GIF that
progresses through the steps on the live page), plus a Google AI-Overview proof card
showing people prefer to book online over calling.

Universal copy (not per-industry). The multi-step GIF is `multi_form.gif` shipped in
the repo; swap it for an industry-matched qualifier later if desired.

- FORMS_CSS: scoped <style> — all vars live on .fp-section so nothing leaks into the
  page's globals; all classes prefixed .fp-/.cf-/.ev/.g* .
- build_forms(cfg): returns the <section> HTML.
"""

FORMS_CSS = """<style id="forms-css">
.fp-section{--blue:#2563EB;--navy:#0F1E35;--ink:#0F1E35;--muted:#7C8697;--gold:#C8A84B;--green:#1F8F55;--red:#D2402E;--line:#E6ECF3;
  width:100%;background:linear-gradient(180deg,#FFFFFF 0%,#F1F6FF 100%);padding:64px 24px 74px;font-family:'Open Sans',sans-serif;color:var(--ink)}
.fp-inner{max-width:1060px;margin:0 auto}
.fp-kicker{display:flex;align-items:center;justify-content:center;gap:12px;color:var(--gold);font-family:'Montserrat',sans-serif;font-weight:800;font-size:14px;letter-spacing:2.5px;text-transform:uppercase}
.fp-kicker:before,.fp-kicker:after{content:'';width:30px;height:3px;background:var(--gold);border-radius:2px}
.fp-head{font-family:'Montserrat',sans-serif;font-weight:900;font-size:38px;line-height:1.12;letter-spacing:-1px;color:var(--ink);text-align:center;margin-top:14px}
.fp-head em{color:var(--blue);font-style:normal}
.fp-lead{font-size:18px;line-height:1.5;color:#4A5568;text-align:center;max-width:820px;margin:13px auto 40px}
.fp-cols{display:flex;align-items:flex-start;justify-content:center;gap:0}
.fp-col{flex:1;max-width:420px;display:flex;flex-direction:column;align-items:center}
.fp-col.mid{flex:0 0 70px;max-width:70px;align-self:center}
.fp-vs{width:52px;height:52px;border-radius:50%;background:var(--navy);color:#fff;font-family:'Montserrat',sans-serif;font-weight:900;font-size:16px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 22px rgba(15,20,40,.2);margin-top:150px}
.fp-lab{font-family:'Montserrat',sans-serif;font-weight:800;font-size:13px;letter-spacing:.4px;text-transform:uppercase;display:flex;align-items:center;gap:8px;margin-bottom:16px}
.fp-lab .b{width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;font-weight:900}
.fp-col.bad .fp-lab{color:var(--red)}.fp-col.bad .fp-lab .b{background:var(--red)}
.fp-col.good .fp-lab{color:var(--green)}.fp-col.good .fp-lab .b{background:var(--green)}
.fp-phone{width:300px;background:#0F1E35;border-radius:36px;padding:11px;box-shadow:0 24px 54px rgba(15,20,40,.22)}
.fp-col.good .fp-phone{box-shadow:0 26px 60px rgba(37,99,235,.28)}
.fp-screen{background:#fff;border-radius:26px;overflow:hidden;height:452px;position:relative}
.fp-screen img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.cf{padding:22px 20px}
.cf-h{font-family:'Montserrat',sans-serif;font-weight:900;font-size:20px;color:var(--navy);margin-bottom:3px}
.cf-sub{font-size:12px;color:var(--muted);margin-bottom:16px}
.cf-f{margin-bottom:12px}
.cf-l{font-size:11px;font-weight:700;color:#6b7686;margin-bottom:5px;text-transform:uppercase;letter-spacing:.4px}
.cf-i{height:34px;border:1px solid #d7dde6;border-radius:7px;background:#fbfcfe}
.cf-i.ta{height:74px}
.cf-btn{margin-top:6px;height:40px;border-radius:8px;background:#8a94a3;color:#fff;font-family:'Montserrat',sans-serif;font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center;letter-spacing:.4px}
.fp-dem{margin-top:16px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 15px;display:flex;align-items:center;gap:11px;width:300px}
.fp-dem .ic{flex:0 0 auto;width:30px;height:30px;border-radius:50%;color:#fff;font-weight:900;font-size:14px;display:flex;align-items:center;justify-content:center}
.fp-col.bad .fp-dem .ic{background:var(--red)}.fp-col.good .fp-dem .ic{background:var(--green)}
.fp-dem .t{font-family:'Montserrat',sans-serif;font-weight:800;font-size:13.5px;color:var(--navy);line-height:1.25}
.fp-dem .s{font-size:11.5px;color:var(--muted);margin-top:2px}
.fp-foot{text-align:center;font-family:'Montserrat',sans-serif;font-weight:800;font-size:19px;color:var(--ink);margin-top:34px}
.fp-foot em{color:var(--blue);font-style:normal}
.ev{max-width:760px;margin:42px auto 0}
.ev-lead{text-align:center;font-family:'Montserrat',sans-serif;font-weight:800;font-size:18px;color:var(--ink);margin-bottom:18px}
.ev-lead em{color:var(--blue);font-style:normal}
.gcard{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px 26px;box-shadow:0 16px 40px rgba(15,20,40,.09)}
.gbar{display:flex;align-items:center;gap:14px;height:44px;border:1px solid #dfe1e5;border-radius:22px;padding:0 18px;box-shadow:0 1px 5px rgba(32,33,36,.1);max-width:540px}
.gbar .gq{flex:1;font-size:15px;color:#202124}
.gbar svg{width:19px;height:19px;flex:0 0 auto}
.gai{display:flex;align-items:center;gap:8px;margin-top:18px;font-family:'Montserrat',sans-serif;font-weight:700;font-size:14.5px;color:#1a73e8}
.gai .spark{width:17px;height:17px;fill:#4285f4}
.gans{font-size:16.5px;line-height:1.55;color:#202124;margin-top:11px}
.gans .hl{background:#d2e3fc;color:#0b57d0;font-weight:600;border-radius:3px;padding:1px 3px}
.gsrc{display:flex;align-items:center;gap:9px;margin-top:16px;font-size:12.5px;color:#5f6368}
.gsrc .chip{border:1px solid #dadce0;border-radius:20px;padding:4px 11px;display:flex;align-items:center;gap:6px;color:#3c4043;font-weight:600}
.gsrc .dot{width:13px;height:13px;border-radius:4px}
@media(max-width:760px){.fp-cols{flex-direction:column;align-items:center}.fp-col,.fp-col.mid{max-width:100%}.fp-vs{margin:14px 0}.fp-head{font-size:29px}.gbar .gq{font-size:13px}}
</style>"""


def build_forms(cfg=None):
    return (
        '<section class="fp-section"><div class="fp-inner">'
        '<div class="fp-kicker">Where leads are won or lost</div>'
        '<h2 class="fp-head">A contact form makes them work. <em>Ours does the work for them.</em></h2>'
        '<p class="fp-lead">Here&rsquo;s the part almost nobody thinks about: a traditional form asks a stranger to sit down, gather their thoughts, and type it all out. Most won&rsquo;t &mdash; they close the tab and move on. Ours does the work for them. They just tap what they need.</p>'
        '<div class="fp-cols">'
          '<div class="fp-col bad">'
            '<div class="fp-lab"><span class="b">&times;</span> Makes them do the work</div>'
            '<div class="fp-phone"><div class="fp-screen"><div class="cf">'
              '<div class="cf-h">Contact Us</div><div class="cf-sub">Fill out the form and we&rsquo;ll get back to you.</div>'
              '<div class="cf-f"><div class="cf-l">Full Name</div><div class="cf-i"></div></div>'
              '<div class="cf-f"><div class="cf-l">Email</div><div class="cf-i"></div></div>'
              '<div class="cf-f"><div class="cf-l">Phone</div><div class="cf-i"></div></div>'
              '<div class="cf-f"><div class="cf-l">Message</div><div class="cf-i ta"></div></div>'
              '<div class="cf-btn">Send</div>'
            '</div></div></div>'
            '<div class="fp-dem"><span class="ic">&times;</span><div><div class="t">A blank box to fill out</div><div class="s">Sit, think, type &mdash; most just close the tab</div></div></div>'
          '</div>'
          '<div class="fp-col mid"><div class="fp-vs">VS</div></div>'
          '<div class="fp-col good">'
            '<div class="fp-lab"><span class="b">&#10003;</span> Does the work for them</div>'
            '<div class="fp-phone"><div class="fp-screen"><img src="multi_form.gif" alt="Interactive multi-step form"></div></div>'
            '<div class="fp-dem"><span class="ic">&#10003;</span><div><div class="t">They just tap what they need</div><div class="s">One simple choice at a time &mdash; far more finish &amp; book</div></div></div>'
          '</div>'
        '</div>'
        '<div class="fp-foot">One asks a stranger to work. <em>The other just asks them to tap.</em></div>'
        '<div class="ev">'
          '<div class="ev-lead">And it&rsquo;s not just easier &mdash; <em>it&rsquo;s what people actually want.</em></div>'
          '<div class="gcard">'
            '<div class="gbar">'
              '<svg viewBox="0 0 24 24"><path fill="#9aa0a6" d="M20 19.5l-5.4-5.4a7 7 0 10-1.4 1.4l5.4 5.4 1.4-1.4zM4 9.5a5.5 5.5 0 1111 0 5.5 5.5 0 01-11 0z"/></svg>'
              '<span class="gq">Do people prefer to call or book online?</span>'
              '<svg viewBox="0 0 24 24"><path fill="#4285f4" d="M12 15a3 3 0 003-3V6a3 3 0 00-6 0v6a3 3 0 003 3z"/><path fill="#34a853" d="M17 12a5 5 0 01-10 0H5a7 7 0 006 6.9V22h2v-3.1A7 7 0 0019 12h-2z"/></svg>'
            '</div>'
            '<div class="gai"><svg class="spark" viewBox="0 0 24 24"><path d="M12 2l2.2 6.4L21 10.6l-6.8 2.2L12 19.4l-2.2-6.6L3 10.6l6.8-2.2z"/></svg>AI Overview</div>'
            '<div class="gans"><span class="hl">Most consumers prefer to book online rather than call</span>, with roughly 60&ndash;90% favoring digital self-service for its speed, 24/7 availability, and control.</div>'
            '<div class="gsrc"><span class="chip"><span class="dot" style="background:#1f8e5a"></span>Easy!Appointments</span><span class="chip"><span class="dot" style="background:#4285f4"></span>FullyBooked</span> &middot; 7 sources</div>'
          '</div>'
        '</div>'
        '</div></section>'
    )
