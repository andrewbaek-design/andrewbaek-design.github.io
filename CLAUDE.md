# CLAUDE.md

Guardrails and conventions for the MedMe marketing website. Read this **before** making any change. These rules exist because they were learned the hard way; violations create work for future-you.

---

## 1. Architecture in 90 seconds

This is a **static HTML site** with a 165-line Python preprocessor ([build.py](build.py)).

```
src/                  ← SOURCE templates. Edit these.
  us/, ca/, legal/, company/, etc. (paths mirror live URLs)
partials/             ← Shared fragments included via {{> partials/x }}.
  nav-us.html, nav-ca.html, footer-us.html, footer-ca.html,
  util-bar-us.html, util-bar-ca.html, trust-band-us.html,
  logo-medme.html, cookie-banner.html
assets/               ← Shared CSS, JS, SVG. Globally cached.
  brand.css           Design system. Tokens, components, nav, buttons.
  homepage-us.css     US homepage page-scoped styles (large).
  homepage-ca.css     CA homepage page-scoped styles.
  site.js             Nav dropdown, mobile drawer, reveal-on-scroll, region switch.
us/, ca/, legal/, …   ← BUILT OUTPUT. Currently committed.
                        Do not hand-edit. Re-run python3 build.py.
```

**Workflow.** Edit `src/` or `partials/`, then:

```sh
python3 build.py            # builds src/ → root *.html files
python3 -m http.server 8000 # serve locally; visit /us/ or /ca/
```

**Template syntax.** Only three forms are supported:

| Syntax | Behavior |
|---|---|
| `{{> partials/nav-us }}` | Inline the contents of `partials/nav-us.html`. |
| `{{ page.title }}` | Substitute a key from the page's front-matter. |
| `{{# any comment }}` | Removed at build time. |

Front-matter is optional YAML-ish at the top of `src/*.html`:

```
---
region: us
page.title: MedMe, United States
---
```

---

## 2. Hard rules. Do not violate.

These are tested constraints from prior feedback rounds. Treat as build-blocking.

### Typography
- **No em-dashes (U+2014).** Use commas, colons, or periods. Hyphen-minus is fine.
- **No `text-transform: uppercase`** in user-facing copy. No hand-uppercased strings.
- **Title Case kickers.** Section kickers use Title Case: `Why MedMe`, `What It Does`, `Built For Every Pharmacy`. Not `WHY MEDME` or `why medme`.
- **Avoid widow lines.** Use `text-wrap: balance` on display headlines, `text-wrap: pretty` on paragraphs. Manually `<br>` only when balance/pretty can't fix it.
- **Headlines stay short.** Two visual lines max on display. If it doesn't fit, the copy is too long.

### Motion
- **Every animation must respect `prefers-reduced-motion: reduce`.** Wrap keyframes or set `animation: none` inside the media query. Skipping this is an accessibility regression.
- **Animations should be infinite + low-energy** for ambient decoration (waveforms, pulses, breathe). Don't trigger transitions on page load that fight the user's scroll.

### Content honesty
- **No fabricated customer names in mockups.** Use only customers explicitly approved (currently: Heritage Rx for case studies, NCAP / North Carolina Association of Pharmacists for the published pilot). Everything else uses anonymized labels ("Top-100 retail chain", "State Association").
- **No fabricated stats.** If a number doesn't come from a real source, frame it as a structural label (e.g., "10 to 15" cohort), not a claim.
- **Flag overclaims before shipping.** The product does not have: multi-speaker transcription, in-context drug info / protocols, on-device speech recognition, 99.99% uptime (use 99.9% if at all), or auto-fill in real time (auto-fill is one-click).

### Brand and copy
- **Spell out "North Carolina Association of Pharmacists"** rather than "NCAP" wherever space allows. The badge inside the constellation visualization is the only place "NCAP" is acceptable as an abbreviation.
- **Do not publicize specific pilot commercial terms** (e.g., "$0 platform fee", "2 to 4 week onboarding"). Use general framings ("member pricing", "phased onboarding") instead.

