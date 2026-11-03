# TLC offer and weekly guide
## Offer
The previous draft described tasks before the customer recognized the need. Lead with unused memberships, a strong business that is not top-of-mind, and an event idea without anyone managing the work. Explain the role, process and deliverables after the problem.
Core engagements remain fractional brand representation and corporate/community event management. Bilingual outreach and branding/content support that work and keep their explanatory pages. No claim to replace marketing agencies.
Do not turn relationship access into guaranteed referrals, appointments, sales or exclusive membership privileges. No invented testimonials, metrics or attendance.
Representation prices/counts remain prior decisions; verify availability, expense handling and definitions before launch. Events remain custom-priced.
## Theme
Fine route lines, gold magnifying-glass illustration, field-note panel, numbered assignments, light map grid, follow-the-clues guide and restrained Put TLC on the case CTA.
Official logos and real photos still need to be placed. Never fabricate people or event proof. Do not rename official services just for the theme.
## Weekly guide
Stable route: /where-is-carmen/
Heading: Where in Marion County Is Carmen Today?
Curated BUSINESS opportunities, not an exhaustive county calendar or a claim Carmen attends every event.
Required: official title, timezone-aware date/time, organizer, venue/address, cost as published or honest omission, official source, verification timestamp, registration/info URL, unique business takeaway.
Confirmed appearances require separate evidence; private attendanceEvidence must never be rendered in the public page.
Initial preview has no event fixtures and explicitly says listings have not been loaded.
Use ONE verified ledger for social and website. Preserve Sunday-Saturday range of the existing weekly task.
After social publication, record the actual post URL, mark the reviewed ledger approved, run scripts/publish-weekly-guide.ps1 -DataPath <approved-ledger-path>, review compiled HTML, and commit on the draft branch. Script does not deploy.
Until the redesign launches, keep website updates in draft. Later add dated archives if useful; clearly date old guides and never label them fresh current listings.
The Sunday task prepares the website handoff alongside social assets. It cannot independently detect social publication; no automatic post-to-website integration is configured.
## Ledger contract
data/weekly-guide.json is an empty draft. Never fill it with assumed recurring events.
Top level: status approved; weekStart yyyy-MM-dd Sunday; weekEnd yyyy-MM-dd Saturday; socialPublishedUrl actual HTTPS post URL; updatedAt ISO; events array.
Each event: id, name, organizer, start ISO with offset, optional end, venue, address, county Marion, state FL, category, whyItMatters, sourceUrl official HTTPS, optional registrationUrl HTTPS, optional costText, verificationStatus verified, verifiedAt ISO, carmenAttending boolean, attendanceEvidence when true.
Categories: Networking, Workshop, Ribbon cutting, Grand opening, Professional event.
Full ledger validation precedes page mutation. All rendered user text/URLs are HTML-escaped. Keep private working ledgers outside public GitHub; commit only public-safe content and compiled HTML.
