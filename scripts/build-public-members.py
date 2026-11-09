"""Publish public BBLO profiles from approved directory facts and sourced enrichment.

Never copy private member phone/email fields into public profiles. Public contact
fields must be explicitly present in bblo-public-profiles.json with source URLs.
"""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
from urllib.parse import quote, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://doitwithtlc.com'
VERSION = '20261109-public-members'

def esc(value): return escape(str(value), quote=True)
def safe_url(value):
    return value if value and (value.startswith('/') and not value.startswith('//') or urlsplit(value).scheme in ('http', 'https')) else ''
def email_link(subject, body=''):
    return 'mailto:carmen@doitwithtlc.com?subject=' + quote(subject) + '&body=' + quote(body)
def section(body, cls=''):
    return '<section class="' + cls + '"><div class="wrap">' + body + '</div></section>'
def action(url, label, external=False, cls='button'):
    if not (url.startswith('mailto:') or url.startswith('tel:') or safe_url(url)): return ''
    extra = ' target="_blank" rel="sponsored noopener"' if external else ''
    return '<a class="' + cls + '" href="' + esc(url) + '"' + extra + '>' + esc(label) + '</a>'
def profile_url(m): return '/bblo/members/' + m['slug'] + '/'

def build(root=ROOT):
    members = json.loads((root / 'data/bblo-members.json').read_text())
    public = json.loads((root / 'data/bblo-public-profiles.json').read_text())
    ads = json.loads((root / 'data/bblo-advertising.json').read_text())['placements']
    board={m['member_slug']:m['role'] for m in json.loads((root/'data/bblo-board.json').read_text())['members']}
    for m in members:
        if m['slug'] not in public: raise ValueError('Missing public profile: ' + m['slug'])
    people = sorted([{**m, **public[m['slug']]} for m in members], key=lambda m: m['company'].casefold())
    by_slug = {m['slug']:m for m in people}
    # Reuse current production navigation, typography, shared assets and footer.
    template = (root / 'bblo/members/mj-photography/index.html').read_text()
    template = re.sub(r'<script type="application/ld\+json">.*?</script>', '', template, flags=re.S)
    template = re.sub(r'<link[^>]+href="/assets/bblo/members-public.css[^>]+>', '', template)
    template = re.sub(r'<script[^>]+src="/assets/bblo/members-public.js[^>]*></script>', '', template)
    template = re.sub(r'<link rel="icon"[^>]*>', '', template)
    def page(route, title, description, body, schema=None, image=None):
        text = re.sub(r'<title>.*?</title>', lambda _: '<title>' + esc(title) + '</title>', template)
        robots='noindex,follow' if route=='/bblo/profile-update/' else 'index,follow,max-image-preview:large'
        text = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="'+robots+'">', text)
        for name, value in [('description', description), ('og:title',title), ('og:description', description), ('og:url', ORIGIN+route)]:
            text = re.sub(r'(<meta (?:name|property)="'+name+r'" content=")[^"]*(">)', lambda m: m[1]+esc(value)+m[2], text)
        text = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="'+ORIGIN+route+'">',text)
        if image:
            text = re.sub(r'(<meta property="og:image" content=")[^"]*(">)', lambda m:m[1]+ORIGIN+'/assets/'+esc(image)+m[2],text)
        text = re.sub(r'<main\b[^>]*>.*?</main>', lambda _:'<main id="main" class="bblo-public">'+body+'</main>',text,flags=re.S)
        text = re.sub(r'<script[^>]+src="/assets/bblo/bblo.js[^>]*></script>', '', text)
        crumbs = {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'TLC','item':ORIGIN+'/'},{'@type':'ListItem','position':2,'name':'BBLO member businesses','item':ORIGIN+'/bblo/members/'},{'@type':'ListItem','position':3,'name':title.split(' | ')[0],'item':ORIGIN+route}]}
        structured = [crumbs] + ([schema] if schema else [])
        head = '<link rel="icon" type="image/jpeg" href="/logo.jpg"><link rel="stylesheet" href="/assets/bblo/members-public.css?v='+VERSION+'"><script src="/assets/bblo/members-public.js?v='+VERSION+'" defer></script>'
        head += ''.join('<script type="application/ld+json">'+json.dumps(s,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>' for s in structured)
        text = text.replace('</head>',head+'</head>')
        dest = root / route.strip('/') / 'index.html'
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(text)

    def paid_cards(location):
        cards=[]
        now=datetime.now(timezone.utc)
        for ad in ads:
            if ad.get('location')!=location: continue
            if ad.get('status')!='approved' or not ad.get('label')=='Sponsored': raise ValueError('Advertising requires approval and disclosure')
            if ad.get('member_slug') not in by_slug: raise ValueError('Unknown advertiser')
            start=datetime.fromisoformat(ad['start']);end=datetime.fromisoformat(ad['end'])
            if start.tzinfo is None or end.tzinfo is None or end<=start:raise ValueError('Advertising needs valid dates with timezone offsets')
            if not start<=now<end:continue
            m=by_slug[ad['member_slug']]
            if ad.get('group') and ad['group']!=m['group']:raise ValueError('Advertising group must match the member category')
            cards.append('<article class="card paid-member" data-ad-start="'+esc(ad['start'])+'" data-ad-end="'+esc(ad['end'])+'" data-member="'+esc(m['company']+' '+m['name']+' '+' '.join(m['services']))+'" data-group="'+esc(m['group'])+'"><p class="member-label">Sponsored</p><h3>'+esc(m['company'])+'</h3><p>'+esc(m['category'])+'</p>'+action(profile_url(m),'Explore '+m['company'])+'</article>')
        if not cards:return ''
        if len(cards)>(3 if location=='directory' else 1):raise ValueError('Advertising capacity exceeded for '+location)
        note='All members remain available in the directory below.' if location=='directory' else '<a href="/bblo/members/">Explore all BBLO member businesses.</a>'
        return section('<p class="eyebrow">Paid advertising</p><h2>Featured member businesses</h2><div class="grid three">'+''.join(cards)+'</div><p class="note">Sponsored placement is advertising. '+note+'</p>','sponsored-members')

    for m in people:
        route=profile_url(m)
        contact=[]
        # Intentionally use only sourced public contact fields, never raw directory contacts.
        extra=public[m['slug']]
        if (extra.get('phone') or extra.get('email')) and not extra.get('sources'):raise ValueError('Public contacts need a source')
        if extra.get('phone'):
            digits=re.sub(r'\D','',extra['phone']);contact.append(action('tel:+1'+digits,extra['phone'],'', 'button secondary'))
        if extra.get('email'):contact.append(action('mailto:'+extra['email'],'Email '+m['company'],cls='button secondary'))
        if m.get('website'):contact.append(action(m['website'],'Visit '+m['company'],True))
        for key,label in [('facebook','Facebook'),('instagram','Instagram')]:
            if m.get(key):contact.append(action(m[key],m['company']+' on '+label,True,'text-link'))
        connect=action(email_link('BBLO introduction: '+m['company'],'Please connect me with '+m['name']+' at '+m['company']+'.\n\nMy name:\nMy business:\nWhat I need help with:\nBest way to reach me:\n'),'Request a BBLO introduction',cls='button secondary')
        photo=''
        if m.get('photo'):
            photo='<figure class="member-public-photo"><img src="/assets/'+esc(m['photo'])+'" alt="'+esc(m['name']+' · '+m['company'])+'" loading="lazy" decoding="async">'+('<figcaption>'+esc(m['photo_credit'])+'</figcaption>' if m.get('photo_credit') else '')+'</figure>'
        title=m['company']+' | '+(' · '.join(m['services'][:2]))+' | BBLO'
        desc=m['company']+': '+', '.join(m['services'])+'. '+('Serving '+', '.join(m['areas'])+'. ' if m['areas'] else '')+'Meet '+m['name']+' through BBLO and explore business links.'
        hero=section('<a class="text-link" href="/bblo/members/">← All member businesses</a><p class="eyebrow">BBLO member business · '+esc(m['group'])+'</p><h1>'+esc(m['company'])+'</h1><p class="lead">'+esc(' · '.join(m['services'][:3]))+'</p><p class="member-representative">Your BBLO connection: <strong>'+esc(m['name'])+'</strong></p>','hero')
        if m['slug'] in board:
            hero=hero.replace('</div></section>','<p>BBLO leadership: '+esc(board[m['slug']])+' · <a href="/bblo/board/">Meet the board →</a></p></div></section>')
        body=hero+section('<div class="member-public-layout"><div><h2>Get to know '+esc(m['company'])+'</h2><p class="member-intro">'+esc(m['summary'])+'</p><h2>Services &amp; specialties</h2><ul class="service-tags">'+''.join('<li>'+esc(s)+'</li>' for s in m['services'])+'</ul>'+('<h2>Service area</h2><p>'+esc(' · '.join(m['areas']))+'</p>' if m['areas'] else '')+('<h2>Languages</h2><p>'+esc(' · '.join(m['languages']))+'</p>' if m.get('languages') else '')+'<p class="note">Contact the business to confirm current services, availability and service area.</p></div><aside class="member-connect"><p class="eyebrow">Make the connection</p>'+photo+'<h2>Connect with '+esc(m['name'])+'</h2><div class="member-contact-actions">'+''.join(contact)+connect+'</div><p class="note">Introduction requests open your email app. Review and send the message to TLC.</p></aside></div>')
        if m.get('activities'):
            body+=section('<p class="eyebrow">In the BBLO community</p><h2>Member activity</h2>'+''.join('<article class="card"><h3><a href="'+esc(a['url'])+'">'+esc(a['title'])+'</a></h3><p>'+esc(a['description'])+'</p></article>' for a in m['activities']))
        body+=section('<p class="eyebrow">Your public business profile</p><h2>Part of your paid BBLO membership.</h2><p>Your standard business page and directory listing are included with membership. Optional advertising placements are arranged separately and labeled Sponsored.</p><div class="actions">'+action('/bblo/profile-update/?member='+quote(m['slug']),'Update this business profile',cls='button secondary')+action('/bblo/advertise/','Explore advertising options',cls='text-link')+'</div>','map-section')
        entity={'@type':'Organization','@id':ORIGIN+route+'#business','name':m['company'],'description':m['summary'],'memberOf':{'@type':'Organization','name':'Bilingual Business Leaders of Ocala','url':ORIGIN+'/bblo/'},'sameAs':[m[k] for k in ('website','facebook','instagram') if m.get(k) and safe_url(m[k])]}
        if m.get('website'):entity['url']=m['website']
        if extra.get('phone'):entity['telephone']=extra['phone']
        if extra.get('email'):entity['email']=extra['email']
        if m.get('areas'):entity['areaServed']=m['areas']
        schema={'@context':'https://schema.org','@type':'ProfilePage','url':ORIGIN+route,'name':m['company']+' — BBLO member profile','mainEntity':entity}
        page(route,title,desc,body,schema,m.get('photo'))

    groups=sorted(set(m['group'] for m in people))
    cards=[]
    for m in people:
        search=' '.join([m['company'],m['name'],m['category'],m['group'],*m['services'],*m['areas'],*m.get('languages',[])])
        cards.append('<article class="card member-public-card" data-member="'+esc(search)+'" data-group="'+esc(m['group'])+'"><p class="member-label">'+esc(m['group'])+'</p><h2><a href="'+profile_url(m)+'">'+esc(m['company'])+'</a></h2><p class="member-person">'+esc(m['name'])+'</p><p>'+esc(' · '.join(m['services']))+'</p>'+('<p class="note">'+esc(' · '.join(m['areas']))+'</p>' if m['areas'] else '')+action(profile_url(m),'Explore business profile →',cls='text-link')+'</article>')
    body=section('<p class="eyebrow">BBLO · A TLC community &amp; visibility program</p><h1>Find your next<br><em>local business connection.</em></h1><p class="lead">Explore the people and services in Bilingual Business Leaders of Ocala. Find a business, learn what it does, and connect through its public profile.</p><div class="actions">'+action('/bblo/benefits/','See membership benefits')+action('/bblo/advertise/','Advertising opportunities',cls='button secondary')+'</div>','hero')
    body+=section('<div class="member-filters"><div><label for="member-search">Business, person, service or area</label><input id="member-search" type="search" placeholder="Try roofing, headshots, plumbing…"></div><div><label for="member-category">Business category</label><select id="member-category"><option value="">All categories</option>'+''.join('<option>'+esc(g)+'</option>' for g in groups)+'</select></div></div><p id="member-count" role="status" aria-live="polite">'+str(len(people))+' businesses</p>'+paid_cards('directory')+'<h2>Member business directory</h2><p class="note">Standard listings are alphabetical. Featured advertising, when available, appears separately and is labeled Sponsored.</p><div class="grid three member-directory">'+''.join(cards)+'</div><p id="member-empty" hidden>No matching business. Try another service or clear the category filter.</p><noscript><p>All member businesses are listed below; browser search can help you find a service.</p></noscript>')
    body+=section('<h2>Membership keeps your business in the picture.</h2><p>A public business profile and standard directory listing are included with paid BBLO membership. Member information is reviewed before publication; a listing does not certify licenses or guarantee results.</p><div class="actions">'+action('/bblo/profile-update/','Send a profile update')+action('/bblo/advertise/','Ask about extra visibility',cls='button secondary')+'</div>','map-section')
    schema={'@context':'https://schema.org','@type':'ItemList','name':'BBLO member business directory','itemListElement':[{'@type':'ListItem','position':i+1,'name':m['company'],'url':ORIGIN+profile_url(m)} for i,m in enumerate(people)]}
    page('/bblo/members/','BBLO Member Business Directory | Ocala & Marion County | TLC','Find BBLO member businesses by service, category or name. Explore public business profiles, company websites and local connections through TLC.',body,schema)

    update=section('<p class="eyebrow">Included with paid BBLO membership</p><h1>Your business.<br><em>Accurately represented.</em></h1><p class="lead">Send the details you want on your public BBLO profile. We review updates before publishing.</p><p>Complete this form to prepare an email. Review the draft, attach original photos or your unchanged logo, then send it from your email app.</p>','hero')
    update+=section('<form id="member-profile-update" class="member-update-form"><div class="grid two"><label>Your name<input name="contact_name" autocomplete="name" required></label><label>Your contact email<input name="contact_email" type="email" autocomplete="email" required></label></div><p class="note">These two fields are for follow-up. Public contact details are requested separately below.</p><label>Member business<select name="member_slug" required><option value="">Choose your business</option>'+''.join('<option value="'+esc(m['slug'])+'">'+esc(m['company'])+'</option>' for m in people)+'</select></label><label>Public business name<input name="public_name"></label><label>What does your business do?<textarea name="description" rows="5" placeholder="Your services, who you help, and what customers should know."></textarea></label><label>Services &amp; specialties<textarea name="services" rows="3"></textarea></label><div class="grid two"><label>Service areas<input name="service_areas"></label><label>Languages offered<input name="languages"></label><label>Public business phone<input name="public_phone" type="tel"></label><label>Public business email<input name="public_email" type="email"></label><label>Business website<input name="website" type="url"></label><label>Public Google Business Profile link<input name="google_profile" type="url"></label><label>Facebook page<input name="facebook" type="url"></label><label>Instagram page<input name="instagram" type="url"></label></div><label>Anything else we should know?<textarea name="notes" rows="3"></textarea></label><label class="member-consent"><input name="publish_permission" type="checkbox" required> I authorize BBLO to publish the public business information I provide. I have permission to share any logo or photos I attach.</label><p>Only submit information intended for public business use. Your private member records are separate.</p><button class="button" type="submit">Prepare my profile update</button><p id="profile-email-status" role="status" aria-live="polite"></p><div id="profile-email-preview" hidden><h2>Review your update</h2><pre id="profile-email-text"></pre><a id="profile-email-send" class="button">Open email draft to TLC</a><p>If your email app does not open, copy the text and email carmen@doitwithtlc.com. Attach your original logo and approved images in that email. Your profile changes after BBLO reviews the update.</p></div></form>')
    page('/bblo/profile-update/','Update Your BBLO Business Profile | TLC','Send approved public business information, services and links for your included BBLO member profile.',update)

    advertising=section('<p class="eyebrow">Optional advertising · TLC &amp; BBLO</p><h1>Give your business<br><em>an extra place to be seen.</em></h1><p class="lead">Your standard BBLO business profile is included with paid membership. Advertising adds a separate, clearly labeled placement for an agreed period.</p>','hero')
    offers=[('Featured directory placement','A Sponsored business card above the standard member directory, linked to your public profile. Category relevance, display dates and rotation are agreed before booking.'),('Homepage business feature','A dedicated Sponsored placement on the TLC homepage, connecting visitors with your member profile or agreed business destination.'),('Sponsored business story','A separate, labeled business feature built from your approved information and original images, with links to your profile and business website.')]
    advertising+=section('<h2>Explore additional visibility</h2><div class="grid three">'+''.join('<article class="card"><p class="member-label">Optional advertising</p><h3>'+a+'</h3><p>'+b+'</p></article>' for a,b in offers)+'</div><h2>Know exactly what you are booking.</h2><p>We confirm the placement, dates, rotation, creative, destination link, price and responsibilities in writing. Availability is confirmed individually. Advertising does not change alphabetical standard listings or promise a Google position, visitor count, inquiries or sales.</p><p>Paid placements are labeled Sponsored and commercial outbound links are identified appropriately for search engines.</p><div class="actions">'+action(email_link('BBLO advertising inquiry','My business:\nPlacement of interest:\nPreferred dates:\nDestination website:\nBest way to reach me:\n'),'Ask about placement availability')+action('/bblo/members/','Explore member businesses',cls='button secondary')+'</div><p class="note">This button opens an email draft for you to review and send. Placement and payment are confirmed separately.</p>')
    page('/bblo/advertise/','BBLO Advertising & Featured Business Placements | TLC','Explore optional featured directory placements, homepage business features and sponsored stories alongside your included BBLO membership profile.',advertising)

    # Keep the promise explicit where members compare membership options.
    benefit=root/'bblo/benefits/index.html'
    text=benefit.read_text()
    start='<!-- included-member-profile:start -->';end='<!-- included-member-profile:end -->'
    included=start+section('<p class="eyebrow">Included with paid membership</p><h2>A public profile.<br>A place for your business to be found.</h2><p>Your BBLO membership includes a dedicated public business page, a standard directory listing, services and specialties, approved business links, and the member photos or logo you provide. Public profile updates are reviewed by BBLO.</p><p>Profiles are made eligible for search indexing; inclusion and ranking are determined by the search engine. Extra advertising placements are optional and arranged separately.</p><div class="actions">'+action('/bblo/members/','Explore the directory')+action('/bblo/profile-update/','Update your profile',cls='button secondary')+action('/bblo/advertise/','Optional advertising',cls='text-link')+'</div>')+end
    if start in text:text=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:included,text,flags=re.S)
    else:text=text.replace('</main>',included+'</main>')
    benefit.write_text(text)
    # Add an entry from the existing partner page without rebuilding its navigation.
    partners=root/'bblo/partners/index.html';text=partners.read_text()
    if 'href="/bblo/advertise/"' not in text:
        text=text.replace('</main>',section('<h2>Your member profile is included. Extra placement is optional.</h2><p>Explore directory advertising, homepage features and sponsored business stories.</p>'+action('/bblo/advertise/','Explore advertising opportunities'))+'</main>')
    partners.write_text(text)
    # A homepage slot only renders after an approved, dated placement exists.
    home=root/'index.html';text=home.read_text();start='<!-- member-home-ad:start -->';end='<!-- member-home-ad:end -->'
    home_cards=paid_cards('homepage')
    block=start+home_cards+end
    text=re.sub(re.escape(start)+r'.*?'+re.escape(end),'',text,flags=re.S)
    text,count=re.subn(r'(<main\b[^>]*>.*?<section\b[^>]*>.*?</section>)',lambda match:match[1]+block,text,count=1,flags=re.S)
    if count!=1:raise ValueError('Homepage hero insertion point missing')
    text=re.sub(r'<link[^>]+href="/assets/bblo/members-public.css[^>]+>', '', text)
    text=re.sub(r'<script[^>]+src="/assets/bblo/members-public.js[^>]*></script>', '', text)
    if home_cards:
        text=text.replace('</head>','<link rel="stylesheet" href="/assets/bblo/members-public.css?v='+VERSION+'"><script src="/assets/bblo/members-public.js?v='+VERSION+'" defer></script></head>')
    home.write_text(text)
    return len(people)

if __name__=='__main__':
    print('Published '+str(build())+' public member profiles and membership discovery pages.')
