# Community calendar and event pages

`data/bblo-events.json` is the shared public event source. Keep event IDs stable when editing titles, dates, venues or organizer links. The calendar and detail pages use the same records; do not edit generated detail HTML.

Run `python scripts/build-event-agenda.py` after an approved calendar change. This generates `/community-events/{id}/`, `/community-events/archive/`, the crawlable calendar agendas and `sitemap.xml`. Only `published: true` entries receive public event pages. Unknown times, organizers, addresses and prices stay unknown. A draft with missing times stays unpublished.

Calendar cards link to the local detail page. The detail page links to the recorded official event source and, when supplied and verified, `organizer_url`. External links do not create backlinks to TLC. TLC is the publisher; the recorded organizer remains the host.

Known end times control expiry. An event without a confirmed end time stays listed through its local America/New_York date; the displayed end time remains unknown. Event pages update the status and related events every minute while open. The upcoming carousel removes ended/cancelled/postponed dates. Past dates remain in calendar history and the archive. Past detail URLs stay live, visibly marked ended and linked to upcoming events; no stale calendar-add action. Date changes keep the same URL. For a new recurring occurrence, create a new ID/date; do not reuse last week's date.

`Refresh calendar event pages` rebuilds and deploys after source changes and daily at 06:15 UTC (normally 1:15 AM EST / 2:15 AM EDT; GitHub may delay scheduled runs). It commits generated updates and refreshes the sitemap. The existing approval workflow runs the same builder before deployment. Live browser status provides immediate expiry between daily builds. Unpublished prior listings become noindex notices and leave the sitemap.

This automation does not monitor social pages for cancellations, import external form submissions or invent future recurring dates. Those changes still require source verification and calendar approval. The existing event submission form/approval workflow is unchanged.

Validate with `python scripts/check-event-pages.py` and `python scripts/check-seo.py`. Event structured data is included only for current/upcoming physical events with a confirmed address; missing optional fields are not fabricated. Search engines determine indexing and placement.
