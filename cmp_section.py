# -*- coding: utf-8 -*-
"""
cmp_section.py — the "How we write your site" comparison section.
A prospect-education block: two identical site previews, contractor-jargon vs
customer-language, plus the search-demand gap. Proves why SBP writes in the
customer's words (tied to the Reddit/FB/Trends research).

- INDUSTRY_COMPARE: per-vertical display copy (23 verticals, keyed on industry_lc,
  same keys as INDUSTRY_TERMS). Numbers are ILLUSTRATIVE.
- build_cmp(cfg): returns the <section> HTML, deriving labels/CTA/URL from the
  same CFG fields the rest of the proposal uses (provider_term, service_term,
  preview_domain). Falls back to roofing if the industry is unmapped.
- CMP_CSS: scoped <style> (all classes prefixed .cmp- to avoid page collisions).

Used by build_proposal.py (regenerates per client) and apply_cmp.py (patches the
current index.html). When the n8n proposal wrapper is built, it mirrors this map
exactly like INDUSTRY_TERMS.
"""

INDUSTRY_COMPARE = {
    'cleaning': {
        'bad_h': 'Recurring Residential Sanitation &amp; Surface Disinfection Services',
        'bad_bullets': ['Detailed vertical &amp; horizontal surface sanitation', 'EPA-registered disinfectant application', 'Recurring service-level agreements'],
        'bad_term': 'residential sanitation services', 'bad_num': '~30',
        'good_h': 'Come Home to a Spotless House &mdash; Without Lifting a Finger',
        'good_bullets': ['The same trusted cleaner every visit', 'We bring everything &mdash; you do nothing', 'Book online in 60 seconds'],
        'good_term': 'house cleaning near me', 'good_num': '~4,400',
    },
    'diesel mechanic': {
        'bad_h': 'Heavy-Duty Diesel Powertrain Diagnostics &amp; Aftertreatment Service',
        'bad_bullets': ['DPF/DEF aftertreatment regeneration', 'ECM diagnostics &amp; drivetrain calibration', 'DOT-compliant preventive maintenance'],
        'bad_term': 'diesel powertrain diagnostics', 'bad_num': '~20',
        'good_h': 'Truck Down? We Get You Back on the Road &mdash; Fast.',
        'good_bullets': ['Same-day diagnosis, no long waits', 'Upfront pricing before we touch it', 'Mobile service that comes to you'],
        'good_term': 'diesel mechanic near me', 'good_num': '~2,900',
    },
    'electrical': {
        'bad_h': 'Residential Electrical Systems, Panel Upgrades &amp; Circuit Diagnostics',
        'bad_bullets': ['200A load-center upgrades', 'AFCI/GFCI circuit protection', 'Code-compliant branch wiring'],
        'bad_term': 'residential circuit diagnostics', 'bad_num': '~25',
        'good_h': 'Flickering Lights or a Dead Outlet? A Licensed Electrician, Today.',
        'good_bullets': ['Licensed, insured, upfront pricing', 'Same-day for outlets, panels &amp; fixtures', 'We leave it clean and safe'],
        'good_term': 'electrician near me', 'good_num': '~3,300',
    },
    'fencing': {
        'bad_h': 'Residential Perimeter Fencing Installation &amp; Post-Setting Services',
        'bad_bullets': ['Galvanized post-setting &amp; footings', 'Pressure-treated &amp; composite panel systems', 'Property-line survey coordination'],
        'bad_term': 'perimeter fencing installation', 'bad_num': '~30',
        'good_h': 'A Fence That Lasts &mdash; Installed Right, Finished On Time.',
        'good_bullets': ['Free quote with an exact price', 'Wood, vinyl or aluminum &mdash; your call', 'We show up and finish the job'],
        'good_term': 'fence installation near me', 'good_num': '~2,400',
    },
    'flooring': {
        'bad_h': 'Residential Subfloor Preparation &amp; Resilient Flooring Installation',
        'bad_bullets': ['Moisture-barrier &amp; subfloor leveling', 'LVP, engineered hardwood &amp; tile systems', 'Acclimation &amp; expansion-gap standards'],
        'bad_term': 'resilient flooring installation', 'bad_num': '~40',
        'good_h': 'New Floors That Wow &mdash; Installed Clean, On Schedule.',
        'good_bullets': ['Free in-home estimate', 'We move the furniture, you relax', 'No mess left behind'],
        'good_term': 'flooring installers near me', 'good_num': '~2,600',
    },
    'funeral home': {
        'bad_h': 'Funeral Pre-Arrangement, Interment &amp; Memorialization Services',
        'bad_bullets': ['Pre-need arrangement counseling', 'Interment &amp; cremation coordination', 'Memorialization &amp; keepsake options'],
        'bad_term': 'interment memorialization services', 'bad_num': '~20',
        'good_h': 'A Caring, Affordable Send-Off &mdash; We Handle Everything.',
        'good_bullets': ['Compassionate guidance, no pressure', 'Clear, upfront pricing', 'We take care of every detail'],
        'good_term': 'funeral homes near me', 'good_num': '~3,100',
    },
    'home care': {
        'bad_h': 'In-Home Non-Medical ADL Assistance &amp; Care Coordination',
        'bad_bullets': ['Activities of daily living (ADL) support', 'Care-plan management &amp; coordination', 'HIPAA-compliant caregiver matching'],
        'bad_term': 'non-medical ADL assistance', 'bad_num': '~40',
        'good_h': 'Worried About Mom Living Alone? Trusted Caregivers, a Few Hours a Day.',
        'good_bullets': ['Help with bathing, meals &amp; medication reminders', 'Background-checked caregivers you can trust', 'Start with a free in-home visit'],
        'good_term': 'home care for elderly parent', 'good_num': '~2,900',
    },
    'hvac': {
        'bad_h': 'Residential HVAC System Diagnostics, Refrigerant &amp; Load Calculation',
        'bad_bullets': ['Manual-J load calculations', 'Refrigerant charge &amp; superheat tuning', 'SEER2-rated system installation'],
        'bad_term': 'hvac load calculation', 'bad_num': '~30',
        'good_h': 'No AC on the Hottest Day? We&rsquo;ll Have You Cool by Tonight.',
        'good_bullets': ['Same-day repair, honest pricing', 'We fix it before we sell you a new one', '24/7 emergency service'],
        'good_term': 'ac repair near me', 'good_num': '~5,400',
    },
    'landscaping': {
        'bad_h': 'Residential Landscape Design, Turf Management &amp; Hardscape Installation',
        'bad_bullets': ['Soil amendment &amp; turf agronomy', 'Irrigation zoning &amp; drainage grading', 'Hardscape &amp; retaining-wall systems'],
        'bad_term': 'turf management services', 'bad_num': '~25',
        'good_h': 'A Yard the Whole Street Notices &mdash; Without the Weekend Work.',
        'good_bullets': ['A reliable weekly crew that shows up', 'Design, cleanups &amp; mowing', 'Free walkthrough &amp; quote'],
        'good_term': 'landscapers near me', 'good_num': '~3,300',
    },
    'mobile mechanic': {
        'bad_h': 'On-Site Automotive Diagnostics &amp; Component-Level Repair',
        'bad_bullets': ['OBD-II diagnostic scanning', 'Brake, suspension &amp; drivetrain service', 'OEM-spec component replacement'],
        'bad_term': 'on-site automotive diagnostics', 'bad_num': '~20',
        'good_h': 'Car Won&rsquo;t Start? We Come to You and Fix It There.',
        'good_bullets': ['We come to your driveway or work', 'Upfront price before we start', 'Honest &mdash; no upsells'],
        'good_term': 'mobile mechanic near me', 'good_num': '~2,700',
    },
    'mobile truck repair': {
        'bad_h': '24/7 Mobile Heavy-Duty Roadside &amp; Fleet Repair Services',
        'bad_bullets': ['Roadside DOT breakdown response', 'Air-brake &amp; electrical diagnostics', 'Fleet preventive-maintenance contracts'],
        'bad_term': 'heavy-duty roadside repair', 'bad_num': '~20',
        'good_h': 'Broke Down on the Highway? We Roll to You, 24/7.',
        'good_bullets': ['Fast roadside response, day or night', 'Get your load moving again', 'Upfront pricing on the phone'],
        'good_term': 'mobile truck repair near me', 'good_num': '~1,900',
    },
    'mold remediation': {
        'bad_h': 'Microbial Remediation, Containment &amp; Air-Quality Restoration',
        'bad_bullets': ['HEPA containment &amp; negative-air', 'Antimicrobial application protocols', 'Post-remediation clearance testing'],
        'bad_term': 'microbial remediation services', 'bad_num': '~30',
        'good_h': 'Found Mold? Protect Your Family &mdash; We Remove It for Good.',
        'good_bullets': ['Free inspection, honest assessment', 'Safe for kids &amp; pets', 'We handle the insurance paperwork'],
        'good_term': 'mold removal near me', 'good_num': '~2,800',
    },
    'moving': {
        'bad_h': 'Residential Relocation, Load Consolidation &amp; Transit Logistics',
        'bad_bullets': ['Inventory &amp; load consolidation', 'Furniture disassembly &amp; crating', 'Transit valuation coverage'],
        'bad_term': 'residential relocation logistics', 'bad_num': '~25',
        'good_h': 'Moving Day, Handled &mdash; Nothing Broken, No Surprise Fees.',
        'good_bullets': ['Flat upfront price, no hostage fees', 'We wrap and protect everything', 'On-time, careful crew'],
        'good_term': 'movers near me', 'good_num': '~4,100',
    },
    'painting': {
        'bad_h': 'Interior &amp; Exterior Surface Preparation &amp; Coating Application',
        'bad_bullets': ['Substrate prep &amp; priming', 'Elastomeric &amp; low-VOC coatings', 'Multi-coat application standards'],
        'bad_term': 'surface coating application', 'bad_num': '~20',
        'good_h': 'Fresh Paint, Done Right &mdash; Clean Lines, No Mess, On Time.',
        'good_bullets': ['Free color consult &amp; quote', 'We prep properly so it lasts', 'Tidy crew, finished when promised'],
        'good_term': 'house painters near me', 'good_num': '~3,200',
    },
    'pest control': {
        'bad_h': 'Integrated Pest Management &amp; Perimeter Barrier Treatments',
        'bad_bullets': ['Integrated pest management (IPM)', 'Perimeter barrier applications', 'Recurring service agreements'],
        'bad_term': 'integrated pest management', 'bad_num': '~30',
        'good_h': 'Roaches, Ants or Rodents? Gone Fast &mdash; Safe for Your Family.',
        'good_bullets': ['Same-week treatment', 'Safe for kids &amp; pets', 'Guaranteed &mdash; we come back free'],
        'good_term': 'pest control near me', 'good_num': '~4,000',
    },
    'plumbing': {
        'bad_h': 'Residential Hydro-Jetting, Trenchless Pipe Lining &amp; Backflow',
        'bad_bullets': ['Hydro-jetting &amp; trenchless pipe lining', 'Backflow prevention &amp; testing', 'PEX repipe &amp; fixture rough-in'],
        'bad_term': 'trenchless pipe lining', 'bad_num': '~40',
        'good_h': 'Burst Pipe or No Hot Water? An Honest Plumber, Today.',
        'good_bullets': ['Same-day, upfront flat pricing', 'We stop the leak before it does more damage', '24/7 emergency service'],
        'good_term': 'plumber near me', 'good_num': '~6,600',
    },
    'remodeling': {
        'bad_h': 'Full-Scope Residential Renovation &amp; Design-Build Services',
        'bad_bullets': ['Design-build project management', 'Structural &amp; permit coordination', 'Millwork &amp; finish carpentry'],
        'bad_term': 'design-build renovation', 'bad_num': '~30',
        'good_h': 'Dreaming of a New Kitchen? On Budget, On Time &mdash; No Ghosting.',
        'good_bullets': ['A clear timeline &amp; fixed budget', 'One team, start to finish', 'We don&rsquo;t disappear mid-project'],
        'good_term': 'home remodeling near me', 'good_num': '~2,500',
    },
    'roofing': {
        'bad_h': 'Architectural Shingle Systems &amp; Ice-and-Water Shield Installation',
        'bad_bullets': ['Synthetic underlayment &amp; hip-and-ridge ventilation', 'Class-4 impact-resistant membranes', 'OSHA-compliant tear-off &amp; re-decking'],
        'bad_term': 'architectural shingle installation', 'bad_num': '~30',
        'good_h': 'Roof Leaking After the Storm? We Stop It Fast &mdash; and Handle Your Insurance.',
        'good_bullets': ['Leak fixed before it rots your ceiling', 'Insurance-approved &mdash; we file the claim', 'Same-week emergency repairs'],
        'good_term': 'roof leaking after storm', 'good_num': '~3,600',
    },
    'septic tank': {
        'bad_h': 'Septic System Pumping, Drainfield &amp; Effluent Management',
        'bad_bullets': ['Tank pumping &amp; baffle inspection', 'Drainfield restoration &amp; jetting', 'Effluent-filter &amp; pump service'],
        'bad_term': 'drainfield effluent management', 'bad_num': '~20',
        'good_h': 'Septic Backing Up? We&rsquo;re On the Way &mdash; Fair, Fast, No Mess.',
        'good_bullets': ['Same-day emergency pumping', 'Upfront price, no surprises', 'We leave your yard clean'],
        'good_term': 'septic service near me', 'good_num': '~2,100',
    },
    'solar': {
        'bad_h': 'Photovoltaic System Design, Interconnection &amp; Net-Metering',
        'bad_bullets': ['PV array design &amp; string sizing', 'Utility interconnection &amp; net-metering', 'Microinverter &amp; monitoring setup'],
        'bad_term': 'photovoltaic interconnection', 'bad_num': '~20',
        'good_h': 'Cut Your Power Bill &mdash; Honest Solar, No High-Pressure Games.',
        'good_bullets': ['Real numbers on your actual savings', 'No pushy sales tactics', 'We honor the warranty for years'],
        'good_term': 'solar panels near me', 'good_num': '~3,000',
    },
    'therapy/counseling': {
        'bad_h': 'Evidence-Based Psychotherapy &amp; Cognitive-Behavioral Modalities',
        'bad_bullets': ['CBT/DBT evidence-based modalities', 'Biopsychosocial intake assessment', 'Insurance &amp; superbill processing'],
        'bad_term': 'cognitive behavioral modalities', 'bad_num': '~30',
        'good_h': 'Feeling Overwhelmed? Talk to a Therapist Who Gets It &mdash; This Week.',
        'good_bullets': ['Now accepting new clients', 'In-person or online', 'We take your insurance'],
        'good_term': 'therapist near me', 'good_num': '~5,000',
    },
    'tree repair': {
        'bad_h': 'Arboricultural Hazard Mitigation &amp; Structural Cabling',
        'bad_bullets': ['Hazard-tree risk assessment', 'Structural cabling &amp; bracing', 'Crown reduction &amp; deadwooding'],
        'bad_term': 'arboricultural hazard mitigation', 'bad_num': '~20',
        'good_h': 'Storm-Damaged or Leaning Tree? We Make It Safe &mdash; Fast.',
        'good_bullets': ['Emergency response, fully insured', 'Free assessment &amp; quote', 'We clean up every branch'],
        'good_term': 'emergency tree service near me', 'good_num': '~1,800',
    },
    'tree service': {
        'bad_h': 'Professional Arboriculture, Removal &amp; Vegetation Management',
        'bad_bullets': ['ISA-certified removal &amp; pruning', 'Stump grinding &amp; vegetation management', 'Crane-assisted large-tree removal'],
        'bad_term': 'vegetation management services', 'bad_num': '~25',
        'good_h': 'Overgrown or Dangerous Tree? Trimmed or Gone &mdash; Safely, No Damage.',
        'good_bullets': ['Fully insured, free quote', 'Removal, trimming &amp; stump grinding', 'We protect your property &amp; clean up'],
        'good_term': 'tree removal near me', 'good_num': '~4,700',
    },
}

