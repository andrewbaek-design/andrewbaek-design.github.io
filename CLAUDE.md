# CLAUDE.md

Guardrails and conventions for the MedMe marketing website. Read this **before** making any change. These rules exist because they were learned the hard way; violations create work for future-you.

---

## 1. Architecture in 90 seconds

This is an **Astro 5 static site**. All source and build config lives under `astro/`. The repo root holds only docs, the GitHub Actions workflow, and `.gitignore`.

```
astro/
  src/
    pages/             File-based routes. astro/src/pages/legal/privacy.astro → /legal/privacy/
    layouts/           Shared HTML shells: BaseLayout.astro (US), BaseLayoutCa.astro (CA).
    components/        Shared partials: NavUs, NavCa, FooterUs, FooterCa, UtilBarUs, UtilBarCa,
                       LogoMedme, CookieBanner, TrustBandUs.
    content/           Content collections (Markdown sidecars with typed frontmatter).
      legal/           privacy, hipaa, pipeda, terms (.md files)
      us/              about (.md file)
    content.config.ts  Zod schemas for collections.
  public/
    assets/            brand.css, homepage-us.css, homepage-ca.css, site.js, SVGs.
                       Served from /assets/* unchanged. No Astro processing.
  astro.config.mjs     Site config (directory format, trailing-slash, remark plugins).
  package.json         Astro dep + scripts.
  CLAUDE.md            Astro-specific notes (kept; cross-linked from here for now).

.github/workflows/pages.yml   CI build + deploy to GitHub Pages.
```

**Workflow.** Edit `astro/src/**`, then:

```sh
cd astro
npm install                    # first time only
npm run dev                    # dev server on http://localhost:4321
npm run build                  # production build → astro/dist/
```

**Template syntax.** Astro `.astro` files are HTML + a frontmatter block. JSX-style expressions in the body.

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import { getEntry, render } from 'astro:content';

const entry = await getEntry('legal', 'privacy');
const { Content } = await render(entry);
const { title, description, kicker, headline, lede } = entry.data;
---
<BaseLayout title={title} description={description}>
  <h1 set:html={headline}></h1>
  <Content />
</BaseLayout>
```

Key Astro features in use here:
- `<Component />` — child component invocation. Imports go in the `---` block.
- `{expression}` — interpolate a JS expression.
- `set:html={value}` — render trusted HTML from a frontmatter string (used for headlines/ledes that contain inline `<span>` / `<strong>`).
- `is:inline` on `<script>` / `<style>` — pass-through without Astro/Vite processing. Used for JSON-LD blocks and page-specific JS.
- `<slot name="head" />` / `<slot name="end-of-body" />` — BaseLayout exposes named slots for pages to inject head extras or trailing scripts.

### Content Collections (sidecar Markdown for page copy)

Pages that are mostly long-form prose use Astro Content Collections. The `.md` file holds the copy, the `.astro` file holds the layout shell.

Two collections exist today:

- **`legal`** — privacy, hipaa, pipeda, terms. Schema: required `title`, `description`, `kicker`, `headline`, `lede` + optional CTA fields. See [astro/src/content/legal/privacy.md](astro/src/content/legal/privacy.md).
- **`usPages`** — about. Looser schema with per-section kickers/headlines/leads. See [astro/src/content/us/about.md](astro/src/content/us/about.md).

**When to use a sidecar `.md`.** Pages that are mostly prose (legal, about, careers, blog posts). Pages with heavy custom motion, mockups, or multi-section structured layouts should stay as plain `.astro` files with content embedded.

**Markdown rendering.** Astro's default Markdown is CommonMark + GFM. Custom heading IDs (`## 1. Scope {#scope}` syntax used by the legal pages) are enabled via the `remark-custom-heading-id` plugin in [astro/astro.config.mjs](astro/astro.config.mjs). Without that plugin, Astro auto-slugs heading text and existing TOC anchors break.

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

### Tokens (single source of truth: [`astro/public/assets/brand.css`](astro/public/assets/brand.css))

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

**Inverse trap: never replace the literal hex in the token definitions themselves.** The `:root { --indigo: #063E54; ... }` block in `brand.css` is the source of truth. Replacing those literals with `var(--indigo)` etc. creates a circular self-reference, CSS resolves the variable to empty, and every page silently falls back to browser defaults (white background instead of seashell, etc.). The token definitions in `brand.css` carry a comment that says "Do not replace these with var() references." Respect it.

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

### CSS scoping strategy

Page-inline `<style>` blocks in `.astro` files are **scoped by default** (Astro adds a `data-astro-cid-*` attribute selector). This was validated against the 24 source pages with inline CSS: only one (the geo-redirect root index) needed `is:global` because it targets `body`/`html` directly.

**Use `<style is:global>` only when:**

1. The rules target a partial/layout element (`.nav__*`, `.site-footer__*`, `.util-bar__*`). Scoped styles don't reach into child components.
2. The rules target `body` or `html` directly.
3. The rules redeclare a brand-token-level `@font-face`, `:root` custom properties, or any global side-effect.

**`brand.css` stays a global stylesheet** loaded via `<link>` in `BaseLayout.astro`. Page-inline styles for layout/scope-specific cosmetics live in each `.astro` file under a default `<style>` block.

