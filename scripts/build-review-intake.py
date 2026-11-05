"""Keep reviews separate from service inquiries in preview and production."""
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]
FORM = 'https://api.leadconnectorhq.com/widget/form/bXcB7ATkN8KrFWchQdL2'
VERSION = '20261105-reviews'

def invitation(prefix, bblo=False):
    heading = 'A connection worth talking about?' if bblo else 'Got a little love to share?'
    body = ('A welcoming first visit, a useful introduction or something you learned—tell us about your BBLO experience.' if bblo else 'Worked with TLC or connected through BBLO? We’d love to hear what the experience was like, in your own words.')
    return f'<section class="testimonial-invite review-invite" id="share-review"><div class="wrap"><p class="eyebrow">Reviews &amp; testimonials</p><h2>{heading}</h2><p>{body}</p><p>English or Spanish welcome. You choose whether we may share your words publicly.</p><a class="button" href="{prefix}/share-your-experience/">Share my experience →</a></div></section>'

def navigation(s, prefix):
    contact = f'<a href="{prefix}/contact/">Contact</a>'
    menu = f'<details class="nav-dropdown contact-dropdown"><summary>Contact Us <span aria-hidden="true">⌄</span></summary><div class="dropdown-links"><a href="{prefix}/contact/">Let’s connect</a><a href="{prefix}/share-your-experience/">Share a little love · Reviews &amp; Testimonials</a></div></details>'
    s = s.replace(contact, menu)
    pattern = r'(<details class="nav-dropdown bblo-dropdown".*?<div class="dropdown-links">)(.*?)(</div></details>)'
    def add(m):
        link = f'<a href="{prefix}/share-your-experience/">Share Your BBLO Experience</a>'
        return m[1] + m[2] + ('' if link in m[2] else link) + m[3]
    return re.sub(pattern, add, s, flags=re.S)

def build(root, prefix):
    contact = root/'contact/index.html'
    if not contact.exists():
        return
    template = contact.read_text()
    main = f'''<main id="main" data-page="/share-your-experience/"><section class="hero"><div class="wrap"><p class="eyebrow">TLC &amp; BBLO · Reviews &amp; testimonials</p><h1>Your experience.<br><em>Your words.</em></h1><p class="lead">A door opened. An event brought to life. A connection that mattered.</p><p>Tell us about your experience with The Liaison Companies or BBLO. A few honest sentences are all it takes. English or Spanish welcome.</p><a class="button" href="#review-form">Let’s hear it →</a></div></section><section id="review-form"><div class="wrap" style="max-width:900px"><h2>Tell us how it went.</h2><p>Check TLC, BBLO or both. For TLC, choose the service you’re reviewing. Your email stays private. Sharing your review publicly is optional and always requires our review and approval.</p><p><a class="text-link" href="{FORM}">Open the review form in its own page →</a></p><iframe src="{FORM}" title="Share a review or testimonial for TLC or BBLO" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" style="display:block;width:100%;height:1600px;border:0;border-radius:12px;background:#fff"></iframe><p>Need help? <a href="mailto:carmen@doitwithtlc.com?subject=Website%20review">Email Carmen</a>.</p></div></section></main>'''
    page = re.sub(r'<main\b.*?</main>', lambda _: main, template, flags=re.S)
    page = re.sub(r'<title>.*?</title>', '<title>Share Your Experience | TLC &amp; BBLO Reviews</title>', page)
    desc = 'Share your first-hand review or testimonial for The Liaison Companies or BBLO. Choose the service, write your experience and set your sharing permission.'
    page = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*(")', lambda m:m[1]+desc+m[2], page)
    page = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m:m[1]+'Share Your Experience | TLC &amp; BBLO'+m[2], page)
    page = page.replace('https://doitwithtlc.com'+prefix+'/contact/', 'https://doitwithtlc.com'+prefix+'/share-your-experience/')
    page = navigation(page, prefix)
    page = re.sub(r'(/assets/site\.js)(?:\?v=[^"\s]+)?', r'\1?v='+VERSION, page)
    out = root/'share-your-experience/index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)

    for route in ['contact','client-stories','bblo','bblo/testimonials','inquire']:
        p = root/route/'index.html'
        if not p.exists():
            continue
        s = p.read_text()
        s = navigation(s, prefix)
        s = s.replace(f'{prefix}/inquire/?service=feedback', f'{prefix}/share-your-experience/')
        if route == 'client-stories':
            s = s.replace('Have private feedback or a concern? You can use the same email and mark it private.', 'Prefer to keep your feedback private? Leave the publication permission unchecked on the review form.')
        if route in ['contact','bblo','bblo/testimonials','inquire'] and 'id="share-review"' not in s:
            s = s.replace('<section class="carmen-trail"', invitation(prefix, route.startswith('bblo'))+'<section class="carmen-trail"', 1)
        if route == 'inquire' and 'get("service")==="feedback"' not in s:
            s = s.replace('<head>', f'<head><script>if(new URLSearchParams(location.search).get("service")==="feedback")location.replace("{prefix}/share-your-experience/"+location.hash);</script>', 1)
        s = re.sub(r'(/assets/site\.js)(?:\?v=[^"\s]+)?', r'\1?v='+VERSION, s)
        p.write_text(s)

if __name__ == '__main__':
    build(REPO/'website-preview', '/website-preview')
    # Production is generated from preview by build-production.py. Updating a
    # retained production checkout here also keeps bounded review edits in sync.
    build(REPO, '')
