"""Build curated review galleries from the supplied event media."""
from pathlib import Path
import html,json,re

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/'website-preview'
BASE='/website-preview'
media=json.loads((REPO/'data/gallery-media.json').read_text())
template=(ROOT/'events/unstoppable-2026/index.html').read_text()
header=re.search(r'<header>.*?</header>',template,re.S).group()
footer=re.search(r'<footer>.*?</footer>',template,re.S).group()
nav=re.search(r'<nav class="bblo-subnav".*?</nav>',(ROOT/'bblo/index.html').read_text(),re.S).group()
nav=re.sub(r' aria-current="page"','',nav).replace('href="'+BASE+'/bblo/gallery/"','href="'+BASE+'/bblo/gallery/" aria-current="page"')
def esc(value):return html.escape(str(value),quote=True)
def link(path,label,cls='button'):return '<a class="'+cls+'" href="'+BASE+path+'">'+label+'</a>'
def section(body,cls=''):return '<section class="'+cls+'"><div class="wrap">'+body+'</div></section>'
def hero(label,title,copy):return section('<p class="eyebrow">'+label+'</p><h1>'+title+'</h1><p class="lead">'+copy+'</p>','hero')
def photo(p):
 return '<figure class="photo"><a href="'+BASE+'/assets/'+p['src']+'" target="_blank" rel="noopener" aria-label="Open photograph: '+esc(p['caption'])+'"><img src="'+BASE+'/assets/'+p['src']+'" alt="'+esc(p['caption'])+'" width="'+str(p['width'])+'" height="'+str(p['height'])+'" loading="lazy" decoding="async"></a></figure>'
def videos(items):
 if not items:return ''
 return section('<p class="eyebrow">Short video moments</p><h2>Press play.<br>Step into the moment.</h2><div class="grid gallery-video-grid">'+''.join('<article><h3>'+esc(v['title'])+'</h3><p>'+esc(v['description'])+' · '+str(v['duration'])+' seconds.</p><video class="gallery-video" controls playsinline preload="none" poster="'+BASE+'/assets/'+v['poster']+'"><source src="'+BASE+'/assets/'+v['src']+'" type="video/mp4">Your browser does not support this video.</video></article>' for v in items)+'</div>','map-section')
def write(route,title,description,body,is_bblo=False,cover='photos/unstoppable-debbie-carmen.jpg'):
 s='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>'+esc(title)+' | TLC</title><meta name="description" content="'+esc(description)+'"><meta property="og:title" content="'+esc(title)+'"><meta property="og:image" content="https://doitwithtlc.com'+BASE+'/assets/'+cover+'"><link rel="stylesheet" href="'+BASE+'/assets/design.css?v=20261103-bblo-community"><link rel="stylesheet" href="'+BASE+'/assets/bblo/bblo.css?v=20261103-bblo-community"><link rel="stylesheet" href="'+BASE+'/assets/galleries/gallery.css?v=20261103-event-galleries"><script src="'+BASE+'/assets/site.js?v=20261103-bblo-community" defer></script></head><body><a class="skip" href="#main">Skip to content</a>'+header+(nav if is_bblo else '')+'<main id="main" class="media-gallery-page">'+body+'</main>'+footer+'</body></html>'
 p=ROOT/route.strip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)

unstoppable=media['unstoppable']
body=hero('Unstoppable 2026 · October 7, 2026','The moments.<br><em>The people. The experience.</em>','A closer look at Unstoppable 2026 at the College of Central Florida’s Klein Center, from the setup to the stage and the connections in between.')
body+=section('<p class="eyebrow">From the event archive</p><h2>A night worth remembering.</h2><div class="gallery portfolio-gallery curated-gallery">'+''.join(photo(p) for p in unstoppable['photos'])+'</div>')+videos(unstoppable['videos'])
body+=section('<h2>See how the experience came together.</h2><div class="actions">'+link('/events/unstoppable-2026/','← Event portfolio','button secondary')+link('/inquire/?service=events','Let’s plan your event')+'</div>')
write('/events/unstoppable-2026/gallery/','Unstoppable 2026 Photo & Video Gallery','Selected real photographs and short videos from Unstoppable 2026.',body)

albums=[
 {'key':'bblo-10-09','slug':'2026-10-09','date':'October 9, 2026','intro':'Member presentations, business conversation and a group photo at Media Minds.','cover':3},
 {'key':'bblo-09-25','slug':'2026-09-25','date':'September 25, 2026','intro':'Business presentations and a morning together with the BBLO group at Media Minds.','cover':3},
 {'key':'bblo-08-28','slug':'2026-08-28','date':'August 28, 2026','intro':'A look around the meeting tables, with business conversation and candid member moments at Media Minds.','cover':0}
]
cards=[]
for a in albums:
 data=media[a['key']];cover=data['photos'][a['cover']]
 cards.append('<article class="album-card">'+photo(cover)+'<div class="card-copy"><p class="eyebrow">BBLO meeting</p><h2>'+a['date']+'</h2><p>'+a['intro']+'</p>'+link('/bblo/gallery/'+a['slug']+'/', 'Open album →','text-link')+'</div></article>')
 body=hero('BBLO meeting · '+a['date'],'The BBLO experience.<br><em>One meeting at a time.</em>',a['intro'])+section('<div class="gallery portfolio-gallery curated-gallery">'+''.join(photo(p) for p in data['photos'])+'</div>')+videos(data['videos'])
 body+=section('<div class="actions">'+link('/bblo/gallery/','← Photo &amp; video albums','button secondary')+link('/bblo/join/','Come meet us')+'</div>')
 write('/bblo/gallery/'+a['slug']+'/',a['date']+' · BBLO Photo & Video Album',a['intro'],body,True,cover['src'])
body=hero('BBLO photos & videos','See the people.<br><em>Feel the connection.</em>','Browse moments from BBLO meetings, member presentations and business conversations. Open a dated album to see the photographs and available short videos.')+section('<div class="grid three gallery-album-grid">'+''.join(cards)+'</div>')
body+=section('<p class="eyebrow">Beyond our regular meetings</p><h2>See BBLO in the community.</h2><p>Explore activity albums with the story behind each visit and contact information for the organizations involved.</p>'+link('/bblo/community-impact/','Explore community activity albums'),'map-section')
write('/bblo/gallery/','BBLO Photos & Videos','Browse BBLO meeting photographs and short video moments in separate dated albums.',body,True,media['bblo-10-09']['photos'][3]['src'])

# Keep the approved portfolio photographs, including its Debbie and Carmen image.
portfolio=ROOT/'events/unstoppable-2026/index.html'
s=portfolio.read_text();s=re.sub(r'<!-- expanded-gallery-start -->.*?<!-- expanded-gallery-end -->','',s,flags=re.S)
cta='<!-- expanded-gallery-start -->'+section('<p class="eyebrow">More from Unstoppable 2026</p><h2>Explore the photo &amp; video gallery.</h2><p>See more guest moments, stage photographs, event details and short video clips.</p>'+link('/events/unstoppable-2026/gallery/','Open the event gallery'))+'<!-- expanded-gallery-end -->'
s=s.replace('<section class="dark">',cta+'<section class="dark">',1);portfolio.write_text(s)
print('Built Unstoppable gallery and three dated BBLO meeting albums.')
