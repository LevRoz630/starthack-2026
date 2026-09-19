import { $, el, answerCard, askAbout, bySlot, chf, renderGroup } from '/shared/dom.js';

const params = new URLSearchParams(location.search);
const API = (params.get('api') || location.origin).replace(/\/$/, '');

const SLOT_TITLES = {
  who: 'Who', development: 'Development', health: 'Health check', watch: 'Watch',
  outlook: 'Outlook', actions: 'Next best actions',
};
const SLOT_ORDER = Object.keys(SLOT_TITLES);

const state = { clients: [], filter: '', tab: 'all', impact: {}, selected: null, poll: null };

// --- client list --------------------------------------------------------------

async function loadClients() {
  try {
    const resp = await fetch(`${API}/clients`);
    state.clients = resp.ok ? await resp.json() : [];
    setConn(true);
  } catch {
    setConn(false);
  }
  renderClientList();
}

function matchesTab(c) {
  if (state.tab === 'ext') return !!c.external;
  if (state.tab === 'hit') return Math.abs(shareOf(c.client)) >= 0.01;
  return true;
}

function renderClientList() {
  const list = $('#client-list');
  list.replaceChildren();
  const q = state.filter.trim().toLowerCase();
  const matchesQuery = (c) => !q || c.client.toLowerCase().includes(q) || (c.name || '').toLowerCase().includes(q);
  $('#count-all').textContent = state.clients.length;
  $('#count-hit').textContent = state.clients.filter((c) => Math.abs(shareOf(c.client)) >= 0.01).length;
  $('#count-ext').textContent = state.clients.filter((c) => c.external).length;
  const rows = state.clients.filter((c) => matchesQuery(c) && matchesTab(c));
  for (const c of rows) {
    const li = el('li');
    const btn = el('button');
    btn.type = 'button';
    btn.setAttribute('aria-current', String(c.client === state.selected));
    const nameRow = el('span', 'client-name');
    nameRow.append(statusDot(c.client));
    nameRow.append(el('span', null, c.name || c.client));
    if (c.external) nameRow.append(el('span', 'tag ext', 'ex-custody'));
    btn.append(nameRow);
    const sub = c.aum ? `${c.client} · ${c.currency || 'CHF'} ${chf.format(c.aum)}` : c.client;
    btn.append(el('span', 'client-sub', sub));
    btn.addEventListener('click', () => selectClient(c.client));
    li.append(btn);
    list.append(li);
  }
  if (!rows.length) list.append(el('li', 'client-sub', 'No matching clients.'));
}

const shareOf = (ref) => (state.impact[ref] ? state.impact[ref].share : 0);

// Their triage dot: red where today cost more than 2% of the book, amber for a loss
// worth a look, green for a gain, and a hollow ring for the clients today barely
// touched -- a dot on every row would mark nothing.
function statusDot(ref) {
  const share = shareOf(ref);
  const dot = el('span', 'status');
  if (share <= -0.02) dot.classList.add('bad');
  else if (share <= -0.005) dot.classList.add('warn');
  else if (share >= 0.005) dot.classList.add('ok');
  else dot.classList.add('none');
  return dot;
}

// --- who to call first ---------------------------------------------------------

const signedMoney = (amount) => `${amount < 0 ? '−' : '+'}CHF ${chf.format(Math.abs(amount))}`;
const signedPct = (share) => `${share < 0 ? '−' : '+'}${Math.abs(share * 100).toFixed(1)}%`;

