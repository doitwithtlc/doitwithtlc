# TLC search visibility review — November 9, 2026

## Confirmed findings and changes

Read both Search Console notices delivered to carmen@doitwithtlc.com on November 9. One concerns sitemap URLs; the other concerns page indexing. Neither email contains Google's affected-URL examples or counts. The exact report remains unverified without signed-in Search Console access.

Fetched all 65 production HTML page routes from the live domain: all returned HTTP 200. The homepage and four service pages currently allow indexing; none of the 65 responses had an X-Robots-Tag header. This establishes accessibility and directives, not actual Google index inclusion.

The previous 40-URL sitemap included `/bblo/community-impact/`, which has a `noindex,follow` directive, a canonical pointing to `/bblo/gallery/`, and an immediate HTML redirect there. Keep this intentional alias excluded; remove it from the sitemap. This is a confirmed conflict consistent with the warning, not proof it is Google's only reported URL.

Added three public destinations missing from the sitemap: `/bblo/events/`, `/bblo/field-trip-friday/`, and `/bblo/visit/`. The resulting sitemap contains 42 canonical, indexable URLs. Utility pages `/app/`, `/bblo/check-in/`, and `/share-your-experience/` remain outside the sitemap. Existing member-profile exclusions, review-page exclusions and home alias exclusions are preserved.

Added Service JSON-LD to the four service pages, using their existing descriptions, TLC's organization identity and existing Ocala/Marion County service area. This helps describe the services; it does not promise a special search result or a ranking increase.

Added `scripts/check-seo.py`. Run `python scripts/check-seo.py --write-sitemap` after production page changes; run without the flag to validate. It checks sitemap coverage, indexability and canonical consistency, main headings, descriptions, missing image alt attributes and local page/asset references. It excludes preview content and intentional utility destinations.

## Validation

- 65 live production routes: HTTP 200.
- Local public landing-page headings, descriptions, alt attributes and canonical sitemap checks: passed.
- Local internal page and referenced asset paths: no missing paths found. This does not test external forms, delivery or CRM automation.
- Existing page JSON-LD plus added Service objects: parsed successfully.
- Corrected the Field Trip Friday description, which duplicated the BBLO gallery description. No duplicate titles or descriptions remain among checked indexable production HTML pages.
- Main service pages already use Ocala in their titles and descriptions. Their content is served in HTML.
- Main service-page images mostly use lazy loading. No performance score or Core Web Vitals result has been measured in this review.

## Verified referring pages

Actual website hyperlinks to TLC were verified on:

- https://members.ocalacep.com/directory/Details/the-liaison-companies-4812458
- https://members.belleviewcep.com/directory/Details/the-liaison-companies-4812458
- https://cervlaw.com/2026/10/31/ocala-business-attorney-chris-cervellera-presents-7-contract-blind-spots-with-local-bilingual-business-leaders-of-ocala-bblo/

The two CEP pages are powered by the same directory platform; do not treat them as evidence of two independent memberships or independent editorial endorsements. Public discovery is a sample, not a complete backlink inventory or link-quality score. No external listings were changed and no outreach was sent.

## Search visibility and remaining verification

Public search returned TLC's homepage for a brand-representation/Ocala query, but one retrieved search snapshot still displayed the earlier homepage copy. Public search is not a reliable Google ranking baseline and does not establish a #1 position. Record actual Google queries, clicks, impressions, CTR and average positions in Search Console before claiming improvement.

Required next checks inside the correct Search Console property:

1. Export affected examples for both noindex notices and compare Google's last crawl with current live directives.
2. Inspect the homepage, brand representation, event management, bilingual outreach and branding/content URLs. Confirm index status and Google's selected canonical; request indexing only where appropriate.
3. Submit or refresh `https://doitwithtlc.com/sitemap.xml` and confirm successful processing. Validate fixes for unintended exclusions; intentional excluded aliases need not be indexed.
4. Review Links, Manual Actions, Security Issues, Crawl Stats and Core Web Vitals. The emailed warning does not supply these reports.
5. Establish query/page performance baselines for brand representation, corporate/community event management and bilingual outreach in Ocala/Marion County. Segment branded and service searches.

Additional work not claimed complete: mobile visual/accessibility audit, measured speed/Core Web Vitals, external-link availability sweep, real inquiry submission/delivery tests, Google Business Profile accuracy/categories and Maps visibility, and a full backlink inventory. The calendar's event listings load through JavaScript; consider build-time HTML listings from the approved event ledger in a separate calendar change, preserving its current filters and approved data.

## Recommended business priorities

Resolve Google-reported indexing exceptions first. Then strengthen service-specific local proof with approved client stories and actual event portfolios, connect relevant portfolio pages to the service they demonstrate, and request contextual links from genuine partners where TLC's work is featured. Keep external directory descriptions aligned with TLC's current visibility and relationship-building services. Do not buy bulk backlinks or create thin location pages.

No guarantee of indexing dates or first-place placement. Google notes that recrawling can take days to weeks, and sitemap submission is a discovery hint rather than a ranking guarantee.

Official references:

- https://developers.google.com/search/docs/crawling-indexing/block-indexing
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
