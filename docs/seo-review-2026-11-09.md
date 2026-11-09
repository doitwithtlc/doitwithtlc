# TLC search visibility review — November 9, 2026

## Confirmed Search Console findings

Signed in as carmen@doitwithtlc.com to the https://doitwithtlc.com/ property. Read Page Indexing, Performance, Links, Manual Actions, Security Issues, Core Web Vitals, Sitemaps and individual service URL inspections.

The indexing report (last updated November 5) shows 32 indexed pages and 10 excluded pages:

| Reason | Count | Finding |
| --- | ---: | --- |
| Excluded by noindex | 1 | `/bblo/community-impact/`, the intentional alias of `/bblo/gallery/`. This is the exact URL behind the emailed warning. |
| Discovered, currently not indexed | 8 | Nonprofit spotlights, Rancho Reposo, three dated BBLO galleries, BBLO Support, Client Stories, and the Unstoppable gallery. Google had not crawled these examples. |
| Crawled, currently not indexed | 1 | `/bblo/events/`, last crawled November 7. Google did not supply a specific content-quality diagnosis. |

The homepage and all four service pages individually show “URL is on Google / Page is indexed.” Brand Representation also shows crawl allowed, indexing allowed, successful smartphone Googlebot fetch, and matching Google-selected canonical. Index inclusion is not a ranking guarantee.

A subsequent individual inspection also shows the calendar is indexed, with a successful smartphone Googlebot fetch and a matching selected canonical. Use that current URL result over the older summary exclusion. It reports a temporary sitemap-processing error in its historical discovery details; the freshly submitted sitemap separately processed successfully with 42 URLs. Do not attribute this index inclusion to today's changes without evidence.

Google reports no manual actions and no security issues.

## Changes published

- Removed `/bblo/community-impact/` from the sitemap while retaining its intentional noindex redirect to BBLO in Action.
- Added the public calendar, visitor page and Field Trip Friday page to the sitemap. It now contains 42 canonical, indexable URLs.
- Submitted the refreshed sitemap in Search Console. Google confirmed successful submission and processing on November 9, with 42 discovered pages.
- Added Service JSON-LD to all four service pages using existing service descriptions and the existing Ocala/Marion County service area.
- Replaced the duplicate Field Trip Friday meta description with a distinct, relevant description.
- Added `scripts/check-seo.py` to validate production discovery and internal paths. Use `--write-sitemap` when refreshing the sitemap after page changes.
- Added readable, collapsible event agendas to the calendar and Field Trip Friday pages, generated from the same approved public ledger. This exposes event names, dates, locations and organizer links in HTML without requiring JavaScript. It preserves the interactive calendar and includes explicit wording that past dates are also shown. This addresses a crawlability opportunity; it does not establish why Google previously declined indexing.
- Added `scripts/build-event-agenda.py` and integrated agenda refresh into the existing event-approval publication workflow. Direct calendar-data edits should also run this script before publication.
- Declared the existing, unchanged `/logo.jpg` as the homepage favicon. Google's historical 404 examples were repeated requests for `/favicon.ico`; no broken content URLs appeared among those examples. The old default ICO URL is not redirected by GitHub Pages.

Intentional member-profile, preview, review-page and home-alias exclusions remain. Utility pages are outside the sitemap. The noindex report may continue showing the intentional alias; its exclusion does not require making it indexable.

## Performance baseline

Search Console Web search, August 8–November 7, 2026:

| Metric | Value |
| --- | ---: |
| Clicks | 13 |
| Impressions | 215 |
| CTR | 6% |
| Average position | 11.2 |

This is the property-wide average across different searches, not the rank for TLC's services. The visible query table contains 18 reportable queries; query totals do not account for all activity. Examples include BBLO (13 impressions, average position 5.0), “schedule a marketing consultation ocala” (8 impressions, 72.2), and “b2c marketing strategies ocala” (4 impressions, 58.5). These last two terms describe observed searches, not recommended TLC positioning. No visible evidence supports claiming #1 for the core services.

