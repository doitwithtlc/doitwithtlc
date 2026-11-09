"""Validate production discovery; use --write-sitemap to refresh canonical URLs."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://doitwithtlc.com'
# Utility experiences do not need organic-search landing pages.
UTILITY = {'/app/', '/bblo/check-in/', '/share-your-experience/'}

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.meta, self.canonical, self.links, self.schemas = {}, [], [], []
        self.h1 = self.missing_alt = 0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            self.meta[a.get('name', a.get('property', ''))] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a.get('href'))
        if tag == 'h1': self.h1 += 1
        if tag == 'img' and 'alt' not in a: self.missing_alt += 1
        if tag == 'a': self.links.append(a.get('href', ''))
        if tag in ('img', 'script', 'iframe'): self.links.append(a.get('src', ''))
        if tag == 'link' and a.get('rel') == 'stylesheet': self.links.append(a.get('href', ''))

def inspect(root):
    pages = {}
    for file in sorted(root.rglob('index.html')):
        if 'website-preview' in file.relative_to(root).parts or '.git' in file.parts:
            continue
        route = '/' if file.parent == root else '/' + file.parent.relative_to(root).as_posix() + '/'
        pages[route] = Page(file.read_text())
    return pages

def write_sitemap(root):
    pages = inspect(root)
    urls = sorted(route for route, p in pages.items() if route not in UTILITY
            and 'noindex' not in p.meta.get('robots', '').lower()
            and p.canonical == [ORIGIN + route])
    (root / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join('<url><loc>' + escape(ORIGIN + route) + '</loc></url>\n' for route in urls)
        + '</urlset>\n')

def validate(root):
    pages = inspect(root)
    sitemap = {urlsplit(e.text).path for e in ET.parse(root / 'sitemap.xml').iter()
               if e.tag.endswith('loc')}
    errors = []
    for route in sitemap:
        p = pages.get(route)
        if p is None or 'noindex' in p.meta.get('robots', '').lower():
            errors.append(route + ': sitemap contains missing or noindex page')
        elif p.canonical != [ORIGIN + route]:
            errors.append(route + ': sitemap canonical mismatch')
    for route, p in pages.items():
        if 'noindex' not in p.meta.get('robots', '').lower() and route not in UTILITY:
            if route not in sitemap: errors.append(route + ': missing from sitemap')
            if p.h1 != 1: errors.append(route + ': expected one H1')
            if not p.meta.get('description'): errors.append(route + ': missing description')
            if p.missing_alt: errors.append(route + ': image missing alt attribute')
        for link in p.links:
            u = urlsplit(link)
            if not link or u.scheme or u.netloc or link.startswith('#'): continue
            target = root / unquote(urlsplit(urljoin(route, link)).path).lstrip('/')
            if target.is_dir(): target /= 'index.html'
            if not target.exists(): errors.append(route + ': broken local link ' + link)
    return {'pages': len(pages), 'sitemap_urls': len(sitemap), 'errors': errors}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--write-sitemap', action='store_true')
    args = parser.parse_args()
    if args.write_sitemap: write_sitemap(args.root)
    result = validate(args.root)
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['errors']))
