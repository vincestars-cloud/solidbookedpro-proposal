#!/usr/bin/env python3
"""Render a client proposal from proposal.template.html.

  python3 render_proposal.py --industry "roofing" --company "Apex Roofing" \
      --city "Tampa" --state FL --phone "(813) 555-0142" --out apex.html

  python3 render_proposal.py --client clients/gihon.json --out index.html

Anything not supplied is derived: slug/domain/demo-url from the company name,
all case variants + plurals from the industry terms, and any missing content
block from a sensible generated default.
Exit code is non-zero if the output still contains unresolved {{TOKENS}}.
"""
import argparse, json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))


def slugify(s):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')


def plural(w):
    if w.endswith(('s', 'x', 'ch', 'sh')): return w + 'es'
    if w.endswith('y') and w[-2:-1] not in 'aeiou': return w[:-1] + 'ies'
    return w + 's'


def esc(s):
    """HTML-escape a plain client value without double-escaping existing entities."""
    s = re.sub(r'&(?!(?:[a-zA-Z][a-zA-Z0-9]{1,8}|#\d{1,6}|#x[0-9a-fA-F]{1,6});)', '&amp;', str(s))
    return s.replace('<', '&lt;').replace('>', '&gt;')


def tc(s):
    small = {'a', 'an', 'the', 'of', 'for', 'and', 'or', 'in', 'on', 'at', 'to'}
    out = []
    for i, w in enumerate(s.split()):
        out.append(w if (w.isupper() and len(w) > 1) else
                   (w.capitalize() if (i == 0 or w.lower() not in small) else w.lower()))
    return ' '.join(out)


def load_block(name, block_dir):
    """Load a content-block fragment: blocks/<industry>/<name>.html, else blocks/_default/<name>.html."""
    for d in (block_dir, '_default'):
        if not d:
            continue
        path = os.path.join(HERE, 'blocks', d, name + '.html')
        if os.path.exists(path):
            return open(path, encoding='utf-8').read()
    return ''


