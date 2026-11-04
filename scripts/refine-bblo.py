"""Apply Carmen's compact BBLO structure and approved-media networking strip."""
from pathlib import Path
import html, json, re

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/'website-preview'
BASE='/website-preview'
FORM='https://api.leadconnectorhq.com/widget/form/XfFmoR9nEROeXCLyPO09'

STORIES={
 'habitat-vet-build':('Habitat Vet Build','Showing up for a place to call home.','BBLO took part in a Habitat Vet Build, connecting local business owners with the work of building homes and supporting our neighbors.','Affordable housing connects to the wellbeing of the whole community. Working alongside Habitat gives business owners a practical way to contribute time, build relationships through shared work and learn where their support can be useful.'),
 'emergency-management-tour':('Behind the Response','Knowing who to turn to before an emergency.','Our Field Trip Friday took BBLO inside Marion County Emergency Management to learn about preparedness, communications and coordinated response.','A business is part of a wider community when an emergency happens. Meeting the people behind local response resources helps owners ask better questions about preparedness and think ahead about their teams, customers and continuity.'),
 'community-nonprofit-spotlights':('Meet the Missions','Local causes. Real ways to help.','The Rock Program and Champions for Champions came to BBLO to share their missions and help business owners understand the needs they serve.','The Rock Program helps meet local students’ essential needs. Champions for Champions provides inclusive programs for people with special needs and their families. Hearing directly from these organizations helps members recognize opportunities to volunteer, share resources and connect the right people with support.'),
 'rancho-reposo':('Beyond the Business Card','Meet a local business by stepping into its world.','BBLO visited Rancho Reposo in Morriston for a closer look at its Friesian horse experiences and the business behind them.','A firsthand visit makes a business easier to understand and talk about. Field trips give members time to ask questions, learn what makes an experience distinctive and build relationships beyond their usual meeting setting.'),
 'ms-veteran-america':('Showing Up for Women Veterans','Visibility with a purpose beyond business.','Ms. Veteran America brings attention and support to Final Salute, Inc., which serves homeless women veterans and their children.','Participating in community events connects business visibility with issues that deserve attention. This event creates an opportunity to learn about women veterans’ housing needs and direct others to the organization doing that work.')
}

def section(body,cls=''):
 return '<section class="'+cls+'"><div class="wrap">'+body+'</div></section>'
def card(path,title,copy):
 return '<a class="card connection-card" href="'+BASE+path+'"><h3>'+title+'</h3><p>'+copy+'</p><span class="text-link">Explore →</span></a>'

