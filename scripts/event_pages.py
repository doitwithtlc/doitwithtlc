"""Build stable, crawlable event detail pages from the public calendar ledger."""
import json
import re
from datetime import datetime, time
from html import escape
from pathlib import Path
from urllib.parse import urlencode, urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://doitwithtlc.com'
TZ = ZoneInfo('America/New_York')
KINDS = {'business':'Business Event','workshop':'Workshop','training':'Training','vendor':'Vendor Event','fundraiser':'Fundraiser','culture':'Cultural Event','family':'Family Event','bblo':'BBLO Event','community':'Community Event','field-trip':'Field Trip Friday'}
MARKER = '<!-- generated-community-event -->'


def event_route(event):
    identity = event['id']
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', identity):
        raise ValueError('Unsafe event ID: ' + identity)
    return '/community-events/' + identity + '/'


def parse(value):
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError('Event timestamps require a timezone')
    return result.astimezone(TZ)


def cutoff(event):
    if event.get('end'):
        return parse(event['end'])
    # Missing end times remain unknown. Keep the listing through its local day.
    return datetime.combine(parse(event['start']).date(), time.max, TZ)


def state(event, now):
    if event.get('status') in ('cancelled', 'canceled'):
        return 'Event cancelled'
    if event.get('status') == 'postponed':
        return 'Event postponed'
    if now > cutoff(event):
        return 'Event has ended'
    return ('Happening now' if event.get('end') else 'Scheduled today') if now >= parse(event['start']) else 'Upcoming event'


def external(value):
    return value if urlsplit(value or '').scheme in ('http', 'https') else ''


# Only unambiguous public admission labels are eligible for a zero-price offer.
FREE_ADMISSION = {
    'free', 'free and open to the public', 'free admission and parking',
    'free; rsvp required', 'free admission; vendor fees apply',
    'free admission; optional chalk activity $5',
}


def event_offer(event):
    # A displayed, verified all-in ticket price can be supplied explicitly.
    verified = event.get('verified_offer')
    if isinstance(verified, dict):
        price = verified.get('price')
        url = external(verified.get('url'))
        if type(price) in (int, float) and 0 <= price < float('inf') and url and verified.get('currency') == 'USD':
            return {'@type':'Offer','price':price,'priceCurrency':'USD','url':url}
    if (event.get('cost') or '').strip().casefold() not in FREE_ADMISSION:
        return None
    offer = {'@type':'Offer','price':0,'priceCurrency':'USD'}
    # An event information page is not necessarily a ticket checkout.
    # The existing source is a ticket URL only for explicit Eventbrite event links.
    url = external(event.get('url'))
    if url and urlsplit(url).hostname in ('www.eventbrite.com','eventbrite.com') and urlsplit(url).path.startswith('/e/'):
        offer['url'] = url
    return offer


def event_performers(event):
    result = []
    for performer in event.get('performers') or []:
        if not isinstance(performer, dict):
            continue
        name = performer.get('name')
        kind = performer.get('type')
        if isinstance(name, str) and name.strip() and kind in ('Person','PerformingGroup'):
            result.append({'@type':kind,'name':name.strip()})
    return result


def button(href, label, secondary=False):
    return '<a class="button'+(' secondary' if secondary else '')+'" href="'+escape(href, quote=True)+'">'+escape(label)+'</a>'


def display_date(value, pattern):
    # Numeric components avoid platform-specific %-d and %-I directives.
    pattern = pattern.replace('%-d', str(value.day)).replace('%-I', str(value.hour % 12 or 12))
    return value.strftime(pattern)


def date_label(event):
    start = parse(event['start'])
    if event.get('date_only'):
        return display_date(start, '%A, %B %-d, %Y') + ' · Deadline date; closing hour not announced'
    label = display_date(start, '%A, %B %-d, %Y · %-I:%M %p')
    if event.get('end'):
        end = parse(event['end'])
        label += '–' + display_date(end, '%-I:%M %p' if start.date() == end.date() else '%B %-d, %Y · %-I:%M %p')
    if event.get('end_time_pending'):
        label += ' · End time: TBD'
    return label + ' ' + start.strftime('%Z')


def card(event):
    return '<article class="event-related-card"><p class="eyebrow">'+escape(KINDS.get(event.get('category'),'Community Event'))+'</p><h3><a href="'+event_route(event)+'">'+escape(event['title'])+'</a></h3><p>'+escape(date_label(event))+'</p><p>'+escape(event.get('location',''))+'</p></article>'



