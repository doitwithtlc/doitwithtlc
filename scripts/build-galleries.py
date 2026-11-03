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
 return section('<p class="eyebrow">Short video moments</p><h2>Press play.<br>Step into the moment.</h2><div class="grid gallery-video-grid">'+''.join('<article>'+('<h3>'+esc(v['title'])+'</h3><p>'+esc(v['description'])+' · '+str(v['duration'])+' seconds.</p>' if v['description'] else '<p class="note">Video '+str(i)+' · '+str(v['duration'])+' seconds</p>')+'<video class="gallery-video" controls playsinline preload="none" aria-label="'+esc(v['title'])+' · video '+str(i)+'" poster="'+BASE+'/assets/'+v['poster']+'"><source src="'+BASE+'/assets/'+v['src']+'" type="video/mp4">Your browser does not support this video.</video></article>' for i,v in enumerate(items,1))+'</div>','map-section')
def write(route,title,description,body,is_bblo=False,cover='photos/unstoppable-debbie-carmen.jpg'):
 s='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>'+esc(title)+' | TLC</title><meta name="description" content="'+esc(description)+'"><meta property="og:title" content="'+esc(title)+'"><meta property="og:image" content="https://doitwithtlc.com'+BASE+'/assets/'+cover+'"><link rel="stylesheet" href="'+BASE+'/assets/design.css?v=20261103-bblo-community"><link rel="stylesheet" href="'+BASE+'/assets/bblo/bblo.css?v=20261103-bblo-community"><link rel="stylesheet" href="'+BASE+'/assets/galleries/gallery.css?v=20261103-event-galleries"><script src="'+BASE+'/assets/site.js?v=20261103-bblo-community" defer></script></head><body><a class="skip" href="#main">Skip to content</a>'+header+((nav.replace('href="'+BASE+'/bblo/gallery/" aria-current="page"','href="'+BASE+'/bblo/gallery/"').replace('href="'+BASE+'/bblo/community-impact/"','href="'+BASE+'/bblo/community-impact/" aria-current="page"') if route.startswith('/bblo/community-impact/') else nav) if is_bblo else '')+'<main id="main" class="media-gallery-page">'+body+'</main>'+footer+'</body></html>'
 p=ROOT/route.strip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)

unstoppable=media['unstoppable']
body=hero('Unstoppable 2026 · October 7, 2026','The moments.<br><em>The people. The experience.</em>','A closer look at Unstoppable 2026 at the College of Central Florida’s Klein Center, from the setup to the stage and the connections in between.')
body+=section('<p class="eyebrow">From the event archive</p><h2>A night worth remembering.</h2><div class="gallery portfolio-gallery curated-gallery">'+''.join(photo(p) for p in unstoppable['photos'])+'</div>')+videos(unstoppable['videos'])
body+=section('<h2>See how the experience came together.</h2><div class="actions">'+link('/events/unstoppable-2026/','← Event portfolio','button secondary')+link('/inquire/?service=events','Let’s plan your event')+'</div>')
write('/events/unstoppable-2026/gallery/','Unstoppable 2026 Photo & Video Gallery','Selected real photographs and short videos from Unstoppable 2026.',body)

albums=json.loads((REPO/'data/bblo-gallery-albums.json').read_text())
def cover(a):
 return next(p for p in media[a['key']]['photos'] if p['src'].endswith('/'+a['cover_name']))
def card(a):
 data=media[a['key']]
 image=photo(cover(a)).replace('href="'+BASE+'/assets/'+cover(a)['src']+'"','href="'+BASE+a['route']+'"').replace(' target="_blank" rel="noopener"','')
 image=re.sub(r'aria-label="[^"]*"','aria-label="Open album: '+esc(a['title'])+'"',image,count=1)
 return '<article class="album-card">'+image+'<div class="card-copy"><p class="eyebrow">'+a['label']+' · '+a['date']+'</p><h2>'+esc(a['title'])+'</h2><p>'+esc(a['intro'])+'</p>'+link(a['route'], 'Open album →','text-link')+'</div></article>'
