// Advisor phone: idle -> ringing -> in call -> after call.
// All API text is rendered with textContent, never as HTML.

import { $, $$, el, answerCard, askAbout, bySlot, chf, renderGroup } from '/shared/dom.js';

const params = new URLSearchParams(location.search);
const API = (params.get('api') || location.origin).replace(/\/$/, '');
const WS_BASE = API.replace(/^http/, 'ws');
const WS_URL = `${WS_BASE}/ws`;
// Two demos. SILENT replays a saved run -- questions and answer cards on their real
// timing, nothing spoken, no network -- which is what the video is filmed against.
// VOICED runs a different client and scenario through ElevenLabs and the live
// speech-to-text, so the cards are produced rather than replayed. ?script= overrides.
const SILENT_SCRIPT = params.get('script') || 'walter';
const VOICED_SCRIPT = params.get('voiced') || 'walter';
let DEMO_CLIENT = params.get('demo') || null;   // filled from the script by loadDemo()

const SLOT_TITLES = {
  who: 'Client',
  development: 'Development',
  health: 'Health check',
  watch: 'Watch',
  outlook: 'Outlook',
  actions: 'Next best actions',
  reason: 'Why they are calling',
  digest: 'What fell',
  holding: 'What held up',
};

const state = {
  screen: 'idle',
  briefing: null,
  answers: [],        // {question, answers: [{text, source}]}
  callStarted: null,
  timer: null,
  approved: {},
  line: null,         // 'recorded' while the call's own audio is being transcribed
  demoRunning: false, // a recorded demo call is running on the server
};

// --- formatting -------------------------------------------------------------

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

function callerName(briefing) {
  return briefing.name || briefing.client;
}

// What the advisor can actually take in while the phone is ringing: why they are
// calling, what it cost, the two or three biggest pieces of that, and what held up.
// Sources are dropped here and the digest is capped -- the full set with every source
// is a tap away under "Full briefing", and on the dashboard.
const RINGING_DIGEST = 3;

// Which fund a loss came through is detail for during the call, not for the four seconds
// before the advisor picks up. The number and the share stay; the attribution tail goes,
// and the untrimmed sentence with its source is under "Full briefing" once the call starts.
const shorten = (text) => text.replace(/,? mostly via .*$/, '.').replace(/\.\.$/, '.');

function renderBrief(container, briefing, { withImpact, brief = false }) {
  container.replaceChildren();
  const groups = bySlot(briefing);
  // id -> weight, so each line can be drawn at the size of what it actually cost.
  const weights = Object.fromEntries((briefing.facts || []).map((f) => [f.id, f.weight || 0]));
  const opts = { weights, ...(brief ? { sources: 'hidden' } : {}) };
  const card = el('div', 'card');

  // Keep the reason above the number: it is what the advisor needs first.
  if (groups.reason) card.append(group('reason', groups.reason.slice(0, brief ? 1 : undefined), null, opts));

  if (withImpact && briefing.impact && briefing.impact.amount) {
    const box = el('div', 'impact');
    box.append(el('p', 'eyebrow', 'Today on the book'));
    const cls = briefing.impact.amount < 0 ? 'loss' : 'gain';
    box.append(el('p', `amount ${cls}`, signedMoney(briefing.impact.amount)));
    box.append(el('p', 'share', signedPct(briefing.impact.share)));
    card.append(box);
  }

  for (const slot of ['digest', 'holding']) {
    let lines = groups[slot];
    if (!lines) continue;
    if (brief && slot === 'digest') {
      // "Behind the move" is a headline, not an exposure; one is context, two is noise.
      const moves = lines.filter((l) => !/^Behind the move/.test(l.text));
      const headline = lines.find((l) => /^Behind the move/.test(l.text));
      lines = moves.slice(0, RINGING_DIGEST).concat(headline ? [headline] : []);
    }
    if (brief) lines = lines.map((l) => ({ ...l, text: shorten(l.text) }));
    card.append(group(slot, lines, null, opts));
  }
  // Profile note from the caller slot, if any, goes last on the full briefing.
  const profile = (groups.caller || []).slice(1);
  if (!brief && profile.length) card.append(group('caller', profile, 'Profile'));

  if (card.childElementCount) container.append(card);
}