for file in ROOT.rglob('index.html'):
 if file==ROOT/'index.html':continue
 s=file.read_text()
 # One destination for current partner benefits and brand inquiries.
 s=s.replace(BASE+'/bblo/support/',BASE+'/bblo/partners/#feature-your-brand')
 s=s.replace('Community build archive','Community build').replace('Local housing nonprofit and the organization behind the Vet Build archive.','A local nonprofit focused on safe, affordable housing and community participation.')
 s=s.replace('>Visitor Experience<','>Member &amp; Visitor Experiences<')
 s=s.replace('>Photos & Videos<','>BBLO in Action<').replace('>BBLO Partners<','>Partners &amp; Brand Opportunities<')
 s=re.sub(r'<a[^>]*href="'+re.escape(BASE)+r'/bblo/partners/#feature-your-brand"[^>]*>Brand Opportunities</a>','',s)
 # Member login is an entry in the BBLO dropdown, not a repeated page promotion.
 route='/'+str(file.parent.relative_to(ROOT)).strip('/')+'/'
 if route!='/bblo/member-center/':
  head,sep,body=s.partition('</header>')
  body=re.sub(r'<a[^>]*href="'+re.escape(BASE)+r'/bblo/member-center/"[^>]*>.*?</a>','',body,flags=re.S)
  s=head+sep+body
 if '<nav class="bblo-subnav"' in s:
  def clean_subnav(m):
   part=m.group()
   part=re.sub(r'<a[^>]*href="'+re.escape(BASE)+r'/bblo/member-center/"[^>]*>.*?</a>','',part,flags=re.S)
   return part
  s=re.sub(r'<nav class="bblo-subnav".*?</nav>',clean_subnav,s,flags=re.S)
 if route=='/bblo/support/':
  s=re.sub(r'<link rel="canonical" href="[^"]+">','<link rel="canonical" href="https://doitwithtlc.com/website-preview/bblo/support/">',s)
 if route=='/bblo/':
  s=s.replace('class="bblo-page"','class="bblo-page compact-bblo"')
  s=re.sub(r'<section[^>]*><div class="wrap"><div class="split"><div><p class="eyebrow">For members</p>.*?</section>','',s,flags=re.S)
  s=re.sub(r'<section class="service-connect".*?</section>','',s,flags=re.S)
  options=[('/bblo/members/','Meet Our Members','Find the people and services behind your next business connection.'),('/bblo/board/','Meet Our Board','Get to know the people helping guide BBLO.'),('/bblo/community-impact/','Making a Difference','See where we show up, what we learn and how we connect with local causes.'),('/bblo/testimonials/','Member &amp; Visitor Experiences','Read member and visitor feedback shared with permission and approved by BBLO.'),('/bblo/present/','Share Your Expertise','Have something useful to teach business owners? Start here.'),('/bblo/gallery/','BBLO in Action','Step into our meetings, field trips and community connections.'),('/bblo/partners/','Partners &amp; Brand Opportunities','Explore member benefits or bring a useful product or service to BBLO.')]
  new=section('<p class="eyebrow">Explore BBLO</p><h2>Find your next connection.</h2><div class="grid three route-cards">'+''.join(card(*x) for x in options)+'</div>','map-section')
  s=re.sub(r'<section[^>]*><div class="wrap"><p class="eyebrow">Explore BBLO</p>.*?</section>',lambda _:new,s,flags=re.S)
  s=s.replace('The people. The activity. The connection.','Connections that reach beyond business.')
 if route=='/bblo/testimonials/':
  s=re.sub(r'<title>.*?</title>','<title>Member &amp; Visitor Experiences | BBLO · TLC</title>',s)
  s=re.sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="Member and visitor feedback shared with permission and approved by BBLO.">',s)
  members=json.loads((REPO/'data/bblo-members.json').read_text())
  quotes=''.join('<article class="card"><blockquote><p>'+html.escape(m['quote'])+'</p><cite>'+html.escape(m['name'])+' · '+html.escape(m['company'])+'</cite></blockquote></article>' for m in members if m.get('quote') and m.get('quote_approved'))
  public=section('<p class="eyebrow">Member &amp; visitor experiences</p><h1>The experience.<br><em>In their own words.</em></h1><p class="lead">Member and visitor feedback shared with permission and approved by BBLO.</p>','hero')
  public+=section('<div class="grid">'+quotes+'</div>') if quotes else section('<h2>Member and visitor stories are on the way.</h2><p>We’ll share experiences here after contributors give permission and BBLO reviews their feedback.</p>')
  trail=re.search(r'<section class="carmen-trail".*?</section>',s,re.S)
  s=re.sub(r'(<main\b[^>]*>).*?(</main>)',lambda m:m[1]+public+(trail.group() if trail else '')+m[2],s,flags=re.S)
  s=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="Read visitor experiences shared with permission and approved by BBLO.">',s)
 if route=='/bblo/join/':
  s=re.sub(r'<!-- after-visit-start -->.*?<!-- after-visit-end -->','',s,flags=re.S)
  after='<!-- after-visit-start -->'+section('<p class="eyebrow">Share your experience</p><h2>What has BBLO meant to you?</h2><p>Whether you’re a member or a visitor, share feedback and optional photos privately with BBLO. Nothing is published without permission and review.</p><a class="button" href="'+FORM+'">Share your BBLO experience</a>')+'<!-- after-visit-end -->'
  s=s.replace('<section class="carmen-trail"',after+'<section class="carmen-trail"',1)
 # Purposeful, event-specific activity copy; keep individual media captions removed.
 if route.startswith(('/bblo/community-impact/','/bblo/gallery/')) or route=='/bblo/':
  def activity_card(m):
   part=m.group()
   for slug,(title,hook,intro,why) in STORIES.items():
    if '/community-impact/'+slug+'/' in part:
     part=re.sub(r'(<h[23][^>]*>).*?(</h[23]>)',lambda h:h[1]+title+h[2],part,count=1,flags=re.S)
     part=re.sub(r'(<div class="card-copy">.*?</h[23]>)<p>.*?</p>',lambda h:h[1]+'<p>'+intro+'</p>',part,count=1,flags=re.S)
     part=re.sub(r'aria-label="[^"]*:(?: Explore| Open album)[^"]*"','aria-label="Open '+html.escape(title,quote=True)+'"',part)
     break
   return part
  s=re.sub(r'<article class="album-card">.*?</article>',activity_card,s,flags=re.S)
  slug=route.rstrip('/').split('/')[-1]
  if slug in STORIES:
   title,hook,intro,why=STORIES[slug]
   s=re.sub(r'(<h1[^>]*>).*?(</h1>)',lambda m:m[1]+title+m[2],s,count=1,flags=re.S)
   s=re.sub(r'(<p class="lead">).*?(</p>)',lambda m:m[1]+intro+m[2],s,count=1,flags=re.S)
   s=re.sub(r'<!-- activity-purpose-start -->.*?<!-- activity-purpose-end -->','',s,flags=re.S)
   purpose='<!-- activity-purpose-start -->'+section('<p class="eyebrow">Why it matters</p><h2>'+hook+'</h2><p>'+why+'</p>','activity-purpose')+'<!-- activity-purpose-end -->'
   hero=re.search(r'<section class="hero[^\"]*">.*?</section>',s,re.S)
   if hero:s=s[:hero.end()]+purpose+s[hero.end():]
   s=re.sub(r'<div class="split"><div><p class="eyebrow">What we were doing</p>.*?</div></div>','',s,flags=re.S)
   s=s.replace('From the meeting archive','Meet the Missions').replace('An 11-second clip from the September 4 meeting archive. Play it when you’re ready.','Hear a moment from the nonprofit presentations at BBLO.')
  if route=='/bblo/community-impact/':
   s=re.sub(r'(<p class="lead">).*?(</p>)',r'\1We meet the people behind local causes, learn how our community works and look for meaningful ways to get involved.\2',s,count=1,flags=re.S)
   s=s.replace('More from our community archive','Working alongside our community').replace('Explore the existing BBLO-sponsored build archive and Habitat for Humanity of Marion County contact information.','A shared day of work with Habitat connects business owners with the need for safe, affordable housing and ways to contribute.')
  if route=='/bblo/gallery/':
   s=re.sub(r'<title>.*?</title>','<title>BBLO in Action | Meetings, Visits &amp; Community | TLC</title>',s)
   s=s.replace('BBLO photos &amp; videos','BBLO in Action').replace('BBLO photos & videos','BBLO in Action')
   s=re.sub(r'(<p class="lead">).*?(</p>)',r'\1The conversations, shared experiences and community involvement that make BBLO more than a weekly meeting.\2',s,count=1,flags=re.S)
 file.write_text(s)

