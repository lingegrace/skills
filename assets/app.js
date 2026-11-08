// Grace's Skill Library — interactions. No dependencies.
(function () {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ───────── 1. Swipeable card stack (home) ───────── */
  const stack = $('#stack');
  if (stack) {
    const box = $('.stack-cards', stack);
    let cards = $$('.scard', box);
    const hint = $('.stack-hint', stack);
    const layout = () => cards.forEach((c, i) => {
      c.style.zIndex = String(cards.length - i);
      c.style.transform = i === 0 ? '' : `translateY(${i * 12}px) scale(${1 - i * 0.045}) rotate(${(i % 2 ? 1.6 : -1.4) * i}deg)`;
      c.style.opacity = i > 3 ? '0' : '1';
      c.setAttribute('aria-hidden', i === 0 ? 'false' : 'true');
      c.querySelectorAll('a').forEach(a => a.tabIndex = i === 0 ? 0 : -1);
    });
    const next = () => {
      const top = cards[0]; if (!top) return;
      hint && hint.classList.add('done');
      top.classList.add('flying');
      top.style.transform = 'translateY(-420px) rotate(-8deg)';
      setTimeout(() => { top.classList.remove('flying'); cards.push(cards.shift()); layout(); }, reduce ? 0 : 420);
    };
    let startY = 0, dy = 0, dragging = false;
    box.addEventListener('pointerdown', ev => {
      if (ev.target.closest('a')) return;
      const top = cards[0]; if (!top || !top.contains(ev.target)) return;
      dragging = true; startY = ev.clientY; dy = 0; top.style.transition = 'none'; top.setPointerCapture(ev.pointerId);
    });
    box.addEventListener('pointermove', ev => {
      if (!dragging) return; dy = Math.min(40, ev.clientY - startY);
      cards[0].style.transform = `translateY(${dy}px) rotate(${dy / 30}deg)`;
    });
    const end = () => {
      if (!dragging) return; dragging = false; const top = cards[0]; top.style.transition = '';
      if (dy < -60) next(); else { top.style.transform = ''; if (Math.abs(dy) < 4) next(); }
    };
    box.addEventListener('pointerup', end); box.addEventListener('pointercancel', end);
    $('.stack-next', stack).addEventListener('click', next);
    stack.addEventListener('keydown', ev => { if (ev.key === 'ArrowUp') { ev.preventDefault(); next(); } });
    layout();
  }

  /* ───────── 2. "I'm a…" picker ───────── */
  const whoChips = $$('.who-chip');
  const whoPre = $('.who-pre'), whoWord = $('.who-word');
  const pickWho = chip => {
    whoChips.forEach(c => c.setAttribute('aria-pressed', c === chip));
    $$('[data-who-group]').forEach(g => { g.hidden = g.dataset.whoGroup !== chip.dataset.who; });
    if (whoWord) {
      whoWord.classList.add('swap');
      setTimeout(() => { whoPre.textContent = chip.dataset.pre; whoWord.textContent = chip.dataset.word; whoWord.classList.remove('swap'); }, reduce ? 0 : 220);
    }
  };
  if (whoChips.length) {
    // rotate through the personas every 4s until the visitor picks one; pause while hovering
    let i = 0, timer = null, chosen = false, hovering = false;
    const wrap = $('#who'), chipsBox = $('.who-chips');
    const tick = () => { if (chosen || hovering || document.hidden) return; i = (i + 1) % whoChips.length; pickWho(whoChips[i]); };
    if (!reduce) { chipsBox.classList.add('auto'); timer = setInterval(tick, 4000); }
    wrap.addEventListener('pointerenter', () => { hovering = true; });
    wrap.addEventListener('pointerleave', () => { hovering = false; });
    whoChips.forEach((chip, n) => chip.addEventListener('click', () => {
      chosen = true; i = n; clearInterval(timer); chipsBox.classList.remove('auto'); pickWho(chip);
    }));
  }

  /* ───────── 3. Folders: click a tab to bring that folder to the front ───────── */
  const ftabs = $$('.ftab');
  const openFolder = tab => {
    ftabs.forEach(t => { const on = t === tab; t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1; });
    $$('.folder').forEach(p => { p.hidden = p.dataset.panel !== tab.dataset.folder; });
  };
  ftabs.forEach((tab, n) => {
    tab.addEventListener('click', () => openFolder(tab));
    tab.addEventListener('keydown', ev => {
      const k = ev.key === 'ArrowRight' ? 1 : ev.key === 'ArrowLeft' ? -1 : 0;
      if (!k) return; ev.preventDefault();
      const next = ftabs[(n + k + ftabs.length) % ftabs.length]; next.focus(); openFolder(next);
    });
  });

  /* ───────── 4. Catalog: search that understands you ───────── */
  const q = $('#q');
  const indexEl = $('#skill-index');
  if (q && indexEl) {
    const index = JSON.parse(indexEl.textContent);
    const chips = $$('[data-filter-field]');
    const params = new URLSearchParams(location.search);
    // landing on the catalog shows Product Management first; 'All' shows everything (Social Science first)
    let field = params.get('field') || (params.get('q') ? 'all' : 'product');
    if (params.get('q')) q.value = params.get('q');

    // Chinese and shorthand → English search words
    const SYN = {
      '文献': 'literature review', '综述': 'literature review', '论文': 'paper thesis academic', '访谈': 'interview qualitative',
      '问卷': 'survey questionnaire', '竞品': 'competitor', '市场': 'market', '会议': 'meeting', '纪要': 'meeting minutes notes',
      '周报': 'weekly report', '简历': 'resume cv', '面试': 'interview practice job', '群面': 'group interview practice',
      '雅思': 'ielts', '口语': 'speaking', '写作': 'writing', '作文': 'essay writing', '润色': 'editing polish', '错题': 'mistake',
      '复习': 'study plan review', '备考': 'exam study plan', '学习': 'learning study tutor', '读书': 'book reading', '产品': 'product',
      '需求': 'prd requirements', '定位': 'positioning', '文案': 'copy landing page', '领英': 'linkedin', '核查': 'fact check',
      '事实': 'fact check', '研究': 'research', '摘要': 'abstract', '引用': 'citation reference', '参考文献': 'citation reference',
      '伦理': 'ethics', '审稿': 'peer review reviewer', '主题分析': 'thematic analysis', '定量': 'quantitative statistics',
      '统计': 'statistics quantitative', '社会学': 'sociology', '营销': 'marketing', '用户': 'user customer', '评论': 'review',
      '选题': 'topic discovery', '趋势': 'trend', '报告': 'report', '决策': 'decision memo', '流程': 'sop process', '知识库': 'knowledge base',
      '提示词': 'prompt', '技能': 'skill', '去ai味': 'human writing', '降ai': 'human writing', '公众号': 'newsletter article',
      'cv': 'resume', 'jd': 'job description resume', 'lit': 'literature', 'seo': 'seo search keyword', 'ux': 'usability product critique',
      'voc': 'voice customer review', 'okr': 'goals report', 'minutes': 'meeting', 'humanize': 'human writing', 'humanizer': 'human writing',
      'detector': 'human writing', 'copywriting': 'copy landing', 'thesis': 'thesis dissertation academic', 'dissertation': 'thesis academic',
      'essay': 'writing academic', 'deck': 'presentation', 'memo': 'decision memo', 'notes': 'notes meeting', 'transcript': 'transcript interview meeting',
      'rival': 'competitor', 'competition': 'competitor', 'qual': 'qualitative', 'quant': 'quantitative', 'stats': 'statistics',
      'gtm': 'launch go-to-market', 'persona': 'persona', 'icp': 'persona customer', 'flashcards': 'active recall', 'exam': 'exam study',
      'like me': 'voice style', 'my voice': 'voice style', 'my style': 'voice style', 'sound like': 'voice style', 'tone of voice': 'voice style',
      'sounds like ai': 'human writing', 'sounds robotic': 'human writing', 'to my boss': 'executive', 'for my manager': 'executive weekly report',
      '文风': 'voice style', '风格': 'voice style', '像我': 'voice style', '汇报': 'executive report', '领导': 'executive',
    };
    const STOP = new Set(['a', 'an', 'the', 'and', 'or', 'for', 'to', 'of', 'in', 'on', 'my', 'me', 'i', 'with', 'from', 'into', 'help', 'want', 'need', 'how', 'do', 'make', 'write', 'skill', 'skills', 'like', 'can', 'something', 'thing', 'better', 'good', 'please']);
    const SUFFIX = ['ically', 'ations', 'ation', 'ical', 'ness', 'ment', 'ings', 'ing', 'ies', 'ied', 'ers', 'er', 'ed', 'es', 'al', 'ic', 'ly', 's', 'y'];
    const stem = w => { for (const s of SUFFIX) if (w.length - s.length >= 4 && w.endsWith(s)) return w.slice(0, -s.length); return w; };
    const expand = text => { let t = ' ' + text.toLowerCase() + ' '; for (const k in SYN) if (t.includes(k)) t += ' ' + SYN[k]; return t; };
    const tokens = text => expand(text).split(/[^a-z0-9一-鿿]+/).filter(w => w && !STOP.has(w)).map(stem);
    const lev = (a, b) => { if (Math.abs(a.length - b.length) > 2) return 9; const d = Array.from({ length: a.length + 1 }, (_, i) => [i]);
      for (let j = 1; j <= b.length; j++) d[0][j] = j;
      for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++) d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      return d[a.length][b.length]; };
    const docs = index.map(r => ({ name: r.n, f: r.f, fields: [[tokens(r.n.replace(/-/g, ' ')), 3], [tokens(r.t), 3], [tokens(r.k), 2.2], [tokens(r.m), 1.6], [tokens(r.s), 1.2], [tokens(r.g + ' ' + r.o), 1], [tokens(r.f), .8]] }));
    // rarer words count more (a simple IDF), so "sociological" outweighs "interview"
    const df = {};
    docs.forEach(d => new Set(d.fields.flatMap(([toks]) => toks)).forEach(w => { df[w] = (df[w] || 0) + 1; }));
    const idf = t => { let n = df[t] || 0; if (!n) for (const w in df) if (t.length >= 4 && (w.startsWith(t) || t.startsWith(w))) n = Math.max(n, df[w]); return Math.log(1 + docs.length / (1 + n)); };
    const score = (doc, qt) => {
      let total = 0, hit = 0;
      for (const t of qt) {
        const wt = idf(t);
        let best = 0;
        for (const [toks, w] of doc.fields) {
          let fieldBest = 0;
          for (const d of toks) {
            let s = 0;
            if (d === t) s = 1; else if (t.length >= 4 && (d.startsWith(t) || t.startsWith(d)) && Math.min(d.length, t.length) >= 4) s = .75;
            else if (t.length >= 5 && lev(t, d) <= (t.length >= 8 ? 2 : 1)) s = .55;
            if (s > fieldBest) fieldBest = s;
          }
          best += fieldBest * w;   // a word that appears in the name AND the tagline AND the terms counts more
        }
        if (best > 0) hit++; total += best * wt;
      }
      return qt.length ? total * (hit / qt.length) / 3 : 0;
    };
    const results = $('#results'), resultsCards = $('#resultsCards'), title = $('#resultsTitle');
    const reqMsg = $('#reqMsg');
    const cardFor = name => $(`.drawer-section .card[data-name="${CSS.escape(name)}"]`);
    const apply = () => {
      const term = q.value.trim();
      chips.forEach(ch => ch.setAttribute('aria-pressed', ch.dataset.filterField === field));
      const slugOf = c => c && c.dataset.field;
      if (!term) {
        results.hidden = true;
        $$('.drawer-section').forEach(sec => { sec.hidden = field !== 'all' && sec.dataset.section !== field; });
      } else {
        const qt = tokens(term);
        let ranked = docs.map(d => ({ d, s: score(d, qt) })).filter(x => x.s > 0).sort((a, b) => b.s - a.s);
        ranked = ranked.filter(x => field === 'all' || slugOf(cardFor(x.d.name)) === field);
        const strong = ranked.filter(x => x.s >= 1.2);
        resultsCards.innerHTML = '';
        const show = (strong.length ? strong : ranked).slice(0, 12);
        show.forEach(x => { const c = cardFor(x.d.name); if (c) resultsCards.appendChild(c.cloneNode(true)); });
        title.textContent = strong.length ? `Best matches for "${term}"` : (ranked.length ? `No exact match for "${term}". Closest skills:` : `Nothing in the catalog for "${term}" yet.`);
        results.hidden = false;
        $$('.drawer-section').forEach(sec => { sec.hidden = true; });
        if (reqMsg && !reqMsg.dataset.touched) reqMsg.value = strong.length ? '' : `A skill for: ${term}`;
        if (!strong.length) $('#requestWrap').classList.add('nudge'); else $('#requestWrap').classList.remove('nudge');
      }
      const p = new URLSearchParams(); if (field !== 'all') p.set('field', field); if (term) p.set('q', term);
      history.replaceState(null, '', location.pathname + (p.toString() ? '?' + p : '') + location.hash);
    };
    if (reqMsg) reqMsg.addEventListener('input', () => { reqMsg.dataset.touched = '1'; });
    chips.forEach(ch => ch.addEventListener('click', () => { field = ch.dataset.filterField; apply(); }));
    let t; q.addEventListener('input', () => { clearTimeout(t); t = setTimeout(apply, 120); });
    apply();
  }

  /* ───────── 5. Forms: request a skill, custom skill, feedback ───────── */
  const endpoint = ($('#lamp') && $('#lamp').dataset.endpoint) || '';
  let gform = null;
  try { gform = $('#lamp') && $('#lamp').dataset.gform ? JSON.parse($('#lamp').dataset.gform) : null; } catch (err) { gform = null; }
  const send = async (form, type) => {
    const data = Object.fromEntries(new FormData(form));
    data.type = type; data.page = location.pathname + location.search;
    if (gform && gform.action) {
      // Google Form: post each value to its question's entry ID. The response is opaque (no-cors).
      const f = gform.fields || {};
      const body = new URLSearchParams();
      for (const k of ['type', 'message', 'email', 'page']) if (f[k] && data[k] != null) body.append(f[k], String(data[k]));
      await fetch(gform.action, { method: 'POST', mode: 'no-cors', body });
      return;
    }
    if (!endpoint) throw new Error('not-connected');
    if (/script\.google(usercontent)?\.com/.test(endpoint)) {
      // Google Apps Script web app → appends a row to Grace's Google Sheet and emails her.
      // text/plain avoids a CORS preflight; the response is opaque, so a network error is the only failure we can see.
      await fetch(endpoint, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(data) });
      return;
    }
    const r = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) });
    if (!r.ok) throw new Error('failed');
  };
  $$('form[data-form]').forEach(form => form.addEventListener('submit', async ev => {
    ev.preventDefault();
    const type = form.dataset.form, note = $('.form-note', form), btn = $('button[type="submit"]', form);
    btn.disabled = true; note.textContent = 'Sending…';
    const isEnvelope = form.classList.contains('request');
    if (isEnvelope) form.classList.add('sending');
    try {
      await send(form, type);
      if (isEnvelope) {
        setTimeout(() => {
          form.classList.add('sent');
          if (!$('.thanks', form)) form.insertAdjacentHTML('beforeend', `<div class="thanks"><img class="thanks-cat" src="${document.querySelector('link[rel=apple-touch-icon]').href}" alt="" width="96" height="96"><b>Received.</b><span class="muted">${type === 'consult' ? "Thank you. I'll reply by email soon." : 'Thank you. Your request is on my desk.'}</span><button type="button" class="btn btn-line again">Send another</button></div>`);
          $('.again', form).onclick = () => { form.reset(); form.classList.remove('sending', 'sent'); btn.disabled = false; note.textContent = ''; };
        }, reduce ? 0 : 900);
      } else { form.classList.add('sent'); note.textContent = 'Thank you. It reached me.'; }
    } catch (err) {
      form.classList.remove('sending'); btn.disabled = false;
      note.textContent = err.message === 'not-connected' ? "This form isn't connected yet, so nothing was sent. Please check back soon." : 'Something went wrong. Please try again.';
    }
  }));
  $$('[data-open-form]').forEach(b => b.addEventListener('click', () => {
    const form = $('#consult form'); if (!form) return;
    const msg = $('textarea', form);
    if (b.dataset.openForm === 'waitlist') msg.value = `Please add me to the waitlist for: ${b.dataset.plan}`;
    $('#consult').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    setTimeout(() => msg.focus(), 400);
  }));

  /* ───────── 6. Feedback lamp: pull the cord ───────── */
  const lamp = $('#lamp');
  if (lamp) {
    const cord = $('#lampCord'), panel = $('#lampPanel');
    const toggle = () => {
      const on = !lamp.classList.contains('on');
      lamp.classList.toggle('on', on); panel.hidden = !on; cord.setAttribute('aria-expanded', on);
      if (on) setTimeout(() => $('textarea', panel).focus(), 200);
    };
    let y0 = 0, pulled = 0, down = false, moved = false;
    cord.addEventListener('pointerdown', ev => { down = true; moved = false; y0 = ev.clientY; pulled = 0; cord.classList.add('pulling'); cord.setPointerCapture(ev.pointerId); });
    cord.addEventListener('pointermove', ev => { if (!down) return; pulled = Math.max(0, Math.min(60, ev.clientY - y0)); if (pulled > 3) moved = true; cord.style.transform = `translateY(${pulled}px)`; });
    const release = () => { if (!down) return; down = false; cord.classList.remove('pulling'); cord.style.transform = ''; if (!moved || pulled > 18) toggle(); };
    cord.addEventListener('pointerup', release); cord.addEventListener('pointercancel', release);
    cord.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); toggle(); } });
    document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && lamp.classList.contains('on')) toggle(); });
    // click anywhere outside the lamp and its card to put it away
    document.addEventListener('pointerdown', ev => {
      if (lamp.classList.contains('on') && !panel.contains(ev.target) && !cord.contains(ev.target)) toggle();
    });
  }

  /* ───────── Back to top: appears once the reader reaches the last section ───────── */
  const toTop = $('#toTop');
  if (toTop) {
    const last = $('#ai-governance') || $$('.col-section').pop();
    const check = () => { if (!last) return; toTop.hidden = last.getBoundingClientRect().top > innerHeight * 0.85; };
    addEventListener('scroll', check, { passive: true }); check();
    toTop.addEventListener('click', ev => { ev.preventDefault(); scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
  }

  /* ───────── 7. Install tabs + copy buttons ───────── */
  $$('.install').forEach(box => {
    const tabs = $$('[data-tab]', box);
    tabs.forEach(t => t.addEventListener('click', () => {
      tabs.forEach(x => x.setAttribute('aria-selected', x === t));
      $$('[data-pane]', box).forEach(p => { p.hidden = p.dataset.pane !== t.dataset.tab; });
    }));
  });
  $$('[data-copy]').forEach(b => b.addEventListener('click', () => {
    navigator.clipboard?.writeText(b.dataset.copy).then(() => { const t = b.textContent; b.textContent = 'Copied ✓'; setTimeout(() => b.textContent = t, 1500); });
  }));
})();