Astro renames `@keyframes` identifiers in scoped blocks (e.g. `hero-video-pulse` → `hero-video-pulse-XXXXX`) and rewrites the matching `animation:` references in the same scope, so 58 page-local keyframes survive without modification.

---

## 4. Project structure rules

### When to use a component vs. inline markup

- **Component** (in `astro/src/components/`) if the markup is shared across **3+ pages**. Current shared components: NavUs/NavCa, FooterUs/FooterCa, UtilBarUs/UtilBarCa, LogoMedme, CookieBanner, TrustBandUs.
- **Inline in the `.astro` page** if it's truly one-of-a-kind (a specific page's hero motion graphic).

### When to add CSS to brand.css vs. a page-inline `<style>` block

- **brand.css** if the rule is used or could be used on 3+ pages.
- **homepage-{us,ca}.css** if it's homepage-only (loaded via head slot from `astro/src/pages/{us,ca}/index.astro`).
- **Page-inline `<style>` in the `.astro` file** if it's genuinely page-scoped. Scoping is automatic.

### File naming

- Source paths mirror live URLs. `astro/src/pages/us/pharmacy/independents.astro` → `/us/pharmacy/independents/`.
- Lowercase, hyphen-separated. No spaces. No camelCase.
- Image / SVG mockups go in `astro/public/assets/<page-slug>-mockup.svg` if shared, or `astro/public/assets/<topic>-<descriptor>.svg`.

### When to use a sidecar `.md` (Content Collection) vs. embed content in `.astro`

- **Sidecar `.md`** when the page is mostly long-form prose with little structural variation per section (legal, about, blog posts, case studies). The author edits `.md`, not `.astro`.
- **Embed in `.astro`** for marketing pages with multi-section custom layouts, motion, mockups, or interactive widgets.

---

## 5. Conventions for AI-assisted edits

This project has been built largely with Claude Code. Every AI edit must:

1. **Read the hard rules in section 2** before making any change.
2. **Search for an existing component or pattern** before inventing a new one. Check `astro/src/components/` and `brand.css` first.
3. **Run `npm run build` from `astro/`** after non-trivial edits to verify the build still passes. Output goes to `astro/dist/` (gitignored).
4. **For copy edits on pages with a sidecar `.md`**, edit the `.md`, not the `.astro` page shell.
5. **For multi-page changes** (e.g. trust band uptime stat, nav structure), edit the shared component, not each page.
6. **`brand.css` is the global stylesheet.** Page-inline `<style>` blocks are scoped. Don't move scoped CSS into brand.css unless 3+ pages need it.

---

## 6. Deploy

`.github/workflows/pages.yml` runs on every push to `main`:

1. Checkout the repo
2. Set up Node 20 + cached npm
3. `npm ci` in `astro/`
4. `npm run build` in `astro/` → `astro/dist/`
5. Upload `astro/dist/` as the Pages artifact
6. Deploy to GitHub Pages

Manual re-deploy from the Actions tab is also wired up (`workflow_dispatch`).

The repo lives at https://github.com/andrewbaek-design/andrewbaek-design.github.io. Production hosting at `medmehealth.com` continues to run on Webflow; this codebase is a design-direction reference shared with the marketing team for porting into Webflow via the Webflow MCP server.

---

## 7. Useful commands

```sh
# All commands run from astro/ unless noted.

cd astro

npm install               # install Astro + deps (first time, or after package.json changes)
npm run dev               # dev server on http://localhost:4321
npm run build             # production build → astro/dist/
npm run preview           # serve astro/dist/ on http://localhost:4321

# From repo root, find hardcoded brand colors (token violations):
grep -rnE "#063E54|#C3C430|#FAF9F5" astro/src astro/public/assets

# Verify constraint compliance:
grep -rnP "[\x{2014}]" astro/src                          # em-dashes (must be empty)
grep -rnP "text-transform:\s*uppercase" astro/src         # uppercase (must be empty)
```

---

## 8. Recent project history

For context on why some patterns exist and others were rejected:

- **2026-05-22 strategy session (Christine).** Light theme (not dark), stacked hero, simplified UI mockups, "Pharmacy EHR" terminology debated (use on enterprise pages, off the homepage hero), associations page reframed around member growth + advocacy + outcomes data.
- **2026-06-15 review (Audrey, Sayna, Andrew, Fawad, Mika).** 54 open comments compiled in Notion. Most flagged product overclaims that have since been corrected on the AI Clinical Assistant, Patient Concierge, and Specialty pages.
- **2026-06-17 round 2 polish.** Hero converted to 2-column, trust band dark, Why MedMe lit cards, Built-for-Every-Pharmacy section background tinted, Platform CTAs removed, AI-Native section fully dark mode, nav menu items now carry leading icons.
- **2026-06-16 framework migration.** Site moved from a hand-rolled 360-line Python preprocessor (`build.py` + `{{> partials/X }}` template syntax) to Astro 5 with file-based routing, typed Content Collections, scoped page styles, and a 5-step GitHub Actions deploy. All 62 pages migrated with tag-count parity verified. Two intentional improvements over legacy: every page now carries a `<a href="#main">` skip-link, and duplicate `site.js` loads on pages that referenced both the util-bar partial and an inline script tag are now deduplicated. Legacy `build.py`, `src/`, `partials/`, and root-level `assets/` were removed in the same change; recoverable from git history pre-migration commit.

The git log is the canonical record. This file just summarizes the conventions that emerged.