# Combine partner benefits and feature-your-brand inquiries at one destination.
p=ROOT/'bblo/partners/index.html';s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>Partners &amp; Brand Opportunities | BBLO · TLC</title>',s)
s=re.sub(r'<!-- brand-opportunities-start -->.*?<!-- brand-opportunities-end -->','',s,flags=re.S)
s=re.sub(r'<section[^>]*><div class="wrap"><p class="eyebrow">Bring your brand to BBLO</p>.*?</section>','',s,flags=re.S)
s=s.replace('<h1>Your membership.<br><em>More business value.</em></h1>','<h1>Partners. Benefits.<br><em>Business opportunities.</em></h1>')
s=s.replace('<p class="eyebrow">BBLO Partners</p>','<p class="eyebrow">Partners &amp; Brand Opportunities</p>')
combined='<!-- brand-opportunities-start -->'+section('<div id="feature-your-brand"><p class="eyebrow">Feature your brand</p><h2>Have something our businesses can use?</h2><p>Bring BBLO a useful product, service, demonstration or member offer. Tell us who it helps and how it fits our business community.</p><div class="grid three"><article class="card"><h3>Share your expertise.</h3><p>Help members understand your product or service and where it can make a difference in their businesses.</p></article><article class="card"><h3>Create a member benefit.</h3><p>Propose an offer, resource or service that gives BBLO members practical value.</p></article><article class="card"><h3>Build the right fit.</h3><p>We’ll discuss available opportunities, pricing, responsibilities and what’s included before confirming anything.</p></article></div><div class="actions"><a class="button" href="mailto:bblocala@gmail.com?subject=BBLO%20Brand%20Feature%20Inquiry">Ask about brand opportunities</a></div><p class="note">Include your business name, website, what you offer and your preferred timing.</p></div>','map-section')+'<!-- brand-opportunities-end -->'
s=s.replace('<section class="carmen-trail"',combined+'<section class="carmen-trail"',1);p.write_text(s)
# Old saved links resolve to the combined page; no second menu entry.
p=ROOT/'bblo/support/index.html';s=p.read_text()
if 'data-partner-redirect' not in s:s=s.replace('</head>','<meta data-partner-redirect http-equiv="refresh" content="0;url='+BASE+'/bblo/partners/#feature-your-brand"></head>')
p.write_text(s)

