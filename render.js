/* render.js — JS port of render_proposal.py's engine, for the n8n build workflow.
 * Pure module: no fs/fetch. Caller supplies the template string, the industries
 * object, and a `blocks` map { "<dir>/<name>": "<html>" }.
 *
 *   const { buildProposal } = require('./render.js')       // node
 *   const { html, slug, industryKey } = buildProposal({ cfg, template, industries, blocks, assetBase })
 *
 * Keep this equivalent to render_proposal.py (both read the same template +
 * industries.json + blocks/). Verified to reproduce Gihon + Porter.
 */
(function (root) {
  function slugify(s) {
    return String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
  }
  function plural(w) {
    if (/(s|x|ch|sh)$/.test(w)) return w + 'es';
    if (/y$/.test(w) && !/[aeiou]y$/.test(w)) return w.slice(0, -1) + 'ies';
    return w + 's';
  }
  function esc(s) {
    s = String(s).replace(/&(?!(?:[a-zA-Z][a-zA-Z0-9]{1,8}|#\d{1,6}|#x[0-9a-fA-F]{1,6});)/g, '&amp;');
    return s.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function tc(s) {
    const small = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'or', 'in', 'on', 'at', 'to']);
    return String(s).split(/\s+/).map((w, i) => {
      if (w.length > 1 && w === w.toUpperCase()) return w;
      if (i === 0 || !small.has(w.toLowerCase())) return w.charAt(0).toUpperCase() + w.slice(1).toLowerCase();
      return w.toLowerCase();
    }).join(' ');
  }

  function buildCtx(cfg, ind, blocks) {
    const loadBlock = (name, dir) => {
      for (const d of [dir, '_default']) {
        if (!d) continue;
        const key = d + '/' + name;
        if (blocks && blocks[key] != null) return blocks[key];
      }
      return '';
    };
    const industry = ind.industry || tc(cfg.industry_key);
    const cn = ind.customer_noun;
    const cn_s = ind.customer_noun_s || cn.replace(/s$/, '');
    const prov = ind.provider_term;
    const svc = ind.service_term;
    const outcome = ind.outcome || ('book more ' + cn);
    const company = cfg.company_name;
    const slug = cfg.slug || slugify(company);
    const city = cfg.city || '';
    const proofSlug = ind.proof_slug || ind._block_dir || slugify(cfg.industry_key || '');
    const dflt = ind._defaults || {};
    const jar = ind.jargon || {};
    const cus = ind.customer || {};
    const assets = Object.assign({}, dflt.assets || {}, ind.assets || {});
    const blockDir = ind._block_dir || '';

    const ctx = {
      COMPANY_NAME: esc(company),
      COMPANY_SLUG: slug,
      PREVIEW_DOMAIN: cfg.preview_domain || (slugify(company).replace(/-/g, '') + '.com'),
      CITY: esc(city),
      STATE_ABBR: esc(cfg.state || ''),
      PHONE: esc(cfg.phone || ''),
      INDUSTRY: industry,
      INDUSTRY_LC: industry.toLowerCase(),
      INDUSTRY_UC: industry.toUpperCase(),
      CUSTOMER_NOUN: cn,
      CUSTOMER_NOUN_S: cn_s,
      CUSTOMER_NOUN_TC: tc(cn),
      CUSTOMER_NOUN_UC: cn.toUpperCase(),
      CUSTOMER_NOUN_TC_MORE: 'More ' + tc(cn),
      BUYER_NOUN: ind.buyer_noun || cn,
      BUYER_NOUN_S: ind.buyer_noun_s || cn_s,
      WORKER_TERM: ind.worker_term || prov,
      PROVIDER_TERM: prov,
      PROVIDER_TERM_PL: plural(prov),
      PROVIDER_TERM_PL_TC: tc(plural(prov)),
      SERVICE_TERM: svc,
      SERVICE_TERM_TC: tc(svc),
      SERVICE_TERM_PL: plural(svc),
      SERVICE_TERM_PL_TC: tc(plural(svc)),
      OUTCOME_LC: outcome,
      OUTCOME_TC: tc(outcome),
      OUTCOME_UPPER: outcome.toUpperCase(),
      OUTCOME_RESULT: ind.outcome_result || tc(outcome),
      OUTCOME_SEEN: ind.outcome_seen || ('More ' + tc(cn) + ' See You'),
      JARGON_HEADLINE: jar.headline || ('Comprehensive ' + industry + ' Services &amp; Solutions'),
      JARGON_BULLETS: (jar.bullets || [
        'Full-scope ' + industry.toLowerCase() + ' system specification',
        'Code-compliant installation &amp; documentation',
        'Certified technical assessment &amp; reporting']).map(b => '<li>' + b + '</li>').join(''),
      JARGON_CTA: jar.cta || 'Request Service',
      JARGON_QUERY: jar.query || (industry.toLowerCase() + ' services'),
      JARGON_VOLUME: jar.volume || dflt.jargon_volume || '~40',
      CUSTOMER_HEADLINE: cus.headline || ('Need a ' + tc(prov) + ' You Can Trust? Free ' + tc(svc) + ', Straight Answer.'),
      CUSTOMER_BULLETS: (cus.bullets || [
        'Clear pricing before any work starts',
        'Licensed, insured, local ' + plural(prov),
        'Book a free ' + svc + ' this week']).map(b => '<li>' + b + '</li>').join(''),
      CUSTOMER_CTA: cus.cta || ('Get a Free ' + tc(svc)),
      CUSTOMER_QUERY: cus.query || (industry.toLowerCase() + ' near me'),
      CUSTOMER_VOLUME: cus.volume || dflt.customer_volume || '~2,900',
      SERVICES_LIST: (ind.services || dflt.services || []).map(s => '<li>' + s + '</li>').join(''),
      SERVICE_CARDS: '<div class="mp-cards">' + (ind.services || dflt.services || []).slice(0, 6).map(s =>
        '<div class="mp-card"><span class="mp-thumb"></span><span class="mp-cn">' + s +
        '</span><span class="mp-go">View page &rarr;</span></div>').join('') + '</div>',
      SERVICE_CHIPS: '<div class="msf-opts">' + (ind.services || dflt.services || []).slice(0, 4).map((s, i) =>
        i === 0 ? '<button class="msf-opt sel">' + s + '<span class="msf-ck">&#10003;</span></button>'
                : '<button class="msf-opt">' + s + '</button>').join('') + '</div>',
      SERVICE_FIRST: (ind.services || dflt.services || [tc(svc)])[0],
      CONTACT_ID: cfg.contact_id || '',
      REASON_SPECIALIST_BODY: ind.specialist_body || (
        'We build for ' + industry.toLowerCase() + ' and nothing else, so we know what makes ' + cn +
        (city ? ' in ' + city : '') + ' pick one ' + prov + ' and skip the rest. ' +
        'Every page is written to earn that call. Generic agencies just guess.'),
      ASSET_MULTIPAGE: assets.multipage || '',
      ASSET_PROOF: assets.proof || '',
      BLUEPRINT_PDF: assets.blueprint || '',
      ASSET_PROOF_REDDIT: assets.proof_reddit || ('assets/research/' + proofSlug + '-reddit.png'),
      ASSET_PROOF_FB: assets.proof_fb || ('assets/research/' + proofSlug + '-facebook.png'),
      DEMO_URL: cfg.demo_url || '{{contact.demo_url}}',
      REVIEW_TEXT: ind.review_text || (
        'The team was fantastic &mdash; professional, honest, and did exactly what they said. ' +
        'For the first time, I actually trust who I call. <strong>Best ' + prov + ' experience we&rsquo;ve had' +
        (city ? ' in {{CITY}}.' : '.') + '</strong>'),
      REVIEW_REPLY: ind.review_reply || (
        'Thank you so much, that truly means a lot to us. I&rsquo;ll pass it along to the whole team. ' +
        'Welcome to the {{COMPANY_NAME}} family.'),
      HOW_TRAFFIC: loadBlock('how_traffic', blockDir),
      HOW_TRUST: loadBlock('how_trust', blockDir),
      HOW_CONVERSION: loadBlock('how_conversion', blockDir),
    };
    ctx['contact.first_name'] = cfg.first_name != null ? cfg.first_name : '{{contact.first_name}}';
    return ctx;
  }

  // prefix relative local asset URLs so a page served from /p/<slug>/ still loads them
  function absolutizeAssets(html, base) {
    if (!base) return html;
    return html.replace(/\b(src|poster|href)="(?!https?:|data:|#|\{\{|mailto:|tel:)([a-zA-Z0-9_][a-zA-Z0-9_./-]*\.(?:png|gif|webp|jpe?g|svg|pdf|mp4))"/g,
      (m, attr, path) => attr + '="' + base + path + '"')
      .replace(/url\('?(?!https?:|data:|\{\{)([a-zA-Z0-9_][a-zA-Z0-9_./-]*\.(?:png|gif|webp|jpe?g|svg))'?\)/g,
        (m, path) => "url('" + base + path + "')");
  }

  function buildProposal(opts) {
    const cfg = Object.assign({}, opts.cfg);
    const industries = opts.industries.industries;
    const defaults = opts.industries._defaults || {};
    let key = String(cfg.industry_key || '').toLowerCase().trim();
    let matched = key;
    if (!industries[key]) {
      const hits = Object.keys(industries).filter(k => k.indexOf(key) >= 0 || key.indexOf(k) >= 0);
      if (!hits.length) throw new Error('unknown industry "' + key + '"');
      matched = hits[0];
    }
    const ind = Object.assign({}, industries[matched], { _defaults: defaults, _block_dir: slugify(matched) });
    const ctx = buildCtx(cfg, ind, opts.blocks || {});
    let html = opts.template;
    const keys = Object.keys(ctx).sort((a, b) => b.length - a.length);
    for (let pass = 0; pass < 2; pass++) {
      for (const k of keys) html = html.split('{{' + k + '}}').join(String(ctx[k]));
    }
    html = absolutizeAssets(html, opts.assetBase || '');
    const unresolved = [...new Set((html.match(/\{\{([A-Za-z_]+)\}\}/g) || []))];
    return { html, slug: ctx.COMPANY_SLUG, industryKey: matched, unresolved };
  }

  const api = { buildProposal, slugify, tc, plural, esc, absolutizeAssets };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SBPRender = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
