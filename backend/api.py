"""HTTP + WebSocket API over the briefing engine.

    uvicorn backend.api:app --reload --port 8000

Endpoints (JSON unless noted):

    GET  /health
    GET  /clients                      client list for the dashboard
    POST /clients                      upload a clients.json-shaped file (multipart "file" or JSON body)
    GET  /briefing/{ref}               the 60-second briefing; Apertus-phrased once ready, fact text until then
    GET  /market/scenarios             available scenarios
    GET  /market/state                 current market moves and headlines
    POST /market/events                {"scenario": name} or {"ticks": [...]}: update the market, re-rank
    GET  /callers                      clients the market hit hardest, with their likely reason to call
    GET  /call/{ref}                   the incoming-call briefing for a client
    POST /call/incoming                {"from": "+41..."} or {"client": ref}; Twilio form posts work too.
                                       Pushes the call briefing to every /ws subscriber.
    POST /ask                          {"client": ref, "question": "..."}: the facts that answer it
    WS   /ws                           pushes {"type": "incoming_call" | "market", ...} events
    GET  /phone/                       the advisor phone app (web/phone)

Environment: DEMO_SCENARIO preloads a scenario; BRIEFING_LLM=0 turns off Apertus phrasing.
"""

import asyncio
import json
import os
import re
import tempfile
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

from . import briefing, callmode
from .data import ROOT, load
from .facts import client_name, compute
from .market import MarketState, load_scenario, scenarios

PHONEBOOK = ROOT / 'data' / 'phonebook.json'
PHONE_APP = ROOT / 'web' / 'phone'


class State:
    def __init__(self):
        self.store = load()
        self.market = MarketState()
        self.phrased = {}           # ref -> briefing phrased by the LLM
        self.pending = set()        # refs being phrased right now
        self.sockets = set()
        self.use_llm = os.getenv('BRIEFING_LLM', '1') != '0'
        self.pool = ThreadPoolExecutor(max_workers=4)
        self.phonebook = self._phonebook()

    def _phonebook(self):
        """Caller numbers -> ClientRef. The data has no phone numbers, so the demo maps
        its own in data/phonebook.json (gitignored: those are real numbers)."""
        if not PHONEBOOK.exists():
            return {}
        with open(PHONEBOOK, encoding='utf-8') as f:
            return {normalise_number(k): v for k, v in json.load(f).items() if not k.startswith('_')}

    def precompute(self, refs=None):
        """Phrase briefings in the background so the dashboard never waits on the LLM."""
        if not self.use_llm:
            return
        for ref in refs or list(self.store.clients):
            if ref not in self.pending:
                self.pending.add(ref)
                self.pool.submit(self._phrase, ref)

    def _phrase(self, ref):
        try:
            b = briefing.build(self.store, ref, use_llm=True)
            if b['provider'] != 'template':
                self.phrased[ref] = b
        finally:
            self.pending.discard(ref)

    async def broadcast(self, event):
        dead = set()
        for ws in self.sockets:
            try:
                await ws.send_json(event)
            except (RuntimeError, WebSocketDisconnect):
                dead.add(ws)
        self.sockets -= dead


state = None


def normalise_number(number):
    return re.sub(r'[^\d+]', '', number or '')


def error(status, message):
    return JSONResponse({'error': message}, status_code=status)


def client_or_404(ref):
    if ref not in state.store.clients:
        return None, error(404, f'unknown client {ref}')
    return state.store.clients[ref], None


async def body(request):
    """JSON or form body as a dict; Twilio posts forms."""
    if 'application/json' in request.headers.get('content-type', ''):
        try:
            data = await request.json()
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None
    return dict(await request.form())


async def health(request):
    return JSONResponse({'ok': True, 'clients': len(state.store.clients), 'market': state.market.name,
                         'phrased': len(state.phrased), 'llm': state.use_llm})


async def list_clients(request):
    rows = [{'client': ref, 'name': client_name(c), 'aum': c.get('AssetsUnderManagementInDefaultCurrency'),
             'currency': c.get('ReportingCurrency'), 'risk_profile': c.get('RiskProfileName')}
            for ref, c in sorted(state.store.clients.items())]
    return JSONResponse(rows)