function group(slot, sentences, title, opts) {
  return renderGroup(slot, sentences, title || SLOT_TITLES[slot] || slot, opts);
}

function fillCaller(briefing) {
  for (const node of $$('[data-caller-name]')) node.textContent = callerName(briefing);
  for (const node of $$('[data-caller-ref]')) node.textContent = briefing.client;
}

// --- ringing ----------------------------------------------------------------

function ring(briefing) {
  if (state.screen === 'call') return; // never interrupt a call in progress
  state.briefing = briefing;
  state.answers = [];
  state.heard = [];
  $('#heard').replaceChildren();
  state.approved = {};
  state.line = null;
  fillCaller(briefing);
  renderBrief($('#screen-ringing [data-brief]'), briefing, { withImpact: true, brief: true });
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
  renderBrief($('#screen-call [data-brief]'), b, { withImpact: false, brief: true });
  $('#answers').replaceChildren();
  showLive('');
  $('#waiting').hidden = false;
  $('#ask-form').hidden = true;
  $('#type-toggle').setAttribute('aria-expanded', 'false');
  setListenButton(state.line);
  // Nothing is dialled on a simulated call, so the microphone is the only way the client
  // can be heard. Answer is a user gesture, which is what getUserMedia requires.
  if (!state.line) startListening();
  state.callStarted = Date.now();
  $('#timer').textContent = '0:00';
  clearInterval(state.timer);
  state.timer = setInterval(() => { $('#timer').textContent = clock(Date.now() - state.callStarted); }, 1000);
  show('call');
  // Deliberately no focus() on the ask input: the listener is already running and
  // answers arrive over the socket, so focusing here would only raise the software
  // keyboard over the briefing at the moment the advisor picks up.
}

async function ask(question) {
  if (!state.briefing) return null;
  const entry = await askAbout(API, state.briefing.client, question);
  if (!entry) return null;
  state.answers.unshift(entry);
  $('#answers').prepend(answerCard(entry, { sources: 'collapsed' }));
  $('#waiting').hidden = true;
  return entry;
}

// Inject a question heard on the line (used by the recorded-call pipeline).
window.pushAnswer = (question) => ask(question);

// --- live listening -------------------------------------------------------------
// The client's voice reaches /listen (this phone's microphone, 16 kHz PCM16) or
// or the recorded call's own audio; either way transcripts and answers come back on /ws.

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
  if (source === 'recorded') btn.dataset.source = 'recorded'; else delete btn.dataset.source;
  // What the advisor needs to know is whether it can hear the client, not what tapping
  // does; the label is the state, and the dot pulses while audio is arriving.
  $('#listen-label').textContent = source === 'mic' ? 'Hearing you'
    : source === 'recorded' ? 'On the line' : 'Not hearing';
  btn.disabled = source === 'recorded';
  btn.title = source === 'mic' ? 'Stop listening' : 'Start listening';
}

function showLive(text, kind) {
  const line = $('#live-transcript');
  line.textContent = text || '';
  line.className = `live${kind ? ` ${kind}` : ''}`;
}

// Events from the listener (either source) for the client on the line.
function onListenerEvent(event) {
  if (!state.briefing || event.client !== state.briefing.client) return;
  if (event.type === 'listening' && event.source !== 'browser') {
    if (mic.ws) stopListening();   // the recorded line is the client; the phone mic would hear the advisor too
    state.line = 'recorded';
    setListenButton('recorded');
  }
  if (event.type === 'listening_stopped' && event.source !== 'browser') { state.line = null; setListenButton(mic.ws ? 'mic' : null); }
  if (event.type === 'listener_error') showLive(`Listener: ${event.error}`, 'error');
  if (state.screen !== 'call') return;
  if (event.type === 'transcript') showLive(event.text, event.final ? 'final' : '');
  if (event.type === 'heard') {
    // Not a card: a quiet line now, and a line in the call note later.
    state.heard = state.heard || [];
    state.heard.push({ kind: event.kind, label: event.label, text: event.text });
    const item = el('li');
    item.dataset.kind = event.kind;
    item.append(el('span', 'kind', event.label), document.createTextNode(event.text));
    $('#heard').prepend(item);
  }
  if (event.type === 'answer') {
    const entry = { question: event.question, answers: event.answers || [], chain: !!event.chain };
    state.answers.unshift(entry);
    $('#answers').prepend(answerCard(entry, { sources: 'collapsed' }));
  $('#waiting').hidden = true;
    // The final question stays under the header: it is what the new card answers,
    // and clearing it here used to collapse the strip just as the card arrived.
  }
}

