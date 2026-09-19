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