async def upload_clients(request):
    """Add clients from a clients.json-shaped file, e.g. the jury's test client."""
    if 'multipart/form-data' in request.headers.get('content-type', ''):
        upload = (await request.form()).get('file')
        if upload is None or isinstance(upload, str):
            return error(400, 'expected a multipart field "file"')
        raw = await upload.read()
    else:
        raw = await request.body()
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return error(400, 'file is not valid JSON')
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not data or not all(isinstance(c, dict) and c.get('ClientRef') for c in data):
        return error(400, 'expected a clients.json-shaped array of clients, each with a ClientRef')
    previous = {c['ClientRef']: state.store.clients.get(c['ClientRef']) for c in data}
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(data, f)
    state.store.add_clients(f.name)
    os.unlink(f.name)
    refs = [c['ClientRef'] for c in data]
    failed = {}
    for ref in refs:
        state.phrased.pop(ref, None)
        try:
            compute(state.store.clients[ref], state.store)
        except Exception as e:  # a malformed client must not take the upload down with it
            failed[ref] = f'{type(e).__name__}: {e}'
            if previous[ref] is None:
                state.store.clients.pop(ref, None)
            else:
                state.store.clients[ref] = previous[ref]
    state.precompute([r for r in refs if r not in failed])
    return JSONResponse({'added': [r for r in refs if r not in failed], 'failed': failed},
                        status_code=200 if len(failed) < len(refs) else 422)


async def get_briefing(request):
    ref = request.path_params['ref']
    _, err = client_or_404(ref)
    if err:
        return err
    if ref in state.phrased:
        return JSONResponse({**state.phrased[ref], 'phrasing': 'ready'})
    b = briefing.build(state.store, ref, use_llm=False)
    if state.use_llm:
        state.precompute([ref])
    return JSONResponse({**b, 'phrasing': 'pending' if state.use_llm else 'off'})


def market_json():
    m = state.market
    return {'scenario': m.name, 'description': m.description, 'simulated': m.simulated, 'as_of': m.as_of,
            'moves': [{'dimension': v.dimension, 'bucket': v.bucket, 'change': v.change, 'level': v.level,
                       'ticker': v.ticker, 'origin': v.origin} for v in m.moves.values()],
            'headlines': m.headlines}


async def list_scenarios(request):
    return JSONResponse(scenarios())


async def market_state(request):
    return JSONResponse(market_json())


async def market_event(request):
    data = await body(request)
    if data is None:
        return error(400, 'expected a JSON object')
    if data.get('scenario'):
        if data['scenario'] not in scenarios():
            return error(404, f'unknown scenario {data["scenario"]}; known: {", ".join(scenarios())}')
        state.market = load_scenario(data['scenario'])
    elif isinstance(data.get('ticks'), list):
        state.market.apply(data['ticks'])
        state.market.name = data.get('name') or state.market.name
        state.market.simulated = bool(data.get('simulated', state.market.simulated))
    else:
        return error(400, 'expected "scenario" or "ticks"')
    callers = callmode.rank_callers(state.store, state.market)[:10]
    await state.broadcast({'type': 'market', 'market': market_json(), 'callers': callers})
    return JSONResponse({'market': market_json(), 'callers': callers})


async def callers(request):
    limit = int(request.query_params.get('limit', 10))
    return JSONResponse(callmode.rank_callers(state.store, state.market)[:limit])


async def get_call(request):
    ref = request.path_params['ref']
    _, err = client_or_404(ref)
    return err or JSONResponse(callmode.build_call(state.store, ref, state.market))


async def incoming_call(request):
    data = await body(request)
    if data is None:
        return error(400, 'expected a JSON object or form')
    number = normalise_number(data.get('from') or data.get('From'))
    ref = data.get('client') or state.phonebook.get(number)
    if not ref:
        return error(404, f'no client for caller {number or "(none)"}; add it to data/phonebook.json')
    _, err = client_or_404(ref)
    if err:
        return err
    b = callmode.build_call(state.store, ref, state.market)
    await state.broadcast({'type': 'incoming_call', 'from': number, 'briefing': b})
    return JSONResponse(b)


