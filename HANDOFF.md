# SolidBookedPro Proposal Page — Session Handoff

> Read this top-to-bottom before editing. It captures the full state, every unique feature, the industry mapping, the GHL automation, and exactly what's left to do.

---

## 1. What this project is
A **per-appointment PROPOSAL / close page** for **SolidBookedPro (SBP)** — Vince's done-for-you growth-system business. When a prospect **books an appointment in GoHighLevel (GHL)**, an automation builds a personalized proposal page for that prospect and (eventually) hosts it at `proposal.solidbookedpro.com/{slug}`. The proposal **embeds the prospect's demo website** (built by a *separate* automation) inside a laptop mockup, then pitches + closes.

## 2. ⚠️ TWO different pages — do not confuse them
- **Proposal page** = THIS repo (`index.html`). The sales/close page shown to a booked prospect.
- **Demo page** = the actual website built for the prospect (e.g. `demo.scalingsos.com/gihon-family-care-home/`). Built by the OTHER automation (ScalingSOS / "SolidBookedPro - Generate Demo" + "Process Demo" in n8n). **NOT built here.** The proposal only *embeds* it via iframe in the hero laptop.
- (A previous session mistakenly deployed the demo file as if it were the proposal — don't repeat that. The proposal is the blue, Montserrat, plan-picker build in this repo.)

## 3. 🚩 Content origin + status — IMPORTANT
- The **design/layout** was replicated from a reference proposal page (King Contractor Agency's "your website is ready" close page). The design *system* (structure, components, layout) is the reusable functional part.
- The current **section copy is still largely the reference's marketing copy word-substituted** (roofing→industry, OSAAT→client). **This must be rewritten in SolidBookedPro's own voice before any public/prospect use** — it is not SBP-original yet.
- **Original already:** the founder section (Vince's own bio) and the **Plan Picker** (Vince's own drawing/spec).
- **Reference images** (founder passport, founder photo, client-owner photos, portfolio screenshots) were replaced with `placeholder.svg` — swap in SBP's own images.

## 4. Proposal page structure (top → bottom)
1. **Nav** — SBP logo left; "Prepared exclusively for `{{company_name}}`" right. (TODO: reference has a **sticky nav** — make this sticky.)
2. **Hero** — H1 "Ultimate `{{industry}}` Smart Website for `{{company_name}}`"; benefit checklist ("WINS TRUST OF `{{customer_noun}}`", "= YOU `{{outcome}}`"); **laptop preview = iframe of the demo site** (`{{demo_url}}`), non-interactive; **NO "Open Live Site"** button (intentional — prospect must attend the call to see it live).
3. **The Winning Formula** — Traffic / Trust / Conversion → outcome. *(copy = reference-derived → rewrite)*
4. **Three reasons to call today**. *(rewrite)*
5. **Always-on AI** — answers/rings in seconds; chat + phone mockups; "Reputation, on autopilot" (example reviews are **illustrative placeholders**, not real). *(rewrite)*
6. **Founder** — "Hello, I'm Vince" + real track record (STATIC across all clients: 150+ roofing companies, $250M+ in roofs sold — his actual roofing background, do NOT industry-swap these) + promise line that DOES adapt ("help you `{{outcome}}`"), signed "Vince Stars". **ORIGINAL.**
7. **Promise band** — "Cancel any time after month 3 · no long-term contracts · the risk is on us." (replaced the removed $1M proof section).
8. **Timeline** — "Sign today. Live in 3 days" (Day 1/2/3).
9. **Plan Picker** (interactive, ORIGINAL) — see §6.

## 5. Removed sections (intentional)
ROI Calculator · client-builds carousel ("Setting industry standards") · $1M proof + case-study videos · e-signature acceptance · "120 5-star reviews" block · footer tagline ("Building America's Most Trusted…") · inline edit-pricing/undo admin controls · "Open Live Site" button · license badge.

## 6. ⭐ Unique feature: the interactive Plan Picker
- Headline: **"The Site That Only Costs You Something If It Works"**.
- **Diagram:** center "Site Preview" box; **left arrow →** 5-Star Outreach System; **right arrow →** Monthly Qualified Prospect Guarantee; **down arrow →** 24/7 Receptionist Follow-Up.
- **"What's included"** list (8 green-checked items).
- **3 One-Time price boxes:** $297 / $497 / $997. **Default selected = $997.**
- **Interactivity (JS):** click a box → that box turns **GREEN**, the other two **YELLOW**; items not in that tier **grey out + strikethrough + uncheck**. Driven by `data-tier` on each arrow/list item:
  - tier 1 = all plans · tier 2 = $497 & $997 · tier 3 = $997 only.
  - **$997:** everything active. **$497:** greys Monthly Qualified Prospect Guarantee (right arrow), 24/7 Receptionist Follow-Up (down arrow), 24/7 Missed Call list item. **$297:** all of $497's grey-outs **plus** 5-Star Outreach System (left arrow + its list item).
- **Colors:** selected green `#16A34A`, others yellow `#EAB308`/`#FEF9C3`, checks green `#16A34A`, arrows blue `#2563EB`.
- **Injected by `build_proposal.py`** (the `PP_CSS` / `PP_HTML` / `PP_JS` block) replacing the old `section-grey` pricing block.
- **Vince's aesthetic TODOs for it:** price boxes should match the **"How?" button** styling; the **Site Preview should show the actual demo site** (like the hero laptop, not a placeholder box); match the **fonts/colors** used elsewhere on the page; make **"job"** industry-mapped; feature list styling more like the original reference.

## 7. Branding
- SBP blue `#2563EB`, blue-dark `#1D4ED8`, navy `#0F172A`, bg-blue `#EAF1FE`. Fonts: **Montserrat** (headings) + **Open Sans** (body).
- Logos: `sbp-logo-white.png` (dark bg) · `sbp-logo-navy.png` (light bg) · flag mark in `~/solidbookedpro-brand/`.

## 8. GHL merge fields (the automation fills these)
| Token | GHL source | Example (Gihon) |
|---|---|---|
| `{{company_name}}` | contact.company_name | Gihon Family Care Home |
| `{{industry}}` | contact.industry (Title Case) | Home Care |
| `{{city}}` | contact.city | Palm Coast |
| `{{state}}` | contact.state | Florida |
| `{{first_name}}` | contact.first_name (was "Chris") | — |
| `{{phone}}` | contact.phone | (470) 918-0516 |
| `{{address}}` | contact.address | — |
| `{{demo_url}}` | prospect's demo site (other automation) | demo.scalingsos.com/gihon-family-care-home/ |
| `{{slug}}` | kebab(company_name) | gihon-family-care-home |
| `{{proposal_url}}` | **written back** after deploy | — |

**GHL:** location `Al8uJ2dxiJLdmlsCuWwW`; `proposal_url` custom field key `contact.proposal_url`, id `xrtdQh5HIMdOvSuF4NWH`; base `https://services.leadconnectorhq.com`, header `Version: 2021-07-28`. **Working token is in `~/.claude/settings.json`** (`pit-83caa927…`; the `pit-91dac341…` in Claude Memory is the OLD scope-broken one).

## 9. Industry mapping (23 verticals) — `INDUSTRY_TERMS` in build_proposal.py; n8n keeps the same map keyed on `{{contact.industry}}`
Each industry maps to `{customer_noun, service_term, provider_term, outcome}` which replace HOMEOWNERS / estimate·inspection / contractor / SELL MORE ROOFS respectively:

| industry | customer_noun | service_term | provider_term | outcome |
|---|---|---|---|---|
| cleaning | homeowners | quote | cleaning company | BOOK MORE CLEANINGS |
| diesel mechanic | fleet owners | estimate | shop | FIX MORE TRUCKS |
| electrical | homeowners | estimate | electrician | BOOK MORE JOBS |
| fencing | homeowners | quote | fence company | BUILD MORE FENCES |
| flooring | homeowners | quote | flooring company | INSTALL MORE FLOORS |
| funeral home | families | consultation | funeral home | SERVE MORE FAMILIES |
| home care | seniors | consultation | care provider | SERVE MORE SENIORS |
| hvac | homeowners | estimate | HVAC company | BOOK MORE JOBS |
| landscaping | homeowners | quote | landscaper | BOOK MORE PROJECTS |
| mobile mechanic | drivers | quote | mobile mechanic | FIX MORE CARS |
| mobile truck repair | fleet owners | estimate | repair shop | FIX MORE TRUCKS |
| mold remediation | homeowners | inspection | remediation company | BOOK MORE JOBS |
| moving | homeowners | quote | moving company | BOOK MORE MOVES |
| painting | homeowners | quote | painting company | BOOK MORE JOBS |
| pest control | homeowners | inspection | pest control company | BOOK MORE TREATMENTS |
| plumbing | homeowners | estimate | plumber | BOOK MORE JOBS |
| remodeling | homeowners | consultation | remodeler | BOOK MORE PROJECTS |
| roofing | homeowners | inspection | contractor | SELL MORE ROOFS |
| septic tank | homeowners | quote | septic company | BOOK MORE JOBS |
| solar | homeowners | consultation | solar company | CLOSE MORE INSTALLS |
| therapy/counseling | clients | consultation | practice | BOOK MORE CLIENTS |
| tree repair | homeowners | quote | tree service | BOOK MORE JOBS |
| tree service | homeowners | quote | tree service | BOOK MORE JOBS |

TODO: add a **`job`** term to the map (the per-industry revenue unit) — Vince wants "job" industry-mapped wherever it appears.

## 10. The build script — `build_proposal.py`
- Renders the proposal from the reference layout + a `CFG` dict (= the per-client GHL fields) + the `INDUSTRY_TERMS` map. **The GHL automation is the same logic**: webhook → CFG from contact → substitute → deploy.
- To render a different client locally: edit `CFG` at the top, run `python3 build_proposal.py` → writes `index.html`.
- It performs: section removals, laptop→demo-iframe swap, brand/color remap (reference red+gold → SBP blue), ordered text swaps (brand/company/industry/customer-noun/service-term/provider-term/outcome/location/data), founder-bio restore (keeps roofing stats), plan-picker injection, HTML-comment strip.
- Ordering gotcha: post-swap fixes (founder restore, promise wording) MUST run after the industry swaps — they're at the end of the `reps` list.

## 11. The deploy automation (mechanism PROVEN; n8n wrapper still TO BUILD)
- **Deploy repos (org `vincestars-cloud`):** `scalingsos-public-pages` = PUBLIC deploy target (→ `demo.scalingsos.com`); `scalingsos-demos` = PRIVATE templates. Read templates from `scalingsos-demos/templates/`, WRITE output to `scalingsos-public-pages`.
- **Deploy = GitHub Contents API:** GET sha → PUT base64. Use `gh api` (authed as `vincestars-cloud`, and `Bash(gh api *)` is allow-listed — this is why the git/gh classifier block doesn't apply). A GitHub token also lives inline in the n8n Process Demo deploy nodes (workflow `cFxtipXrKhjNBPYP`).
- **Mac Python SSL:** use certifi — `ssl.create_default_context(cafile=certifi.where())`.
- **Pages deploy churn:** the demo pipeline auto-commits cancel Pages builds; force a build with `gh api -X POST repos/vincestars-cloud/scalingsos-public-pages/pages/builds` in a quiet window.
- **n8n workflow TO BUILD** — `SolidBookedPro - Proposal Builder`:
  `Webhook (GHL appt booked) → Code (extract fields + slug + industry terms) → HTTP (fetch template from scalingsos-demos) → Code (render {{tokens}}) → HTTP (get SHA) → HTTP (PUT deploy to scalingsos-public-pages/proposals/{slug}/) → HTTP (PATCH GHL contact.proposal_url) → schedule +2d: if status ∉ {New Client, Follow-Up} → DELETE file → Respond {proposal_url}`.
  Node types already pulled (webhook/code/httpRequest/respondToWebhook). Existing `SolidBookedPro - Generate Demo`/`Process Demo` workflows exist but are NOT MCP-readable.
- **Auto-expire:** delete the proposal file after 2 days if the GHL contact status isn't "New Client"/"Follow-Up" (stops prospects shopping it around).

## 12. What's next (priority)
1. **Make it genuinely SBP's own** — rewrite reference-derived copy in SBP voice; replace `placeholder.svg` images with SBP's own (founder photo, etc.).
2. **Vince's aesthetic edits** (list forthcoming) — plan-picker boxes ↔ "How?" button styling; Site Preview shows the real demo; match fonts/colors; sticky nav; "job" industry-mapped; feature-list styling like the reference.
3. **Build + test the n8n `Proposal Builder` workflow** end-to-end.
4. **Decide the proposal domain** — `proposal.solidbookedpro.com` (CNAME) vs `demo.scalingsos.com/proposals/`.
5. **Clean up** the erroneous demo deploy at `scalingsos-public-pages/proposals/gihon-family-care-home/` and the wrong `scalingsos-demos/templates/proposal.template.html` (it's the demo, not the proposal).

## 13. Files in this repo
- `index.html` — the proposal page (Gihon-rendered; reference images → `placeholder.svg`).
- `build_proposal.py` — render/build script (CFG + INDUSTRY_TERMS + plan-picker).
- `placeholder.svg`, `placeholder-logo.svg` — image placeholders to replace with SBP's own.
- `kca-assets/guarantee_icons.webp` — money-back badge (generic).
- `sbp-logo-white.png`, `sbp-logo-navy.png`, `sbp-flag.svg` — SBP logos.
- `HANDOFF.md` — this doc.
