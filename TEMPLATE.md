# SolidBooked Pro — Proposal Template System

`index.html` is no longer hand-edited per client. It is a **build artifact**:

```
proposal.template.html  +  industries.json  +  clients/<name>.json
        └────────────── render_proposal.py ──────────────┘
                              ↓
                        <client>.html
```

**Proven lossless:** rendering the Gihon config reproduces the current live
`index.html` **byte-for-byte**. Nothing was lost in templatizing.

---

## Render a proposal

```bash
# from a saved client file
python3 render_proposal.py --client clients/gihon.json --out index.html

# ad-hoc, any of the 26 verticals
python3 render_proposal.py \
  --industry roofing \
  --company "Apex Roofing & Exteriors" \
  --city Tampa --state FL --phone "(813) 555-0142" \
  --out apex.html
```

Anything omitted is derived: `slug` and `preview_domain` from the company name,
every case variant / plural from the industry terms, and any missing copy block
from a generated default. The script **exits non-zero if any `{{TOKEN}}` is left
unresolved**, so a broken render can never be deployed silently.
`{{contact.*}}` GHL merge fields are intentionally left in place.

## The two token layers

**1. Word-level** — swapped everywhere automatically:

| Client | Industry |
|---|---|
| `COMPANY_NAME` `COMPANY_SLUG` `PREVIEW_DOMAIN` `CITY` `STATE_ABBR` `PHONE` | `INDUSTRY(_LC/_UC)` `CUSTOMER_NOUN(_S/_TC/_UC)` `BUYER_NOUN` `PROVIDER_TERM(_PL)` `WORKER_TERM` `SERVICE_TERM(_PL/_TC)` `OUTCOME_LC/_TC/_UPPER` `OUTCOME_RESULT` `OUTCOME_SEEN` |

Three nouns are deliberately separate because they are **not** the same person:

- `CUSTOMER_NOUN` — who receives the service (*seniors*, *homeowners*, *patients*)
- `BUYER_NOUN` — who actually decides/pays (*families* for home care, usually the same as customer elsewhere)
- `WORKER_TERM` — who shows up at the door (*caregiver*, *roofer*, *plumber*)

**2. Content blocks** — too vertical-specific to derive from a word swap, so they
live in `industries.json`:

`JARGON_HEADLINE/BULLETS/CTA/QUERY/VOLUME` · `CUSTOMER_HEADLINE/BULLETS/CTA/QUERY/VOLUME`
· `SERVICES_LIST` · `REASON_SPECIALIST_BODY` · `ASSET_MULTIPAGE` · `ASSET_PROOF` · `BLUEPRINT_PDF`

## Adding / improving a vertical

Only `customer_noun`, `provider_term`, `service_term` and `outcome` are required —
everything else falls back to a sane generated default.

```jsonc
"dental": {
  "industry": "Dental",
  "customer_noun": "patients", "customer_noun_s": "patient",
  "provider_term": "practice", "worker_term": "dentist",
  "service_term": "appointment",
  "outcome": "book more patients", "outcome_result": "More Patients Booked",

  // optional but strongly recommended — bespoke always beats generated:
  "services": ["Cleanings", "Implants", "Invisalign", "Emergency Dentistry"],
  "jargon":   { "headline": "...", "bullets": ["..."], "cta": "...", "query": "...", "volume": "~40" },
  "customer": { "headline": "...", "bullets": ["..."], "cta": "...", "query": "...", "volume": "~2,900" },
  "assets":   { "multipage": "dental-multipage.png", "proof": "dental-proof.png" }
}
```

The renderer prints a warning naming exactly which blocks fell back to generated
copy and whether fallback screenshots were used — treat those warnings as the
to-do list for that vertical.

**Currently authored bespoke:** home care, roofing, plumbing.
**Terms-only (generated copy):** 23 more verticals — hvac, electrical, cleaning,
landscaping, fencing, flooring, painting, pest control, mold remediation, moving,
remodeling, septic, solar, tree service, diesel/mobile mechanic, mobile truck
repair, body shop, funeral home, therapy, dental, med spa, law.

## Known per-industry work remaining

These are still home-care images and must be reshot per vertical (the renderer
warns when they are used as fallbacks):

- `ASSET_MULTIPAGE` — the "a page for every service" screenshot
- `ASSET_PROOF` — the customer-language research strip
- The testimonial/review copy and the founder bio remain SBP-generic by design.

## GHL / n8n wiring

The automation builds the same config object from the webhook, then substitutes:

| config key | GHL field |
|---|---|
| `company_name` | `{{contact.company_name}}` |
| `industry_key` | `{{contact.industry}}` (lowercased; fuzzy-matched to a preset) |
| `city` / `state` | `{{contact.city}}` / `{{contact.state}}` |
| `phone` | `{{contact.phone}}` |
| `first_name` | `{{contact.first_name}}` — leave unset to keep the literal merge field |

Unknown industries fuzzy-match to the closest preset; if there is no match the
render fails loudly rather than shipping a page full of the wrong words.

## Regenerating the template

If the page is edited directly, re-derive the template from the rendered page:

```bash
python3 templatize.py index.html proposal.template.html
```

It prints every substitution, then audits for residual client/industry words —
that residual list must be empty.