# Everyday words a client uses, mapped to the words our facts use.
SYNONYMS = {
    'tech': 'information technology', 'technology': 'information technology',
    'lost': 'about', 'lose': 'about', 'loss': 'about', 'down': 'about', 'much': 'about',
    'dollar': 'dollar', 'usd': 'dollar', 'euro': 'euro', 'franc': 'franc', 'currency': 'dollar',
    'gold': 'gold', 'bonds': 'bonds', 'bond': 'bonds', 'cash': 'cash', 'risk': 'volatility',
    'rules': 'suitability', 'compliance': 'suitability', 'hedged': 'hedged', 'hedge': 'hedged',
    'safe': 'holding', 'held': 'holding', 'performance': 'value', 'year': '12 months',
    'pharma': 'health care', 'health': 'health care', 'banks': 'financials', 'crypto': 'bitcoin',
}
WORD = re.compile(r"[a-z]+")
STOP = {'the', 'a', 'an', 'my', 'i', 'is', 'are', 'was', 'what', 'how', 'did', 'do', 'on', 'in', 'of', 'to',
        'have', 'has', 'me', 'we', 'you', 'and', 'or', 'about', 'today', 'with', 'for', 'it\'s', 'there'}


async def ask(request):
    """Answer a client's question with the facts that match it best, never with new text."""
    data = await body(request)
    if data is None or not data.get('client') or not data.get('question'):
        return error(400, 'expected {"client": ref, "question": "..."}')
    client, err = client_or_404(data['client'])
    if err:
        return err
    facts, _ = callmode.call_facts(client, state.store, state.market)
    facts += [f for f in compute(client, state.store) if f.slot != 'who']
    words = [w for w in WORD.findall(data['question'].lower()) if w not in STOP]
    terms = {SYNONYMS.get(w, w) for w in words}
    scored = []
    for f in facts:
        text = f.text.lower()
        score = sum(2 if ' ' in t else 1 for t in terms if t in text)
        if score:
            scored.append((score, f.slot in ('digest', 'holding', 'reason'), f))
    scored.sort(key=lambda s: (-s[0], not s[1]))
    seen, answers = set(), []
    for _, _, f in scored:
        if f.id not in seen:
            seen.add(f.id)
            answers.append({'text': f.text, 'source': f.source, 'fact': f.id})
        if len(answers) == 2:
            break
    return JSONResponse({'client': data['client'], 'question': data['question'], 'answers': answers,
                         'found': bool(answers)})


async def websocket(ws):
    await ws.accept()
    state.sockets.add(ws)
    await ws.send_json({'type': 'hello', 'market': market_json()})
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        state.sockets.discard(ws)


@asynccontextmanager
async def lifespan(app):
    global state
    state = State()
    if os.getenv('DEMO_SCENARIO'):
        state.market = load_scenario(os.environ['DEMO_SCENARIO'])
    await asyncio.get_running_loop().run_in_executor(None, state.precompute)
    yield
    state.pool.shutdown(wait=False, cancel_futures=True)


app = Starlette(
    routes=[
        Route('/health', health),
        Route('/clients', list_clients, methods=['GET']),
        Route('/clients', upload_clients, methods=['POST']),
        Route('/briefing/{ref}', get_briefing),
        Route('/market/scenarios', list_scenarios),
        Route('/market/state', market_state),
        Route('/market/events', market_event, methods=['POST']),
        Route('/callers', callers),
        Route('/call/incoming', incoming_call, methods=['POST']),
        Route('/call/{ref}', get_call),
        Route('/ask', ask, methods=['POST']),
        WebSocketRoute('/ws', websocket),
        Mount('/phone', StaticFiles(directory=PHONE_APP, html=True), name='phone'),
    ],
    middleware=[Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])],
    lifespan=lifespan,
)
