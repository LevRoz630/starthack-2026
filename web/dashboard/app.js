// Advisor dashboard: pick a client, one click, the 60-second briefing.
// All API text is rendered with textContent, never as HTML.

import { $, $$, el, answerCard, askAbout, bySlot, chf, renderGroup } from '/shared/dom.js';

const params = new URLSearchParams(location.search);
const API = (params.get('api') || location.origin).replace(/\/$/, '');

const SLOT_TITLES = {
  who: 'Who', development: 'Development', health: 'Health check', watch: 'Watch',
  outlook: 'Outlook', actions: 'Next best actions',
};
const SLOT_ORDER = Object.keys(SLOT_TITLES);

const state = { clients: [], filter: '', selected: null, poll: null };

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

function renderClientList() {
  const list = $('#client-list');
  list.replaceChildren();
  const q = state.filter.trim().toLowerCase();
  const rows = state.clients.filter((c) => !q || c.client.toLowerCase().includes(q) || (c.name || '').toLowerCase().includes(q));
  for (const c of rows) {
    const li = el('li');
    const btn = el('button');
    btn.type = 'button';
    btn.setAttribute('aria-current', String(c.client === state.selected));
    const nameRow = el('span', 'client-name', c.name || c.client);
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

// --- who to call first ---------------------------------------------------------

const signedMoney = (amount) => `${amount < 0 ? '−' : '+'}CHF ${chf.format(Math.abs(amount))}`;
const signedPct = (share) => `${share < 0 ? '−' : '+'}${Math.abs(share * 100).toFixed(1)}%`;

async function loadCallers() {
  let market, rows;
  try {
    [market, rows] = await Promise.all([
      fetch(`${API}/market/state`).then((r) => r.json()),
      fetch(`${API}/callers?limit=5`).then((r) => r.json()),
    ]);
  } catch {
    return;
  }
  const active = market && market.scenario && market.scenario !== 'empty';
  $('#callfirst').hidden = !(active && rows.length);
  if (!active || !rows.length) return;
  // The SIMULATED tag next to it already says so; don't say it twice.
  $('#market-name').textContent = (market.description || market.scenario).replace(/^SIMULATED[.:]?\s*/, '');
  $('#market-sim').hidden = !market.simulated;

  const list = $('#caller-list');
  list.replaceChildren();
  for (const row of rows) {
    const li = el('li');
    const btn = el('button');
    btn.type = 'button';
    const head = el('span', 'caller-head');
    head.append(el('span', 'client-name', row.name || row.client));
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

async function selectClient(ref) {
  state.selected = ref;
  renderClientList();
  clearInterval(state.poll);
  $('#empty').hidden = true;
  $('#card').hidden = false;
  $('#audio').removeAttribute('src');
  $('#answers').replaceChildren();   // the last client's answers are not about this one
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
  if (ref !== state.selected) return; // a later click won a race
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
  $('#b-name').textContent = ref;
  $('#b-ref').textContent = 'Could not load this briefing.';
  $('#slots').replaceChildren(el('p', 'muted', String(e.message || e)));
  $('#b-words').textContent = '';
  $('#b-read').textContent = '';
  $('#b-coverage').textContent = '';
  $('#b-provider').textContent = '';
  $('#rejected-box').hidden = true;
}

function renderBriefing(b) {
  $('#b-name').textContent = b.name || b.client;
  $('#b-ref').textContent = `${b.client} · as of ${b.as_of}`;
  $('#b-words').textContent = `${b.words} words`;
  $('#b-read').textContent = `~${Math.max(1, Math.round(b.words / 3.3))}s to read`;

  const groups = bySlot(b);
  const populated = SLOT_ORDER.filter((slot) => groups[slot] && groups[slot].length);
  $('#b-coverage').textContent = `${populated.length}/${SLOT_ORDER.length} sections have data`;

  const providerLabel = { apertus: 'Phrased by Apertus', openai: 'Phrased by OpenAI', template: 'Fact text',
                          pending: 'Phrasing…' }[b.provider] || b.provider;
  $('#b-provider').textContent = b.phrasing === 'pending' ? 'Phrasing…' : providerLabel;

  const slotsBox = $('#slots');
  slotsBox.replaceChildren();
  for (const slot of SLOT_ORDER) {
    if (!groups[slot] || !groups[slot].length) continue;
    slotsBox.append(renderGroup(slot, groups[slot], SLOT_TITLES[slot]));
  }

  const rejected = b.rejected || [];
  $('#rejected-box').hidden = rejected.length === 0;
  $('#rejected-count').textContent = `(${rejected.length})`;
  const rlist = $('#rejected-list');
  rlist.replaceChildren();
  for (const r of rejected) {
    rlist.append(el('li', null, `"${r.text}" — ${r.reason}`));
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
// The same POST /ask the phone uses during a live call, so the advisor can keep asking
// after the 60 seconds are up. Answers are facts with their sources, never new text.

async function askQuestion(question) {
  const ref = state.selected;
  if (!ref || !question.trim()) return;
  const input = $('#ask-input');
  const send = $('#ask-send');
  input.value = '';
  send.disabled = true;
  const pending = el('li', 'answer-card pending');
  pending.append(el('p', 'q', `\u201C${question.trim()}\u201D`));
  pending.append(el('p', 'a', 'Looking\u2026'));
  $('#answers').prepend(pending);
  const entry = await askAbout(API, ref, question);
  send.disabled = false;
  if (ref !== state.selected) { pending.remove(); return; }  // they switched client mid-question
  pending.replaceWith(answerCard(entry));
  input.focus();
}

// --- connection ----------------------------------------------------------------

function setConn(ok) {
  $('#conn').dataset.state = ok ? 'open' : 'closed';
  $('#conn-label').textContent = ok ? 'Live' : 'Offline';
}

// --- wiring -------------------------------------------------------------------

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

// The market can move while the page is open (POST /market/events): re-rank at once.
try {
  const ws = new WebSocket(`${API.replace(/^http/, 'ws')}/ws`);
  ws.addEventListener('message', (msg) => {
    let event;
    try { event = JSON.parse(msg.data); } catch { return; }
    if (event.type === 'market') loadCallers();
  });
} catch { /* the dashboard works without live updates */ }
