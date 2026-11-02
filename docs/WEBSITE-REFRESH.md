# TLC website refresh — November 2, 2026
Status: implementation draft, not launch-ready. Keep this branch separate from main until the asset and integration work below passes.

## Findings from the live site and source
- Current homepage narrows TLC to Hispanic market entry and omits corporate/community event management.
- Founders Partnership, SmartPlug, Market Expansion and $500K+ qualification do not reflect the current brief.
- handleSubmit() only hides the form and shows success. No request, email, database, or CRM write occurs. This is a confirmed lead-delivery defect.
- Dark inline card backgrounds with dark text, pale service bullets on white cards, tiny uppercase body copy and low-opacity labels undermine readability.
- No responsive breakpoint in the old CSS. Navigation lacks service-page discovery.
- A Drive hotlink supplies the logo and hides it on error. Use an inspected, official local asset.
- Existing schema publishes a street address and office hours not verified for this project. Draft omits both.
- No dedicated BBLO route, service pages, sitemap, or robots file exists in the original repository.
- Website source is a static HTML GitHub repository with CNAME. GitHub Pages is indicated by repository metadata; verify Pages configuration and current DNS before deployment.
- No analytics or Search Console access inspected. No claim is made about current rankings, traffic, conversions or Core Web Vitals.

## Draft implementation
Eight HTML pages: home, representation, events, bilingual outreach, branding/content, BBLO, Carmen, contact. Server-readable HTML, descriptive titles, canonical URLs, Open Graph metadata, Organization schema, accessible navigation/skip link, responsive shared stylesheet, sitemap and robots.
Email and telephone links replace the non-delivering form. Email links are clearly labeled; no success event is simulated.
Representation: Starter $1,500; Growth $3,000; Platinum $5,500; six-month minimum. Included quantities follow the supplied prior decisions. Review exact package definitions and current availability before public launch.
Events/content/bilingual support are custom-scoped. No invented prices.
BBLO draft uses supplied meeting arrangements and membership terms. Confirm fees, meeting venue, exact street address, upcoming exceptions and payment/application URLs before launch.
Draft intentionally contains no invented client results, stock meetings, fake testimonials, fabricated partner badges or AI people.

## Design completion
Palette: navy #0B1F3A, gold #C9A227, cream #F5F1E8, white and black.
Direction: established, editorial, premium, people-centered. Large legible headings, concise sans-serif body text, real photography, strong service hierarchy, restrained gold.
Replace text-only masthead with the inspected official TLC logo, unchanged. Add official BBLO logo unchanged.
Required real assets: Carmen hero portrait; brand representation in action; corporate/community event wide shot; BBLO meeting wide shot; Carmen biography portrait; supporting relationship/event photos.
Search already located Social Media folder and possible BBLO images. Search results alone are not image approval. Download, inspect, select, crop without identity changes, optimize and commit assets before launch. Do not use Drive access links as public image hosting. Do not commit private Drive URLs or account metadata to public code.
Add meaningful alt text, explicit dimensions, modern compressed formats, hero loading priority and lazy loading below the fold.
Add two approved work examples, ideally Unstoppable and a representation engagement, describing Carmen/TLC's actual scope. Any testimonial or metrics must be verified and approved for public display.
Browser QA: desktop, 390px mobile, keyboard, contrast, overflow, all CTAs, official logos and image cropping. This has not yet been done.

## C-Suiteware architecture
Keep the primary website in this GitHub repository. Keep CRM, forms, reminders and agreed workflows in C-Suiteware.
Public C-Suiteware site advertises website builder, workflows, messaging and basic API. It uses LeadConnector assets; this suggests a HighLevel-related stack, but account capabilities and exact configuration are NOT verified.
Official HighLevel docs support Sites > Blogs, authors, metadata, canonical URLs, scheduled publishing and automatic blog sitemaps. Treat those instructions as conditional until confirmed inside Carmen's C-Suiteware account.
Preferred editorial home: /blog/ on the primary domain if a supported integration can serve real, indexable pages there. DNS alone cannot delegate /blog/ to a different provider. GitHub Pages alone does not provide reverse-proxy routing.
Practical C-Suiteware-hosted alternative: insights.doitwithtlc.com with matching TLC header, footer and service links. Confirm C-Suiteware's actual domain requirements first. Do not move the root or www away from the current site accidentally.
Do not use iframe-only blog embedding as the primary content architecture. Do not duplicate each full article on both hosts.
Do not promise that a subfolder or subdomain by itself yields a ranking advantage.