## Backlinks

Search Console reports 14 external links, all to the homepage, from six domains:

| Linking domain | Linking pages |
| --- | ---: |
| bniamerica.com | 4 |
| bniwcf.com | 3 |
| cervlaw.com | 3 |
| ocalacep.com | 2 |
| boldladiesdirectory.com | 1 |
| linkedin.com | 1 |

These are Google's reported links, not an exhaustive internet backlink inventory. The BNI domains can reflect related network placements. Public hyperlinks also verified at:

- https://members.ocalacep.com/directory/Details/the-liaison-companies-4812458
- https://members.belleviewcep.com/directory/Details/the-liaison-companies-4812458
- https://cervlaw.com/2026/10/31/ocala-business-attorney-chris-cervellera-presents-7-contract-blind-spots-with-local-bilingual-business-leaders-of-ocala-bblo/

The two CEP listings share a directory platform. Do not interpret them as evidence of separate memberships. No external listings were changed, no disavow submitted and no outreach sent. Search Console's internal-links report currently says zero/no data; local checks confirm the website has working internal links, so this is not proof those links are absent.

## Speed, accessibility and technical verification

Homepage PageSpeed Insights report:
https://pagespeed.web.dev/analysis/https-doitwithtlc-com/894ys1afdy?utm_source=search_console&form_factor=mobile&hl=en

| Lab test | Mobile | Desktop |
| --- | ---: | ---: |
| Performance | 100 | 100 |
| Accessibility | 100 | 100 |
| Best Practices | 100 | 100 |
| Basic SEO | 100 | 100 |
| Largest Contentful Paint | 1.5 seconds | 0.4 seconds |
| Total Blocking Time | 0 ms | 0 ms |
| Cumulative Layout Shift | 0.008 | 0.001 |

These are automated homepage lab results, not a full-site accessibility certification, service-page speed score or ranking assessment. Search Console lacks enough real-user Chrome UX data for mobile and desktop Core Web Vitals. PageSpeed still identifies optional opportunities around image delivery, render-blocking requests and cache lifetimes.

An additional Event Management mobile lab test also scored 100 in all four categories, with LCP 1.5 seconds, TBT 0 ms and CLS 0.029:
https://pagespeed.web.dev/analysis/https-doitwithtlc-com-services-event-management/4q3ooxywt7?hl=en&form_factor=mobile

Search Console reports a valid robots.txt and no host problems in the previous 90 days. Crawl statistics (updated November 6) show 276 requests and an average response time of 101 ms. This is Google's crawl response metric, not a visitor page-load time.

All 65 production HTML routes responded HTTP 200 in the live audit. No X-Robots-Tag response headers were found. Local checks passed for sitemap/indexability/canonical consistency, public landing-page main headings, descriptions, alt attributes and internal page/asset paths. JSON-LD parsed successfully; the duplicate description was corrected. Calendar generator checks cover escaping, unpublished-entry exclusion and repeatable output. External CRM form delivery was not tested.

## Business priorities

1. Let Google recrawl the accepted sitemap and improved calendar; inspect the calendar and request indexing after publication.
2. Build search relevance for brand representation, corporate/community event management and bilingual outreach in Ocala and Marion County. Use real project evidence and approved client stories instead of stretching TLC into generic marketing-agency terms.
3. Earn contextual links to the relevant service and portfolio pages from genuine partner coverage. Current reported backlinks all point to the homepage. Do not buy bulk backlinks or build thin location pages.
4. Review Google Business Profile separately for categories, website URL, service area, reviews and Maps discovery. That account was not opened or changed during this Search Console audit.
5. Verify actual inquiry delivery and conversion tracking separately; search visibility alone does not establish qualified leads.

There is no guaranteed indexing date or #1 placement. Recrawling can take days to weeks. No recurring monitoring automation was created.

Official references:

- https://developers.google.com/search/docs/crawling-indexing/block-indexing
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