# Two scrolling columns, with two visible rows, using unchanged approved photos.
p=ROOT/'where-is-carmen/index.html';s=p.read_text()
s=re.sub(r'<!-- networking-strip-start -->.*?<!-- networking-strip-end -->','',s,flags=re.S)
photos=[('curated-bblo/20260828/20260828_103010.webp','BBLO business gathering at Media Minds'),('bblo/community/emergency-group.webp','BBLO visit to Marion County Emergency Management'),('photos/unstoppable-debbie-carmen.jpg','Debbie Cowan and Carmen at Unstoppable'),('curated-bblo/20261009/fb_img_1791564240253.webp','BBLO members together'),('bblo/community/nonprofit-group.webp','Nonprofit presenters and BBLO participants'),('photos/community-food-vendors.jpg','Local business participation at Salsa On The Square')]
tracks=''
for items in (photos[::2],photos[1::2]):
 group=''.join('<figure><img src="'+BASE+'/assets/'+src+'" alt="'+alt+'" width="1200" height="900" loading="eager" decoding="async"></figure>' for src,alt in items)
 repeat=''.join('<figure><img src="'+BASE+'/assets/'+src+'" alt="" width="1200" height="900" loading="lazy" decoding="async"></figure>' for src,alt in items)
 tracks+='<div class="photo-track"><div class="photo-track-group">'+group+'</div><div class="photo-track-group" aria-hidden="true">'+repeat+'</div></div>'
strip='<!-- networking-strip-start --><aside class="networking-strip" aria-label="Networking and community moments"><div class="strip-window">'+tracks+'</div><button class="strip-pause" type="button" data-pause-strip aria-pressed="false">Pause photo motion</button></aside><!-- networking-strip-end -->'
hero=re.search(r'<section class="hero[^\"]*">.*?</section>',s,re.S)
if hero:
 part=hero.group()
 if '<div class="networking-intro">' in part:
  part=re.sub(r'(<div class="wrap">)<div class="networking-intro">(.*)</div>(</div></section>)',lambda m:m[1]+m[2]+m[3],part,flags=re.S)
 part=part.replace('class="hero"','class="hero networking-hero"')
 # The left column stays semantic; the image strip occupies the right column.
 part=re.sub(r'(<div class="wrap">)(.*)(</div></section>)',lambda m:m[1]+'<div class="networking-intro">'+m[2]+'</div>'+strip+m[3],part,flags=re.S)
 s=s[:hero.start()]+part+s[hero.end():]
p.write_text(s)
print('Refined BBLO content, member access, combined partners and networking strip.')
