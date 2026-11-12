"""Render the approved public event ledger as crawlable HTML alongside the calendar."""
import json
import re
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from event_pages import build as build_event_pages, event_route

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- published-event-agenda:start -->'
END = '<!-- published-event-agenda:end -->'

def render(events, category=None):
    rows = []
    for event in events:
        if event.get('published') is not True or (category and event.get('category') != category):
            continue
        start = datetime.fromisoformat(event['start']).astimezone(ZoneInfo('America/New_York'))
        end = datetime.fromisoformat(event['end']).astimezone(ZoneInfo('America/New_York')) if event.get('end') else None
        label = start.strftime('%B %-d, %Y · %-I:%M %p %Z')
        if event.get('date_only'):
            label = start.strftime('%B %-d, %Y') + ' · Deadline date; closing hour not announced'
        if end:
            label += '–' + end.strftime('%-I:%M %p %Z' if end.date() == start.date() else '%B %-d, %Y · %-I:%M %p %Z')
        if event.get('end_time_pending'):
            label += ' · End time: TBD'
        title = escape(event['title'])
        url = event_route(event)
        if url:
            title = '<a href="' + escape(url, quote=True) + '">' + title + '</a>'
        place = ' · '.join(str(event.get(key) or '') for key in ('location', 'address') if event.get(key))
        rows.append((start, '<li><h3>' + title + '</h3><p><time datetime="'
                     + escape(event['start'], quote=True) + '">' + escape(label)
                     + '</time><br>' + escape(place) + '</p></li>'))
    if not rows:
        content = '<p>Confirmed visits will appear here when published.</p>'
    else:
        content = '<ul>' + ''.join(row for _, row in sorted(rows, key=lambda item: item[0])) + '</ul>'
    return (START + '<section aria-labelledby="published-agenda-title"><div class="wrap">'
            '<details><summary id="published-agenda-title">Published event dates at a glance</summary>'
            '<p>Browse the published dates below, including past events. Use the calendar above for filters and upcoming events. '
            'Each event has its own detail page with organizer information. <a href="/community-events/archive/">Browse past events</a>.</p>' + content
            + '</details></div></section>' + END)

def build(root=ROOT):
    build_event_pages(root)
    events = json.loads((root / 'data/bblo-events.json').read_text())['events']
    for route, category in [('bblo/events/index.html', None), ('bblo/field-trip-friday/index.html', 'field-trip')]:
        page = root / route
        text = page.read_text()
        agenda = render(events, category)
        if START in text:
            text, count = re.subn(re.escape(START) + r'.*?' + re.escape(END), lambda _: agenda, text, flags=re.S)
        elif category is None:
            anchor = '<section id="submit-event"'
            count = text.count(anchor)
            text = text.replace(anchor, agenda + anchor, 1)
        else:
            count = text.count('</main>')
            text = text.replace('</main>', agenda + '</main>', 1)
        if count != 1:
            raise ValueError('Expected exactly one agenda location: ' + route)
        page.write_text(text)

if __name__ == '__main__':
    build()
    import runpy
    runpy.run_path(str(ROOT / 'scripts/check-seo.py'))['write_sitemap'](ROOT)
    print('Event pages, archives, agendas and sitemap refreshed from the shared calendar data.')