// --- the advisor's turn in a recorded demo call --------------------------------------
// Demo machinery only, never on screen: a real client does not wait for a server. The
// recorded client asks, the card arrives, then it waits while the phone listens to the
// advisor (locally, nothing is sent) and tells the server once they stop talking.
// If the room is too loud or the mic is refused: double-tap the call timer, or press
// Space on a laptop. The server carries on by itself after turn_timeout anyway.

const turn = { stream: null, ctx: null, timer: null, arming: null, active: false };

function beginTurn() {
  stopTurn();
  turn.active = true;
  // Start listening once the client's own voice has finished playing from the speaker.
  const voice = $('#caller-voice');
  const left = voice && !voice.paused && !voice.ended && isFinite(voice.duration)
    ? (voice.duration - voice.currentTime) * 1000 : 0;
  turn.arming = setTimeout(startTurnDetector, Math.max(300, left + 300));
}

async function startTurnDetector() {
  try {
    turn.stream = await navigator.mediaDevices.getUserMedia({
      audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true },
    });
  } catch {
    return;   // no mic: the discreet fallbacks or the server's timeout end the turn
  }
  turn.ctx = new (window.AudioContext || window.webkitAudioContext)();
  const analyser = turn.ctx.createAnalyser();
  analyser.fftSize = 1024;
  turn.ctx.createMediaStreamSource(turn.stream).connect(analyser);
  const buf = new Float32Array(analyser.fftSize);
  const started = Date.now();
  let noise = 0;
  let loud = 0;
  let quiet = 0;
  let heard = false;
  turn.timer = setInterval(() => {
    analyser.getFloatTimeDomainData(buf);
    let sum = 0;
    for (const v of buf) sum += v * v;
    const rms = Math.sqrt(sum / buf.length);
    if (Date.now() - started < 600) { noise = Math.max(noise, rms); return; }   // room level first
    const speaking = rms > Math.max(0.015, noise * 2.5);
    if (speaking) { loud += 50; quiet = 0; if (loud >= 300) heard = true; }
    else { quiet += 50; if (!heard) loud = 0; }
    if (heard && quiet >= 1300) endTurn();    // spoke, then 1.3 s of quiet: done
  }, 50);
}

function stopTurn() {
  clearTimeout(turn.arming);
  clearInterval(turn.timer);
  if (turn.stream) for (const t of turn.stream.getTracks()) t.stop();
  if (turn.ctx) turn.ctx.close().catch(() => {});
  Object.assign(turn, { stream: null, ctx: null, timer: null, arming: null, active: false });
}

function endTurn() {
  if (!turn.active) return;
  stopTurn();
  fetch(`${API}/demo/next`, { method: 'POST' }).catch(() => {});
}

// --- after call ---------------------------------------------------------------

// A recorded demo call keeps running on the server until told otherwise. Stopping it from
// End call / Decline lets the next "Start the call" begin straight away. A call the server
// ends itself is not stopped: that run finished and becomes the saved replay.
function stopDemo() {
  // Always tell the server, even if this page missed the demo starting (reloaded mid-call):
  // stopping when nothing runs is harmless, a call left running is not.
  state.demoRunning = false;
  fetch(`${API}/demo/stop`, { method: 'POST' }).catch(() => {});
}

