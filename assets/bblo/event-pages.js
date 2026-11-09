'use strict';
// Calendar data is the single source. Live status changes do not wait for a rebuild.
(()=>{
 const route=e=>'/community-events/'+encodeURIComponent(e.id)+'/';
 const localDay=d=>new Intl.DateTimeFormat('en-CA',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(d));
 const active=(e,now)=>!['cancelled','canceled','postponed'].includes(e.status)&&(e.end?new Date(e.end)>=now:localDay(e.start)>=localDay(now));
 const status=(e,now)=>['cancelled','canceled'].includes(e.status)?'Event cancelled':e.status==='postponed'?'Event postponed':!active(e,now)?'Event has ended':new Date(e.start)<=now?(e.end?'Happening now':'Scheduled today'):'Upcoming event';
 const el=(tag,text)=>{const n=document.createElement(tag);if(text)n.textContent=text;return n;};
 const date=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',month:'long',day:'numeric',year:'numeric',hour:'numeric',minute:'2-digit',timeZoneName:'short'});
 const card=e=>{const article=el('article');article.className='event-related-card';const h=el('h3'),a=el('a',e.title);a.href=route(e);h.append(a);article.append(h,el('p',date.format(new Date(e.start))),el('p',e.location));return article;};
 let events=[];
 function refresh(){
  const now=new Date(),detail=document.querySelector('[data-event-id]'),current=detail&&events.find(e=>e.id===detail.dataset.eventId);
  if(current){const label=status(current,now),badge=document.querySelector('[data-event-state]');badge.textContent=label;badge.dataset.ended=String(!active(current,now));document.querySelectorAll('[data-upcoming-action]').forEach(n=>n.hidden=!active(current,now));}
  const related=document.querySelector('[data-related-events]');
  if(related){const list=events.filter(e=>active(e,now)&&(!current||e.id!==current.id)).sort((a,b)=>(current?Number(a.category!==current.category)-Number(b.category!==current.category):0)||new Date(a.start)-new Date(b.start)).slice(0,3);related.replaceChildren(...list.map(card));if(!list.length)related.append(el('p','Explore the community calendar for newly announced dates.'));}
  const archive=document.querySelector('[data-event-archive]');if(archive)archive.replaceChildren(...events.filter(e=>!active(e,now)).sort((a,b)=>new Date(b.start)-new Date(a.start)).map(card));
 }
 fetch('/data/bblo-events.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error('Calendar unavailable');return r.json();}).then(data=>{events=data.events.filter(e=>e.published===true);refresh();setInterval(refresh,60000);}).catch(()=>{/* Crawlable HTML remains available if the connection fails. */});
})();