---

## 3. Design system

### Tokens (single source of truth: [`assets/brand.css`](assets/brand.css))

```
--indigo: #063E54           Primary brand color. Use for h1/h2, dark sections.
--matcha: #C3C430           Accent. Use sparingly: kickers, single accent words.
--seashell: #FAF9F5         Default page background. Warm off-white.
--indigo-dark: #042B3B      Deepest navy.
--indigo-80/95: tinted indigo variants for hierarchy on dark.
--indigo-04/08/12: low-alpha indigos for borders / dividers / subtle bg.
--container: 1440px         Main content max-width.
--tile-pad-x: page horizontal padding.
--radius-lg, --radius-md, --radius-sm: rounded corners.
--font-display, --font-body: Montserrat (single font; weights differ).
```

**Never hardcode a brand color.** If you write `#063E54` instead of `var(--indigo)`, you're creating a future find-and-replace burden. Same for `#C3C430` (matcha) and `#FAF9F5` (seashell).

### Buttons (3-tier global system)

| Class | Use when |
|---|---|
| `.btn-primary` | Primary action. One per visible viewport. "Book a demo." |
| `.btn-ghost` | Secondary action. Outlined. Pairs with primary. |
| `.btn-underline` | Tertiary. Card-internal CTAs, "Learn more" arrows. Use when multiple parallel CTAs in a grid would over-emphasize each one. `.btn-underline--on-dark` modifier for navy backgrounds. |

`.pill` and `.pill--solid` exist for the matcha-fill primary-CTA pill variant. `.btn-primary--accent` exists for matcha-fill on dark sections.

### Components

| Class | Description |
|---|---|
| `.tile`, `.tile--light`, `.tile--navy`, `.tile--prominent`, `.tile--ai-dark` | Section containers. `--light` is seashell bg, `--navy` is indigo bg, `--prominent` adds extra padding/emphasis, `--ai-dark` is the dark variant for AI-Native style sections. |
| `.tile__inner`, `.tile__head`, `.tile__head--centered`, `.tile__inner--narrow` | Inner wrappers and head block. |
| `.h-display`, `.h-display--xl` | Display headline. Balanced text-wrap. |
| `.kicker`, `.kicker--matcha` | Section eyebrow. Title Case. |
| `.lead` | Section lede paragraph. |
| `.pulse-rings`, `.pill-cta-row`, `.pill-cta-row--center` | Pulsing-ring decoration around primary CTA in dark closing sections. |

### Page-scoped patterns to avoid duplicating

These appear inline on multiple pages. If you're adding a 22nd one, **promote to brand.css instead**:

- `.sub-hero` + `__inner` / `__text` / `__bg` / `__lede` / `__cta` / `__breadcrumb` — appears inline in **21 pages**. Use the same definition each time.
- `.bl-card` (blog/resources cards) — appears in 5 Resources pages.
- "Card" patterns: prefer `.h-card`-based variants over inventing yet another `.foo-card` prefix. The site already has 16 different card-prefix names; we don't need a 17th.

### Cache busting

Every CSS link uses a `?v=N` query string for cache busting. Examples:
- `<link href="/assets/brand.css?v=65">` — bump when brand.css changes.
- `<link href="/assets/homepage-us.css?v=4">` — bump when homepage-us.css changes.

When you change `brand.css`, run a global find-replace for the current `?v=N` and bump everywhere. There is no automation for this yet (a known weakness).

---

## 4. Project structure rules

### When to use partials vs inline

- **Use a partial** if the markup is shared across **3+ pages** (nav, footer, trust band).
- **Inline** if it's truly one-of-a-kind (a specific page's hero motion graphic).
- **Don't** include partials inside other partials more than 2 levels deep.

