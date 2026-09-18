// Advisor phone: idle -> ringing -> in call -> after call.
// All API text is rendered with textContent, never as HTML.

const params = new URLSearchParams(location.search);
const API = (params.get('api') || location.origin).replace(/\/$/, '');
const WS_BASE = API.replace(/^http/, 'ws');
const WS_URL = `${WS_BASE}/ws`;
const DEMO_CLIENT = params.get('demo');

const SLOT_TITLES = {
  reason: 'Why they are calling',
  digest: 'What fell',
  holding: 'What held up',
  talk: 'Talking points',
  issue: 'Open issue',
};

const state = {
  screen: 'idle',
  briefing: null,
  answers: [],        // {question, answers: [{text, source}]}
  callStarted: null,
  timer: null,
  approved: {},
};

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// --- formatting -------------------------------------------------------------

const chf = new Intl.NumberFormat('de-CH', { maximumFractionDigits: 0 });

function signedMoney(amount, ccy = 'CHF') {
  const sign = amount < 0 ? '−' : '+';
  return `${sign}${ccy} ${chf.format(Math.abs(amount))}`;
}

function signedPct(share) {
  const sign = share < 0 ? '−' : '+';
  return `${sign}${Math.abs(share * 100).toFixed(2)}%`;
}

function clock(ms) {
  const s = Math.floor(ms / 1000);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
}

// --- screens ----------------------------------------------------------------

function show(screen) {
  state.screen = screen;
  for (const section of $$('.screen')) section.hidden = section.dataset.screen !== screen;
  window.scrollTo(0, 0);
}

function bySlot(briefing) {
  const groups = {};
  for (const s of briefing.sentences || []) (groups[s.slot] ||= []).push(s);
  return groups;
}

function callerName(briefing) {
  return briefing.name || briefing.client;
}

function renderBrief(container, briefing, { withImpact }) {
  container.replaceChildren();
  const groups = bySlot(briefing);

  if (withImpact && briefing.impact && briefing.impact.amount) {
    const box = el('div', 'impact');
    box.append(el('p', 'eyebrow', 'Today on the book'));
    const cls = briefing.impact.amount < 0 ? 'loss' : 'gain';
    box.append(el('p', `amount ${cls}`, signedMoney(briefing.impact.amount)));
    box.append(el('p', 'share', signedPct(briefing.impact.share)));
    // Keep the reason above the number: it is what the advisor needs first.
    if (groups.reason) container.append(group('reason', groups.reason));
    container.append(box);
  } else if (groups.reason) {
    container.append(group('reason', groups.reason));
  }

  for (const slot of ['digest', 'holding', 'talk', 'issue']) {
    if (groups[slot]) container.append(group(slot, groups[slot]));
  }
  // Profile note from the caller slot, if any, goes last on the full briefing.
  const profile = (groups.caller || []).slice(1);
  if (profile.length) container.append(group('caller', profile, 'Profile'));
}

function group(slot, sentences, title) {
  const box = el('section', `group ${slot}`);
  box.append(el('h3', null, title || SLOT_TITLES[slot] || slot));
  const list = el('ul');
  for (const s of sentences) list.append(el('li', null, s.text));
  box.append(list);
  return box;
}

function fillCaller(briefing) {
  for (const node of $$('[data-caller-name]')) node.textContent = callerName(briefing);
  for (const node of $$('[data-caller-ref]')) node.textContent = briefing.client;
  const simulated = Boolean(briefing.market && briefing.market.simulated && briefing.market.scenario !== 'empty');
  for (const node of $$('[data-sim]')) node.hidden = !simulated;
}

// --- ringing ----------------------------------------------------------------

function ring(briefing) {
  if (state.screen === 'call') return; // never interrupt a call in progress
  state.briefing = briefing;
  state.answers = [];
  state.approved = {};
  fillCaller(briefing);
  renderBrief($('#screen-ringing [data-brief]'), briefing, { withImpact: true });
  show('ringing');
  startRingtone();
}

function startRingtone() {
  const audio = $('#ringtone');
  try {
    audio.currentTime = 0;
    const played = audio.play();
    if (played && played.catch) played.catch(() => {}); // missing file or autoplay blocked
  } catch { /* ignore */ }
  if (navigator.vibrate) navigator.vibrate([400, 200, 400, 200, 400]);
}

function stopRingtone() {
  const audio = $('#ringtone');
  try { audio.pause(); } catch { /* ignore */ }
  if (navigator.vibrate) navigator.vibrate(0);
}

// --- in call ----------------------------------------------------------------

function answer() {
  stopRingtone();
  const b = state.briefing;
  const reason = (bySlot(b).reason || [])[0];
  $('[data-reason-line]').textContent = reason ? reason.text : '';
  $('[data-impact-line]').textContent = b.impact && b.impact.amount
    ? `Today: ${signedMoney(b.impact.amount)} (${signedPct(b.impact.share)})` : '';
  $('[data-impact-line]').className = `impact-line ${b.impact && b.impact.amount < 0 ? 'loss' : ''}`;
  renderBrief($('#screen-call [data-brief]'), b, { withImpact: false });
  $('#answers').replaceChildren();
  state.callStarted = Date.now();
  $('#timer').textContent = '0:00';
  clearInterval(state.timer);
  state.timer = setInterval(() => { $('#timer').textContent = clock(Date.now() - state.callStarted); }, 1000);
  show('call');
  $('#ask-input').focus();
}

