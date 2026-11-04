(() => {
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const search = document.getElementById('member-search');
  if (search) {
    const cards = [...document.querySelectorAll('[data-member]')];
    search.addEventListener('input', () => {
      const query = normalize(search.value.trim());
      let count = 0;
      cards.forEach(card => { card.hidden = !normalize(card.dataset.member).includes(query); if (!card.hidden) count++; });
      document.getElementById('member-count').textContent = `${count} ${count === 1 ? 'business' : 'businesses'}`;
      document.getElementById('member-empty').hidden = count !== 0;
    });
  }

  document.querySelectorAll('[data-win-builder]').forEach(builder => {
    let nextId = 0;
    const list = builder.querySelector('[data-win-list]');
    const template = builder.querySelector('[data-win-template]');
    const area = builder.querySelector('[data-win-area]');
    const toggle = builder.querySelector('[data-win-toggle]');
    const update = () => {
      const entries = [...list.querySelectorAll('[data-win-entry]')];
      entries.forEach((entry, i) => {
        entry.querySelector('[data-win-number]').textContent = i + 1;
        const remove = entry.querySelector('[data-remove-win]');
        remove.disabled = entries.length === 1;
        remove.setAttribute('aria-label', `Remove win ${i + 1}`);
      });
      builder.querySelector('[data-win-count]').textContent = `${entries.length} ${entries.length === 1 ? 'win entry' : 'win entries'}`;
      const enabled = !toggle || toggle.checked;
      area.hidden = !enabled;
      area.querySelectorAll('input,select,textarea').forEach(control => { control.disabled = !enabled; if (!enabled) control.setCustomValidity(''); });
    };
    const add = () => {
      nextId++;
      const host = document.createElement('div');
      host.innerHTML = template.innerHTML.replaceAll('__INDEX__', String(nextId));
      const entry = host.firstElementChild;
      entry.querySelectorAll('input[type="number"]').forEach(input => { input.min = '0'; input.step = '0.01'; });
      entry.querySelector('[data-remove-win]').addEventListener('click', () => { entry.remove(); update(); builder.dispatchEvent(new Event('change', { bubbles: true })); });
      entry.querySelectorAll('[data-win-type]').forEach(checkbox => checkbox.addEventListener('change', () => entry.querySelector('[data-win-type]').setCustomValidity('')));
      list.append(entry);
      update();
      return entry;
    };
    builder.querySelector('[data-add-win]').addEventListener('click', () => {
      const entry = add();
      entry.querySelector('[data-win-type]').focus();
      builder.dispatchEvent(new Event('change', { bubbles: true }));
    });
    if (toggle) toggle.addEventListener('change', update);
    add();
  });

  document.querySelectorAll('.bblo-review-form').forEach(form => {
    const summary = form.querySelector('.form-summary');
    const clear = () => { summary.hidden = true; };
    form.addEventListener('input', clear);
    form.addEventListener('change', clear);
    form.addEventListener('submit', event => {
      event.preventDefault();
      form.querySelectorAll('[data-win-entry]').forEach(entry => {
        const first = entry.querySelector('[data-win-type]');
        if (first.disabled) return;
        first.setCustomValidity(entry.querySelector('[data-win-type]:checked') ? '' : 'Choose at least one type for this win.');
      });
      if (!form.reportValidity()) return;
      summary.replaceChildren();
      const heading = document.createElement('h3');
      heading.textContent = 'Review your proposal';
      summary.append(heading);
      const addLine = (label, value) => {
        const line = document.createElement('p');
        line.textContent = `${label.replace(/\s*\*$/, '')}: ${value}`;
        summary.append(line);
      };
      [...form.elements].forEach(control => {
        if (!control.name || control.disabled || !control.value || control.closest('[data-win-entry]') || control.hasAttribute('data-ui') || control.hasAttribute('data-consent') || ['submit', 'button'].includes(control.type)) return;
        if (['checkbox', 'radio'].includes(control.type) && !control.checked) return;
        const label = control.labels?.[0]?.textContent?.trim() || control.name;
        addLine(label, control.type === 'checkbox' ? control.value : control.value);
      });
      let number = 0;
      form.querySelectorAll('[data-win-entry]').forEach(entry => {
        if (entry.querySelector('[data-win-type]').disabled) return;
        number++;
        const title = document.createElement('h4'); title.textContent = `Win ${number}`; summary.append(title);
        addLine('Types', [...entry.querySelectorAll('[data-win-type]:checked')].map(c => c.value).join(' · '));
        entry.querySelectorAll('input:not([data-win-type]),select,textarea').forEach(control => { if (control.value) addLine(control.labels[0].textContent.trim(), control.value); });
      });
      const answers = [...summary.querySelectorAll('p')].map(p => p.textContent).join('\n\n');
      const action = document.createElement('a');
      action.className = 'button';
      action.textContent = 'Open email draft to BBLO';
      action.href = 'mailto:bblocala@gmail.com?subject=' + encodeURIComponent('BBLO presentation proposal') + '&body=' + encodeURIComponent(answers + '\n\nPermission: BBLO may contact me about this proposal.');
      const note = document.createElement('p');
      note.textContent = 'Review the draft, attach any supporting photos and press Send in your email app. Nothing has been sent by this page. If your email app does not open, copy the answers above and email bblocala@gmail.com.';
      summary.append(action, note);
      summary.hidden = false;
      summary.focus();
    });
  });
})();
