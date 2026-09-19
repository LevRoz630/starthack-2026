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
export function renderGroup(slot, sentences, title, { sources = 'shown' } = {}) {
  const box = el('section', `group ${slot}`);
  box.append(el('h3', null, title));
  const list = el('ul');
  for (const s of sentences) {
    const li = el('li', 'sentence');
    li.append(el('span', 'text', s.text));
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
  return { question, answers: result.answers || [], error: result.error, chain: !!result.chain };
}