### When to add CSS to brand.css vs page-inline

- **brand.css** if the rule is used or could be used on 3+ pages.
- **homepage-{us,ca}.css** if it's homepage-only.
- **Inline `<style>` in src/*.html** if it's genuinely page-scoped.

If you find yourself copy-pasting CSS between two pages, stop and consider whether the third page would want it too.

### File naming

- Source paths mirror live URLs. `src/us/pharmacy/independents.html` → `/us/pharmacy/independents/`.
- Lowercase, hyphen-separated. No spaces. No camelCase.
- Image / SVG mockups go in `assets/<page-slug>-mockup.svg` if shared, or `assets/<topic>-<descriptor>.svg`.

---

## 5. Conventions for AI-assisted edits

This project has been built largely with Claude Code. Every AI edit must:

1. **Read the project conventions in section 2** before making any change.
2. **Search for an existing pattern** before inventing a new one. The site already has `.tile`, `.h-card`, `.bl-card`, `.feature`, `.partner-card` (and more). Reuse, don't recreate.
3. **Bump the relevant `?v=N`** when changing `brand.css` or page CSS files.
4. **Run `python3 build.py`** after every edit; commit both source and built output (current convention, will change in a future round).
5. **For copy edits**, change source only — don't manually edit built output files.
6. **For multi-page changes** (e.g., trust band uptime stat), check whether the value is also inlined on the homepage at [src/us/index.html](src/us/index.html). The homepage carries its own inline trust band that doesn't pull from `partials/trust-band-us.html`.

---

## 6. Currently deferred work

Known weaknesses, not yet addressed. Do not introduce new instances of these patterns:

- **Inline CSS duplication.** `.sub-hero` and several card patterns are duplicated across 12-21 pages each. A future round will promote these to `brand.css`. Until then, add to brand.css instead of inlining if you're touching a third page.
- **No content layer.** Page copy lives inside HTML. A future round will consider Markdown front-matter or a small JSON data layer for high-churn copy.
- **No framework.** A future round will consider migrating to Astro or Eleventy.
- **Built output is committed.** A future round will move to an Actions-based deploy that builds artifacts off-tree.

If the team agrees to act on any of these, this file gets updated alongside.

---

## 7. Useful commands

```sh
# Build everything in src/
python3 build.py

# Build with check mode (exits 1 if any output would change)
python3 build.py --check

# Serve locally
python3 -m http.server 8000

# Optimize SVGs (after npm i -g svgo, or via npx)
npx svgo assets/*.svg

# Count inline CSS duplication
grep -rln "\.sub-hero {" src/ | wc -l

# Find hardcoded brand colors (token violations)
grep -rnE "#063E54|#C3C430|#FAF9F5" src/ assets/

# Verify constraint compliance before commit
grep -rnP "[\x{2014}]" src/ partials/      # em-dashes (must be empty)
grep -rnP "text-transform:\s*uppercase" src/ partials/    # uppercase (must be empty)
```

---

## 8. Recent project history

For context on why some patterns exist and others were rejected:

- **2026-05-22 strategy session (Christine).** Light theme (not dark), stacked hero, simplified UI mockups, "Pharmacy EHR" terminology debated (use on enterprise pages, off the homepage hero), associations page reframed around member growth + advocacy + outcomes data.
- **2026-06-15 review (Audrey, Sayna, Andrew, Fawad, Mika).** 54 open comments compiled in Notion. Most flagged product overclaims that have since been corrected on the AI Clinical Assistant, Patient Concierge, and Specialty pages.
- **2026-06-17 round 2 polish.** Hero converted to 2-column, trust band dark, Why MedMe lit cards (port of the Independents "Clear Path" lighting effect), Built-for-Every-Pharmacy section background tinted, Platform CTAs removed, AI-Native section fully dark mode, nav menu items now carry leading icons.

The git log is the canonical record. This file just summarizes the conventions that emerged.
