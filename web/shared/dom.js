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
export function renderGroup(slot, sentences, title) {
  const box = el('section', `group ${slot}`);
  box.append(el('h3', null, title));
  const list = el('ul');
  for (const s of sentences) {
    const li = el('li', 'sentence');
    li.append(el('span', 'text', s.text));
    for (const source of s.sources || []) li.append(el('span', 'source', source));
    list.append(li);
  }
  box.append(list);
  return box;
}