def share_controls(event):
    url = ORIGIN + event_route(event)
    text = '\n'.join(filter(None, [event['title'], date_label(event), event.get('location'), event.get('address')]))
    body = text + '\n' + url
    links = [('Text', 'sms:?'+urlencode({'body':body})),
             ('Email', 'mailto:?'+urlencode({'subject':event['title'],'body':body})),
             ('WhatsApp', 'https://wa.me/?'+urlencode({'text':body})),
             ('Facebook', 'https://www.facebook.com/sharer/sharer.php?'+urlencode({'u':url})),
             ('LinkedIn', 'https://www.linkedin.com/sharing/share-offsite/?'+urlencode({'url':url})),
             ('X', 'https://twitter.com/intent/tweet?'+urlencode({'text':text,'url':url}))]
    html = '<details class="event-share" data-event-share data-share-title="'+escape(event['title'],quote=True)+'" data-share-text="'+escape(text,quote=True)+'" data-share-url="'+escape(url,quote=True)+'"><summary>Share event</summary><div class="event-share-options">'
    html += '<button type="button" data-share-native hidden>Share with an app</button>'
    for label, href in links:
        html += '<a href="'+escape(href,quote=True)+'"'+(' data-share-sms' if label=='Text' else '')+(' target="_blank" rel="noopener noreferrer"' if href.startswith('https:') else '')+'>'+label+'</a>'
    html += '<button type="button" data-share-copy hidden>Copy link</button></div><p class="event-share-url"><a href="'+url+'">'+escape(url)+'</a></p><p class="event-share-status" role="status"></p></details>'
    return html