CMP_CSS = """<style id="cmp-css">
.cmp-section{background:linear-gradient(180deg,#FFFFFF 0%,#F1F6FF 100%);padding:64px 24px 72px;font-family:'Open Sans',sans-serif}
.cmp-inner{max-width:1080px;margin:0 auto}
.cmp-kicker{display:flex;align-items:center;justify-content:center;gap:12px;color:#C8A84B;font-family:'Montserrat',sans-serif;font-weight:800;font-size:14px;letter-spacing:2.5px;text-transform:uppercase}
.cmp-kicker:before,.cmp-kicker:after{content:'';width:30px;height:3px;background:#C8A84B;border-radius:2px}
.cmp-head{font-family:'Montserrat',sans-serif;font-weight:900;font-size:38px;line-height:1.12;letter-spacing:-1px;color:#0F1E35;text-align:center;margin-top:14px}
.cmp-head em{color:#2563EB;font-style:normal}
.cmp-lead{font-family:'Open Sans',sans-serif;color:#4A5568;font-size:18px;line-height:1.5;text-align:center;max-width:800px;margin:13px auto 36px}
.cmp-cols{display:flex;align-items:stretch;gap:0;justify-content:center;flex-wrap:nowrap}
.cmp-col{flex:1;max-width:452px;display:flex;flex-direction:column}
.cmp-col.mid{flex:0 0 66px;max-width:66px;align-items:center;justify-content:center}
.cmp-vs{width:52px;height:52px;border-radius:50%;background:#0F1E35;color:#fff;font-family:'Montserrat',sans-serif;font-weight:900;font-size:16px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 22px rgba(15,20,40,.2)}
.cmp-lab{font-family:'Montserrat',sans-serif;font-weight:800;font-size:13px;letter-spacing:.4px;text-transform:uppercase;display:flex;align-items:center;gap:8px;margin-bottom:12px}
.cmp-lab .b{width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;font-weight:900}
.cmp-col.bad .cmp-lab{color:#D2402E}.cmp-col.bad .cmp-lab .b{background:#D2402E}
.cmp-col.good .cmp-lab{color:#1F8F55}.cmp-col.good .cmp-lab .b{background:#1F8F55}
.cmp-brow{background:#fff;border:1px solid #E6ECF3;border-radius:12px;overflow:hidden;box-shadow:0 16px 36px rgba(15,20,40,.1);flex:1;display:flex;flex-direction:column}
.cmp-col.good .cmp-brow{border-color:rgba(31,143,85,.4);box-shadow:0 18px 40px rgba(31,143,85,.16)}
.cmp-bar{height:31px;background:#EEF2F7;display:flex;align-items:center;gap:6px;padding:0 12px;border-bottom:1px solid #E6ECF3}
.cmp-bar i{width:9px;height:9px;border-radius:50%;background:#CBD5E1}
.cmp-bar .u{margin-left:9px;flex:1;height:17px;background:#fff;border:1px solid #E6ECF3;border-radius:8px;font-family:'Open Sans',sans-serif;font-size:10px;color:#7C8697;display:flex;align-items:center;padding:0 9px}
.cmp-hero{padding:22px 22px 20px;flex:1}
.cmp-h{font-family:'Montserrat',sans-serif;font-weight:900;font-size:20px;line-height:1.2;color:#0F1E35;min-height:96px}
.cmp-bl{list-style:none;margin:14px 0 16px;padding:0}
.cmp-bl li{display:flex;gap:9px;font-family:'Open Sans',sans-serif;font-size:14px;color:#33415a;line-height:1.32;margin-bottom:8px}
.cmp-bl li:before{content:'';flex:0 0 auto;width:7px;height:7px;border-radius:50%;background:#2563EB;margin-top:5px}
.cmp-cta{display:inline-block;background:#2563EB;color:#fff;font-family:'Montserrat',sans-serif;font-weight:800;font-size:13px;padding:11px 17px;border-radius:8px}
.cmp-dem{margin-top:14px;background:#fff;border:1px solid #E6ECF3;border-radius:12px;padding:13px 16px;display:flex;align-items:center;gap:11px}
.cmp-dem .ic{flex:0 0 auto;width:32px;height:32px;border-radius:50%;color:#fff;font-weight:900;font-size:14px;display:flex;align-items:center;justify-content:center}
.cmp-col.bad .cmp-dem .ic{background:#D2402E}.cmp-col.good .cmp-dem .ic{background:#1F8F55}
.cmp-dem .n{font-family:'Montserrat',sans-serif;font-weight:900;font-size:18px;color:#0F1E35;line-height:1}
.cmp-dem .l{font-family:'Open Sans',sans-serif;font-size:12.5px;color:#7C8697;margin-top:2px}
.cmp-foot{text-align:center;font-family:'Montserrat',sans-serif;font-weight:800;font-size:19px;color:#0F1E35;margin-top:30px}
.cmp-foot .a{color:#2563EB}
@media(max-width:760px){.cmp-cols{flex-direction:column}.cmp-col,.cmp-col.mid{max-width:100%}.cmp-vs{margin:12px 0}.cmp-head{font-size:29px}}
</style>"""


