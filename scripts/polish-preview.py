"""Apply shared brand, navigation and accessibility improvements to review pages.

Run after the page generators. Preview stays noindex until production launch.
"""
from pathlib import Path
import html, json, re

ROOT = Path(__file__).resolve().parents[1] / 'website-preview'
BASE = '/website-preview'
VERSION = '20261103-polish'
ASSETS = BASE + '/assets/brand/'
SECTIONS = [('','About BBLO'),('join/','How to Join'),('members/','Meet Our Members'),('board/','Meet Our Board'),('community-impact/','Our Community Impact'),('gallery/','Photos & Videos'),('testimonials/','Visitor Experience'),('present/','Interested in Presenting?'),('partners/','BBLO Partners'),('support/','Brand Opportunities'),('member-center/','Member Login')]
DROPDOWN = '<details class="nav-dropdown"><summary>BBLO <span aria-hidden="true">⌄</span></summary><div class="dropdown-links">' + ''.join(f'<a href="{BASE}/bblo/{route}">{label}</a>' for route,label in SECTIONS) + '</div></details>'

def icon(name, cls='clue-icon'):
 return f'<img class="{cls}" src="{ASSETS}clue-{name}.webp" alt="" width="128" height="128" loading="lazy" decoding="async">'

TRAIL = '<section class="carmen-trail" aria-label="Follow Carmen"><div class="wrap"><a class="carmen-figure" href="'+BASE+'/where-is-carmen/" aria-label="Follow Carmen to business opportunities"><img src="'+ASSETS+'carmen-silhouette.webp" alt="Carmen’s navy-and-gold detective silhouette" width="384" height="576" loading="lazy" decoding="async"><span class="carmen-reveal">Your next business clue →</span></a><div><p class="eyebrow">Where in Ocala is Carmen today?</p><h2>You Can’t Be Everywhere,<br>But Your Brand Can.</h2><p>Find opportunities, meet the people behind local businesses and put your next introduction in motion.</p><div class="clue-links"><a href="'+BASE+'/where-is-carmen/">'+icon('calendar')+'<span>Find business opportunities</span></a><a href="'+BASE+'/bblo/members/">'+icon('business-card')+'<span>Meet BBLO businesses</span></a><a href="'+BASE+'/inquire/">'+icon('open-door')+'<span>Start a conversation</span></a></div></div></div></section>'

count=0
for file in ROOT.rglob('index.html'):
 if file == ROOT/'index.html': continue
 s=file.read_text()
 s=re.sub(r'<details class="nav-dropdown">.*?</details>',lambda _:DROPDOWN,s,flags=re.S)
 s=s.replace('>Testimonials<','>Visitor Experience<')
 s=s.replace('/assets/brand/tlc-white.png','/assets/brand/tlc-white.webp')
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
 route='/'+str(file.parent.relative_to(ROOT)).strip('/')+'/'
 # Each preview canonical identifies its actual equivalent content. Production
 # launch must switch these to production URLs together with indexing rules.
 s=re.sub(r'<link rel="canonical" href="[^\"]+">',f'<link rel="canonical" href="https://doitwithtlc.com{BASE}{route}">',s)
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
