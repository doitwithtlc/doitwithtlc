(() => {
  const normalize = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const search=document.getElementById('member-search');
  const category=document.getElementById('member-category');
  const directory=[...document.querySelectorAll('.member-public-card[data-member]')];
  const paid=[...document.querySelectorAll('.paid-member')];
  const adActive=card=>{
    const now=Date.now(),start=Date.parse(card.dataset.adStart),end=Date.parse(card.dataset.adEnd);
    return Number.isFinite(start)&&Number.isFinite(end)&&start<=now&&now<end;
  };
  function filter(){
    const terms=normalize(search?.value.trim()||'').split(/\s+/).filter(Boolean),group=category?.value||'';
    const matches=card=>(!group||card.dataset.group===group)&&terms.every(term=>normalize(card.dataset.member).includes(term));
    let count=0;
    directory.forEach(card=>{card.hidden=!matches(card);if(!card.hidden)count++;});
    paid.forEach(card=>{card.hidden=!adActive(card)||!matches(card);});
    document.querySelectorAll('.sponsored-members').forEach(section=>{section.hidden=![...section.querySelectorAll('.paid-member')].some(card=>!card.hidden);});
    if(search){document.getElementById('member-count').textContent=`${count} ${count===1?'listing':'listings'}`;document.getElementById('member-empty').hidden=count!==0;}
  }
  search?.addEventListener('input',filter);category?.addEventListener('change',filter);filter();
  const form=document.getElementById('member-profile-update');
  if(form){
    const member=new URLSearchParams(location.search).get('member');
    if(member&&[...form.elements.member_slug.options].some(option=>option.value===member))form.elements.member_slug.value=member;
    form.addEventListener('submit',event=>{
      event.preventDefault();if(!form.reportValidity())return;
      const lines=['BBLO public business profile update',''];
      [...form.elements].forEach(control=>{
        if(!control.name||!control.value||control.type==='checkbox')return;
        const label=control.labels?.[0]?.childNodes[0]?.textContent.trim()||control.name;
        const value=control.name==='member_slug'?control.selectedOptions[0].textContent:control.value;
        lines.push(`${label}: ${value}`,'');
      });
      lines.push('Permission: I authorize BBLO to publish the public business information provided. I have permission to share attached logos and photos.','Attach original logo and approved photos before sending.');
      const body=lines.join('\n');
      document.getElementById('profile-email-text').textContent=body;
      document.getElementById('profile-email-send').href='mailto:carmen@doitwithtlc.com?subject='+encodeURIComponent('BBLO profile update: '+form.elements.member_slug.selectedOptions[0].textContent)+'&body='+encodeURIComponent(body);
      document.getElementById('profile-email-preview').hidden=false;
      document.getElementById('profile-email-status').textContent='Your draft is ready below. Review it, then open your email app to send it. Nothing has been sent yet.';
    });
    form.addEventListener('input',()=>{document.getElementById('profile-email-preview').hidden=true;document.getElementById('profile-email-status').textContent='';});
    form.addEventListener('change',()=>{document.getElementById('profile-email-preview').hidden=true;document.getElementById('profile-email-status').textContent='';});
  }
})();
