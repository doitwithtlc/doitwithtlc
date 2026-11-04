"""Apply shared brand, navigation and accessibility improvements to review pages.

Run after the page generators. Preview stays noindex until production launch.
"""
from pathlib import Path
import html, json, re

ROOT = Path(__file__).resolve().parents[1] / 'website-preview'
BASE = '/website-preview'
VERSION = '20261103-services'
ASSETS = BASE + '/assets/brand/'
MEDIA = json.loads((ROOT.parent/'data/gallery-media.json').read_text())
DIMENSIONS = {BASE+'/assets/'+photo['src']:(photo['width'],photo['height']) for album in MEDIA.values() for photo in album['photos'] if photo.get('width') and photo.get('height')}
SECTIONS = [('','About BBLO'),('join/','How to Join'),('members/','Meet Our Members'),('board/','Meet Our Board'),('community-impact/','Our Community Impact'),('gallery/','Photos & Videos'),('testimonials/','Visitor Experience'),('present/','Interested in Presenting?'),('partners/','BBLO Partners'),('support/','Brand Opportunities'),('member-center/','Member Login')]
DROPDOWN = '<details class="nav-dropdown bblo-dropdown"><summary>BBLO <span aria-hidden="true">⌄</span></summary><div class="dropdown-links">' + ''.join(f'<a href="{BASE}/bblo/{route}">{label}</a>' for route,label in SECTIONS) + '</div></details>'

TLC_MENU = '<details class="nav-dropdown tlc-dropdown"><summary>The Liaison Companies <span aria-hidden="true">⌄</span></summary><div class="dropdown-links"><a href="'+BASE+'/home/">Home / Our Services</a><a href="'+BASE+'/services/brand-representation/">Brand Representation</a><a href="'+BASE+'/services/event-management/">Event Management</a><a href="'+BASE+'/bblo/">BBLO</a><a href="'+BASE+'/services/bilingual-outreach/">Bilingual Outreach</a><a href="'+BASE+'/services/branding-content/">Branding &amp; Content</a><a href="'+BASE+'/about/">Meet Carmen</a></div></details>'
VIRTUAL = 'https://calendar.app.google/WQ41dAo7znAJeruT8'
IN_PERSON = 'https://calendar.app.google/B2fesYe5HteXBfE77'
def connect_section(label, subject, address='carmen@doitwithtlc.com'):
 from urllib.parse import quote
 return '<section class="service-connect" id="connect"><div class="wrap"><p class="eyebrow">Your next step</p><h2>Let’s talk about '+label+'.</h2><p>Request information by email or choose a virtual or in-person 1:1 with Carmen.</p><div class="actions"><a class="button" href="mailto:'+address+'?subject='+quote(subject)+'">Email for information</a><a class="button secondary" href="'+VIRTUAL+'">Book a virtual 1:1</a><a class="button secondary" href="'+IN_PERSON+'">Book an in-person 1:1</a></div></div></section>'

def icon(name, cls='clue-icon'):
 return f'<img class="{cls}" src="{ASSETS}clue-{name}.webp" alt="" width="128" height="128" loading="lazy" decoding="async">'

TRAIL = '<section class="carmen-trail" aria-label="Follow Carmen"><div class="wrap"><a class="carmen-figure" href="'+BASE+'/where-is-carmen/" aria-label="Follow Carmen to business opportunities"><img src="'+ASSETS+'carmen-silhouette.webp" alt="Carmen’s navy-and-gold detective silhouette" width="384" height="576" loading="lazy" decoding="async"><span class="carmen-reveal">Your next business clue →</span></a><div><p class="eyebrow">Where in Ocala is Carmen today?</p><h2>You Can’t Be Everywhere,<br>But Your Brand Can.</h2><p>Find opportunities, meet the people behind local businesses and put your next introduction in motion.</p><div class="clue-links"><a href="'+BASE+'/where-is-carmen/">'+icon('calendar')+'<span>Find business opportunities</span></a><a href="'+BASE+'/bblo/members/">'+icon('business-card')+'<span>Meet BBLO businesses</span></a><a href="'+BASE+'/inquire/">'+icon('open-door')+'<span>Start a conversation</span></a></div></div></div></section>'

