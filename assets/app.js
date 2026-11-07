// Catalog filters, install tabs, copy buttons. No dependencies.
(function () {
  // ── catalog: search + field chips, with ?field= and ?q= in the URL ──
  const q = document.getElementById('q');
  const chips = document.querySelectorAll('[data-filter-field]');
  if (q || chips.length) {
    const params = new URLSearchParams(location.search);
    let field = params.get('field') || 'all';
    if (params.get('q') && q) q.value = params.get('q');
    const apply = () => {
      const term = (q && q.value || '').trim().toLowerCase();
      let shown = 0;
      document.querySelectorAll('.drawer-section').forEach(sec => {
        let inSec = 0;
        sec.querySelectorAll('.card').forEach(c => {
          const ok = (field === 'all' || c.dataset.field === field) && (!term || c.dataset.search.includes(term));
          c.hidden = !ok; if (ok) inSec++;
        });
        sec.hidden = inSec === 0; shown += inSec;
      });
      chips.forEach(ch => ch.setAttribute('aria-pressed', ch.dataset.filterField === field));
      const empty = document.getElementById('empty'); if (empty) empty.hidden = shown > 0;
      const p = new URLSearchParams();
      if (field !== 'all') p.set('field', field);
      if (term) p.set('q', term);
      history.replaceState(null, '', location.pathname + (p.toString() ? '?' + p : ''));
    };
    chips.forEach(ch => ch.addEventListener('click', () => { field = ch.dataset.filterField; apply(); }));
    if (q) q.addEventListener('input', apply);
    apply();
  }

  // ── install tabs ──
  document.querySelectorAll('.install').forEach(box => {
    const tabs = box.querySelectorAll('[data-tab]');
    tabs.forEach(t => t.addEventListener('click', () => {
      tabs.forEach(x => x.setAttribute('aria-selected', x === t));
      box.querySelectorAll('[data-pane]').forEach(p => { p.hidden = p.dataset.pane !== t.dataset.tab; });
    }));
  });

  // ── copy buttons ──
  document.querySelectorAll('[data-copy]').forEach(b => b.addEventListener('click', () => {
    navigator.clipboard?.writeText(b.dataset.copy).then(() => { const t = b.textContent; b.textContent = 'Copied ✓'; setTimeout(() => b.textContent = t, 1500); });
  }));
})();