async function ask(question) {
  question = (question || '').trim();
  if (!question || !state.briefing) return null;
  let result;
  try {
    const resp = await fetch(`${API}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ client: state.briefing.client, question }),
    });
    result = resp.ok ? await resp.json() : { answers: [], error: `HTTP ${resp.status}` };
  } catch (e) {
    result = { answers: [], error: 'No connection' };
  }
  const entry = { question, answers: result.answers || [], error: result.error };
  state.answers.unshift(entry);
  $('#answers').prepend(answerCard(entry));
  return entry;
}

function answerCard(entry) {
  const card = el('li', `answer-card${entry.answers.length ? '' : ' none'}`);
  card.append(el('p', 'q', `“${entry.question}”`));
  if (!entry.answers.length) {
    card.append(el('p', 'a', entry.error ? `Could not answer: ${entry.error}` : 'Nothing in the data answers this.'));
  }
  for (const a of entry.answers) {
    card.append(el('p', 'a', a.text));
    card.append(el('p', 'src', a.source));
  }
  return card;
}

// For the Twilio listener: inject a question heard on the line.
window.pushAnswer = (question) => ask(question);

// An {"answers": [...]} event already computed server-side (browser-mic listener,
// or Twilio's media stream broadcasting over /ws since it can't read replies itself).
function renderPushedAnswer(event) {
  const entry = { question: event.question, answers: event.answers || [],
                  error: event.found ? null : 'Nothing in the data answers this.' };
  state.answers.unshift(entry);
  $('#answers').prepend(answerCard(entry));
}

// --- live listening (experimental; UNTESTED end-to-end, see backend/listener.py) --

const listen = { ws: null, ctx: null, processor: null, stream: null, active: false };

function pcm16Base64(float32, ratio) {
  // Nearest-neighbour downsample to 16kHz (no anti-alias filter — fine for speech
  // at this bitrate, not audiophile-grade) then 16-bit PCM, base64-encoded.
  const outLength = Math.floor(float32.length / ratio);
  const pcm = new Int16Array(outLength);
  for (let i = 0; i < outLength; i++) {
    const s = Math.max(-1, Math.min(1, float32[Math.floor(i * ratio)]));
    pcm[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
  }
  const bytes = new Uint8Array(pcm.buffer);
  let binary = '';
  for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
  return btoa(binary);
}

function setListenButton(text, { live = false, disabled = false } = {}) {
  const btn = $('#listen-toggle');
  if (!btn) return;
  btn.textContent = text;
  btn.disabled = disabled;
  btn.classList.toggle('live', live);
}

async function startListening() {
  if (listen.active || !state.briefing) return;
  setListenButton('Requesting mic…', { disabled: true });
  try {
    listen.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch {
    setListenButton('Mic denied');
    return;
  }
  listen.ctx = new (window.AudioContext || window.webkitAudioContext)();
  const source = listen.ctx.createMediaStreamSource(listen.stream);
  listen.processor = listen.ctx.createScriptProcessor(4096, 1, 1);
  const ratio = listen.ctx.sampleRate / 16000;

  listen.ws = new WebSocket(`${WS_BASE}/call/${encodeURIComponent(state.briefing.client)}/listen`);
  listen.ws.addEventListener('open', () => {
    listen.active = true;
    setListenButton('Stop listening', { live: true });
  });
  listen.ws.addEventListener('message', (msg) => {
    let event;
    try { event = JSON.parse(msg.data); } catch { return; }
    if (event.type === 'answer') {
      renderPushedAnswer(event);
    } else if (event.type === 'error') {
      setListenButton(`Listener unavailable: ${event.error}`);
      stopListening({ keepMessage: true });
    }
  });
  listen.ws.addEventListener('close', () => stopListening({ keepMessage: true }));
  listen.ws.addEventListener('error', () => {});

  listen.processor.onaudioprocess = (e) => {
    if (!listen.ws || listen.ws.readyState !== WebSocket.OPEN) return;
    listen.ws.send(JSON.stringify({ audio_base_64: pcm16Base64(e.inputBuffer.getChannelData(0), ratio) }));
  };
  source.connect(listen.processor);
  listen.processor.connect(listen.ctx.destination);
}

function stopListening({ keepMessage = false } = {}) {
  if (listen.processor) { try { listen.processor.disconnect(); } catch { /* ignore */ } listen.processor = null; }
  if (listen.ctx) { try { listen.ctx.close(); } catch { /* ignore */ } listen.ctx = null; }
  if (listen.stream) { for (const t of listen.stream.getTracks()) t.stop(); listen.stream = null; }
  if (listen.ws) { const ws = listen.ws; listen.ws = null; try { ws.close(); } catch { /* ignore */ } }
  listen.active = false;
  if (!keepMessage) setListenButton('Enable live listening');
}

// --- after call ---------------------------------------------------------------

function endCall() {
  stopListening();
  clearInterval(state.timer);
  const duration = state.callStarted ? clock(Date.now() - state.callStarted) : '0:00';
  $('#note-body').textContent = callNote(duration);
  $('#email-body').textContent = followUpEmail();
  for (const tag of $$('[data-approved]')) tag.hidden = true;
  for (const btn of $$('[data-approve]')) btn.disabled = false;
  show('after');
}

function callNote(duration) {
  const b = state.briefing;
  const groups = bySlot(b);
  const when = new Date().toLocaleString('de-CH', { dateStyle: 'medium', timeStyle: 'short' });
  const lines = [
    `Client: ${callerName(b)} (${b.client})`,
    `Call: ${when}, ${duration}`,
  ];
  if (b.market && b.market.scenario && b.market.scenario !== 'empty') {
    lines.push(`Market context: ${b.market.scenario}${b.market.simulated ? ' (simulated)' : ''}`);
  }
  if (groups.reason) lines.push(`Likely reason: ${groups.reason[0].text}`);
  if (state.answers.length) {
    lines.push('', 'Discussed:');
    for (const entry of [...state.answers].reverse()) {
      lines.push(`- Q: ${entry.question}`);
      for (const a of entry.answers) lines.push(`  A: ${a.text}`);
    }
  }
  if (groups.issue) lines.push('', `Open issue: ${groups.issue[0].text.replace(/^Open issue:\s*/, '')}`);
  return lines.join('\n');
}

function followUpEmail() {
  const b = state.briefing;
  const name = callerName(b);
  const groups = bySlot(b);
  const lines = [`Dear ${name},`, '', 'Thank you for your call today.'];

  if (state.answers.length) {
    const points = [...state.answers].reverse().flatMap((entry) => entry.answers.map((a) => a.text));
    if (points.length) {
      lines.push('', 'As discussed:');
      for (const text of points) lines.push(`- ${text}`);
    }
  } else if (groups.reason) {
    lines.push('', groups.reason[0].text);
  }

  if (groups.issue) {
    lines.push('', `One open item: ${groups.issue[0].text.replace(/^Open issue:\s*/, '')}`);
  }

  lines.push('', 'I will follow up with a short review of your positions and will call you to agree on ' +
    'the next steps.', '', 'Kind regards,');
  return lines.join('\n');
}

function approve(kind) {
  state.approved[kind] = true;
  $(`[data-approved="${kind}"]`).hidden = false;
  $(`[data-approve="${kind}"]`).disabled = true;
}

// --- market + connection ------------------------------------------------------

function setMarket(market) {
  if (!market) return;
  const active = market.scenario && market.scenario !== 'empty';
  $('#market-name').textContent = active ? market.scenario : 'no market move loaded';
  $('#market-sim').hidden = !(active && market.simulated);
}

function setConn(stateName, label) {
  $('#conn').dataset.state = stateName;
  $('#conn-label').textContent = label;
}

let backoff = 500;

function connect() {
  setConn('connecting', 'Connecting');
  let ws;
  try {
    ws = new WebSocket(WS_URL);
  } catch {
    return retry();
  }
  ws.addEventListener('open', () => { backoff = 500; setConn('open', 'Live'); });
  ws.addEventListener('message', (msg) => {
    let event;
    try { event = JSON.parse(msg.data); } catch { return; }
    if (event.type === 'hello' || event.type === 'market') setMarket(event.market);
    if (event.type === 'incoming_call' && event.briefing) ring(event.briefing);
    // From the Twilio media stream, which can't read replies on its own connection.
    if (event.type === 'answer' && state.screen === 'call' && state.briefing && event.client === state.briefing.client) {
      renderPushedAnswer(event);
    }
  });
  ws.addEventListener('close', retry);
  ws.addEventListener('error', () => ws.close());

  function retry() {
    setConn('closed', 'Offline');
    setTimeout(connect, backoff);
    backoff = Math.min(backoff * 2, 10000);
  }
}

// --- wiring -------------------------------------------------------------------

$('#answer').addEventListener('click', answer);
$('#decline').addEventListener('click', () => { stopRingtone(); stopListening(); show('idle'); });
$('#end-call').addEventListener('click', endCall);
$('#done').addEventListener('click', () => show('idle'));
$('#ask-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const input = $('#ask-input');
  ask(input.value);
  input.value = '';
});
$('#listen-toggle').addEventListener('click', () => (listen.active ? stopListening() : startListening()));
for (const btn of $$('[data-approve]')) btn.addEventListener('click', () => approve(btn.dataset.approve));

if (DEMO_CLIENT) {
  const btn = $('#demo-call');
  btn.hidden = false;
  btn.addEventListener('click', async () => {
    try {
      await fetch(`${API}/call/incoming`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client: DEMO_CLIENT }),
      });
    } catch { setConn('closed', 'Offline'); }
  });
}

fetch(`${API}/market/state`).then((r) => r.json()).then(setMarket).catch(() => {});
connect();
