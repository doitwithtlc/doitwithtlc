# BBLO public profiles and optional advertising

## Included membership benefit

Every listed member business has a public profile and a directory listing. TLC, BBLO, Media Minds and MJ Photography appear first in that exact order; remaining businesses follow alphabetically. BBLO's program card links to its existing About page and is not counted as an additional paid member. The profile includes a business description, specialties, known service areas, the named representative, existing approved media, business links and a route to request an introduction. Members can submit corrections, original logos and approved photos through `/bblo/profile-update/`.

The update form prepares an email for the member to review and send. It does not automatically send, update the website, create a CRM record or upload images. BBLO reviews the email and attachments before publication. Do not describe this as a self-service editing portal or automatic CRM integration.

Public profile data comes from `data/bblo-members.json` for existing public identity/media/social links, with reviewed enrichment in `data/bblo-public-profiles.json`. Private phone/email fields from the membership data are never copied automatically. Public contacts must be explicitly sourced in the enrichment file. Missing service areas and photos are omitted. Legacy Insurance's old Ocala Insurance Group URL is withheld pending correction.

## Advertising inventory and fulfilment

No advertiser is active. No advertising price has been published or charged. Website descriptions invite an inquiry and require written confirmation of placement, creative, price, dates, rotation and destination.

| Product | Placement | Scope boundary |
| --- | --- | --- |
| Featured Directory | Separate Sponsored cards after the four priority entries, before remaining alphabetical listings | Up to three simultaneous cards. A category-specific booking must match the member's category. Search results remain relevant. |
| Homepage Feature | Sponsored section directly below the TLC homepage hero | One simultaneous card. Placement does not replace the hero or change standard member listings. |
| Sponsored Business Story | Separate, labeled editorial-style advertising article | A proposed service, not an automated article generator. Requires an approved brief, original media, agreed creation fee, publishing term and destination links. |

Social content, newsletter inclusion, event sponsorship and exclusive category advertising are not automatically included with these products. Define deliverables and verify channel availability before adding them to an agreement. Do not sell an impression quota, lead quota or Google rank. Website clicks/impressions are not yet connected to a verified analytics reporting pipeline; do not promise those reports until measurement is implemented and tested.

## Activate a booked placement

Add an entry to `data/bblo-advertising.json` only after Carmen approves the booking. Required keys are `location` (`directory` or `homepage`), `member_slug`, `status` (`approved`), `label` (`Sponsored`), `start` and `end` (ISO timestamps with timezone offsets). Optional `group` must exactly match the member's business group. This file contains no personal, payment or contract information.

Run `python3 scripts/build-public-members.py`, `python3 scripts/check-public-members.py`, and `python3 scripts/check-seo.py --write-sitemap`. Review the resulting section, then publish using the normal repository deployment. The builder enforces capacity, dates and disclosure. Browser logic hides expired cards on page load. Standard listings are unaffected. If data is changed directly, a rebuild/deployment is required; there is no scheduler or advertising checkout.

The standard profile is part of paid membership, so commercial links from profiles carry `rel="sponsored noopener"`. Additional paid placements are visibly labeled Sponsored. These attributes do not prevent a member profile itself from being indexed. Relevant links and useful profiles support discovery; no ranking credit is sold.

## After changes

Run the public-member builder after updating approved member facts. It regenerates public profiles, directory, membership benefit copy, advertising information, and the email-based profile update page. Run the SEO checker to regenerate the sitemap. The production-promotion builder calls the public-member builder so a future promotion cannot silently revert profiles to noindex.

Use the correct business website and Google profile information when supplied. Do not copy a home address, personal mobile, private email, credentials, license claims, customer results or reviews into a public profile without appropriate verification and publication permission.
