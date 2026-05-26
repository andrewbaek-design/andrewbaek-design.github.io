# MedMe Health — Website Mockup

Static HTML mockups of a redesigned MedMe Health marketing site, with
two regional homepages (United States and Canada), 49 supporting
sub-pages, and a tiny Python build system that keeps shared chrome
(nav, util-bar, footer) in single-source partials.

## Live preview

Hosted on Netlify — open **[medmehealth.netlify.app](https://medmehealth.netlify.app)**
to land on the region picker, or jump directly:

- [US Homepage](https://medmehealth.netlify.app/us)
- [Canada Homepage](https://medmehealth.netlify.app/ca)

Or run locally — `open index.html` lands on the region picker. For the
no-`.html` clean URLs to work locally you'll want a tiny HTTP server:
`python3 -m http.server 8000`.

## Deploying changes

```sh
python3 build.py              # regenerate output HTML from src/ + partials/
netlify deploy --prod --dir=. # push to https://medmehealth.netlify.app
```

Auto-deploy on `git push` is intentionally *not* wired up — manual
CLI deploys keep us in control of when build minutes are consumed.

## URL hierarchy

The site uses clean, extensionless URLs throughout. Files live under
the same path as the URL serves them at; Netlify resolves `/us/pricing`
to the file `us/pricing.html` automatically.

| URL                              | File                            |
|----------------------------------|---------------------------------|
| `/`                              | `index.html` (region picker)    |
| `/us`                            | `us/index.html`                 |
| `/us/pricing`                    | `us/pricing.html`               |
| `/us/platform/ai-scribe`         | `us/platform/ai-scribe.html`    |
| `/ca`                            | `ca/index.html`                 |
| `/ca/platform/ai-concierge`      | `ca/platform/ai-concierge.html` |
| `/login`                         | `login.html`                    |
| `/legal/privacy`                 | `legal/privacy.html`            |
| `/company/careers`               | `company/careers.html`          |
| `/assets/brand.css`              | `assets/brand.css`              |
| `/assets/site.js`                | `assets/site.js`                |

## Repository layout

```
.
├── index.html              Region-picker landing page (/)
├── us/                     United States site (/us, /us/pricing, …)
│   ├── index.html          US homepage
│   ├── pricing.html
│   ├── about.html
│   ├── contact.html
│   ├── customers/
│   ├── pharmacy/
│   ├── platform/
│   └── resources/
├── ca/                     Canada site (/ca, /ca/pricing, …)
│   └── …                   Same shape as us/
├── legal/                  /legal/privacy, /legal/terms, etc.
├── company/                /company/careers, /company/press, /company/status
├── login.html              /login
├── assets/                 Shared CSS + JS
│   ├── brand.css
│   └── site.js
├── partials/               Shared HTML fragments — edit these
│   ├── nav-us.html, nav-ca.html
│   ├── util-bar-us.html, util-bar-ca.html
│   ├── footer-us.html, footer-ca.html
│   └── logo-medme.html
├── src/                    Source templates — edit these, mirror the
│   ├── us/                 published path of each page
│   ├── ca/
│   ├── legal/
│   ├── company/
│   └── login.html
├── build.py                Template engine (stdlib Python)
├── BUILD.md                Build system documentation
└── netlify.toml            Deploy config
```

## Workflow

```sh
# Preview locally (need an HTTP server for clean URLs)
python3 -m http.server 8000
open http://localhost:8000/

# After editing a partial or source template
python3 build.py

# Verify nothing has drifted before publishing
python3 build.py --check       # exits 1 if a rebuild would change output
```

Full build-system docs in [BUILD.md](BUILD.md).

## Design

Brand identity follows the **MedMe Brandguide v1.0** (Feb 2022):

| Token         | Hex       | Role                                       |
|---------------|-----------|--------------------------------------------|
| `--indigo`    | `#063E54` | Primary — most-used colour                 |
| `--seashell`  | `#FFF7F2` | Primary — warm off-white (not pure white)  |
| `--matcha`    | `#C3C430` | Secondary accent — use sparingly           |

Typography: **Urbanist Semibold** for headlines, **Montserrat Bold All-Caps**
for subheads, **Montserrat Medium** for body. Both from Google Fonts.

## License

Internal mockup. All rights reserved.