async function loadCallers() {
  let market, rows;
  try {
    [market, rows] = await Promise.all([
      fetch(`${API}/market/state`).then((r) => r.json()),
      fetch(`${API}/callers?limit=500`).then((r) => r.json()),
    ]);
  } catch {
    return;
  }
  const active = market && market.scenario && market.scenario !== 'empty';
  state.impact = active ? Object.fromEntries(rows.map((r) => [r.client, r])) : {};
  renderClientList();
  if (state.selected) fillStrip(state.selected);
  $('#callfirst').hidden = !(active && rows.length);
  if (!active || !rows.length) return;

  const top = rows.slice(0, 5);
  $('#caller-count').textContent = `(${top.length})`;
  const list = $('#caller-list');
  list.replaceChildren();
  for (const row of top) {
    const li = el('li');
    const btn = el('button');
    btn.type = 'button';
    const head = el('span', 'caller-head');
    const who = el('span', 'client-name');
    who.append(statusDot(row.client));
    who.append(el('span', null, row.name || row.client));
    head.append(who);
    head.append(el('span', `caller-impact ${row.impact < 0 ? 'loss' : 'gain'}`,
                   `${signedMoney(row.impact)} (${signedPct(row.share)})`));
    btn.append(head);
    btn.append(el('span', 'client-sub', row.reason));
    btn.addEventListener('click', () => selectClient(row.client));
    li.append(btn);
    list.append(li);
  }
}

// --- briefing ------------------------------------------------------------------

function clientMeta(ref) {
  return state.clients.find((c) => c.client === ref) || {};
}

// The grey band under the context bar: the numbers that matter for this client, in
// the label-over-value pairs their own portfolio screen uses, with the money right.
function fillStrip(ref, asOf) {
  const c = clientMeta(ref);
  const hit = state.impact[ref];
  const today = $('#f-today');
  today.className = 'fact-value';
  if (hit) {
    today.classList.add(hit.impact < 0 ? 'loss' : 'gain');
    today.textContent = `${signedMoney(hit.impact)} (${signedPct(hit.share)})`;
  } else {
    today.classList.add('flat');
    today.textContent = 'no material move';
  }
  if (asOf) $('#f-asof').textContent = asOf;
  $('#f-custody-box').hidden = !c.external;
  $('#f-custody').textContent = 'held at another bank';
  $('#f-aum').textContent = c.aum ? `${c.currency || 'CHF'} ${chf.format(c.aum)}` : '';
  $('#factstrip').hidden = false;
}

async function selectClient(ref) {
  state.selected = ref;
  renderClientList();
  clearInterval(state.poll);
  const c = clientMeta(ref);
  $('#context-title').textContent = `${c.name || ref} (${ref})`;
  $('#play').hidden = false;
  fillStrip(ref);
  $('#empty').hidden = true;
  $('#card').hidden = false;
  $('#audio').removeAttribute('src');
  $('#answers').replaceChildren();
  await fetchBriefing(ref);
}

