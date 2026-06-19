# MedMe Health, Website

The redesigned MedMe Health marketing site, built with Astro 5. Two
regional homepages (United States and Canada) and ~60 supporting
sub-pages, with shared nav / footer / util-bar as Astro components
and long-form copy authored as Markdown Content Collections.

## Repo

Codebase lives at
**[github.com/andrewbaek-design/andrewbaek-design.github.io](https://github.com/andrewbaek-design/andrewbaek-design.github.io)**.
Public hosting at `medmehealth.com` continues to run on Webflow; this
repo is a design-direction reference handed to the marketing team to
port into Webflow via the Webflow MCP server.

## Quickstart

```sh
cd astro
npm install       # first time only
npm run dev       # http://localhost:4321
```

Visit `/us/`, `/ca/`, `/legal/privacy/`, `/us/about/`, etc. The root
`/` is a geo-aware redirect splash.

## Repository layout

```
.
├── CLAUDE.md                Project conventions, hard rules, design system
├── README.md                You are here
├── .gitignore               astro/dist, astro/node_modules, local artifacts
├── .github/workflows/       GitHub Actions deploy pipeline
└── astro/                   All source + Astro project
    ├── src/
    │   ├── pages/           File-based routes (us/, ca/, legal/, company/)
    │   ├── layouts/         BaseLayout.astro (US), BaseLayoutCa.astro (CA)
    │   ├── components/      NavUs, NavCa, FooterUs, FooterCa, UtilBarUs, …
    │   ├── content/         Markdown content collections (legal/, us/)
    │   └── content.config.ts   Zod schemas
    ├── public/assets/       brand.css, homepage-us.css, site.js, SVGs
    ├── astro.config.mjs
    └── package.json
```

## Deploy

`.github/workflows/pages.yml` runs on every push to `main`:

1. Install Node 20 + npm cache
2. `npm ci` in `astro/`
3. `npm run build` → `astro/dist/`
4. Upload artifact, deploy to GitHub Pages

Manual re-deploys are available from the Actions tab via
`workflow_dispatch`.

## Design

Brand identity follows the MedMe Brandguide v1.0:

| Token        | Hex       | Role                                       |
|--------------|-----------|--------------------------------------------|
| `--indigo`   | `#063E54` | Primary, most-used colour                  |
| `--seashell` | `#FAF9F5` | Warm off-white background (not pure white) |
| `--matcha`   | `#C3C430` | Secondary accent, use sparingly            |

Typography: Montserrat across the site. Variable weights 400-800.
Urbanist is loaded as a backup display face on legacy legal pages.

See [CLAUDE.md](CLAUDE.md) for the full conventions, hard rules, and
component / collection patterns.

## License

Internal. All rights reserved.
