function initializeInquiry() {
 const form=document.getElementById('tlc-inquiry'); if(!form)return;
 const service=form.elements.service,box=document.getElementById('inquiry-review');
 const update=()=>{document.querySelectorAll('.service-fields').forEach(group=>{const show=group.dataset.service===service.value;group.hidden=!show;group.querySelectorAll('input,select,textarea').forEach(control=>control.disabled=!show);});box.hidden=true;};
 const preset=new URLSearchParams(location.hash.includes('?')?location.hash.split('?')[1]:location.search).get('service');
 if([...service.options].some(o=>o.value===preset))service.value=preset;
 service.addEventListener('change',update);update();
 const review=()=>{
  if(!form.reportValidity())return;
  box.replaceChildren();const title=document.createElement('h3');title.textContent='Review your inquiry';box.append(title);
  const answers=[];
  for(const [name,value] of new FormData(form)){
   if(!value||name==='contact_permission')continue;
   const control=form.elements.namedItem(name);
   const label=control?.id?form.querySelector('label[for="'+control.id+'"]'):null;
   const answer=control?.tagName==='SELECT'?control.selectedOptions[0].textContent:String(value);
   const line=(label?label.textContent:name)+': '+answer;
   answers.push(line);const p=document.createElement('p');p.textContent=line;box.append(p);
  }
  answers.push('Permission: TLC may contact me about this inquiry.');
  const address=service.value.startsWith('bblo-')?'bblocala@gmail.com':'carmen@doitwithtlc.com',body=answers.join('\n\n');
  const actions=document.createElement('div');actions.className='email-actions';
  const email=document.createElement('a');email.className='button';email.textContent='Open email draft';
  email.href='mailto:'+address+'?subject='+encodeURIComponent('Website inquiry — '+service.selectedOptions[0].textContent)+'&body='+encodeURIComponent(body);
  const copy=document.createElement('button');copy.type='button';copy.className='button secondary';copy.textContent='Copy inquiry';
  const status=document.createElement('p');status.className='copy-status';status.setAttribute('role','status');
  copy.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(body);status.textContent='Copied. Paste your inquiry into an email to '+address+'.';}catch{status.textContent='Select and copy the answers above, then email '+address+'.';}});
  actions.append(email,copy);box.append(actions,status);
  const note=document.createElement('p');note.textContent='Your email app will open with your answers. Review the message, attach any photos and press Send there. Nothing has been sent by this page.';box.append(note);
  const direct=document.createElement('p');direct.append('Using webmail? Copy your inquiry and send it to ');
  const contact=document.createElement('a');contact.href='mailto:'+address;contact.textContent=address;direct.append(contact,'.');box.append(direct);
  box.hidden=false;box.focus();box.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
 };
 form.addEventListener('submit',event=>{event.preventDefault();review();});
 document.getElementById('review-inquiry').addEventListener('click',review);
 form.addEventListener('input',()=>{box.hidden=true;});
}
function initializeNavigation(){
 const nav=document.getElementById('site-nav'),toggle=document.querySelector('.nav-toggle');if(!nav||!toggle)return;
 const media=matchMedia('(max-width:760px)');
 const setOpen=open=>{nav.hidden=!open;nav.classList.toggle('mobile-open',open);toggle.setAttribute('aria-expanded',String(open));};
 const sync=()=>setOpen(!media.matches);
 sync();media.addEventListener('change',sync);
 toggle.addEventListener('click',()=>setOpen(nav.hidden));
 document.addEventListener('keydown',event=>{if(event.key==='Escape'&&media.matches&&!nav.hidden){setOpen(false);toggle.focus();}});
}
document.addEventListener('DOMContentLoaded',()=>{initializeInquiry();initializeNavigation();document.querySelectorAll('nav a').forEach(a=>{if(a.pathname===location.pathname&&!a.hash)a.setAttribute('aria-current','page');});});
document.addEventListener('click',event=>{document.querySelectorAll('header details[open]').forEach(menu=>{if(!menu.contains(event.target))menu.open=false;});});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){document.querySelectorAll('header details[open]').forEach(menu=>{menu.open=false;menu.querySelector('summary').focus();});}});

// Explicit pause control for the networking photo strip.
document.addEventListener("click",event=>{const button=event.target.closest("[data-pause-strip]");if(!button)return;const strip=button.closest(".networking-strip");const paused=strip.classList.toggle("is-paused");button.setAttribute("aria-pressed",String(paused));button.textContent=paused?"Resume photo motion":"Pause photo motion";});

// Keep discovery links available on existing pages without changing member records.
document.addEventListener('DOMContentLoaded',()=>{
 const prefix=location.pathname.startsWith('/website-preview/')?'/website-preview':'';
 for(const [menu,path,label] of [['.tlc-dropdown .dropdown-links','/local-business-spotlights/','Local Business Spotlights & Nominations'],['.bblo-dropdown .dropdown-links','/bblo/benefits/','Membership Benefits & Pricing'],['.bblo-dropdown .dropdown-links','/bblo/chapters/','Bring BBLO to Your Community']]){
  const box=document.querySelector(menu);if(box&&!box.querySelector('a[href="'+prefix+path+'"]')){const link=document.createElement('a');link.href=prefix+path;link.textContent=label;box.append(link);}
 }
});

// Direct BBLO visitor registration from every shared navigation menu.
document.addEventListener('DOMContentLoaded',()=>{const box=document.querySelector('.bblo-dropdown .dropdown-links');if(box&&!box.querySelector('a[href="https://api.leadconnectorhq.com/widget/form/EWkYWRPYI3SPRLjEPzYo"]')){const link=document.createElement('a');link.href='https://api.leadconnectorhq.com/widget/form/EWkYWRPYI3SPRLjEPzYo';link.textContent='Ready to Visit?';box.prepend(link);}});

 // BBLO announcements and one consolidated photo archive.
 document.addEventListener('DOMContentLoaded',()=>{
 const prefix=location.pathname.startsWith('/website-preview/')?'/website-preview':'';
 document.querySelectorAll('a[href="'+prefix+'/bblo/community-impact/"]').forEach(a=>{
 if(a.closest('nav'))a.remove();else{a.href=prefix+'/bblo/gallery/';if(/community impact/i.test(a.textContent))a.textContent='BBLO in Action';}
 });
 document.querySelectorAll('.bblo-dropdown .dropdown-links,.bblo-subnav').forEach(box=>{
 for(const [path,label] of [['/bblo/field-trip-friday/','Field Trip Friday']]){
 if(!box.querySelector('a[href="'+prefix+path+'"]')){const a=document.createElement('a');a.href=prefix+path;a.textContent=label;box.append(a);}
 }
 });
 });
// Expose the community calendar directly in the main desktop and mobile menu.
document.addEventListener('DOMContentLoaded',()=>{
 const prefix=location.pathname.startsWith('/website-preview/')?'/website-preview':'';
 const nav=document.getElementById('site-nav');if(!nav)return;
 document.querySelectorAll('.bblo-dropdown a[href="'+prefix+'/bblo/events/"]').forEach(a=>a.remove());
 let link=nav.querySelector(':scope > a[data-community-calendar]');
 if(!link){link=document.createElement('a');link.dataset.communityCalendar='';nav.prepend(link);}
 link.href=prefix+'/bblo/events/';link.textContent='Community Event Calendar';
 if(link.pathname===location.pathname)link.setAttribute('aria-current','page');
 document.querySelectorAll('.bblo-subnav a[href="'+prefix+'/bblo/events/"]').forEach(a=>a.textContent='Community Event Calendar');
});