def _pl(w):
    if w.endswith('y'):
        return w[:-1] + 'ies'
    if w.endswith('s'):
        return w
    return w + 's'


def _art(w):
    return 'an' if w[:1].lower() in 'aeiou' else 'a'


def _titlecap(s):
    return s[:1].upper() + s[1:]


def build_cmp(cfg):
    """Return the comparison <section> HTML for this client's industry."""
    lc = cfg.get('industry_lc', 'roofing')
    c = INDUSTRY_COMPARE.get(lc, INDUSTRY_COMPARE['roofing'])
    prov = cfg.get('provider_term', 'contractor')
    svc = _titlecap(cfg.get('service_term', 'estimate'))
    dom = cfg.get('preview_domain', 'yourcompany.com')
    bl = lambda items: ''.join('<li>' + x + '</li>' for x in items)
    return (
        '<section class="cmp-section"><div class="cmp-inner">'
        '<div class="cmp-kicker">How we write your site</div>'
        '<h2 class="cmp-head">Your customers don&rsquo;t search like <em>' + _pl(prov) + '</em>.</h2>'
        '<p class="cmp-lead">Before we write a word, we read what your customers actually type &mdash; on Google, Reddit and Facebook. Then we build your site in their words, not the trade&rsquo;s.</p>'
        '<div class="cmp-cols">'
          '<div class="cmp-col bad">'
            '<div class="cmp-lab"><span class="b">&times;</span> Written like ' + _art(prov) + ' ' + prov + '</div>'
            '<div class="cmp-brow"><div class="cmp-bar"><i></i><i></i><i></i><span class="u">' + dom + '</span></div>'
              '<div class="cmp-hero"><div class="cmp-h">' + c['bad_h'] + '</div><ul class="cmp-bl">' + bl(c['bad_bullets']) + '</ul><span class="cmp-cta">Request ' + svc + '</span></div></div>'
            '<div class="cmp-dem"><span class="ic">&times;</span><div><div class="n">' + c['bad_num'] + '</div><div class="l">searches/mo for &ldquo;' + c['bad_term'] + '&rdquo;</div></div></div>'
          '</div>'
          '<div class="cmp-col mid"><div class="cmp-vs">VS</div></div>'
          '<div class="cmp-col good">'
            '<div class="cmp-lab"><span class="b">&#10003;</span> Written for your customers</div>'
            '<div class="cmp-brow"><div class="cmp-bar"><i></i><i></i><i></i><span class="u">' + dom + '</span></div>'
              '<div class="cmp-hero"><div class="cmp-h">' + c['good_h'] + '</div><ul class="cmp-bl">' + bl(c['good_bullets']) + '</ul><span class="cmp-cta">Get a Free ' + svc + '</span></div></div>'
            '<div class="cmp-dem"><span class="ic">&#10003;</span><div><div class="n">' + c['good_num'] + '</div><div class="l">searches/mo for &ldquo;' + c['good_term'] + '&rdquo;</div></div></div>'
          '</div>'
        '</div>'
        '<div class="cmp-foot">Same team. Same quality. <span class="a">Only one of these gets the call.</span></div>'
        '</div></section>'
    )
