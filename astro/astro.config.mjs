import { defineConfig } from 'astro/config';
import customHeadingId from 'remark-custom-heading-id';

// Site config.
//
// build.format: 'directory' emits e.g. /us/about/index.html so the URL is
// /us/about/. trailingSlash: 'ignore' lets the dev server accept both
// /us/about and /us/about/ — the legacy site's internal links don't have
// trailing slashes (e.g. <a href="/us/pharmacy/independents">) and we
// shouldn't have to rewrite them all.
//
// Markdown: enable {#anchor} custom-id syntax in headings so the existing
// legacy sidecar .md files keep their hand-chosen IDs
// (## 1. Scope {#scope} → <h2 id="scope">). Without this Astro auto-slugs
// heading text and the TOC anchors break.
export default defineConfig({
  site: 'https://medmehealth.com',
  output: 'static',
  build: {
    format: 'directory',
  },
  trailingSlash: 'ignore',
  markdown: {
    remarkPlugins: [customHeadingId],
  },
});
