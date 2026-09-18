// Advisor phone: idle -> ringing -> in call -> after call.
// All API text is rendered with textContent, never as HTML.

const params = new URLSearchParams(location.search);
const API = (params.get('api') || location.origin).replace(/\/$/, '');
const WS_URL = API.replace(/^http/, 'ws') + '/ws';
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
  line: null,         // 'twilio' while the phone line is being transcribed
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
  state.line = null;
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
  fetch(`${API}/call/answered`, { method: 'POST' }).catch(() => {});
  const b = state.briefing;
  const reason = (bySlot(b).reason || [])[0];
  $('[data-reason-line]').textContent = reason ? reason.text : '';
  $('[data-impact-line]').textContent = b.impact && b.impact.amount
    ? `Today: ${signedMoney(b.impact.amount)} (${signedPct(b.impact.share)})` : '';
  $('[data-impact-line]').className = `impact-line ${b.impact && b.impact.amount < 0 ? 'loss' : ''}`;
  renderBrief($('#screen-call [data-brief]'), b, { withImpact: false });
  $('#answers').replaceChildren();
  showLive('');
  setListenButton(state.line);
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

// --- live listening -------------------------------------------------------------
// The client's voice reaches /listen (this phone's microphone, 16 kHz PCM16) or
// /twilio/media (the phone line); either way transcripts and answers come back on /ws.

const LISTEN_RATE = 16000;
const LISTEN_BATCH = LISTEN_RATE / 10;   // send 100 ms per message
const mic = { stream: null, ctx: null, node: null, source: null, ws: null, pending: [] };

// Runs in the audio thread: hands raw Float32 frames to the page.
const WORKLET = `
class Tap extends AudioWorkletProcessor {
  process(inputs) {
    const ch = inputs[0] && inputs[0][0];
    if (ch) this.port.postMessage(ch.slice(0));
    return true;
  }
}
registerProcessor('tap', Tap);`;

function toPcm16(frame, inRate) {
  // Average-downsample Float32 at the device rate to Int16 at 16 kHz.
  const ratio = inRate / LISTEN_RATE;
  const out = new Int16Array(Math.floor(frame.length / ratio));
  for (let i = 0; i < out.length; i++) {
    const start = Math.floor(i * ratio);
    const end = Math.min(frame.length, Math.floor((i + 1) * ratio));
    let sum = 0;
    for (let j = start; j < end; j++) sum += frame[j];
    const v = Math.max(-1, Math.min(1, sum / Math.max(1, end - start)));
    out[i] = v < 0 ? v * 0x8000 : v * 0x7fff;
  }
  return out;
}

function queueAudio(samples) {
  for (const s of samples) mic.pending.push(s);
  while (mic.pending.length >= LISTEN_BATCH && mic.ws && mic.ws.readyState === WebSocket.OPEN) {
    mic.ws.send(Int16Array.from(mic.pending.splice(0, LISTEN_BATCH)).buffer);
  }
}

async function startListening() {
  if (mic.ws || !state.briefing) return;
  setListenButton('mic');
  try {
    mic.stream = await navigator.mediaDevices.getUserMedia({
      audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true },
    });
  } catch (e) {
    showLive('Microphone not available (needs HTTPS and permission).', 'error');
    setListenButton(null);
    return;
  }
  mic.ctx = new (window.AudioContext || window.webkitAudioContext)();
  mic.source = mic.ctx.createMediaStreamSource(mic.stream);
  const onFrame = (frame) => queueAudio(toPcm16(frame, mic.ctx.sampleRate));
  if (mic.ctx.audioWorklet) {
    const url = URL.createObjectURL(new Blob([WORKLET], { type: 'application/javascript' }));
    await mic.ctx.audioWorklet.addModule(url);
    mic.node = new AudioWorkletNode(mic.ctx, 'tap');
    mic.node.port.onmessage = (e) => onFrame(e.data);
    mic.source.connect(mic.node);
  } else {
    mic.node = mic.ctx.createScriptProcessor(4096, 1, 1);
    mic.node.onaudioprocess = (e) => onFrame(e.inputBuffer.getChannelData(0));
    mic.source.connect(mic.node);
    mic.node.connect(mic.ctx.destination);
  }
  const wsUrl = `${API.replace(/^http/, 'ws')}/listen?client=${encodeURIComponent(state.briefing.client)}`;
  mic.ws = new WebSocket(wsUrl);
  mic.ws.binaryType = 'arraybuffer';
  mic.ws.addEventListener('close', () => { if (mic.ws) stopListening(); });
  showLive('Listening…');
}

function stopListening() {
  const ws = mic.ws;
  mic.ws = null;
  if (ws) {
    try { if (ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify({ type: 'stop' })); } catch { /* ignore */ }
    try { ws.close(); } catch { /* ignore */ }
  }
  try { mic.source && mic.source.disconnect(); } catch { /* ignore */ }
  try { mic.node && mic.node.disconnect(); } catch { /* ignore */ }
  if (mic.stream) for (const t of mic.stream.getTracks()) t.stop();
  if (mic.ctx) mic.ctx.close().catch(() => {});
  Object.assign(mic, { stream: null, ctx: null, node: null, source: null, pending: [] });
  setListenButton(null);
}