function endCall() {
  $('#caller-voice').pause();
  stopTurn();
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
    lines.push(`Market context: ${b.market.scenario}`);
  }
  if (groups.reason) lines.push(`Likely reason: ${groups.reason[0].text}`);
  if (state.answers.length) {
    lines.push('', 'Discussed:');
    for (const entry of [...state.answers].reverse()) {
      lines.push(`- Q: ${entry.question}`);
      for (const a of entry.answers) lines.push(`  A: ${a.text}`);
    }
  }
  const heard = state.heard || [];
  const section = (title, kind) => {
    const items = heard.filter((h) => h.kind === kind);
    if (items.length) lines.push('', `${title}:`, ...items.map((h) => `- ${h.text}`));
  };
  section('Instructions given (not executed, confirm in writing)', 'instruction');
  section('To do', 'request');
  section('Open questions (not answered from the data)', 'follow_up');
  section('Noted', 'info');
  return lines.join('\n');
}

// The client may only be sent statements about their own portfolio. The advisor's side
// of the card — why we think they called, the playbook wording, and the market headline
// — never goes into their inbox. Headline facts are id'd news.*, so this catches them.
const ADVISOR_ONLY = /^(reason|news|talk)\b/;

function forTheClient(answers) {
  const out = [];
  for (const a of answers) {
    if (ADVISOR_ONLY.test(a.fact || '')) continue;
    // Two layers often state the same fact in slightly different words; the client
    // should read it once. The opening clause is what identifies it.
    const head = a.text.slice(0, 32).toLowerCase();
    if (out.some((t) => t.slice(0, 32).toLowerCase() === head)) continue;
    if (!out.includes(a.text)) out.push(a.text);
  }
  return out;
}

const MAX_EMAIL_POINTS = 6;

// Card sentences are written for the advisor ("of the book", "after fund look-through");
// the client reads the same fact in their own terms. Numbers are never touched.
function inClientWords(text) {
  return text
    .replace(/ after fund look-through/g, '')
    .replace(/ of the book/g, ' of your portfolio')
    .replace(/^The book is/, 'Your portfolio is')
    .replace(/^(?:Combined portfolio value|Portfolio value)(?= [+−])/, 'Your portfolio moved')
    .replace(/^(Combined portfolio value|Portfolio value)/, 'Your portfolio value')
    .replace(/; value change including deposits and withdrawals\.$/, ' (this includes deposits and withdrawals).');
}

function partOfDay() {
  const h = new Date().getHours();
  return h < 12 ? 'this morning' : h < 18 ? 'this afternoon' : 'this evening';
}

