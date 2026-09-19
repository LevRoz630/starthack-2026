// Tiny DOM helpers shared by web/phone and web/dashboard.

export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

export function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// Groups a briefing's {sentences: [{slot, ...}]} by slot.
export function bySlot(briefing) {
  const groups = {};
  for (const s of briefing.sentences || []) (groups[s.slot] ||= []).push(s);
  return groups;
}

export const chf = new Intl.NumberFormat('de-CH', { maximumFractionDigits: 0 });

// One briefing section: an accent-barred group with an uppercase heading and a
// sentence per fact, each followed by the sources it was computed from. Both
// front-ends render briefings this way, so the markup lives here.
// A signed percentage becomes an arrow and a colour, so a fall and a rise separate
// without being read. Money keeps its minus sign, where the arrow would read as clutter.
const SIGNED = /([\u2212+-])(\d[\d.,']*%)/g;

function withSigns(text) {
  const frag = document.createDocumentFragment();
  let last = 0;
  for (const m of text.matchAll(SIGNED)) {
    // "CHF −4k" and the like keep the minus: only bare percentages get an arrow.
    if (last < m.index) frag.append(text.slice(last, m.index));
    const down = m[1] !== '+';
    frag.append(el('span', `delta ${down ? 'neg' : 'pos'}`, `${down ? '\u2193' : '\u2191'}\u2009${m[2]}`));
    last = m.index + m[0].length;
  }
  if (!last) return null;             // nothing signed: leave the text alone
  frag.append(text.slice(last));
  return frag;
}

// Bars are drawn against the biggest line in the same group, so they compare like with
// like. The magnitude is the fact's own weight, which the briefing already carries.
function bar(share) {
  const track = el('div', 'weightbar');
  const fill = el('div', 'weightbar-fill');
  fill.style.width = `${Math.max(4, Math.min(100, share * 100))}%`;
  track.append(fill);
  return track;
}

export function renderGroup(slot, sentences, title, { sources = 'shown', weights = null } = {}) {
  const box = el('section', `group ${slot}`);
  box.append(el('h3', null, title));
  const list = el('ul');
  // Only the ranked exposures get a bar. A reason, a headline or a single "held up"
  // line has no magnitude to compare against, and a full-width bar under one row says
  // nothing except that it is the only row.
  const sized = (id) => /^digest\.(industry|fx|assetclass|region|currency)\./.test(id);
  const weightOf = (sn) => (weights ? Math.max(0, ...(sn.facts || []).filter(sized).map((id) => weights[id] || 0)) : 0);
  const top = weights ? Math.max(0, ...sentences.map(weightOf)) : 0;
  for (const s of sentences) {
    const li = el('li', 'sentence');
    const text = el('span', 'text');
    const signed = withSigns(s.text);
    if (signed) text.append(signed); else text.textContent = s.text;
    li.append(text);
    if (top > 0 && weightOf(s) > 0) li.append(bar(weightOf(s) / top));
    // The dashboard shows every source; the ringing phone does not. Nobody reads
    // 'S5INFT Index CHG_PCT_1D x clients.json CASE-043 holdings' while a phone rings,
    // and it doubles the text the advisor has to skip past to reach the number.
    if (sources === 'shown') for (const source of s.sources || []) li.append(el('span', 'source', source));
    list.append(li);
  }
  box.append(list);
  return box;
}

// One answer card: the question as asked, then the facts that answer it, each with its
// source. A chain answer renders as numbered steps with the link between them. Both
// front-ends show answers this way, so the markup lives here.
export function answerCard(entry, { sources = 'shown' } = {}) {
  // On the laptop a source is the point: the judge is checking the number came from
  // somewhere. On the phone mid-call it is noise between the advisor and the answer, so
  // it collapses to one tap and the answer gets the room.
  const source = (text) => {
    if (sources !== 'collapsed') return el('p', 'src', text);
    const box = el('details', 'src-toggle');
    box.append(el('summary', null, 'source'));
    box.append(el('p', 'src', text));
    return box;
  };
  const card = el('li', `answer-card${entry.answers.length ? '' : ' none'}`);
  card.append(el('p', 'q', `“${entry.question}”`));
  if (!entry.answers.length) {
    card.append(el('p', 'a', entry.error ? `Could not answer: ${entry.error}` : 'Nothing in the data answers this.'));
  }
  if (entry.chain) {
    card.classList.add('chain');
    const steps = el('ol', 'steps');
    for (const a of entry.answers) {
      const step = el('li', 'step');
      if (a.link) step.append(el('span', 'link', a.link));
      step.append(el('p', 'a', a.text));
      step.append(source(a.source));
      steps.append(step);
    }
    card.append(steps);
    return card;
  }
  for (const a of entry.answers) {
    card.append(el('p', 'a', a.text));
    card.append(source(a.source));
  }
  return card;
}

// Asks POST /ask about one client. Returns the entry rendered by answerCard; never throws,
// because a question that cannot be answered is itself an answer card.
export async function askAbout(api, client, question) {
  question = (question || '').trim();
  if (!question || !client) return null;
  let result;
  try {
    const resp = await fetch(`${api}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ client, question }),
    });
    result = resp.ok ? await resp.json() : { answers: [], error: `HTTP ${resp.status}` };
  } catch (e) {
    result = { answers: [], error: 'No connection' };
  }
  return { question, answers: result.answers || [], error: result.error, chain: !!result.chain,
           heard: result.heard || null };
}
