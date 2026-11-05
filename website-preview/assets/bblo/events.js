'use strict';
document.addEventListener('DOMContentLoaded',async()=>{
 const root=document.querySelector('[data-bblo-events]');if(!root)return;
 const prefix=location.pathname.startsWith('/website-preview/')?'/website-preview':'';
 const category=document.getElementById('event-category'),list=document.getElementById('event-list'),calendar=document.getElementById('event-calendar'),label=document.getElementById('event-month-label'),status=document.getElementById('event-status');
 const formatter=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',month:'long',day:'numeric',year:'numeric'});
 const time=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'2-digit'});
 const dateKey=d=>new Intl.DateTimeFormat('en-CA',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(d));
 const names={bblo:'BBLO Event',community:'Community Event','field-trip':'Field Trip Friday'};
 const safeUrl=value=>{try{let u=new URL(value,location.origin);return ['https:','http:'].includes(u.protocol)?u.href:'#';}catch{return '#';}};
 const el=(tag,text,className)=>{const n=document.createElement(tag);if(text)n.textContent=text;if(className)n.className=className;return n;};
 let events=[],month=new Date();month=new Date(month.getFullYear(),month.getMonth(),1);
 if(root.dataset.bbloEvents==='field-trip')category.value='field-trip';
 function render(){
 const selected=events.filter(e=>category.value==='all'||e.category===category.value);
 label.textContent=month.toLocaleDateString('en-US',{month:'long',year:'numeric'});
 const table=el('table',null,'event-calendar');table.setAttribute('aria-label',label.textContent+' event calendar');
 const head=el('thead'),tr=el('tr');['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].forEach(d=>{const th=el('th',d);th.scope='col';tr.append(th);});head.append(tr);table.append(head);
 const body=el('tbody'),first=month.getDay(),days=new Date(month.getFullYear(),month.getMonth()+1,0).getDate(),today=dateKey(new Date());
 for(let offset=0;offset<first+days;offset+=7){const row=el('tr');for(let col=0;col<7;col++){const cell=el('td'),day=offset+col-first+1;if(day>0&&day<=days){const key=month.getFullYear()+'-'+String(month.getMonth()+1).padStart(2,'0')+'-'+String(day).padStart(2,'0');cell.append(el('span',String(day)));if(key===today)cell.className='today';selected.filter(e=>dateKey(e.start)===key).forEach(e=>{const a=el('a',e.title);a.href='#event-'+e.id;cell.append(a);});}row.append(cell);}body.append(row);}table.append(body);calendar.replaceChildren(table);
 list.replaceChildren();const now=new Date();const upcoming=selected.filter(e=>new Date(e.end||e.start)>=now);
 status.textContent=upcoming.length?upcoming.length+' upcoming '+(upcoming.length===1?'event':'events'):'No upcoming '+(category.value==='field-trip'?'Field Trip Friday dates':'events')+' announced yet.';
 upcoming.forEach(e=>{const card=el('article',null,'event-card');card.id='event-'+e.id;card.append(el('p',names[e.category]||'BBLO Event','eyebrow'),el('h2',e.title),el('p',formatter.format(new Date(e.start))+' · '+time.format(new Date(e.start))+(e.end?'–'+time.format(new Date(e.end)):'')+' ET','event-meta'),el('p',e.location),el('p',e.description));if(e.url){const a=el('a',e.cta||'Event details','button');a.href=safeUrl(e.url);card.append(a);}const add=el('a','Add to my calendar','text-link');const compact=v=>new Date(v).toISOString().replace(/[-:]/g,'').replace(/\.\d{3}Z/,'Z');add.href='https://calendar.google.com/calendar/render?'+new URLSearchParams({action:'TEMPLATE',text:e.title,dates:compact(e.start)+'/'+compact(e.end||e.start),details:e.description+' '+(e.url||''),location:e.location});card.append(document.createTextNode(' '),add);list.append(card);});
 }
 document.getElementById('event-prev').addEventListener('click',()=>{month.setMonth(month.getMonth()-1);render();});
 document.getElementById('event-next').addEventListener('click',()=>{month.setMonth(month.getMonth()+1);render();});
 document.getElementById('event-upcoming').addEventListener('click',()=>{const e=events.find(e=>(category.value==='all'||e.category===category.value)&&new Date(e.start)>=new Date());if(e){const key=dateKey(e.start).split('-');month=new Date(Number(key[0]),Number(key[1])-1,1);}render();});
 category.addEventListener('change',render);
 try{const response=await fetch(prefix+'/data/bblo-events.json',{cache:'no-cache'});if(!response.ok)throw new Error('Unavailable');const data=await response.json();events=data.events.filter(e=>e.published===true).sort((a,b)=>new Date(a.start)-new Date(b.start));render();}catch{status.textContent='The calendar could not load. Please refresh or contact BBLO for event details.';}
});