function followUpEmail() {
  const b = state.briefing;
  const name = callerName(b);
  const heard = state.heard || [];
  const answered = [...state.answers].reverse().flatMap((entry) => entry.answers);
  // Only say what the call was about if the market actually came up in it.
  const aboutMarket = answered.some((a) => /^(digest|topic|total|holding)/.test(a.fact || ''));
  const lines = [`Dear ${name},`, '',
    `Thank you for your call ${partOfDay()}${aboutMarket ? " about today's market move" : ''}.`];

  const points = forTheClient(answered).map(inClientWords);
  if (points.length) {
    lines.push('', 'Here is what we went through:');
    for (const text of points.slice(0, MAX_EMAIL_POINTS)) lines.push(`- ${text}`);
  }

  // What they asked for, in their own words, and what happens next. Nothing noted about
  // their private life goes into an email; that stays in the call note.
  const requests = heard.filter((h) => h.kind === 'request');
  const open = heard.filter((h) => h.kind === 'follow_up');
  if (requests.length || open.length) {
    lines.push('', 'You also asked me to follow up on:');
    for (const h of requests) lines.push(`- "${h.text}" I will take care of this.`);
    for (const h of open) lines.push(`- "${h.text}" I will come back to you with an answer.`);
  }

  // An instruction heard on a call is never executed from the call alone.
  const instructions = heard.filter((h) => h.kind === 'instruction');
  if (instructions.length) {
    lines.push('', 'You also gave me an instruction:');
    for (const h of instructions) lines.push(`- "${h.text}"`);
    lines.push('Nothing has been executed yet. I will send you a proposal to confirm in writing first.');
  }

  const next = instructions.length ? 'I will be in touch shortly.'
    : (requests.length || open.length) ? 'I will get back to you on these points within the next working day.'
      : 'I will call you next week to go through your positions together.';
  lines.push('', next, '', 'Kind regards,');
  return lines.join('\n');
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

// --- prepare for a client -------------------------------------------------------
// Type a name, company or number; get the briefing that is already prepared for them.

async function prepareClient(query, ref) {
  const status = $('#prep-status');
  const list = $('#prep-matches');
  list.replaceChildren();
  status.hidden = false;
  status.textContent = 'Looking up…';
  let data;
  try {
    const params = new URLSearchParams({ q: query || '' });
    if (ref) params.set('client', ref);
    const resp = await fetch(`${API}/prepare?${params}`);
    data = await resp.json();
  } catch {
    status.textContent = 'Offline';
    return;
  }
  if (!data.client) {
    if (!data.matches || !data.matches.length) {
      status.textContent = `No client matches "${query}".`;
      return;
    }
    status.textContent = 'Which one?';
    for (const m of data.matches) {
      const btn = el('button', 'btn secondary wide', `${m.name} · ${m.client}`);
      btn.type = 'button';
      btn.addEventListener('click', () => prepareClient(query, m.client));
      const item = el('li');
      item.append(btn);
      list.append(item);
    }
    return;
  }
  status.hidden = true;
  showPrepared(data);
}

function showPrepared(data) {
  state.prepared = data;
  $('#prep-name').textContent = data.name;
  $('#prep-ref').textContent = data.client;
  const phrasing = $('#prep-phrasing');
  phrasing.hidden = data.briefing.phrasing !== 'ready';
  phrasing.textContent = 'Apertus';
  const brief = $('#prep-brief');
  brief.replaceChildren();
  for (const slot of ['who', 'development', 'health', 'watch', 'outlook', 'actions']) {
    const sentences = data.briefing.sentences.filter((s) => s.slot === slot);
    if (!sentences.length) continue;
    const box = el('section', `group ${slot}`);
    box.append(el('h3', null, SLOT_TITLES[slot]));
    const list = el('ul');
    for (const s of sentences) {
      const item = el('li');
      item.append(el('p', 'a', s.text));
      for (const src of s.sources || []) item.append(el('p', 'src', src));
      list.append(item);
    }
    box.append(list);
    brief.append(box);
  }
  const call = data.call;
  const hasMarket = call && call.market && call.market.scenario && call.market.scenario !== 'empty';
  $('#prep-call-card').hidden = !hasMarket;
  if (hasMarket) {
    renderBrief($('#prep-call-brief'), call, { withImpact: true });
  }
  show('prepared');
}

// The Prepare box is off the idle screen; prepareClient() and the prepared screen stay,
// so putting the form back in index.html is all it takes to bring the flow back.
const prepForm = $('#prep-form');
if (prepForm) {
  prepForm.addEventListener('submit', (e) => {
    e.preventDefault();
    prepareClient($('#prep-input').value.trim());
  });
}
$('#prep-back').addEventListener('click', () => { $('#brief-voice').pause(); show('idle'); });
$('#prep-listen').addEventListener('click', () => {
  const voice = $('#brief-voice');
  if (!state.prepared) return;
  voice.src = `${API}/briefing/${encodeURIComponent(state.prepared.client)}/audio`;
  voice.play().catch(() => {});
});
// Ring as the client looked up: a live call, answered with the microphone. Any recorded
// demo still running is stopped first, or its Answer would start that call too. The
// client also becomes the one "Ring only" uses.
$('#prep-call').addEventListener('click', async () => {
  if (!state.prepared) return;
  DEMO_CLIENT = state.prepared.client;
  $('#demo-caller').textContent = `${state.prepared.name} is ready to call.`;
  $('#brief-voice').pause();
  try {
    await fetch(`${API}/demo/stop`, { method: 'POST' });
    await fetch(`${API}/call/incoming`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ client: state.prepared.client }),
    });
  } catch { setConn('closed', 'Offline'); }
});

// --- market + connection ------------------------------------------------------