function setListenButton(source) {
  const btn = $('#listen');
  btn.setAttribute('aria-pressed', source === 'mic' ? 'true' : 'false');
  if (source === 'twilio') btn.dataset.source = 'twilio'; else delete btn.dataset.source;
  btn.textContent = source === 'mic' ? 'Stop' : source === 'twilio' ? 'On the line' : 'Listen';
  btn.disabled = source === 'twilio';
}

function showLive(text, kind) {
  const line = $('#live-transcript');
  line.textContent = text || '';
  line.className = `live${kind ? ` ${kind}` : ''}`;
}

// Events from the listener (either source) for the client on the line.
function onListenerEvent(event) {
  if (!state.briefing || event.client !== state.briefing.client) return;
  if (event.type === 'listening' && event.source !== 'browser') { state.line = 'twilio'; setListenButton('twilio'); }
  if (event.type === 'listening_stopped' && event.source !== 'browser') { state.line = null; setListenButton(mic.ws ? 'mic' : null); }
  if (event.type === 'listener_error') showLive(`Listener: ${event.error}`, 'error');
  if (state.screen !== 'call') return;
  if (event.type === 'transcript') showLive(event.text, event.final ? 'final' : '');
  if (event.type === 'answer') {
    const entry = { question: event.question, answers: event.answers || [] };
    state.answers.unshift(entry);
    $('#answers').prepend(answerCard(entry));
    showLive('');
  }
}

// --- after call ---------------------------------------------------------------

function endCall() {
  stopListening();
  $('#caller-voice').pause();
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
  const name = callerName(state.briefing);
  return [
    `Dear ${name},`,
    '',
    'Thank you for your call today. As discussed, I have reviewed how today\'s market ' +
      'movements affect your portfolio and noted your questions.',
    '',
    'I will follow up with a short review of your positions and will call you to agree on ' +
      'the next steps.',
    '',
    'Kind regards,',
  ].join('\n');
}

async function approve(kind) {
  const btn = $(`[data-approve="${kind}"]`);
  const tag = $(`[data-approved="${kind}"]`);
  btn.disabled = true;
  tag.hidden = false;
  tag.classList.remove('error');
  tag.textContent = 'Sending…';
  try {
    const resp = await fetch(`${API}/followup/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ client: state.briefing.client, kind, body: $(kind === 'email' ? '#email-body' : '#note-body').textContent }),
    });
    const result = await resp.json();
    if (!resp.ok) throw new Error(result.error || resp.status);
    state.approved[kind] = true;
    tag.textContent = result.sent ? `Sent to ${result.to}` : 'Saved to outbox (email not set up)';
  } catch (err) {
    tag.textContent = `Not sent: ${err.message}`;
    tag.classList.add('error');
    btn.disabled = false;
  }
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
    if (['transcript', 'answer', 'listening', 'listening_stopped', 'listener_error'].includes(event.type)) {
      onListenerEvent(event);
    }
    if (event.type === 'demo_audio' && state.screen === 'call' && state.briefing && event.client === state.briefing.client) {
      const voice = $('#caller-voice');
      voice.src = `${API}${event.url}`;
      voice.play().catch(() => {});
    }
    if (event.type === 'call_ended' && state.screen === 'call' && state.briefing && event.client === state.briefing.client) {
      endCall();
    }
    if (event.type === 'demo_started' || event.type === 'demo_finished') demoStatus(event);
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
$('#decline').addEventListener('click', () => { stopRingtone(); show('idle'); });
$('#end-call').addEventListener('click', endCall);
$('#listen').addEventListener('click', () => (mic.ws ? stopListening() : startListening()));
$('#done').addEventListener('click', () => show('idle'));
$('#ask-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const input = $('#ask-input');
  ask(input.value);
  input.value = '';
});
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

function demoStatus(event) {
  const status = $('#demo-status');
  status.hidden = false;
  status.textContent = event.type === 'demo_started' ? `Recorded call "${event.script}" running`
    : `Recorded call finished (${event.result})`;
}

async function runDemo(mode) {
  const status = $('#demo-status');
  status.hidden = false;
  status.textContent = mode === 'replay' ? 'Replaying the saved call…' : 'Preparing the recorded call…';
  try {
    const resp = await fetch(`${API}/demo/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ script: params.get('script') || 'golf', mode }),
    });
    const result = await resp.json();
    if (!resp.ok) status.textContent = result.error || 'Could not start';
  } catch { status.textContent = 'Offline'; }
}

if (DEMO_CLIENT) {
  for (const [id, mode] of [['#demo-recorded', 'pipeline'], ['#demo-replay', 'replay']]) {
    const b = $(id);
    b.hidden = false;
    b.addEventListener('click', () => runDemo(mode));
  }
}

fetch(`${API}/market/state`).then((r) => r.json()).then(setMarket).catch(() => {});
connect();
