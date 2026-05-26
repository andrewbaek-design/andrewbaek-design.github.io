# Build system

Static HTML mockup with a tiny template engine. Solves the
duplicate-nav problem: edit one partial, every page updates.

## What's in the box

```
medme-website-audit/
├── build.py                ← 110-line Python build script (stdlib only)
├── src/                    ← SOURCE templates — edit these
│   ├── us/                 (mirrors the published URL path)
│   │   ├── index.html
│   │   └── pricing.html, platform/, pharmacy/, ...
│   ├── ca/
│   ├── legal/, company/
│   └── login.html
├── partials/               ← Shared fragments — edit these
│   ├── nav-us.html, nav-ca.html
│   ├── util-bar-us.html, util-bar-ca.html
│   ├── footer-us.html, footer-ca.html
│   └── logo-medme.html
├── assets/                 ← Shared CSS + JS (NOT templated)
│   ├── brand.css
│   └── site.js
├── us/, ca/, legal/, …     ← OUTPUT directories — do not hand-edit
├── index.html              ← Region picker (root URL)
└── login.html              ← OUTPUT for /login
```

## Workflow

**To change the nav, util-bar, or footer:**

```sh
# Edit one of partials/nav-us.html, nav-ca.html, util-bar-{us,ca}, footer-{us,ca}
python3 build.py
```

**To change anything else on a page** (hero, content, CTAs, etc.):

```sh
# Edit src/<region>/<path>.html — same path the URL serves at
python3 build.py
```

**To verify nothing has drifted** (good for pre-commit / pre-publish):

```sh
python3 build.py --check    # exits 1 if any source change would alter output
```

## Template syntax

Inside `src/**/*.html` and `partials/*.html`:

| Syntax                       | What it does                                                   |
|------------------------------|----------------------------------------------------------------|
| `{{> partials/nav-us }}`     | Inline the contents of `partials/nav-us.html`                  |
| `{{ page.title }}`           | Substitute a variable from this template's frontmatter         |
| `{{# anything }}`            | Comment — stripped from the output                             |

Nested partials are supported — `partials/nav-us.html` includes
`{{> partials/logo-medme }}`, which is expanded recursively.

**Frontmatter** (optional, must be at the very top of a source template):

```
---
region: us
page.title: MedMe — United States Homepage
---
<!DOCTYPE html>
...
```

## URL conventions

- All internal links use **absolute paths starting with `/`** (e.g.
  `/us/pricing`, not `pricing.html`). The same partial can be included
  at any depth without breaking links.
- Internal links are **extensionless**: `/us/pricing`, not
  `/us/pricing.html`. Netlify auto-resolves to the matching `.html` file.
- The output structure mirrors `src/`: `src/us/pricing.html` builds to
  `us/pricing.html` and serves at `/us/pricing`.

## Conventions

* Partials shouldn't have a trailing newline — `build.py` strips one anyway
  so editor habits don't leak into the rendered HTML.
* The build is **idempotent**: running it twice produces the same output.
  Use `--check` in CI to fail if a partial change is unmerged.

## When to graduate

If the project grows beyond ~20 pages or you need:

* Page-level layouts (top + bottom shared, middle varies)
* Frontmatter-driven page lists (e.g. "all blog posts")
* Hot reload on save
* Minification, asset hashing, image optimization

…it's time to switch to **[Eleventy](https://www.11ty.dev/)**. Migration is
straightforward because the partial structure is already in place.

For now, `build.py` is enough.
