
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