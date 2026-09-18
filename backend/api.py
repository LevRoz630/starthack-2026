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
    POST /transcribe                   multipart "file" (audio) [+ "client"]: text via ElevenLabs Scribe, plus answers
    GET  /profile/{ref}                the client's profile (temperament, wants, cash needs), each with its note
    GET  /call/{ref}/audio             the call briefing spoken (audio/mpeg, ElevenLabs Flash, cached)
    GET  /briefing/{ref}/audio         the 60-second briefing spoken
    WS   /ws                           pushes {"type": "incoming_call" | "market" | "transcript" | "answer" |
                                       "listening" | "listening_stopped" | "listener_error", ...} events
    POST /twilio/voice                 Twilio webhook: push the briefing, answer with TwiML that plays the
                                       recording notice, streams the caller's audio to us and dials ADVISOR_NUMBER
    WS   /twilio/media                 Twilio Media Streams (mu-law 8 kHz) -> live transcript + answers on /ws
    WS   /listen?client=REF            browser microphone (16 kHz PCM16 frames) -> live transcript + answers on /ws
    GET  /phone/                       the advisor phone app (web/phone)

External custody clients EXT-01..EXT-10 (from the side-challenge PDFs) are loaded at startup.
Environment: DEMO_SCENARIO preloads a scenario; BRIEFING_LLM=0 turns off Apertus phrasing.
"""

import asyncio
import base64
import json
import os
import re
import tempfile
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

from . import briefing, callmode, excustody, listener, profiles, voice
from .data import ROOT, load
from .facts import client_name, compute, risk_profile
from .market import MarketState, load_scenario, scenarios

PHONEBOOK = ROOT / 'data' / 'phonebook.json'
PHONE_APP = ROOT / 'web' / 'phone'


class State:
    def __init__(self):
        self.store = load()
        excustody.load_external(self.store)   # EXT-01..10, read from the side-challenge custody PDFs
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
             'currency': c.get('ReportingCurrency'), 'risk_profile': risk_profile(c)}
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
    return JSONResponse({'client': data['client'], 'question': data['question'],
                         **answer(client, data['question'])})


def answer(client, question):
    """The facts that best match a question: {'answers': [...], 'found': bool}. Never new text."""
    facts, _ = callmode.call_facts(client, state.store, state.market)
    facts += [f for f in compute(client, state.store) if f.slot != 'who']
    words = [w for w in WORD.findall(question.lower()) if w not in STOP]
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
    return {'answers': answers, 'found': bool(answers)}


async def get_profile(request):
    client, err = client_or_404(request.path_params['ref'])
    return err or JSONResponse(profiles.get(client))


async def _audio(sentences):
    try:
        audio, _ = await run_in_threadpool(voice.speak, voice.briefing_script(sentences))
    except Exception as e:  # no key, no network: the card still works without the voice
        return error(503, f'voice unavailable: {type(e).__name__}')
    return Response(audio, media_type='audio/mpeg')


async def call_audio(request):
    ref = request.path_params['ref']
    _, err = client_or_404(ref)
    return err or await _audio(callmode.build_call(state.store, ref, state.market)['sentences'])


async def briefing_audio(request):
    ref = request.path_params['ref']
    _, err = client_or_404(ref)
    if err:
        return err
    b = state.phrased.get(ref) or briefing.build(state.store, ref, use_llm=False)
    return await _audio(b['sentences'])


async def transcribe(request):
    """Audio of the client's question (multipart "file", optional "client") -> text, and the facts that answer it."""
    form = await request.form()
    upload = form.get('file')
    if upload is None or isinstance(upload, str):
        return error(400, 'expected a multipart field "file" with audio')
    try:
        text, seconds = await run_in_threadpool(voice.transcribe, await upload.read(), filename=upload.filename or 'audio')
    except Exception as e:
        return error(503, f'transcription unavailable: {type(e).__name__}')
    out = {'text': text, 'seconds': round(seconds, 2)}
    ref = form.get('client')
    if ref:
        client, err = client_or_404(ref)
        if err:
            return err
        out.update(client=ref, **answer(client, text))
    return JSONResponse(out)