### Blog setup after account verification
1. Confirm Blogs availability, domain permissions, existing automations and timezone.
2. Create The Visibility Debrief. Author: Carmen Garcia Tirado, linked to /about/.
3. Categories: Ocala Business Visibility; Corporate & Community Events; Local Business Intelligence; Bilingual Business Connections; BBLO.
4. Match branding and navigation. Connect selected host, verify HTTPS, actual URL pattern and canonical behavior.
5. Publish one original, reviewed post with image, title, description, author, date, helpful links and one related service CTA.
6. Verify generated sitemap URL, indexing permission, mobile readability and canonical tag. Submit root and blog sitemaps in Search Console. Do not invent a sitemap URL.
7. Embed verified C-Suiteware forms on relevant website pages with a non-embedded fallback contact path. Define actual consent handling based on communication channels.
8. On successful submission: create/update contact, record source and service interest, notify Carmen, acknowledge inquiry and create follow-up task. Notify/acknowledge only through configured consented channels. Do not automatically add all inquiries to promotional subscriptions.
9. Separate workflows for representation, event inquiries, BBLO visits, BBLO membership and newsletter opt-in.
10. Test each path end to end: submission, CRM record, source, notification, acknowledgement, duplicate handling, failure and task creation. Success displays only after actual successful capture.
11. Obtain and review appropriate privacy/consent disclosures for actual tools before enabling analytics, embedded forms and messaging.

## Search and content plan
Goal: qualified organic inquiries and BBLO visitors in the actual service area. Not permanent first place.
Initial query hypotheses, not measured search-volume findings:
- corporate event planner Ocala
- corporate event management Ocala
- client appreciation event planning Ocala
- business representation Ocala
- business networking Ocala
- bilingual business networking Ocala
Map representation queries to representation page, event queries to event page, networking/BBLO queries to BBLO. The phrase fractional brand representation explains the offer but may not match how every buyer searches.
Use Search Console impressions/query data to refine wording after publication. Avoid doorway pages for towns without distinct service evidence.
Maintain Google Business Profile with accurate category, service area, contact details, real photos and genuine client reviews. Do not publish a private address as an office or create an unverified separate BBLO listing.
Earn relevant editorial links from legitimate partner profiles, event coverage and organizer pages; confirm permission/eligibility.
Technical launch checks: HTTPS, domain redirect behavior, unique titles/descriptions/canonicals, sitemap URLs return 200, internal links, mobile performance, accessible forms, social sharing preview and structured data validity. Add truthful Service and Breadcrumb schema as useful; never invented ratings.

### First eight editorial briefs (recommended)
1. What Is Fractional Brand Representation? An Ocala Business Owner's Guide — representation CTA.
2. Your Chamber Membership Is Paid. Who Is Building the Relationships? — representation CTA; explain membership rules differ.
3. Planning a Client Appreciation Event in Ocala: What to Decide First — event inquiry CTA.
4. Business Networking in Ocala: How to Choose Where to Spend Your Time — BBLO visitor CTA; verify organizer details.
5. Bilingual Business Connections in Marion County: You Don't Have to Speak Spanish to Participate — BBLO CTA.
6. What Happens After a Business Event? A Practical Follow-Up Plan — representation CTA.
7. Corporate Event Planning vs. Event-Day Coordination: Define the Work Before You Book — event CTA.
8. A TLC Event Debrief — original approved Unstoppable photos and actual responsibilities, no invented outcomes.
Cadence recommendation: two substantial evergreen articles monthly; a weekly local-business roundup only when verified and useful. Archive dated opportunities accurately and keep evergreen guides updated. Repurpose original insights into Reels, Stories and opted-in email.
Do not mass-produce generic AI local articles or promise rankings from publishing frequency.

## Measurement
Before launch capture available Search Console and analytics baseline.
Track qualified inquiries by service, consultation bookings, phone/email clicks (as clicks, not completed leads), BBLO visitor registrations/actual visits, newsletter consent, organic landing pages and relevant non-brand searches.
Recommended first 90 days: launch/service conversion checks; indexing/query review; improve pages earning relevant impressions; publish original evidence; assess inquiry quality. Targets depend on baseline and capacity, not invented traffic forecasts.

## Research sources
Live/source: https://doitwithtlc.com/ and https://github.com/doitwithtlc/doitwithtlc
CROWD (representation clarity, transparent scope): https://crowdcompany.co/services/business-promotion
BizzAngels (plain-language event representation and evidence presentation; their performance claims not independently verified): https://bizzangels.com/
Dillon Media Group (dedicated local event service page, event types and FAQs): https://dillonmediagroup.com/event-management
Blessed Magnolia (corporate event positioning, process and proof): https://blessedmagnolia.com/corporate-events
C-Suiteware public capabilities: https://csuiteware.com/
Conditional HighLevel setup: https://help.gohighlevel.com/support/solutions/articles/48001220286-getting-started-with-blogs-and-blog-posts
Scheduling: https://help.gohighlevel.com/support/solutions/articles/48001227671
Sitemap: https://help.gohighlevel.com/support/solutions/articles/155000002453-how-to-add-blog-sitemap-
Google SEO: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
Helpful content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
Local search: https://support.google.com/business/answer/7091

## Launch gate
Do not merge this draft until real official assets are placed, current commercial/BBLO details are checked, browser QA passes, and the selected lead-capture path is tested. C-Suiteware blog domain/CRM integrations remain unconfigured. Never describe draft pricing and code as a completed live deployment.
