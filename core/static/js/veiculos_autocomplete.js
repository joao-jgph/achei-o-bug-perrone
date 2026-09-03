document.addEventListener('DOMContentLoaded', function () {
  function makeSuggestionsContainer(inputEl, id) {
    const wrap = document.createElement('div');
    wrap.className = 'position-relative';

    const container = document.createElement('div');
    container.className = 'list-group position-absolute w-100 shadow-sm bg-white d-none';
    container.style.maxHeight = '220px';
    container.style.zIndex = 1050;
    container.setAttribute('role', 'listbox');
    container.id = id;

    inputEl.parentNode.insertBefore(wrap, inputEl);
    wrap.appendChild(inputEl);
    wrap.appendChild(container);
    return container;
  }

  function attachAutocompleteForList(opts) {
    const inputEl = document.getElementById(opts.inputId);
    const hiddenEl = document.getElementById(opts.hiddenId);
    if (!inputEl || !hiddenEl) return;

    const container = makeSuggestionsContainer(inputEl, opts.containerId);

    let items = opts.items.slice();
    let active = -1;

    function renderList(filtered) {
      container.innerHTML = '';
      if (!filtered.length) {
        container.classList.add('d-none');
        return;
      }
      filtered.forEach((it, idx) => {
        const el = document.createElement('button');
        el.type = 'button';
        el.className = 'list-group-item list-group-item-action';
        el.textContent = it.label;
        el.dataset.id = it.id;
        el.dataset.marca = it.marca || '';
        el.addEventListener('click', function () {
          choose(idx, filtered);
        });
        container.appendChild(el);
      });
      container.classList.remove('d-none');
    }

    function choose(idx, currentList) {
      const it = currentList[idx];
      if (!it) return;
      inputEl.value = it.label;
      hiddenEl.value = it.id || '';
      container.classList.add('d-none');
      if (opts.onChoose) opts.onChoose(it);
    }

    function getFiltered() {
      const q = (inputEl.value || '').toLowerCase();
      const marcaFilter = document.getElementById(opts.marcaHiddenForModels || '') || null;
      return items.filter(it => {
        if (opts.marcaOnly && marcaFilter) {
          const marcaVal = marcaFilter.value;
          if (marcaVal && String(it.marca) !== String(marcaVal)) return false;
        }
        return !q || it.label.toLowerCase().indexOf(q) !== -1;
      });
    }

    inputEl.addEventListener('input', function () {
      active = -1;
      if (opts.clearHiddenOnInput) hiddenEl.value = '';
      const filtered = getFiltered();
      renderList(filtered);
    });

    inputEl.addEventListener('keydown', function (ev) {
      const list = container.querySelectorAll('.list-group-item');
      if (!list.length) return;
      if (ev.key === 'ArrowDown') {
        ev.preventDefault();
        active = Math.min(active + 1, list.length - 1);
        updateActive(list);
      } else if (ev.key === 'ArrowUp') {
        ev.preventDefault();
        active = Math.max(active - 1, 0);
        updateActive(list);
      } else if (ev.key === 'Enter') {
        ev.preventDefault();
        if (active >= 0) choose(active, Array.from(list).map(el => ({ id: el.dataset.id, label: el.textContent, marca: el.dataset.marca }))); 
        else {
          // if exact match exists, pick it
          const exact = Array.from(list).find(el => el.textContent === inputEl.value);
          if (exact) {
            inputEl.value = exact.textContent;
            hiddenEl.value = exact.dataset.id || '';
            if (opts.onChoose) opts.onChoose({ id: exact.dataset.id, label: exact.textContent, marca: exact.dataset.marca });
            container.classList.add('d-none');
          }
        }
      } else if (ev.key === 'Escape') {
        container.classList.add('d-none');
      }
    });

    function updateActive(list) {
      list.forEach((el, i) => el.classList.toggle('active', i === active));
      if (active >= 0) list[active].scrollIntoView({ block: 'nearest' });
    }

    document.addEventListener('click', function (ev) {
      if (!container.contains(ev.target) && ev.target !== inputEl) {
        container.classList.add('d-none');
      }
    });

    // initial render (empty -> hidden)
    container.classList.add('d-none');

    return {
      refreshItems(newItems) { items = newItems.slice(); },
      renderCurrent() { renderList(getFiltered()); }
    };
  }

  // build items arrays from markup datalists
  const marcasList = Array.from(document.querySelectorAll('#marcas_list option')).map(o => ({ id: o.dataset.id, label: o.value }));
  const modelosAll = Array.from(document.querySelectorAll('#modelos_list option')).map(o => ({ id: o.dataset.id, label: o.value, marca: o.dataset.marca }));

  const marcaAutocomplete = attachAutocompleteForList({
    inputId: 'id_fk_marca_input',
    hiddenId: 'id_fk_marca_hidden',
    containerId: 'marca_suggestions',
    items: marcasList,
    clearHiddenOnInput: true,
    onChoose: function (it) {
      // when marca chosen, update modelos datasource and clear modelo
      modeloAutocomplete.refreshItems(modelosAll.filter(m => !it.id || String(m.marca) === String(it.id)));
      modeloAutocomplete.renderCurrent();
      document.getElementById('id_fk_modelo_input').value = '';
      document.getElementById('id_fk_modelo_hidden').value = '';
    }
  });

  const modeloAutocomplete = attachAutocompleteForList({
    inputId: 'id_fk_modelo_input',
    hiddenId: 'id_fk_modelo_hidden',
    containerId: 'modelo_suggestions',
    items: modelosAll,
    marcaOnly: true,
    marcaHiddenForModels: 'id_fk_marca_hidden',
    clearHiddenOnInput: true,
    onChoose: function (it) {
      // nothing else
    }
  });

});
