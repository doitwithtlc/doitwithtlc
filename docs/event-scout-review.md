# Event Scout review
Review drafts at https://github.com/doitwithtlc/doitwithtlc/issues?q=is%3Aissue+is%3Aopen+%22%5BEvent+Scout%5D%22

Only the doitwithtlc owner account can approve or reject.
Read the source, review the details, and edit the issue's JSON block if needed.
Comment exactly /approve to publish or /reject to decline.
Missing/conflicting dates or times must be corrected before approval.
The approval workflow validates the event, saves it to data/bblo-events.json, and deploys GitHub Pages.
The draft is closed only after deployment succeeds. If deployment fails, the issue remains open and the workflow run contains the error.
All issues in this repository are public. Include only public event information. Never put submitter names, personal contact details, CRM information, passwords, or tokens in a draft.
The existing LeadConnector submission form remains in place and separate; it does not automatically enter this queue.

## Draft format
Issue title: [Event Scout] Event name — YYYY-MM-DD

Include a readable summary, verification notes, the source and checked date, and this block:
<!-- event-scout-json -->
```json
{
  "title": "",
  "category": "community",
  "start": "",
  "end": "",
  "location": "",
  "address": "",
  "virtual": false,
  "description": "",
  "organizer": "",
  "organizer_url": "",
  "cost": "",
  "url": "",
  "source_url": "",
  "flyer_url": "",
  "opportunities": "",
  "verification_status": "needs_information"
}
```
Use ISO 8601 timestamps with a correct America/New_York UTC offset. Never fabricate an end time.
Allowed categories: business, workshop, training, vendor, fundraiser, culture, family, community, bblo, field-trip.
Set verification_status to verified only after source verification resolves essential details.
Unknown optional text fields remain empty.
Review existing open and closed issues and published events before creating drafts. Rejected and published events should not be resubmitted unchanged.
For updates to a published event, use the original issue so its scout-ID remains stable; reopen, edit and request fresh approval. Do not silently change the calendar.
