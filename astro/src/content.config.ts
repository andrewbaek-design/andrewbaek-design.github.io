import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Legal pages (privacy, hipaa, pipeda, terms). Schema mirrors the
// existing sidecar .md frontmatter, minus the `page.` prefix that
// the legacy build.py uses for variable namespacing. CTA fields
// are optional: privacy and terms have no hero CTAs; hipaa and
// pipeda do (BAA request, Privacy Officer contact).
const legal = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/legal' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    kicker: z.string(),
    headline: z.string(),
    lede: z.string(),
    cta_primary_label: z.string().optional(),
    cta_primary_href: z.string().optional(),
    cta_secondary_label: z.string().optional(),
    cta_secondary_href: z.string().optional(),
  }),
});

// US marketing pages that benefit from sidecar copy (currently: about).
// Looser schema than `legal` because each marketing page has its own
// section-by-section frontmatter shape; every field optional except meta.
const usPages = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/us' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    hero_kicker: z.string().optional(),
    hero_headline: z.string().optional(),
    hero_lede: z.string().optional(),
    hero_cta_label: z.string().optional(),
    hero_cta_href: z.string().optional(),
    mission_kicker: z.string().optional(),
    mission_headline: z.string().optional(),
    journey_kicker: z.string().optional(),
    journey_headline: z.string().optional(),
    journey_lead: z.string().optional(),
    belief_kicker: z.string().optional(),
    belief_headline: z.string().optional(),
    belief_lead: z.string().optional(),
    backed_by_kicker: z.string().optional(),
    backed_by_headline: z.string().optional(),
    backed_by_lead: z.string().optional(),
    closing_kicker: z.string().optional(),
    closing_headline: z.string().optional(),
    closing_lead: z.string().optional(),
    closing_cta_label: z.string().optional(),
    closing_cta_href: z.string().optional(),
  }),
});

export const collections = { legal, usPages };
