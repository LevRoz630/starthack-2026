"""Real, sourced outlook items: news headlines and bank / asset-manager house views.

Nothing here is written by us or an LLM. Headlines are the feeds' own titles
(German ones translated through backend/translate.py, original kept). House-view
lines are sentences copied from the fetched document; the document text is cached
next to them so every line can be checked against its source.

    python -m backend.outlook refresh [--no-llm]   # fetch feeds + house views, write data/outlook/
    python -m backend.outlook show                 # print the cached items

`outlook_facts(exposure_by_industry, total)` picks the item(s) most relevant to a
client's largest exposures for the briefing's Outlook slot.
"""

import hashlib
import html
import io
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests

from .data import ROOT
from .translate import TranslationUnavailable, translate

DIR = ROOT / 'data' / 'outlook'
DOCS = DIR / 'cio-docs'
CIO = DIR / 'cio.json'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/124 Safari/537.36', 'Accept-Language': 'en'}

# (name, url, language). Tested reachable on 2026-09-19; cash.ch, Reuters, swissinfo and
# Handelszeitung were not (broken XML, DNS, 410, broken XML).
FEEDS = [
    ('finews.ch', 'https://www.finews.ch/news?format=feed&type=rss', 'de'),
    ('finews.com', 'https://www.finews.com/news/english-news?format=feed&type=rss', 'en'),
    ('NZZ Wirtschaft', 'https://www.nzz.ch/wirtschaft.rss', 'de'),
    ('NZZ Finanzen', 'https://www.nzz.ch/finanzen.rss', 'de'),
    ('SRF Wirtschaft', 'https://www.srf.ch/news/bnf/rss/1926', 'de'),
    ('CNBC Markets', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258', 'en'),
    ('CNBC Finance', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664', 'en'),
    ('Yahoo Finance', 'https://finance.yahoo.com/news/rssindex', 'en'),
    ('MarketWatch', 'https://feeds.content.dowjones.io/public/rss/mw_marketpulse', 'en'),
    ('Financial Times', 'https://www.ft.com/markets?format=rss', 'en'),
]

# (name, url, label). UBS and Julius Baer answer 403 to scripts; these four are public.
CIO_SOURCES = [
    ('Pictet Asset Management', 'https://am.pictet.com/ch/en/investment-views/multi-asset/2026/'
                                'september-barometer-of-financial-markets-outlook', 'Barometer, Sep 2026'),
    ('Vontobel', 'https://www.vontobel.com/en-ch/insights/monthly-cio-update-september-2026-adding-weight/',
     'Monthly CIO Update, Sep 2026'),
    ('BlackRock Investment Institute', 'https://www.blackrock.com/corporate/insights/blackrock-investment-institute/'
                                       'outlook', '2026 outlook, Q4 update'),
    ('Standard Chartered', 'https://www.sc.com/en/uploads/sites/66/content/docs/'
                           'wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf',
     'Global Market Outlook, Sep 2026'),
]

INDUSTRIES = ('Information Technology', 'Health Care', 'Financials', 'Industrials', 'Consumer Discretionary',
              'Consumer Staples', 'Raw materials', 'Communication Services', 'Real Estate', 'Utilities', 'Energy')
EXTRA = ('Equities', 'Bonds', 'Gold', 'Emerging markets', 'USD', 'EUR', 'CHF')
LABELS = INDUSTRIES + EXTRA

_CI = re.IGNORECASE
TAGS = {
    'Information Technology': [re.compile(r'\b(tech|technology|chips?|semiconductors?|software|nvidia|apple|'
                                          r'microsoft|data cent(?:er|re)s?|cloud computing|artificial intelligence)\b', _CI),
                               re.compile(r'\bAI\b')],
    'Health Care': [re.compile(r'\b(pharma\w*|biotech\w*|drugs?|drugmakers?|health ?care|roche|novartis|lonza|'
                               r'medtech|hospitals?|vaccines?)\b', _CI)],
    'Financials': [re.compile(r'\b(financials|financial sector|banks?|banking|bankers?|insurers?|insurance|'
                              r'asset managers?|wealth managers?|'
                              r'wealth management|private bank\w*|fintech|lenders?|brokers?|julius b[aä]er|'
                              r'credit suisse)\b', _CI), re.compile(r'\bUBS\b')],
    'Industrials': [re.compile(r'\b(industrials?|manufactur\w*|machinery|aerospace|defen[cs]e|airlines?|logistics|'
                               r'schindler|sulzer|freight|shipping|exporters?)\b', _CI), re.compile(r'\bABB\b')],
    'Consumer Discretionary': [re.compile(r'\b(luxury|retail\w*|richemont|swatch|carmakers?|automakers?|tesla|'
                                          r'consumer spending|restaurants?|hotels?|travel)\b', _CI)],
    'Consumer Staples': [re.compile(r'\b(nestl[eé]|food|beverages?|consumer staples|supermarkets?|groceries|'
                                    r'unilever|chocolate)\b', _CI)],
    'Raw materials': [re.compile(r'\b(mining|miners?|metals?|chemicals?|glencore|holcim|copper|steel|materials|'
                                 r'lithium|commodit\w*)\b', _CI)],
    'Communication Services': [re.compile(r'\b(telecoms?|telecommunications?|swisscom|media|streaming|'
                                          r'social media|meta|alphabet|google|netflix)\b', _CI)],
    'Real Estate': [re.compile(r'\b(real estate|property|properties|housing|mortgages?|condos?|home sales|'
                               r'homebuyers?)\b', _CI), re.compile(r'\bREITs?\b')],
    'Utilities': [re.compile(r'\b(utilit(?:y|ies)|power grids?|electricity|axpo)\b', _CI)],
    'Energy': [re.compile(r'\b(oil|natural gas|crude|diesel|fuel|petrol|gasoline|energy prices)\b', _CI),
               re.compile(r'\b(OPEC|LNG)\b')],
    'Equities': [re.compile(r'\b(stocks?|equit(?:y|ies)|stock markets?|shares|wall street|s&p 500|nasdaq|'
                            r'dow|smi)\b', _CI)],
    'Bonds': [re.compile(r'\b(bonds?|yields?|treasur(?:y|ies)|fixed income|credit)\b', _CI)],
    'Gold': [re.compile(r'\bgold\b', _CI)],
    'Emerging markets': [re.compile(r'\bemerging[- ]markets?\b', _CI)],
    'USD': [re.compile(r'\b(dollar|greenback)\b', _CI), re.compile(r'\b(USD|Fed)\b')],
    'EUR': [re.compile(r'\beuro\b(?!\s+(?:area|zone))', _CI), re.compile(r'\b(EUR|ECB)\b')],
    'CHF': [re.compile(r'\b(franc|swiss national bank)\b', _CI), re.compile(r'\b(CHF|SNB)\b')],
}
# Words that state a position. "favourable" and "neutral rates" describe, they don't position.
VIEW = re.compile(r'\b(overweight|underweight|(?:to|at|on) neutral|neutral (?:stance|view|position|on)|'
                  r'upgrad\w*|downgrad\w*|prefer\w*|favou?r(?:s|ing|ed)?|attractive|cautious|constructive|'
                  r'positive on|negative on|stay \w+ on)\b', _CI)


def tag(text, near=None, window=70):
    """Labels whose keywords occur in text; with `near` (a list of positions), only
    keywords within `window` characters of one of them count."""
    out = []
    for label, patterns in TAGS.items():
        spots = [m.start() for p in patterns for m in p.finditer(text)]
        if spots and (near is None or any(abs(a - b) <= window for a in spots for b in near)):
            out.append(label)
    return out


def _id(*parts):
    return hashlib.sha1('|'.join(parts).encode('utf-8')).hexdigest()[:12]


def _when(entry, ns):
    for key in ('pubDate', f'{ns}published', f'{ns}updated', '{http://purl.org/dc/elements/1.1/}date'):
        el = entry.find(key)
        if el is not None and (el.text or '').strip():
            raw = el.text.strip()
            try:
                return parsedate_to_datetime(raw).astimezone(timezone.utc).isoformat(timespec='minutes')
            except (TypeError, ValueError):
                try:
                    return datetime.fromisoformat(raw.replace('Z', '+00:00')).astimezone(timezone.utc).isoformat(
                        timespec='minutes')
                except ValueError:
                    return None
    return None


def parse_feed(content):
    """[(title, link, published)] from RSS 2.0 or Atom."""
    root = ET.fromstring(content)
    atom = '{http://www.w3.org/2005/Atom}'
    out = []
    for item in root.iter('item'):
        title, link = (item.findtext('title') or '').strip(), (item.findtext('link') or '').strip()
        if title and link:
            out.append((html.unescape(title), link, _when(item, atom)))
    for entry in root.iter(f'{atom}entry'):
        title = (entry.findtext(f'{atom}title') or '').strip()
        link_el = entry.find(f'{atom}link')
        link = link_el.get('href', '') if link_el is not None else ''
        if title and link:
            out.append((html.unescape(title), link, _when(entry, atom)))
    return out


def fetch_news(use_llm=True):
    fetched_at = datetime.now(timezone.utc).isoformat(timespec='seconds')
    sources, items = [], []
    for name, url, lang in FEEDS:
        try:
            resp = requests.get(url, headers=UA, timeout=20)
            resp.raise_for_status()
            entries = parse_feed(resp.content)
            sources.append({'name': name, 'url': url, 'lang': lang, 'ok': True, 'count': len(entries)})
        except (requests.RequestException, ET.ParseError) as e:
            sources.append({'name': name, 'url': url, 'lang': lang, 'ok': False, 'error': f'{type(e).__name__}'})
            continue
        for title, link, published in entries:
            items.append({'id': _id(link), 'source': name, 'lang': lang, 'title': title, 'link': link,
                          'published': published, 'feed': url})

    german = [i for i in items if i['lang'] == 'de']
    try:
        english = translate([i['title'] for i in german])
    except TranslationUnavailable:
        english = [i['title'] for i in german]
    for item, en in zip(german, english):
        item['title_de'], item['title'] = item['title'], en

    seen, unique = set(), []
    for item in items:
        if item['id'] not in seen:
            seen.add(item['id'])
            item['tags'], item['tagged_by'] = tag(item['title']), 'keyword'
            unique.append(item)
    if use_llm:
        _llm_tags([i for i in unique if not i['tags']])
    return {'fetched_at': fetched_at, 'sources': sources, 'items': unique}


def _llm_tags(untagged):
    """Let Apertus label headlines the keywords missed; only labels from LABELS survive."""
    from .llm import LLMUnavailable, chat
    for start in range(0, len(untagged), 40):
        chunk = untagged[start:start + 40]
        prompt = ('Label each finance headline with the sectors or assets it is about. Use only these labels: '
                  + ', '.join(LABELS) + '. Use [] if none fits. Return JSON only: {"<number>": ["<label>", ...]}.\n\n'
                  + '\n'.join(f'{n}. {i["title"]}' for n, i in enumerate(chunk)))
        try:
            raw, _ = chat([{'role': 'user', 'content': prompt}], temperature=0, max_tokens=1500)
            labels = json.loads(raw[raw.find('{'):raw.rfind('}') + 1])
        except (LLMUnavailable, ValueError):
            return
        for n, item in enumerate(chunk):
            got = [x for x in (labels.get(str(n)) or []) if x in LABELS]
            if got:
                item['tags'], item['tagged_by'] = got, 'apertus'


def _plain(text):
    text = html.unescape(html.unescape(text))
    text = re.sub(r'(?s)<(script|style|noscript)[^>]*>.*?</\1>', ' ', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\\[rnt]', ' ', text)
    return ' '.join(text.split())


def _document_text(url):
    resp = requests.get(url, headers=UA, timeout=60)
    resp.raise_for_status()
    if 'pdf' in resp.headers.get('content-type', '') or url.lower().endswith('.pdf'):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(resp.content))
        return ' '.join(' '.join((page.extract_text() or '').split()) for page in reader.pages[:16])
    return _plain(resp.text)


SENTENCE = re.compile(r'(?<=[.!?])\s+(?=[A-Z“"‘])')


def extract_views(text, per_source=12):
    """Sentences stating a view (overweight, upgrade, prefer ...) about something we tag.
    One per tag, first occurrence wins; copied verbatim."""
    views, used = [], set()
    for sentence in SENTENCE.split(text):
        s = sentence.strip()
        if not 40 <= len(s) <= 280 or not VIEW.search(s):
            continue
        if re.search(r'cookie|privacy|subscribe|javascript|©', s, _CI):
            continue
        views_at = [m.start() for m in VIEW.finditer(s)]
        tags = [t for t in tag(s, near=views_at) if t not in used]
        if not tags:
            continue
        used.update(tags)
        views.append({'text': s, 'tags': tags})
        if len(views) >= per_source:
            break
    return views


def fetch_cio():
    fetched_at = datetime.now(timezone.utc).isoformat(timespec='seconds')
    sources, items = [], []
    DOCS.mkdir(parents=True, exist_ok=True)
    for name, url, label in CIO_SOURCES:
        try:
            text = _document_text(url)
        except Exception as e:  # any fetch or parse failure just drops that source
            sources.append({'name': name, 'url': url, 'label': label, 'ok': False, 'error': type(e).__name__})
            continue
        doc = _id(url)
        (DOCS / f'{doc}.txt').write_text(text, encoding='utf-8')
        views = extract_views(text)
        sources.append({'name': name, 'url': url, 'label': label, 'ok': True, 'doc': doc, 'count': len(views)})
        for v in views:
            assert v['text'] in text
            items.append({'id': _id(url, v['text']), 'source': name, 'url': url, 'label': label, 'doc': doc,
                          'text': v['text'], 'tags': v['tags']})
    return {'fetched_at': fetched_at, 'sources': sources, 'items': items}


def latest_news():
    snaps = sorted(DIR.glob('news-*.json'))
    if not snaps:
        return {'items': [], 'sources': []}
    with open(snaps[-1], encoding='utf-8') as f:
        return json.load(f)


def cio():
    if not CIO.exists():
        return {'items': [], 'sources': []}
    with open(CIO, encoding='utf-8') as f:
        return json.load(f)


def _news_text(item):
    when = ''
    if item.get('published'):
        d = datetime.fromisoformat(item['published'])
        when = f', {d.day} {d:%b}'
    return f'News ({item["source"]}{when}): "{item["title"]}"'


def outlook_facts(exposure_by_industry, total, limit=1, news=None, views=None):
    """The real outlook items most relevant to a client's largest exposures.

    exposure_by_industry: {industry bucket: amount}, as from facts.exposures()['industry'].
    Returns [{id, slot: 'outlook', text, source, weight}], house views before news,
    or [] when nothing real matches — the slot is then left out, never padded.
    """
    news = news if news is not None else latest_news()
    views = views if views is not None else cio()
    total = total or 1
    ranked = sorted(((k, v) for k, v in (exposure_by_industry or {}).items() if k in INDUSTRIES and v / total >= 0.03),
                    key=lambda kv: -kv[1])[:3]
    # (tier, -weight, recency, fact): house views on a top exposure first, then headlines
    # whose own words name it, then Apertus-tagged headlines, then a general equity view.
    candidates = []
    for industry, amount in ranked:
        share = amount / total
        for v in views.get('items', []):
            if industry in v['tags']:
                candidates.append((0, -share, '', f'outlook.cio.{v["id"]}',
                                   f'{v["source"]} ({v["label"]}): "{v["text"]}"', v['url'], share))
        for n in news.get('items', []):
            if industry in n.get('tags', []) and len(n['tags']) <= 3:
                tier = 1 if n.get('tagged_by') == 'keyword' else 2
                candidates.append((tier, -share, _recency(n), f'outlook.news.{n["id"]}', _news_text(n),
                                   f'{n["source"]}: {n["link"]}', share * 0.8))
    if ranked:
        for v in views.get('items', []):
            if 'Equities' in v['tags']:
                candidates.append((3, 0, '', f'outlook.cio.{v["id"]}', f'{v["source"]} ({v["label"]}): "{v["text"]}"',
                                   v['url'], 0.05))
    out, seen = [], set()
    for _, _, _, fact_id, text, source, weight in sorted(candidates, key=lambda c: c[:3]):
        if fact_id not in seen:
            seen.add(fact_id)
            out.append({'id': fact_id, 'slot': 'outlook', 'text': text, 'source': source, 'weight': weight})
        if len(out) == limit:
            break
    return out


def _recency(item):
    """Sort key that puts the newest headline first."""
    published = item.get('published') or ''
    return ''.join(chr(0x10FFFF - ord(c)) for c in published)


def refresh(use_llm=True):
    DIR.mkdir(parents=True, exist_ok=True)
    news = fetch_news(use_llm)
    path = DIR / f'news-{news["fetched_at"][:10]}.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=1)
    views = fetch_cio()
    with open(CIO, 'w', encoding='utf-8') as f:
        json.dump(views, f, ensure_ascii=False, indent=1)
    ok_feeds = [s['name'] for s in news['sources'] if s['ok']]
    ok_cio = [s['name'] for s in views['sources'] if s['ok']]
    tagged = sum(1 for i in news['items'] if i['tags'])
    print(f'news: {len(news["items"])} headlines ({tagged} tagged) from {len(ok_feeds)} feeds -> {path.name}')
    print(f'house views: {len(views["items"])} lines from {", ".join(ok_cio) or "none"} -> {CIO.name}')
    for s in news['sources'] + views['sources']:
        if not s['ok']:
            print(f'  failed: {s["name"]} ({s["error"]})')


def show():
    for v in cio()['items']:
        print(f'[CIO {v["source"]}] {", ".join(v["tags"])}: {v["text"]}')
    for n in latest_news()['items'][:40]:
        print(f'[{n["source"]}] {", ".join(n["tags"]) or "-"}: {n["title"]}')


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if argv[:1] == ['refresh']:
        refresh(use_llm='--no-llm' not in argv)
    elif argv[:1] == ['show']:
        show()
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