def page_shell(template, title, description, route, content, schemas, image=''):
    # Reuse the live site's navigation and footer, not a second design system.
    head = template.split('</head>',1)[0] + '</head>'
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', lambda _: '<title>'+escape(title)+'</title>', head)
    head = re.sub(r'<meta (?:name|property)="(?:description|og:title|og:description|og:url|og:image|twitter:title|twitter:description|twitter:image)"[^>]*>', '', head)
    head = re.sub(r'<link rel="canonical"[^>]*>', '', head)
    head = re.sub(r'<script src="/assets/bblo/events.js[^>]*></script>', '', head)
    image = image or ORIGIN+'/assets/brand/tlc-white.webp'
    metadata = {'description':description,'og:title':title,'og:description':description,'og:url':ORIGIN+route,'og:image':image}
    tags = ''.join('<meta '+('name' if key=='description' else 'property')+'="'+key+'" content="'+escape(value,quote=True)+'">' for key,value in metadata.items())
    tags += '<link rel="canonical" href="'+ORIGIN+route+'"><link rel="stylesheet" href="/assets/bblo/event-pages.css?v=20261109"><script src="/assets/bblo/event-pages.js?v=20261109" defer></script>'
    tags += ''.join('<script type="application/ld+json">'+json.dumps(s,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>' for s in schemas)
    head = head.replace('</head>',tags+'</head>')
    header = template.split('<body>',1)[1].split('</header>',1)[0]+'</header>'
    footer = '<footer>'+template.split('<footer>',1)[1]
    return head+'<body>'+header+MARKER+content+footer


def build(root=ROOT, now=None):
    now = now or datetime.now(TZ)
    template = (root/'events/index.html').read_text()
    raw = json.loads((root/'data/bblo-events.json').read_text())['events']
    events = [e for e in raw if e.get('published') is True]
    ids = [e['id'] for e in events]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate calendar IDs')
    for event in events:
        event_route(event)
        if event.get('end') and parse(event['end']) <= parse(event['start']):
            raise ValueError('End must follow start: '+event['id'])
        parse(event['start'])
    events.sort(key=lambda e: parse(e['start']))
    upcoming = [e for e in events if state(e,now) in ('Upcoming event','Happening now','Scheduled today')]
    generated = []
    for event in events:
        route = event_route(event)
        label = state(event,now)
        title = event['title']+' | TLC Community Calendar'
        description = (event.get('description') or event['title'])[:240]
        source = external(event.get('url')) or external(event.get('source_url'))
        host = external(event.get('organizer_url'))
        organizer = event.get('organizer') or ('BBLO' if event.get('category') in ('bblo','field-trip') else '')
        image = event.get('image') or event.get('flyer_url') or ''
        if image.startswith('/'):
            image = ORIGIN+image
        image = external(image)
        location = ' · '.join(event.get(k,'') for k in ('location','address') if event.get(k))
        body = '<main id="main" class="event-detail" data-event-id="'+event['id']+'"><section class="hero event-detail-hero"><div class="wrap"><nav class="event-breadcrumb" aria-label="Breadcrumb"><a href="/events/">Community Calendar</a><span aria-hidden="true"> / </span><span>Event details</span></nav><p class="eyebrow">'+escape(KINDS.get(event.get('category'),'Community Event'))+'</p><h1>'+escape(event['title'])+'</h1><p class="event-state" data-event-state role="status">'+label+'</p><p class="lead"><time datetime="'+escape(event['start'])+'">'+escape(date_label(event))+'</time></p><p>'+escape(location)+'</p></div></section>'
        body += '<section><div class="wrap event-detail-grid"><div><h2>About this event</h2><p class="event-description">'+escape(event.get('description',''))+'</p>'
        if organizer:
            body += '<p><strong>Hosted by:</strong> '+escape(organizer)+'</p>'
        if event.get('cost'):
            body += '<p><strong>Cost:</strong> '+escape(event['cost'])+'</p>'
        offer = event_offer(event)
        performers = event_performers(event)
        if event.get('verified_offer') and offer and 'url' in offer:
            body += '<p><strong>Verified admission:</strong> '+escape('$'+format(offer['price'], '.2f')+' USD')+' · '+button(offer['url'],'Ticket information',True)+'</p>'
        if performers:
            body += '<p><strong>Performers:</strong> '+escape(', '.join(p['name'] for p in performers))+'</p>'
        if label in ('Upcoming event','Happening now','Scheduled today'):
            unconfirmed = []
            if not organizer or not host: unconfirmed.append('organizer contact or website')
            if not offer: unconfirmed.append('ticket price or registration details')
            elif 'url' not in offer: unconfirmed.append('registration details, if required')
            if not image: unconfirmed.append('official event flyer')
            if not performers: unconfirmed.append('program or performer details, if applicable')
            if unconfirmed:
                body += '<p class="note"><strong>Details to confirm:</strong> '+escape('; '.join(unconfirmed))+'. Please confirm any missing information directly with the event coordinator or host before attending.</p>'
        if event.get('opportunities'):
            body += '<p><strong>Opportunities:</strong> '+escape(event['opportunities'])+'</p>'
        if not event.get('end') and not event.get('date_only'):
            body += '<p class="note">An end time has not been announced. Confirm with the organizer.</p>'
        if event.get('address_pending'):
            body += '<p class="note">The exact street address needs confirmation. Contact the organizer before traveling.</p>'
        body += '<div class="actions">'
        if source and not urlsplit(source).path.lower().endswith(('.jpg','.jpeg','.png','.webp','.pdf')):
            body += button(source,event.get('cta') or 'Official event information',True)
        if host and host != source:
            body += button(host,'Visit the organizer',True)
        if location and not event.get('address_pending') and not event.get('virtual') and not re.match(r'^(online|virtual|zoom|webinar)$',event.get('location',''),re.I):
            body += button('https://www.google.com/maps/dir/?'+urlencode({'api':1,'destination':event.get('address') or event['location']}),'Get directions',True)
        if event.get('end'):
            compact = lambda d: parse(d).astimezone(ZoneInfo('UTC')).strftime('%Y%m%dT%H%M%SZ')
            calendar = 'https://calendar.google.com/calendar/render?'+urlencode({'action':'TEMPLATE','text':event['title'],'dates':compact(event['start'])+'/'+compact(event['end']),'details':event.get('description','')+' '+ORIGIN+route,'location':location})
            body += '<span data-upcoming-action'+(' hidden' if label not in ('Upcoming event','Happening now','Scheduled today') else '')+'>'+button(calendar,'Add to my calendar',True)+'</span>'
        body += '</div>'+share_controls(event)+'<p class="note">Listed by The Liaison Companies LLC. Hosting and registration remain with the named organizer unless TLC or BBLO is identified as the host. Confirm the organizer’s latest details before attending.</p></div>'
        if image:
            body += '<figure class="event-detail-flyer"><a href="'+escape(image,quote=True)+'"><img src="'+escape(image,quote=True)+'" alt="'+escape(event.get('imageAlt') or event['title']+' flyer',quote=True)+'" decoding="async"></a><figcaption>Open the full event flyer.</figcaption></figure>'
        else:
            body += '<aside class="event-detail-aside"><p class="eyebrow">Find your next connection</p><h2>More happening<br>around Ocala.</h2><p>Explore business events, community gatherings and BBLO activities in one calendar.</p>'+button('/events/','Explore the calendar')+'</aside>'
        body += '</div></section>'
        related = sorted([e for e in upcoming if e['id'] != event['id']],key=lambda e:(e.get('category') != event.get('category'),parse(e['start'])))[:3]
        body += '<section class="event-related"><div class="wrap"><p class="eyebrow">Keep exploring</p><h2>Find your next event.</h2><div class="event-related-grid" data-related-events>'+''.join(card(e) for e in related)+'</div><div class="actions">'+button('/events/','All upcoming events')+button('/community-events/archive/','Past events',True)+'</div></div></section>'
        body += '<section><div class="wrap event-detail-connections"><div><p class="eyebrow">Business visibility in Ocala</p><h2>Get to know the businesses<br>behind the connections.</h2><p>Explore BBLO members, plan a Friday visit or see how TLC represents businesses in the community.</p></div><div class="actions">'+button('/bblo/members/','Meet local businesses',True)+button('/bblo/visit/','Visit BBLO',True)+button('/services/brand-representation/','Explore TLC representation',True)+'</div></div></section></main>'
        schemas = [{'@context':'https://schema.org','@type':'WebPage','name':title,'url':ORIGIN+route,'description':description,'publisher':{'@type':'Organization','name':'The Liaison Companies LLC','url':ORIGIN+'/'}}]
        # Event markup is limited to future/current physical listings with a confirmed address.
        if label in ('Upcoming event','Happening now','Scheduled today') and not event.get('virtual') and event.get('address') and not event.get('address_pending'):
            schema = {'@context':'https://schema.org','@type':'Event','name':event['title'],'url':ORIGIN+route,'startDate':event['start'],'description':event.get('description',''),'eventStatus':'https://schema.org/EventScheduled','location':{'@type':'Place','name':event['location'],'address':event['address']}}
            if event.get('end'): schema['endDate']=event['end']
            if image: schema['image']=[image]
            if organizer:
                schema['organizer']={'@type':'Organization','name':organizer}
                if host: schema['organizer']['url']=host
            if offer: schema['offers']=offer
            if performers: schema['performer']=performers
            schemas.append(schema)
        path=root/route.lstrip('/')/'index.html'
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(page_shell(template,title,description,route,body,schemas,image))
        generated.append(str(path.relative_to(root)))
    past = [e for e in reversed(events) if state(e,now) not in ('Upcoming event','Happening now','Scheduled today')]
    content = '<main id="main" class="event-detail"><section class="hero"><div class="wrap"><p class="eyebrow">Community Calendar archive</p><h1>Past events.<br>More connections ahead.</h1><p class="lead">Browse previous calendar listings and find what is coming up next.</p>'+button('/events/','See upcoming events')+'</div></section><section><div class="wrap"><h2>Previous listings</h2><div class="event-related-grid" data-event-archive>'+''.join(card(e) for e in past)+'</div></div></section></main>'
    path=root/'community-events/archive/index.html';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(page_shell(template,'Past Ocala Community & Business Events | TLC','Browse previous Ocala business and community event listings, then discover upcoming events on the TLC community calendar.','/community-events/archive/',content,[]))
    generated.append(str(path.relative_to(root)))
    # Withdrawn listings become non-indexable notices; no broken URLs or stale promotion.
    current=set(generated)
    folder=root/'community-events'
    for path in folder.glob('*/index.html'):
        relative=str(path.relative_to(root))
        if relative not in current and MARKER in path.read_text():
            notice='<main id="main"><section class="hero"><div class="wrap"><h1>This listing is no longer available.</h1>'+button('/events/','Find upcoming events')+'</div></section></main>'
            html=page_shell(template,'Listing unavailable | TLC','This event listing is no longer published. Find upcoming community events on the TLC calendar.','/'+str(path.parent.relative_to(root))+'/',notice,[])
            html=html.replace('content="index,follow,max-image-preview:large"','content="noindex,follow"')
            path.write_text(html)
            generated.append(relative)
    return generated