def build_ctx(cfg, ind):
    industry = ind.get('industry') or tc(cfg['industry_key'])
    cn   = ind['customer_noun']            # plural, lowercase  e.g. "seniors"
    cn_s = ind.get('customer_noun_s') or cn.rstrip('s')
    prov = ind['provider_term']
    svc  = ind['service_term']
    outcome = ind.get('outcome') or f'book more {cn}'
    company = cfg['company_name']
    slug    = cfg.get('slug') or slugify(company)
    city    = cfg.get('city', '')
    # which research-proof image set to use (defaults to the slugified industry key)
    proof_slug = ind.get('proof_slug') or ind.get('_block_dir') or slugify(ind.get('industry_key', ''))

    d = ind.get('_defaults', {})
    jar = ind.get('jargon', {})
    cus = ind.get('customer', {})
    assets = {**d.get('assets', {}), **ind.get('assets', {})}

    ctx = {
        # ---- client ----
        'COMPANY_NAME': esc(company),
        'COMPANY_SLUG': slug,
        'PREVIEW_DOMAIN': cfg.get('preview_domain') or (slugify(company).replace('-', '') + '.com'),
        'CITY': esc(city),
        'STATE_ABBR': esc(cfg.get('state', '')),
        'PHONE': esc(cfg.get('phone', '')),
        # ---- industry terms ----
        'INDUSTRY': industry,
        'INDUSTRY_LC': industry.lower(),
        'INDUSTRY_UC': industry.upper(),
        'CUSTOMER_NOUN': cn,
        'CUSTOMER_NOUN_S': cn_s,
        'CUSTOMER_NOUN_TC': tc(cn),
        'CUSTOMER_NOUN_UC': cn.upper(),
        'CUSTOMER_NOUN_TC_MORE': 'More ' + tc(cn),
        'BUYER_NOUN': ind.get('buyer_noun') or cn,
        'BUYER_NOUN_S': ind.get('buyer_noun_s') or cn_s,
        'WORKER_TERM': ind.get('worker_term') or prov,
        'PROVIDER_TERM': prov,
        'PROVIDER_TERM_PL': plural(prov),
        'PROVIDER_TERM_PL_TC': tc(plural(prov)),
        'SERVICE_TERM': svc,
        'SERVICE_TERM_TC': tc(svc),
        'SERVICE_TERM_PL': plural(svc),
        'SERVICE_TERM_PL_TC': tc(plural(svc)),
        'OUTCOME_LC': outcome,
        'OUTCOME_TC': tc(outcome),
        'OUTCOME_UPPER': outcome.upper(),
        'OUTCOME_RESULT': ind.get('outcome_result') or tc(outcome),
        'OUTCOME_SEEN': ind.get('outcome_seen') or f'More {tc(cn)} See You',
        # ---- content blocks (bespoke if present, else generated) ----
        'JARGON_HEADLINE': jar.get('headline') or f'Comprehensive {industry} Services &amp; Solutions',
        'JARGON_BULLETS': ''.join(f'<li>{b}</li>' for b in (jar.get('bullets') or [
            f'Full-scope {industry.lower()} system specification',
            'Code-compliant installation &amp; documentation',
            'Certified technical assessment &amp; reporting'])),
        'JARGON_CTA': jar.get('cta') or 'Request Service',
        'JARGON_QUERY': jar.get('query') or f'{industry.lower()} services',
        'JARGON_VOLUME': jar.get('volume') or d.get('jargon_volume', '~40'),
        'CUSTOMER_HEADLINE': cus.get('headline') or
            f'Need a {tc(prov)} You Can Trust? Free {tc(svc)}, Straight Answer.',
        'CUSTOMER_BULLETS': ''.join(f'<li>{b}</li>' for b in (cus.get('bullets') or [
            'Clear pricing before any work starts',
            f'Licensed, insured, local {plural(prov)}',
            f'Book a free {svc} this week'])),
        'CUSTOMER_CTA': cus.get('cta') or f'Get a Free {tc(svc)}',
        'CUSTOMER_QUERY': cus.get('query') or f'{industry.lower()} near me',
        'CUSTOMER_VOLUME': cus.get('volume') or d.get('customer_volume', '~2,900'),
        'SERVICES_LIST': ''.join(f'<li>{s}</li>' for s in (ind.get('services') or d.get('services', []))),
        'SERVICE_CARDS': '<div class="mp-cards">' + ''.join(
            f'<div class="mp-card"><span class="mp-thumb"></span><span class="mp-cn">{s}</span>'
            f'<span class="mp-go">View page &rarr;</span></div>'
            for s in (ind.get('services') or d.get('services', []))[:6]) + '</div>',
        'SERVICE_CHIPS': '<div class="msf-opts">' + ''.join(
            (f'<button class="msf-opt sel">{s}<span class="msf-ck">&#10003;</span></button>' if i == 0
             else f'<button class="msf-opt">{s}</button>')
            for i, s in enumerate((ind.get('services') or d.get('services', []))[:4])) + '</div>',
        'SERVICE_FIRST': (ind.get('services') or d.get('services') or [svc.title()])[0],
        'CONTACT_ID': cfg.get('contact_id', ''),
        'REASON_SPECIALIST_BODY': ind.get('specialist_body') or (
            f'We build for {industry.lower()} and nothing else, so we know what makes {cn}'
            f'{" in " + city if city else ""} pick one {prov} and skip the rest. '
            'Every page is written to earn that call. Generic agencies just guess.'),
        # ---- assets ----
        'ASSET_MULTIPAGE': assets.get('multipage', ''),
        'ASSET_PROOF': assets.get('proof', ''),
        'BLUEPRINT_PDF': assets.get('blueprint', ''),
        # per-industry research proof screenshots (bespoke path, else derived from the proof slug)
        'ASSET_PROOF_REDDIT': assets.get('proof_reddit') or f'assets/research/{proof_slug}-reddit.png',
        'ASSET_PROOF_FB': assets.get('proof_fb') or f'assets/research/{proof_slug}-facebook.png',
        # ---- demo site: real URL for a saved client, else the GHL merge field ----
        'DEMO_URL': cfg.get('demo_url') or '{{contact.demo_url}}',
        # ---- Google-review card (bespoke per industry, else a sensible default) ----
        'REVIEW_TEXT': ind.get('review_text') or (
            f'The team was fantastic &mdash; professional, honest, and did exactly what they said. '
            f'For the first time, I actually trust who I call. <strong>Best {prov} experience we&rsquo;ve had'
            + (' in {{CITY}}.' if city else '.') + '</strong>'),
        'REVIEW_REPLY': ind.get('review_reply') or (
            'Thank you so much, that truly means a lot to us. I&rsquo;ll pass it along to the whole team. '
            'Welcome to the {{COMPANY_NAME}} family.'),
        # ---- the 3 "How?" deep-dive panels (bespoke per industry, else generic) ----
        'HOW_TRAFFIC': load_block('how_traffic', ind.get('_block_dir', '')),
        'HOW_TRUST': load_block('how_trust', ind.get('_block_dir', '')),
        'HOW_CONVERSION': load_block('how_conversion', ind.get('_block_dir', '')),
    }
    # contact merge-fields stay literal unless overridden
    ctx['contact.first_name'] = cfg.get('first_name', '{{contact.first_name}}')
    return ctx


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--template', default=os.path.join(HERE, 'proposal.template.html'))
    p.add_argument('--industries', default=os.path.join(HERE, 'industries.json'))
    p.add_argument('--client')
    p.add_argument('--industry'); p.add_argument('--company'); p.add_argument('--city')
    p.add_argument('--state'); p.add_argument('--phone'); p.add_argument('--slug')
    p.add_argument('--preview-domain'); p.add_argument('--first-name')
    p.add_argument('--out', default='out.html')
    a = p.parse_args()

    cfg = json.load(open(a.client, encoding='utf-8')) if a.client else {}
    for k, v in [('industry_key', a.industry), ('company_name', a.company), ('city', a.city),
                 ('state', a.state), ('phone', a.phone), ('slug', a.slug),
                 ('preview_domain', a.preview_domain), ('first_name', a.first_name)]:
        if v: cfg[k] = v
    if not cfg.get('company_name') or not cfg.get('industry_key'):
        sys.exit('need --company and --industry (or --client file with company_name + industry_key)')

    data = json.load(open(a.industries, encoding='utf-8'))
    key = cfg['industry_key'].lower().strip()
    inds = data['industries']
    if key not in inds:
        matches = [k for k in inds if key in k or k in key]
        if not matches:
            sys.exit(f'unknown industry "{key}". known: {", ".join(sorted(inds))}')
        key = matches[0]
        print(f'note: industry "{cfg["industry_key"]}" -> "{key}"')
    ind = dict(inds[key]); ind['_defaults'] = data.get('_defaults', {})
    ind['_block_dir'] = slugify(key)

    ctx = build_ctx(cfg, ind)
    html = open(a.template, encoding='utf-8').read()
    # two passes so a content block's own {{CITY}}/{{COMPANY_NAME}}/{{PROVIDER_TERM}} tokens resolve
    for _ in range(2):
        for k, v in sorted(ctx.items(), key=lambda kv: -len(kv[0])):
            html = html.replace('{{' + k + '}}', str(v))

    open(a.out, 'w', encoding='utf-8').write(html)

    unresolved = sorted({t for t in re.findall(r'\{\{([A-Za-z_.]+)\}\}', html) if '.' not in t})
    generated = [k for k in ('jargon', 'customer') if k not in inds[key]]
    print(f'rendered {a.out}  ({len(html):,} bytes)  industry="{key}"  company="{cfg["company_name"]}"')
    if generated:
        print(f'  ! generated default copy for: {", ".join(generated)} — add bespoke copy in industries.json')
    if inds[key].get('assets', {}).get('multipage') is None:
        print('  ! using fallback screenshots (ASSET_MULTIPAGE / ASSET_PROOF) — supply per-industry images')
    if unresolved:
        print(f'  !! UNRESOLVED TOKENS: {", ".join(unresolved)}')
        sys.exit(1)
    print('  all tokens resolved')


if __name__ == '__main__':
    main()