async def websocket(ws):
    await ws.accept()
    state.sockets.add(ws)
    await ws.send_json({'type': 'hello', 'market': market_json()})
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        state.sockets.discard(ws)


def _ws_base(scope_owner):
    """wss://host of this server as the caller sees it, honouring tunnel headers."""
    headers = scope_owner.headers
    proto = (headers.get('x-forwarded-proto') or scope_owner.url.scheme).split(',')[0].strip()
    host = (headers.get('x-forwarded-host') or headers.get('host') or scope_owner.url.netloc).split(',')[0].strip()
    return f'{"wss" if proto in ("https", "wss") else "ws"}://{host}'


async def twilio_voice(request):
    """Twilio's incoming-call webhook. The phone rings with the briefing before the advisor's line does."""
    data = await body(request) or {}
    number = normalise_number(data.get('From') or data.get('from'))
    ref = data.get('client') or state.phonebook.get(number)
    advisor = os.getenv('ADVISOR_NUMBER')
    if ref in state.store.clients:
        b = callmode.build_call(state.store, ref, state.market)
        await state.broadcast({'type': 'incoming_call', 'from': number, 'call_sid': data.get('CallSid'),
                               'briefing': b})
        xml = listener.twiml(f'{_ws_base(request)}/twilio/media', ref, advisor)
    else:
        xml = listener.twiml(None, None, advisor)
    return Response(xml, media_type='application/xml')


def _session(ref, client, fmt, source):
    return listener.Session(ref, state.broadcast, lambda text: answer(client, text), fmt=fmt, source=source)


async def twilio_media(ws):
    """Twilio Media Streams: only the caller's (inbound) track goes to speech-to-text."""
    await ws.accept()
    session = None
    try:
        while True:
            msg = listener.parse_twilio(await ws.receive_text())
            if msg['event'] == 'start' and session is None:
                client = state.store.clients.get(msg.get('client'))
                if client is not None:
                    session = _session(msg['client'], client, 'ulaw_8000', 'twilio')
                    await session.start()
            elif msg['event'] == 'media' and session and msg.get('track', 'inbound') == 'inbound':
                await session.send_audio(msg['audio'])
            elif msg['event'] == 'stop':
                break
    except WebSocketDisconnect:
        pass
    finally:
        if session:
            await session.close()


async def listen(ws):
    """The phone page's microphone: binary 16 kHz PCM16 frames, or JSON {"audio_base_64": ...}."""
    await ws.accept()
    ref = ws.query_params.get('client')
    client = state.store.clients.get(ref)
    if client is None:
        await ws.close(code=4404)
        return
    session = _session(ref, client, 'pcm_16000', 'browser')
    await session.start()
    try:
        while True:
            message = await ws.receive()
            if message['type'] == 'websocket.disconnect':
                break
            if message.get('bytes'):
                await session.send_audio(message['bytes'])
            elif message.get('text'):
                try:
                    data = json.loads(message['text'])
                except json.JSONDecodeError:
                    continue
                if data.get('type') == 'stop':
                    break
                if data.get('audio_base_64'):
                    await session.send_audio(base64.b64decode(data['audio_base_64']))
    except WebSocketDisconnect:
        pass
    finally:
        await session.close()


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
        Route('/transcribe', transcribe, methods=['POST']),
        Route('/profile/{ref}', get_profile),
        Route('/call/{ref}/audio', call_audio),
        Route('/briefing/{ref}/audio', briefing_audio),
        WebSocketRoute('/ws', websocket),
        Route('/twilio/voice', twilio_voice, methods=['POST']),
        WebSocketRoute('/twilio/media', twilio_media),
        WebSocketRoute('/listen', listen),
        Mount('/phone', StaticFiles(directory=PHONE_APP, html=True), name='phone'),
    ],
    middleware=[Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])],
    lifespan=lifespan,
)
