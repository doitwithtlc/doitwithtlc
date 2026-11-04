"""Validate the review site's navigation, branding, metadata and safe preview state."""
from pathlib import Path
from html.parser import HTMLParser
import argparse, json, re
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--remote-tree');args=parser.parse_args()
remote=set()
if args.remote_tree:remote={e['path'] for e in json.loads(Path(args.remote_tree).read_text())['tree'] if e['type']=='blob'}
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=set();self.links=[];self.images=[];self.h1=0;self.parse_errors=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):
   if a['id'] in self.ids:self.parse_errors.append('duplicate id '+a['id'])
   self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='a':self.links.append(a.get('href',''))
  if tag=='img':self.images.append(a)
pages={p:Page(p.read_text()) for p in (ROOT/'website-preview').rglob('index.html')}
errors=[]
for p,page in pages.items():
 if p==ROOT/'website-preview/index.html':continue
 s=p.read_text()
 for error in page.parse_errors:errors.append(f'{p.relative_to(ROOT)}: {error}')
 if page.h1!=1:errors.append(f'{p}: expected one h1')
 if 'noindex' not in s:errors.append(f'{p}: preview noindex missing')
 if s.count('class="carmen-trail"')!=1:errors.append(f'{p}: expected one silhouette section')
 if 'id="site-nav"' not in s:errors.append(f'{p}: navigation control missing')
 if not re.search('<title>.+?</title>',s):errors.append(f'{p}: missing title')
 for image in page.images:
  if 'alt' not in image:errors.append(f'{p}: image missing alt')
 for link in page.links:
  if not link or link.startswith(('http:','https:','mailto:','tel:')):continue
  parts=link.split('#',1);path=parts[0].split('?',1)[0]
  target=ROOT/path.lstrip('/') if path.startswith('/') else (p.parent/path if path else p)
  if path.endswith('/') or target.is_dir():target=target/'index.html'
  if target not in pages and not target.exists() and str(target.relative_to(ROOT)) not in remote:errors.append(f'{p.relative_to(ROOT)}: missing target {link}');continue
  if len(parts)>1 and parts[1] and target in pages and parts[1] not in pages[target].ids:errors.append(f'{p.relative_to(ROOT)}: missing anchor {link}')
 for match in re.finditer('<script type="application/ld\\+json">(.*?)</script>',s,re.S):
  try:json.loads(match[1])
  except ValueError:errors.append(f'{p}: invalid structured data')
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(pages)-1} content pages, internal links/anchors, image alternatives, one h1, JSON-LD and preview protection.')