async function fetchBriefing(ref) {
  let b;
  try {
    const resp = await fetch(`${API}/briefing/${encodeURIComponent(ref)}`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    b = await resp.json();
  } catch (e) {
    renderError(ref, e);
    return;
  }
  if (ref !== state.selected) return;
  renderBriefing(b);
  if (b.phrasing === 'pending') {
    let tries = 0;
    state.poll = setInterval(async () => {
      tries += 1;
      if (tries > 8) { clearInterval(state.poll); return; }
      const fresh = await fetch(`${API}/briefing/${encodeURIComponent(ref)}`).then((r) => r.json()).catch(() => null);
      if (fresh && ref === state.selected) {
        renderBriefing(fresh);
        if (fresh.phrasing !== 'pending') clearInterval(state.poll);
      }
    }, 1200);
  }
}

function renderError(ref, e) {
  $('#slots').replaceChildren(el('p', 'muted', `Could not load this briefing: ${e.message || e}`));
}

function renderBriefing(b) {
  $('#context-title').textContent = `${b.name || b.client} (${b.client})`;
  fillStrip(b.client, b.as_of);

  const groups = bySlot(b);
  const slotsBox = $('#slots');
  slotsBox.replaceChildren();
  const weights = Object.fromEntries((b.facts || []).map((f) => [f.id, f.weight || 0]));
  for (const slot of SLOT_ORDER) {
    if (!groups[slot] || !groups[slot].length) continue;
    slotsBox.append(renderGroup(slot, groups[slot], SLOT_TITLES[slot], { weights, sources: 'hidden' }));
  }
}

// --- audio -----------------------------------------------------------------

async function playBriefing() {
  const ref = state.selected;
  if (!ref) return;
  const audio = $('#audio');
  const btn = $('#play');
  if (audio.getAttribute('src')) { audio.play(); return; }
  btn.disabled = true;
  btn.textContent = 'Loading…';
  try {
    const resp = await fetch(`${API}/briefing/${encodeURIComponent(ref)}/audio`);
    if (!resp.ok) throw new Error(`voice unavailable (${resp.status})`);
    const blob = await resp.blob();
    audio.src = URL.createObjectURL(blob);
    await audio.play();
    btn.textContent = '▸ Listen';
  } catch (e) {
    btn.textContent = 'Voice unavailable';
    setTimeout(() => { btn.textContent = '▸ Listen'; }, 2000);
  } finally {
    btn.disabled = false;
  }
}

// --- upload ------------------------------------------------------------------

async function uploadFile(file) {
  const status = $('#upload-status');
  status.dataset.state = '';
  status.textContent = `Uploading ${file.name}…`;
  const form = new FormData();
  form.append('file', file);
  try {
    const resp = await fetch(`${API}/clients`, { method: 'POST', body: form });
    const out = await resp.json();
    if (!resp.ok && !(out.added && out.added.length)) throw new Error(out.error || 'upload failed');
    status.dataset.state = 'ok';
    status.textContent = `Added: ${out.added.join(', ') || 'none'}${Object.keys(out.failed || {}).length ? `; failed: ${Object.keys(out.failed).join(', ')}` : ''}`;
    await loadClients();
    if (out.added && out.added.length) selectClient(out.added[0]);
  } catch (e) {
    status.dataset.state = 'error';
    status.textContent = `Could not upload: ${e.message || e}`;
  }
}

// --- follow-up questions -------------------------------------------------------

async function askQuestion(question) {
  const ref = state.selected;
  if (!ref || !question.trim()) return;
  const input = $('#ask-input');
  const send = $('#ask-send');
  input.value = '';
  send.disabled = true;
  const pending = el('li', 'answer-card pending');
  pending.append(el('p', 'q', `“${question.trim()}”`));
  pending.append(el('p', 'a', 'Looking…'));
  $('#answers').prepend(pending);
  const entry = await askAbout(API, ref, question);
  send.disabled = false;
  if (ref !== state.selected) { pending.remove(); return; }
  pending.replaceWith(answerCard(entry, { sources: 'collapsed' }));
  input.focus();
}

// --- connection ----------------------------------------------------------------

function setConn(ok) {
  $('#conn').dataset.state = ok ? 'open' : 'closed';
  $('#conn-label').textContent = ok ? 'Live' : 'Offline';
}

// --- wiring -------------------------------------------------------------------

for (const tab of document.querySelectorAll('.tab')) {
  tab.addEventListener('click', () => {
    state.tab = tab.dataset.tab;
    for (const other of document.querySelectorAll('.tab')) {
      other.setAttribute('aria-pressed', String(other === tab));
    }
    renderClientList();
  });
}
$('#search').addEventListener('input', (e) => { state.filter = e.target.value; renderClientList(); });
$('#play').addEventListener('click', playBriefing);
$('#ask-form').addEventListener('submit', (e) => { e.preventDefault(); askQuestion($('#ask-input').value); });
$('#upload-file').addEventListener('change', (e) => {
  const file = e.target.files && e.target.files[0];
  if (file) uploadFile(file);
  e.target.value = '';
});

loadClients();
loadCallers();
setInterval(() => { loadClients(); loadCallers(); }, 30000);

try {
  const ws = new WebSocket(`${API.replace(/^http/, 'ws')}/ws`);
  ws.addEventListener('message', (msg) => {
    let event;
    try { event = JSON.parse(msg.data); } catch { return; }
    if (event.type === 'market') loadCallers();
  });
} catch { /* the dashboard works without live updates */ }
