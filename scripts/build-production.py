"""Promote approved preview HTML to production routes after launch approval.

Run with --output pointing to a staging directory. Copy the existing assets
tree unchanged alongside the generated pages when publishing.
"""
import argparse
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]

def build(source, output):
    routes = []
    for page in sorted(source.rglob('index.html')):
        relative = page.relative_to(source)
        if relative == Path('index.html'):
            continue
        target = Path('index.html') if relative == Path('home/index.html') else relative
        text = page.read_text().replace('/website-preview/', '/')
        text = text.replace('/home/', '/')
        text = re.sub(r'<meta name="robots" content="[^"]*">',
                      '<meta name="robots" content="index,follow,max-image-preview:large">', text)
        route = '/' if target == Path('index.html') else '/' + target.parent.as_posix() + '/'
        text = re.sub(r'<link rel="canonical" href="[^"]+">',
                      '<link rel="canonical" href="https://doitwithtlc.com' + route + '">', text)
        text = re.sub(r'<meta property="og:url" content="[^"]+">',
                      '<meta property="og:url" content="https://doitwithtlc.com' + route + '">', text)
        member_profile = relative.parts[:2] == ('bblo', 'members') and len(relative.parts) > 3
        if member_profile:
            # Direct member contact details are held back from this launch.
            text = re.sub(r'<dl class="contact-list">.*?</dl>', '', text, flags=re.S)
            text = text.replace('<h3>Connect directly.</h3>', '<h3>Explore their business.</h3>')
            text = re.sub(r'<p class="note">Business contact information supplied.*?</p>',
                          '<p class="note">Visit the available business website or social pages to learn more.</p>', text)
            text = text.replace('content="index,follow,max-image-preview:large"', 'content="noindex,follow"')
        # Native navigation must expose the new pages even with JavaScript disabled.
        for menu, href, label in [
            ('carmen-dropdown', '/cafecito-with-carmen/', 'Cafecito with Carmen'),
            ('tlc-dropdown', '/local-business-spotlights/', 'Local Business Spotlights &amp; Nominations'),
            ('bblo-dropdown', '/bblo/benefits/', 'Membership Benefits &amp; Pricing'),
            ('bblo-dropdown', '/bblo/chapters/', 'Bring BBLO to Your Community'),
        ]:
            pattern = r'(<details class="nav-dropdown ' + menu + r'".*?<div class="dropdown-links">)(.*?)(</div></details>)'
            def add_link(match):
                body = match[2]
                if 'href="' + href + '"' not in body:
                    body += '<a href="' + href + '">' + label + '</a>'
                return match[1] + body + match[3]
            text = re.sub(pattern, add_link, text, flags=re.S)
        destination = output / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text)
        if not member_profile:
            routes.append(route)
    # Preserve the independently maintained Cafecito editorial routes on promotion.
    import shutil
    blog = ROOT / 'cafecito-with-carmen'
    if blog.exists():
        for article in blog.rglob('index.html'):
            relative = article.relative_to(ROOT)
            destination = output / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if article.resolve() != destination.resolve():
                shutil.copy2(article, destination)
            routes.append('/' + relative.parent.as_posix() + '/')
    alias = output / 'home/index.html'
    alias.parent.mkdir(parents=True, exist_ok=True)
    alias.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="https://doitwithtlc.com/"><meta http-equiv="refresh" content="0;url=/"><title>The Liaison Companies</title></head><body><a href="/">Visit The Liaison Companies</a></body></html>')
    (output / 'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /website-preview/\nSitemap: https://doitwithtlc.com/sitemap.xml\n')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += ''.join('<url><loc>' + escape('https://doitwithtlc.com' + route) + '</loc></url>\n' for route in sorted(routes))
    (output / 'sitemap.xml').write_text(sitemap + '</urlset>\n')
    return routes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=ROOT / 'website-preview')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    print(json.dumps({'pages': len(build(args.source, args.output)), 'output': str(args.output)}))