count=0
for file in ROOT.rglob('index.html'):
 if file == ROOT/'index.html': continue
 s=file.read_text()
 # Rebuild only the main navigation; keep BBLO's separate section menu.
 nav=TLC_MENU+'<a href="'+BASE+'/where-is-carmen/">Where is Carmen?</a>'+DROPDOWN+'<a href="'+BASE+'/contact/">Contact</a><a class="button" href="'+VIRTUAL+'">Schedule a 1:1</a>'
 s=re.sub(r'(<nav[^>]*aria-label="Main navigation"[^>]*>).*?(</nav>)',lambda m:m[1]+nav+m[2],s,flags=re.S)
 s=s.replace('href="/website-preview/" aria-label="The Liaison Companies LLC — Home"','href="/website-preview/home/" aria-label="The Liaison Companies LLC — Home"')
 s=s.replace('>Testimonials<','>Visitor Experience<')
 s=s.replace('/assets/brand/tlc-white.png','/assets/brand/tlc-white.webp')
 def image_dimensions(m):
  tag=m.group();src=re.search(r'src="([^\"]+)"',tag)
  if src and src[1] in DIMENSIONS and not re.search(r'\bwidth=',tag):
   w,h=DIMENSIONS[src[1]];tag=tag[:-1]+f' width="{w}" height="{h}">'
  return tag
 s=re.sub(r'<img\b[^>]+>',image_dimensions,s)
 s=re.sub(r'/bblo/member-center/#(?:member-check-in|member-win|visitor-check-in)', '/bblo/member-center/',s)
 s=re.sub(r'/bblo/testimonials/#(?:share-story|profile-update)', '/bblo/member-center/',s)
 s=s.replace('Members: share your BBLO experience','Open the Member Hub')
 s=s.replace('Representation agreements start at $1,500/month with a six-month minimum.','Representation agreements are tailored to your scope and goals.')
 s=re.sub(r'<section class="visibility-callout">.*?</section>','',s,flags=re.S)
 s=re.sub(r'<section class="carmen-trail".*?</section>','',s,flags=re.S)
 s=s.replace('</main>',TRAIL+'</main>')
 if 'id="site-nav"' not in s:
  s=s.replace('<nav aria-label="Main navigation">','<button class="nav-toggle" type="button" aria-expanded="true" aria-controls="site-nav">Menu</button><nav id="site-nav" aria-label="Main navigation">')
 if 'fonts.googleapis.com/css2' not in s:
  s=s.replace('</head>','<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&amp;family=DM+Serif+Display:ital@0;1&amp;display=swap" rel="stylesheet"></head>')
 s=re.sub(r'(/assets/(?:design\.css|site\.js))(?:\?v=[^"\s]+)?',r'\1?v='+VERSION,s)
 s=re.sub(r'(/assets/bblo/bblo\.js)(?:\?v=[^"\s]+)?',r'\1?v='+VERSION,s)
 if '/assets/polish.css' not in s:
  s=s.replace('</head>',f'<link rel="stylesheet" href="{BASE}/assets/polish.css?v={VERSION}"></head>')
 s=re.sub(r'(/assets/polish\.css)(?:\?v=[^"\s]+)?',r'\1?v='+VERSION,s)
 if 'data-nav-fallback' not in s:
  s=s.replace('</head>','<noscript data-nav-fallback><style>@media(max-width:760px){header nav{display:flex!important}.nav-toggle{display:none!important}}</style></noscript></head>')
 route='/'+str(file.parent.relative_to(ROOT)).strip('/')+'/'
 s=re.sub(r'<section class="service-connect".*?</section>','',s,flags=re.S)
 service_routes={'/services/brand-representation/':('your brand representation','Brand Representation Information'),'/services/event-management/':('your event','Event Management Information'),'/services/bilingual-outreach/':('bilingual outreach','Bilingual Outreach Information'),'/services/branding-content/':('your content needs','Branding and Content Information'),'/bblo/':('BBLO','BBLO Information')}
 if route in service_routes:
  label,subject=service_routes[route]
  connection=connect_section(label,subject,'bblocala@gmail.com' if route=='/bblo/' else 'carmen@doitwithtlc.com')
  s=s.replace('<section class="carmen-trail"',connection+'<section class="carmen-trail"',1)
  # Service hero leads straight to the visitor's two contact choices.
  if route.startswith('/services/'):
   hero_part=re.search(r'<section class="hero[^\"]*">.*?</section>',s,re.S)
   if hero_part:
    part=re.sub(r'<div class="actions">.*?</div>','<div class="actions"><a class="button" href="#connect">Request information or book a 1:1</a></div>',hero_part.group(),count=1,flags=re.S)
    s=s[:hero_part.start()]+part+s[hero_part.end():]
 # BBLO media remains visible, with neutral context until Carmen supplies captions.
 if route.startswith(('/bblo/gallery/','/bblo/community-impact/')):
  s=re.sub(r'<figcaption>.*?</figcaption>','',s,flags=re.S)
  s=re.sub(r'(<article>)(?:<h3>.*?</h3>)?<p[^>]*>.*?</p>(<video\b.*?</video>)(</article>)',r'\1\2\3',s,flags=re.S)
  s=re.sub(r'(<p class="lead">).*?(</p>)',r'\1Moments from BBLO meetings, business visibility and community involvement.\2',s,count=1,flags=re.S)
  s=re.sub(r'(<div class="card-copy">.*?</h[23]>)(<p>.*?</p>)',r'\1<p>Meetings, visibility and connecting with our community.</p>',s,flags=re.S)
  # Keep media alternatives useful without claiming an unconfirmed activity.
  s=re.sub(r'(<video\b[^>]*aria-label=")[^\"]*(")',r'\1BBLO community video\2',s)
  s=s.replace('BBLO’s sponsored community-build archive brings together the people, the build site and the shared work.','Moments of BBLO connecting with and giving back to the community.')
  s=s.replace('The photographs document participants together at a Habitat build site and hands-on work in progress. They are shared as a record of BBLO’s community participation.','BBLO members showing up, building relationships and connecting with the community.')
 # Each preview canonical identifies its actual equivalent content. Production
 # launch must switch these to production URLs together with indexing rules.
 s=re.sub(r'<link rel="canonical" href="[^\"]+">',f'<link rel="canonical" href="https://doitwithtlc.com{BASE}{route}">',s)
 if 'rel="canonical"' not in s:
  s=s.replace('</head>',f'<link rel="canonical" href="https://doitwithtlc.com{BASE}{route}"></head>')
 # Decorative clue in the hero, while all headings remain real text.
 s=re.sub(r'<img class="hero-clue"[^>]*>','',s)
 name='calendar' if ('events/' in route or 'where-is-carmen' in route) else 'business-card' if ('members/' in route or 'about/' in route or 'board/' in route) else 'open-door'
 s=s.replace('<p class="eyebrow">',icon(name,'hero-clue')+'<p class="eyebrow">',1)
 # Fetch the first hero photo promptly; gallery media remains lazy.
 hero=re.search(r'<section class="hero[^\"]*">.*?</section>',s,re.S)
 if hero:
  part=hero.group()
  part=re.sub(r'(<img (?!class="hero-clue")[^>]*?) loading="lazy"',r'\1 loading="eager" fetchpriority="high"',part,count=1)
  s=s[:hero.start()]+part+s[hero.end():]
 if route=='/bblo/':
  s=s.replace('About BBLO | BBLO · TLC','Bilingual Business Networking in Ocala | BBLO · TLC')
  s=s.replace('content="About BBLO | BBLO"','content="Bilingual Business Networking in Ocala | BBLO"')
  if '"@type":"Organization"' not in s:
   data={'@context':'https://schema.org','@type':'Organization','name':'Bilingual Business Leaders of Ocala','alternateName':'BBLO','url':'https://doitwithtlc.com/bblo/','parentOrganization':{'@type':'Organization','name':'The Liaison Companies LLC','url':'https://doitwithtlc.com/'},'sameAs':['https://www.instagram.com/bblocala/']}
   s=s.replace('</head>','<script type="application/ld+json">'+json.dumps(data,separators=(',',':'))+'</script></head>')
 # Give repeated album links their visible context in their accessible names.
 def article_names(m):
  part=m.group();heading=re.search(r'<h[23][^>]*>(.*?)</h[23]>',part,re.S)
  if not heading:return part
  label=html.escape(re.sub('<[^>]+>','',heading.group(1)),quote=True)
  return re.sub(r'<a class="text-link" href="([^\"]+)">(Explore →|Profile &amp; contact details →|Open album &amp; meet the organization →)</a>',lambda a:f'<a class="text-link" href="{a[1]}" aria-label="{label}: {a[2]}">{a[2]}</a>',part)
 s=re.sub(r'<article\b.*?</article>',article_names,s,flags=re.S)
 if route=='/inquire/':
  s=s.replace('Review my inquiry','Review &amp; email inquiry')
  s=s.replace('Preview: inquiry submission opens once the connection is tested.','Review your answers, then open an email draft to send them. Nothing is sent automatically. You can attach photos in your email app.')
  s=s.replace('<div id="inquiry-review"','<noscript><p>Email <a href="mailto:carmen@doitwithtlc.com">carmen@doitwithtlc.com</a> or call <a href="tel:3522079770">352-207-9770</a> to discuss your inquiry.</p></noscript><div id="inquiry-review"') if '<noscript>' not in s else s
  s=re.sub(r'(id="inquiry-review" class="form-summary")(?: tabindex="-1")*',r'\1 tabindex="-1"',s)
 if route=='/where-is-carmen/':
  s=s.replace('<p>The next verified website edition is being prepared.</p>','<p>Find the latest business-opportunities posts on TLC’s Instagram. Confirm the date, location and registration with the organizer before attending.</p><a class="button" href="https://www.instagram.com/doitwithtlc/" target="_blank" rel="noopener">See TLC’s latest posts ↗</a>')
 if route=='/bblo/present/':
  s=s.replace('Review my answers','Review &amp; email proposal').replace('Review only — nothing is sent or saved.','Review your answers, then open an email draft to BBLO. You send the final message from your email app.')
  s=re.sub(r'<div class="review-note".*?</div>','<p class="note">Share your proposed topic below, review your answers and email them to BBLO for consideration.</p>',s,flags=re.S)
 # Load the social embed when a visitor approaches it, rather than during the hero.
 if '<behold-widget ' in s:
  s=re.sub(r'<script>\(\(\)=>\{if\(window\.__bhldScript\).*?</script>', '<script>(()=>{const w=document.querySelector("behold-widget");const load=()=>{if(window.__bhldScript)return;window.__bhldScript=true;const s=document.createElement("script");s.type="module";s.src="https://w.behold.so/widget.js";document.head.append(s);};if("IntersectionObserver" in window){const o=new IntersectionObserver(es=>{if(es.some(e=>e.isIntersecting)){load();o.disconnect();}},{rootMargin:"300px"});o.observe(w);}else load();})();</script>',s,flags=re.S)
 # Test tools may access the preview, but search indexing stays disabled.
 assert 'noindex' in s, str(file)
 file.write_text(s);count+=1

print(f'Polished {count} review pages. Preview indexing restrictions preserved.')
