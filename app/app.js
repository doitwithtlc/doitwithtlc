'use strict';
const $=s=>document.querySelector(s);
const views=['home','events','saved','bblo','tlc'];
let events=[],loadState='loading',deferredInstall=null,storageAvailable=true;
let saved=[];try{const raw=JSON.parse(localStorage.getItem('tlc-saved-events')||'[]');saved=Array.isArray(raw)?raw.filter(v=>typeof v==='string'):[];}catch{storageAvailable=false;}
const escapeHTML=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeURL=v=>{if(typeof v!=='string'||!v.trim())return null;try{const u=new URL(v,location.origin);return ['https:','http:'].includes(u.protocol)?u.href:null;}catch{return null;}};
const format=(value,opts)=>new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',...opts}).format(new Date(value));
function toast(message){$('#toast').textContent=message;$('#toast').hidden=false;clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('#toast').hidden=true,4000);}
function route(focus=false){const view=location.hash.slice(1);const active=views.includes(view)?view:'home';document.querySelectorAll('[data-view]').forEach(el=>el.hidden=el.dataset.view!==active);document.querySelectorAll('.bottom-nav a').forEach(a=>{if(a.hash==='#'+active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});document.title=({home:'Your local connection',events:'Community calendar',saved:'Saved events',bblo:'Your BBLO',tlc:'Work with TLC'})[active]+' | TLC';if(focus){window.scrollTo(0,0);$('#main').focus({preventScroll:true});}}
// Blank/missing end means start-only; malformed or reversed explicit ends are rejected.
const missingEnd=e=>e.end==null||(typeof e.end==='string'&&!e.end.trim());
const validEvent=e=>e&&e.published===true&&typeof e.id==='string'&&typeof e.title==='string'&&typeof e.start==='string'&&Number.isFinite(Date.parse(e.start))&&(missingEnd(e)||(typeof e.end==='string'&&Number.isFinite(Date.parse(e.end))&&Date.parse(e.end)>Date.parse(e.start)));
const eventUpcoming=(e,now=Date.now())=>Date.parse(missingEnd(e)?e.start:e.end)>=now;
const eventLink=e=>sharePages.get(e.id)||safeURL(e.url);
const eventTime=e=>e.date_only?'Deadline date; closing hour not announced':format(e.start,{hour:'numeric',minute:'2-digit',...(missingEnd(e)?{timeZoneName:'short'}:{})})+(missingEnd(e)?'':'–'+format(e.end,{hour:'numeric',minute:'2-digit',timeZoneName:'short'}));
function card(e){const link=eventLink(e);const maps=e.address&&!e.virtual?'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(e.address):null;return `<article class="event-card"><div class="date">${format(e.start,{month:'short'})}<b>${format(e.start,{day:'numeric'})}</b><small>${format(e.start,{year:'numeric'})}</small></div><div><p class="category">${escapeHTML(e.category||'Community')}</p><h3>${escapeHTML(e.title)}</h3><p class="meta">${format(e.start,{weekday:'short',month:'short',day:'numeric'})} · ${eventTime(e)}</p><p class="meta">${escapeHTML(e.location||'See event details for location')}</p>${e.cost?`<p class="meta">${escapeHTML(e.cost)}</p>`:''}<p class="description">${escapeHTML(e.description||'')}</p>${e.opportunities?`<p class="description"><strong>Opportunities:</strong> ${escapeHTML(e.opportunities)}</p>`:''}<div class="event-actions">${link?`<a class="primary" href="${escapeHTML(link)}">${escapeHTML(e.cta||'Event details')} ↗</a>`:''}${maps?`<a href="${escapeHTML(maps)}">Directions ↗</a>`:''}<button type="button" data-save="${escapeHTML(e.id)}" aria-pressed="${saved.includes(e.id)}">${saved.includes(e.id)?'♥ Saved':'♡ Save'}</button><button type="button" data-ics="${escapeHTML(e.id)}">Add to calendar</button><button type="button" data-share="${escapeHTML(e.id)}" aria-label="Share ${escapeHTML(e.title)}">Share ↗</button></div></div></article>`;}
function empty(message){return `<div class="empty"><p>${escapeHTML(message)}</p><a href="#events">Explore the calendar →</a></div>`;}
function render(){const upcoming=events.filter(e=>eventUpcoming(e));let list=upcoming;const term=$('#search').value.toLowerCase().trim(),filter=$('#filter').value;if(term)list=list.filter(e=>[e.title,e.location,e.description,e.opportunities].join(' ').toLowerCase().includes(term));if(filter==='workshop')list=list.filter(e=>['workshop','training'].includes(e.category));else if(filter==='opportunities')list=list.filter(e=>Boolean(e.opportunities));else if(filter!=='all')list=list.filter(e=>e.category===filter);
const failure=loadState==='error'?'We couldn’t load current events. Check your connection and tap Refresh.':null;
$('#home-events').innerHTML=failure?empty(failure):upcoming.slice(0,2).map(card).join('')||empty('No upcoming events are published yet. Check back for new opportunities.');
$('#events-list').innerHTML=failure?empty(failure):list.map(card).join('')||empty('No published events match these filters. Try another search or category.');$('#event-count').textContent=failure?'Calendar unavailable':`${list.length} published event${list.length===1?'':'s'}`;
const savedEvents=upcoming.filter(e=>saved.includes(e.id));$('#saved-list').innerHTML=failure?empty(failure):savedEvents.map(card).join('')||empty(saved.length?'Your saved events have ended or are no longer published. Find your next connection on the calendar.':'Nothing saved yet. Tap Save on an event to keep it here.');}
async function load(){if(load.loading)return;load.loading=true;$('#refresh').disabled=true;try{const response=await fetch('/data/bblo-events.json',{cache:'no-store'});if(!response.ok)throw Error('Calendar unavailable');const data=await response.json();if(!Array.isArray(data.events))throw Error('Invalid calendar');events=data.events.filter(validEvent).sort((a,b)=>Date.parse(a.start)-Date.parse(b.start));loadState='ready';}catch{events=[];loadState='error';}finally{load.loading=false;$('#refresh').disabled=false;render();}}
function toggleSave(id){if(!storageAvailable){toast('Your browser is blocking saved events. Allow site storage to save on this device.');return;}const next=saved.includes(id)?saved.filter(x=>x!==id):[...saved,id];try{localStorage.setItem('tlc-saved-events',JSON.stringify(next));saved=next;render();toast(saved.includes(id)?'Saved on this device.':'Removed from saved events.');const button=[...document.querySelectorAll('section:not([hidden]) [data-save]')].find(b=>b.dataset.save===id);button?.focus();}catch{storageAvailable=false;toast('Your browser could not save this event.');}}
const icsEscape=s=>String(s||'').replace(/\\/g,'\\\\').replace(/\r?\n/g,'\\n').replace(/;/g,'\\;').replace(/,/g,'\\,');
const icsDate=s=>new Date(s).toISOString().replace(/[-:]/g,'').replace(/\.\d{3}/,'');
function foldICS(line){let result='',bytes=0;for(const char of line){const length=new TextEncoder().encode(char).length;if(bytes+length>75){result+='\r\n ';bytes=1;}result+=char;bytes+=length;}return result;}
function calendarContent(e){const lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//The Liaison Companies//TLC Events//EN','CALSCALE:GREGORIAN','BEGIN:VEVENT',`UID:${icsEscape(e.id)}@doitwithtlc.com`,`DTSTAMP:${icsDate(Date.now())}`,e.date_only?`DTSTART;VALUE=DATE:${e.start.slice(0,10).replace(/-/g,'')}`:`DTSTART:${icsDate(e.start)}`,...(missingEnd(e)?[]:[`DTEND:${icsDate(e.end)}`]),`SUMMARY:${icsEscape(e.title)}`,`LOCATION:${icsEscape(e.address||e.location)}`,`DESCRIPTION:${icsEscape((e.description||'')+'\n'+(eventLink(e)||''))}`,'END:VEVENT','END:VCALENDAR'];return lines.map(foldICS).join('\r\n')+'\r\n';}
function downloadCalendar(e){const url=URL.createObjectURL(new Blob([calendarContent(e)],{type:'text/calendar;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='tlc-event.ics';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}

// TLC share helpers: generated page links are discovered, never assumed from an ID.
const sharePages=new Map();
const publicCalendar='https://doitwithtlc.com/bblo/events/';
async function loadSharePages(){
  try{
    const response=await fetch('/bblo/events/',{cache:'no-store'});
    if(!response.ok)return;
    const doc=new DOMParser().parseFromString(await response.text(),'text/html');
    for(const a of doc.querySelectorAll('a[href^="/community-events/"]')){
      const path=a.getAttribute('href');
      const match=path.match(/^\/community-events\/([^/]+)\/$/);
      if(match)sharePages.set(decodeURIComponent(match[1]),new URL(path,'https://doitwithtlc.com').href);
    }
    if(loadState==='ready')render();
  }catch{/* Offline or ungenerated event: use source URL, then public calendar. */}
}
function shareDataFor(e){
  if(!e)return {title:'TLC Community Calendar',text:'Discover upcoming events in Ocala and Marion County.',url:publicCalendar};
  return {title:e.title,text:`${e.title}\n${format(e.start,{weekday:'short',month:'short',day:'numeric',...(e.date_only?{}:{hour:'numeric',minute:'2-digit',timeZoneName:'short'})})}${e.date_only?' · Closing hour not announced':''}\n${e.location||'See event details for location'}`,url:sharePages.get(e.id)||safeURL(e.url)||publicCalendar};
}
function shareLinks(data){
  const body=data.text+'\n'+data.url;
  const ios=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  return {text:'sms:'+(ios?'&':'?')+'body='+encodeURIComponent(body),email:'mailto:?subject='+encodeURIComponent(data.title)+'&body='+encodeURIComponent(body),facebook:'https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(data.url),whatsapp:'https://wa.me/?text='+encodeURIComponent(body)};
}
let activeShare=null,shareBusy=false;
function shareFallback(data){
  activeShare=data;
  $('#share-title').textContent=data.title;
  $('#share-url').value=data.url;
  const links=shareLinks(data);
  for(const [name,url] of Object.entries(links))$('#share-'+name).href=url;
  $('#share-status').textContent='Choose how to share. Nothing is sent until you confirm in the chosen app.';
  $('#share-dialog').showModal();
}
async function shareEvent(e){
  if(shareBusy)return;
  const data=shareDataFor(e);
  shareBusy=true;
  try{
    if(typeof navigator.share==='function'&&(typeof navigator.canShare!=='function'||navigator.canShare(data))){
      await navigator.share(data);
    }else shareFallback(data);
  }catch(error){if(error.name!=='AbortError')shareFallback(data);}
  finally{shareBusy=false;}
}
// End TLC share helpers.

document.addEventListener('click',event=>{if(event.target.closest('.skip')){event.preventDefault();$('#main').focus();return;}const share=event.target.closest('[data-share]');if(share){const entry=events.find(e=>e.id===share.dataset.share);if(entry)shareEvent(entry);}const save=event.target.closest('[data-save]');if(save)toggleSave(save.dataset.save);const calendar=event.target.closest('[data-ics]');if(calendar){const entry=events.find(e=>e.id===calendar.dataset.ics);if(entry)downloadCalendar(entry);}});
$('#search').addEventListener('input',render);$('#filter').addEventListener('change',render);$('#refresh').addEventListener('click',load);window.addEventListener('hashchange',()=>route(true));
function connection(){ $('#connection').hidden=navigator.onLine; }window.addEventListener('offline',connection);window.addEventListener('online',()=>{connection();load();});window.addEventListener('storage',e=>{if(e.key==='tlc-saved-events'){try{const value=JSON.parse(e.newValue||'[]');saved=Array.isArray(value)?value.filter(x=>typeof x==='string'):[];render();}catch{}}});
window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();deferredInstall=event;$('#native-install').hidden=false;});window.addEventListener('appinstalled',()=>{$('#install-dialog').close();deferredInstall=null;$('#native-install').hidden=true;$('.install').hidden=true;toast('TLC is ready on your home screen.');});$('.install').addEventListener('click',()=>$('#install-dialog').showModal());$('.close').addEventListener('click',()=>$('#install-dialog').close());$('#native-install').addEventListener('click',async()=>{if(!deferredInstall)return;await deferredInstall.prompt();await deferredInstall.userChoice;deferredInstall=null;$('#native-install').hidden=true;});if(matchMedia('(display-mode: standalone)').matches||navigator.standalone)$('.install').hidden=true;
if('serviceWorker'in navigator)navigator.serviceWorker.register('/app/sw.js',{scope:'/app/'}).catch(()=>{});
route();connection();load();


$('#share-calendar').addEventListener('click',()=>shareEvent());
$('#share-close').addEventListener('click',()=>$('#share-dialog').close());
$('#share-copy').addEventListener('click',async()=>{if(!activeShare)return;try{await navigator.clipboard.writeText(activeShare.url);$('#share-status').textContent='Link copied.';}catch{$('#share-url').focus();$('#share-url').select();$('#share-status').textContent='Select and copy the link above.';}});
loadSharePages();
