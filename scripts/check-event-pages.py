"""Check lifecycle, withdrawal, stable URLs and generated event SEO contracts."""
import copy
import json
import tempfile
from datetime import datetime
from pathlib import Path
from event_pages import ROOT, TZ, build, cutoff, event_route, state, event_offer, event_performers

now=datetime(2026,11,10,16,0,tzinfo=TZ)
e={'id':'fixture-event','title':'Example <event>','published':True,'category':'business','start':'2026-11-10T16:30:00-05:00','end':'2026-11-10T18:30:00-05:00','location':'Venue','address':'123 Main St, Ocala, FL','description':'A real description & details','organizer':'Example host'}
assert event_offer(e) is None
assert event_offer(dict(e,cost='Free for partners')) is None
assert event_offer(dict(e,cost='$20 + fees')) is None
assert event_offer(dict(e,cost='Free')) == {'@type':'Offer','price':0,'priceCurrency':'USD'}
assert event_offer(dict(e,cost='Free',url='https://www.eventbrite.com/e/example-tickets-123'))['url'].endswith('123')
assert event_offer(dict(e,verified_offer={'price':25,'currency':'USD','url':'https://example.com/tickets'}))['price']==25
assert event_performers(e)==[]
assert event_performers(dict(e,performers=[{'type':'Person','name':'Actual artist'},{'type':'Organization','name':'Sponsor'}]))==[{'@type':'Person','name':'Actual artist'}]
assert state(e,now)=='Upcoming event'
assert state(e,datetime(2026,11,10,17,0,tzinfo=TZ))=='Happening now'
assert state(e,datetime(2026,11,10,19,0,tzinfo=TZ))=='Event has ended'
assert state(dict(e,status='cancelled'),now)=='Event cancelled'
assert state(dict(e,status='postponed'),now)=='Event postponed'
unknown={k:v for k,v in e.items() if k!='end'}
assert state(unknown,datetime(2026,11,10,23,59,tzinfo=TZ))=='Scheduled today'
assert state(unknown,datetime(2026,11,11,0,0,tzinfo=TZ))=='Event has ended'
assert cutoff(dict(unknown,start='2027-03-14T01:00:00-05:00')).utcoffset().total_seconds()==-14400
with tempfile.TemporaryDirectory() as folder:
 root=Path(folder)
 (root/'events').mkdir(parents=True)
 (root/'events/index.html').write_text((ROOT/'events/index.html').read_text())
 (root/'data').mkdir()
 events=[e,dict(e,id='unpublished-draft',published=False,start='',end='')]
 ledger=root/'data/bblo-events.json'
 ledger.write_text(json.dumps({'events':events}))
 paths=build(root,now)
 assert not (root/'community-events/unpublished-draft/index.html').exists()
 file=root/(event_route(e).lstrip('/')+'index.html')
 first=file.read_bytes()
 build(root,now)
 assert file.read_bytes()==first,'Build must be idempotent'
 text=file.read_text()
 assert 'Example &lt;event&gt;' in text and '<h1>Example <event>' not in text
 assert '"@type":"Event"' in text
 assert '"offers"' not in text and '"performer"' not in text
 assert 'Please confirm any missing information directly with the event coordinator or host' in text
 assert 'ticket price or registration details' in text and 'official event flyer' in text
 events[0]=dict(e,cost='Free',organizer_url='https://example.com/', image='https://example.com/image.png',performers=[{'type':'Person','name':'Actual artist'}])
 ledger.write_text(json.dumps({'events':events}))
 build(root,now)
 text=file.read_text()
 assert '"offers":{"@type":"Offer","price":0,"priceCurrency":"USD"}' in text
 assert '"performer":[{"@type":"Person","name":"Actual artist"}]' in text and 'Actual artist' in text
 assert '"url":"https://example.com/"' in text and '"image":["https://example.com/image.png"]' in text
 # Same ID survives rescheduling; no old URL breaks.
 events[0]=dict(e,start='2026-11-12T16:30:00-05:00',end='2026-11-12T18:30:00-05:00')
 ledger.write_text(json.dumps({'events':events}))
 build(root,now)
 assert file.exists() and 'November 12' in file.read_text()
 # Past events remain searchable but lose active offers/actions and Event markup.
 build(root,datetime(2026,11,13,0,0,tzinfo=TZ))
 text=file.read_text()
 assert 'Event has ended' in text and 'data-upcoming-action hidden' in text
 assert '"@type":"Event"' not in text
 assert 'Details to confirm:' not in text
 assert '/community-events/fixture-event/' in (root/'community-events/archive/index.html').read_text()
 # Unpublishing removes content from the archive and sitemap eligibility.
 events[0]['published']=False
 ledger.write_text(json.dumps({'events':events}))
 build(root,now)
 assert 'noindex,follow' in file.read_text()
 assert 'Example &lt;event&gt;' not in file.read_text()

published=[e for e in json.loads((ROOT/'data/bblo-events.json').read_text())['events'] if e.get('published') is True]
for e in published:
 path=ROOT/event_route(e).lstrip('/')/'index.html'
 text=path.read_text()
 assert text.count('<h1>')==1
 assert 'href="https://doitwithtlc.com'+event_route(e)+'"' in text
 assert 'View event details' not in text or '<main' in text
print(f'{len(published)} event pages: stable URLs, indexing, lifecycle, DST, no invented end times, drafts, withdrawal and repeat builds passed.')