function setMarket(market) {
  if (!market) return;
  const active = market.scenario && market.scenario !== 'empty';
  $('#market-name').textContent = active ? market.scenario : 'no market move loaded';
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
    if (['transcript', 'answer', 'heard', 'listening', 'listening_stopped', 'listener_error'].includes(event.type)) {
      onListenerEvent(event);
    }
    // A replayed run carries its demo_audio events too, but the silent demo must stay
    // silent: only the live pipeline's audio is played.
    if (event.type === 'demo_audio' && !event.replayed
        && state.screen === 'call' && state.briefing && event.client === state.briefing.client) {
      const voice = $('#caller-voice');
      voice.src = `${API}${event.url}`;
      voice.play().catch(() => {});
    }
    if (event.type === 'call_ended' && state.screen === 'call' && state.briefing && event.client === state.briefing.client) {
      endCall();
    }
    if (event.type === 'demo_started') state.demoRunning = true;
    if (event.type === 'demo_finished') { state.demoRunning = false; stopTurn(); }
    if (event.type === 'demo_turn' && state.screen === 'call' && state.briefing && event.client === state.briefing.client) {
      beginTurn();
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
$('#decline').addEventListener('click', () => { stopDemo(); stopRingtone(); stopListening(); show('idle'); });
$('#end-call').addEventListener('click', () => { stopDemo(); endCall(); });
$('#timer').addEventListener('dblclick', endTurn);
document.addEventListener('keydown', (e) => {
  if (e.code === 'Space' && turn.active && document.activeElement === document.body) { e.preventDefault(); endTurn(); }
});
$('#listen').addEventListener('click', () => (mic.ws ? stopListening() : startListening()));
$('#type-toggle').addEventListener('click', () => {
  const form = $('#ask-form');
  form.hidden = !form.hidden;
  $('#type-toggle').setAttribute('aria-expanded', String(!form.hidden));
  if (!form.hidden) $('#ask-input').focus();
});
$('#done').addEventListener('click', () => show('idle'));
$('#ask-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const input = $('#ask-input');
  ask(input.value);
  input.value = '';
});
for (const btn of $$('[data-approve]')) btn.addEventListener('click', () => approve(btn.dataset.approve));

// Ring the advisor and push the briefing. Nothing is voiced -- a person speaks the
// client's lines into the microphone, which starts itself when the call is answered.
$('#demo-call').addEventListener('click', async () => {
  if (!DEMO_CLIENT) return;
  try {
    await fetch(`${API}/call/incoming`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ client: DEMO_CLIENT }),
    });
  } catch { setConn('closed', 'Offline'); }
});

function demoStatus(event) {
  const status = $('#demo-status');
  status.hidden = false;
  status.textContent = event.type === 'demo_started' ? `Call "${event.script}" running`
    : `Call finished (${event.result})`;
}

async function runDemo(script, mode) {
  const status = $('#demo-status');
  status.hidden = false;
  status.textContent = mode === 'replay' ? 'Starting the call…' : 'Preparing the voiced call…';
  try {
    const resp = await fetch(`${API}/demo/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ script, mode }),
    });
    const result = await resp.json();
    if (!resp.ok) status.textContent = result.error || 'Could not start';
  } catch { status.textContent = 'Offline'; }
}

$('#demo-silent').addEventListener('click', () => runDemo(SILENT_SCRIPT, 'replay'));
$('#demo-voice').addEventListener('click', () => runDemo(VOICED_SCRIPT, 'pipeline'));

// Who each demo rings as, and whether the silent one has a saved run to replay.
async function loadDemo() {
  let info;
  try {
    info = await fetch(`${API}/demo/scripts`).then((r) => r.json());
  } catch {
    return;
  }
  const clients = info.clients || {};
  const names = info.names || {};
  const who = (script) => names[clients[script]] || clients[script] || script;
  DEMO_CLIENT = DEMO_CLIENT || clients[SILENT_SCRIPT] || null;
  const replayable = (info.replayable || {})[SILENT_SCRIPT];
  $('#demo-silent').disabled = !replayable;
  $('#demo-silent').title = replayable ? '' : 'No saved call to replay yet';
  $('#demo-caller').textContent =
    `${who(SILENT_SCRIPT)} calls silently; ${who(VOICED_SCRIPT)} calls with voice.`;
  $('#demo-call').disabled = !DEMO_CLIENT;
}

loadDemo();

fetch(`${API}/market/state`).then((r) => r.json()).then(setMarket).catch(() => {});
connect();