def organization(p):
 contact='<dl class="contact-list">'
 if p['phone']:contact+='<div><dt>Phone</dt><dd><a href="tel:+1'+re.sub(r'\D','',p['phone'])+'">'+esc(p['phone'])+'</a></dd></div>'
 if p['email']:contact+='<div><dt>Email</dt><dd><a href="mailto:'+esc(p['email'])+'">'+esc(p['email'])+'</a></dd></div>'
 if p['address']:contact+='<div><dt>Address</dt><dd>'+esc(p['address'])+'</dd></div>'
 contact+='</dl>'
 return '<article class="card partner-card"><p class="eyebrow">'+esc(p['kind'])+'</p><h3>'+esc(p['name'])+'</h3><p>'+esc(p['about'])+'</p>'+contact+'<div class="actions"><a class="button" href="'+p['website']+'" target="_blank" rel="noopener">Visit website ↗</a><a class="text-link" href="'+p['contact']+'" target="_blank" rel="noopener">Contact ↗</a></div></article>'
community=[a for a in albums if a['kind']=='community']
meetings=[a for a in albums if a['kind']=='meeting']
for a in albums:
 data=media[a['key']]
 title=esc(a['title']) if a['kind']=='community' else 'The BBLO experience.<br><em>One meeting at a time.</em>'
 body=hero(a['label']+' · '+a['date'],title,esc(a['intro']))+section('<div class="gallery portfolio-gallery curated-gallery">'+''.join(photo(p) for p in [cover(a)]+[p for p in data['photos'] if p['src']!=cover(a)['src']])+'</div>')+videos(data['videos'])
 if a['organizations']:body+=section('<p class="eyebrow">Connect with the organization</p><h2>Keep the connection going.</h2><div class="grid">'+''.join(organization(p) for p in a['organizations'])+'</div>')
 body+=section('<div class="actions">'+link('/bblo/gallery/','← Photo &amp; video albums','button secondary')+link('/bblo/join/','Come meet us')+'</div>')
 write(a['route'],a['title']+' · BBLO Photo & Video Album',a['intro'],body,True,cover(a)['src'])
body=hero('BBLO photos & videos','Business connections.<br><em>Community involvement.</em>','Explore BBLO community visits, local causes and member gatherings. Open an album for the photos, videos and organization information.')
body+=section('<p class="eyebrow">BBLO in the community</p><h2>Beyond the meeting.</h2><div class="grid gallery-album-grid">'+''.join(card(a) for a in community)+'</div>')
body+=section('<p class="eyebrow">Meetings & members</p><h2>The people behind the businesses.</h2><div class="grid three gallery-album-grid">'+''.join(card(a) for a in meetings)+'</div>','map-section')
write('/bblo/gallery/','BBLO Photos & Videos','Explore BBLO community activities, visits and member meetings in photo and video albums.',body,True,cover(community[0])['src'])
body=hero('Our community impact','Showing up.<br><em>Getting involved.</em>','Explore BBLO community activities and connect with the organizations behind them.')+section('<div class="grid gallery-album-grid">'+''.join(card(a) for a in community)+'</div>')
body+=section('<p class="eyebrow">More from our community archive</p><h2>Habitat Vet Build.</h2><p>Explore the existing BBLO-sponsored build archive and Habitat for Humanity of Marion County contact information.</p>'+link('/bblo/community-impact/habitat-vet-build/','Open the Habitat album','button secondary'))
write('/bblo/community-impact/','Our Community Impact','BBLO community visits, local causes, photos, videos and organization contact information.',body,True,cover(community[0])['src'])

# Keep the approved portfolio photographs, including its Debbie and Carmen image.
portfolio=ROOT/'events/unstoppable-2026/index.html'
s=portfolio.read_text();s=re.sub(r'<!-- expanded-gallery-start -->.*?<!-- expanded-gallery-end -->','',s,flags=re.S)
cta='<!-- expanded-gallery-start -->'+section('<p class="eyebrow">More from Unstoppable 2026</p><h2>Explore the photo &amp; video gallery.</h2><p>See more guest moments, stage photographs, event details and short video clips.</p>'+link('/events/unstoppable-2026/gallery/','Open the event gallery'))+'<!-- expanded-gallery-end -->'
s=s.replace('<section class="dark">',cta+'<section class="dark">',1);portfolio.write_text(s)
print('Built Unstoppable gallery, four selected community albums and three selected meeting albums.')
