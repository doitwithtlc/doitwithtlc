'use strict';
(() => {
  const origin = 'https://doitwithtlc.com';
  const make = (tag, text) => { const node = document.createElement(tag); if (text) node.textContent = text; return node; };
  const ios = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  function enhance(root) {
    const data = { title: root.dataset.shareTitle, text: root.dataset.shareText, url: root.dataset.shareUrl };
    const status = root.querySelector('[role="status"]');
    const sms = root.querySelector('[data-share-sms]');
    if (ios) sms.href = sms.getAttribute('href').replace('sms:?', 'sms:&');
    const native = root.querySelector('[data-share-native]');
    if (typeof navigator.share === 'function') {
      native.hidden = false;
      native.addEventListener('click', async () => {
        if (native.disabled) return;
        native.disabled = true; status.textContent = '';
        try { await navigator.share(data); }
        catch (error) { if (error.name !== 'AbortError') status.textContent = 'Choose one of the sharing options below, or copy the event link.'; }
        finally { native.disabled = false; }
      });
    }
    const copy = root.querySelector('[data-share-copy]');
    if (typeof navigator.clipboard?.writeText === 'function') {
      copy.hidden = false;
      copy.addEventListener('click', async () => {
        try { await navigator.clipboard.writeText(data.url); status.textContent = 'Event link copied.'; }
        catch { status.textContent = 'Select and copy the event link below.'; }
      });
    }
  }
  function create(event) {
    const root = make('details'); root.className = 'event-share';
    root.dataset.eventShare = ''; root.dataset.shareTitle = event.title;
    root.dataset.shareUrl = origin + '/community-events/' + encodeURIComponent(event.id) + '/';
    const date = new Intl.DateTimeFormat('en-US', {timeZone:'America/New_York',year:'numeric',month:'long',day:'numeric', ...(event.date_only ? {} : {hour:'numeric',minute:'2-digit',timeZoneName:'short'})});
    const when = date.format(new Date(event.start)) + (event.date_only ? ' · Deadline date; closing hour not announced' : event.end ? ' – ' + date.format(new Date(event.end)) : event.end_time_pending ? ' · End time: TBD' : '');
    root.dataset.shareText = [event.title, when, event.location, event.address].filter(Boolean).join('\n');
    root.append(make('summary', 'Share event'));
    const options = make('div'); options.className = 'event-share-options';
    const native = make('button','Share with an app'); native.type = 'button'; native.dataset.shareNative = ''; native.hidden = true; options.append(native);
    const url = root.dataset.shareUrl, text = root.dataset.shareText, body = text + '\n' + url;
    const links = [
      ['Text', 'sms:?' + new URLSearchParams({body})],
      ['Email', 'mailto:?' + new URLSearchParams({subject:event.title,body})],
      ['WhatsApp', 'https://wa.me/?' + new URLSearchParams({text:body})],
      ['Facebook', 'https://www.facebook.com/sharer/sharer.php?' + new URLSearchParams({u:url})],
      ['LinkedIn', 'https://www.linkedin.com/sharing/share-offsite/?' + new URLSearchParams({url})],
      ['X', 'https://twitter.com/intent/tweet?' + new URLSearchParams({text,url})]
    ];
    for (const [label, href] of links) {
      const link = make('a', label); link.href = href;
      if (label === 'Text') link.dataset.shareSms = '';
      if (href.startsWith('https:')) { link.target = '_blank'; link.rel = 'noopener noreferrer'; }
      options.append(link);
    }
    const copy = make('button','Copy link'); copy.type = 'button'; copy.dataset.shareCopy = ''; copy.hidden = true; options.append(copy); root.append(options);
    const permalink = make('p'); permalink.className = 'event-share-url'; const link = make('a', url); link.href = url; permalink.append(link); root.append(permalink);
    const status = make('p'); status.className = 'event-share-status'; status.setAttribute('role','status'); root.append(status);
    enhance(root); return root;
  }
  document.querySelectorAll('[data-event-share]').forEach(enhance);
  window.TlcEventShare = {create};
})();
