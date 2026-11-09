"""Check public profile publication, contact boundaries and advertising disclosures."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import runpy
import tempfile
import shutil

ROOT=Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self,text):
        super().__init__();self.links=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.links.append(dict(attrs))

members=json.loads((ROOT/'data/bblo-members.json').read_text())
approved=json.loads((ROOT/'data/bblo-public-profiles.json').read_text())
for member in members:
    text=(ROOT/'bblo/members'/member['slug']/'index.html').read_text()
    assert 'content="index,follow,max-image-preview:large"' in text,member['slug']
    assert text.count('<h1>')==1,member['slug']
    assert '/bblo/profile-update/?member='+member['slug'] in text
    if member['email'] and member['email']!=approved[member['slug']].get('email'):
        assert member['email'] not in text,member['slug']+': private email exposed'
    for link in Links(text).links:
        if link.get('href','').startswith(('https://','http://')) and 'doitwithtlc.com' not in link['href']:
            # Navigation scheduling links are not member advertising.
            if 'calendar.app.google' in link['href'] or 'clientclub.net' in link['href']:continue
            # Shared site social links are editorial navigation, not a member placement.
            if 'instagram.com/doitwithtlc' in link['href'] or 'facebook.com/doitwithtlc' in link['href']:continue
            assert 'sponsored' in link.get('rel','').split(),(member['slug'],link)
    for schema in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):
        obj=json.loads(schema)
        assert 'aggregateRating' not in obj

legacy=(ROOT/'bblo/members/legacy-insurance/index.html').read_text()
assert 'ocalainsurancegroup.com' not in legacy.lower()
update=(ROOT/'bblo/profile-update/index.html').read_text()
assert 'content="noindex,follow"' in update
assert 'publish_permission' in update

build=runpy.run_path(str(ROOT/'scripts/build-public-members.py'))['build']
targets=[ROOT/'bblo/members/index.html',ROOT/'bblo/benefits/index.html',ROOT/'bblo/partners/index.html',ROOT/'index.html']+[ROOT/'bblo/members'/m['slug']/'index.html' for m in members]
before=[p.read_bytes() for p in targets];build();assert before==[p.read_bytes() for p in targets],'Build changed on repeat'

# Exercise actual paid-placement rendering without activating an advertiser.
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp)
    for folder in ['data','bblo/members','bblo/benefits','bblo/partners']:
        shutil.copytree(ROOT/folder,root/folder,dirs_exist_ok=True)
    shutil.copy2(ROOT/'index.html',root/'index.html')
    path=root/'data/bblo-advertising.json'
    def config(entries):path.write_text(json.dumps({'placements':entries}))
    config([{'location':'directory','member_slug':'mj-photography','status':'approved','label':'Sponsored','start':'2020-01-01T00:00:00-05:00','end':'2099-01-01T00:00:00-05:00'}])
    build(root);text=(root/'bblo/members/index.html').read_text()
    assert 'class="card paid-member"' in text and '>Sponsored<' in text
    assert text.index('class="card paid-member"')<text.index('Member business directory')
    config([{'location':'homepage','member_slug':'mj-photography','status':'approved','label':'Sponsored','start':'2020-01-01T00:00:00-05:00','end':'2099-01-01T00:00:00-05:00'}])
    build(root);home=(root/'index.html').read_text()
    assert 'class="card paid-member"' in home and '/assets/bblo/members-public.js?' in home
    config([{'location':'directory','member_slug':'mj-photography','status':'approved','label':'Sponsored','start':'2020-01-01T00:00:00-05:00','end':'2021-01-01T00:00:00-05:00'}])
    build(root);assert 'class="card paid-member"' not in (root/'bblo/members/index.html').read_text()
    config([{'location':'directory','member_slug':'mj-photography','status':'draft','label':'Featured','start':'2020-01-01T00:00:00-05:00','end':'2099-01-01T00:00:00-05:00'}])
    try:build(root)
    except ValueError:pass
    else:raise AssertionError('Undisclosed/unapproved ad accepted')
print('17 public profiles: indexing, structured data, contact boundaries, disclosures and repeat-build checks passed. Paid placement and expiry checks passed.')
