
function initializeInquiry(){
const form=document.getElementById('tlc-inquiry');if(!form)return;
const service=form.elements.service;
const update=()=>{document.querySelectorAll('.service-fields').forEach(group=>{const show=group.dataset.service===service.value;group.hidden=!show;group.querySelectorAll('input,select,textarea').forEach(control=>control.disabled=!show)});document.getElementById('inquiry-review').hidden=true;};
const preset=new URLSearchParams(location.hash.includes('?')?location.hash.split('?')[1]:location.search).get('service');if([...service.options].some(o=>o.value===preset))service.value=preset;
service.addEventListener('change',update);update();
form.addEventListener('submit',e=>e.preventDefault());
document.getElementById('review-inquiry').addEventListener('click',()=>{if(!form.reportValidity())return;const box=document.getElementById('inquiry-review');box.replaceChildren();const title=document.createElement('h3');title.textContent='Your inquiry summary';box.append(title);[...new FormData(form)].forEach(([name,value])=>{if(!value||name==='contact_permission')return;const p=document.createElement('p');const label=form.querySelector('label[for="'+name+'"]');p.textContent=(label?label.textContent:name)+': '+(name==='service'?service.selectedOptions[0].textContent:value);box.append(p)});const note=document.createElement('p');note.textContent='This preview has not sent your inquiry.';box.append(note);box.hidden=false;box.scrollIntoView({behavior:'smooth',block:'start'});});
}

function initializeSite(){initializeInquiry();const path=location.hash?location.hash.slice(1).split('?')[0]:location.pathname;document.querySelectorAll('nav a').forEach(a=>{const target=a.getAttribute('href').replace(/^#/,'');if(target===path)a.setAttribute('aria-current','page')});}

document.addEventListener('DOMContentLoaded',initializeSite);

function initializeBblo(){
 const search=document.getElementById('member-search');
 if(search){const cards=[...document.querySelectorAll('[data-member]')]; const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();search.addEventListener('input',()=>{const query=normalize(search.value.trim());let count=0;cards.forEach(card=>{card.hidden=!normalize(card.dataset.member).includes(query);if(!card.hidden)count++;});document.getElementById('member-count').textContent=count+' '+(count===1?'business':'businesses');document.getElementById('member-empty').hidden=count!==0;});}
 document.querySelectorAll('.bblo-preview-form').forEach(form=>{form.addEventListener('submit',event=>{event.preventDefault();if(!form.reportValidity())return;const box=form.querySelector('.form-summary');box.replaceChildren();const heading=document.createElement('h3');heading.textContent='Review only — nothing sent or saved';box.append(heading);for(const [name,value] of new FormData(form)){if(!value||name==='permission')continue;const control=form.elements.namedItem(name);const label=control.labels[0].textContent;const line=document.createElement('p');line.textContent=label+': '+value;box.append(line);}box.hidden=false;box.focus();});});
}

initializeBblo();

// Keep native navigation menus usable on mouse, touch and keyboard.
document.addEventListener('click',event=>{document.querySelectorAll('header details[open]').forEach(menu=>{if(!menu.contains(event.target))menu.open=false;});});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){document.querySelectorAll('header details[open]').forEach(menu=>{menu.open=false;menu.querySelector('summary').focus();});}});
