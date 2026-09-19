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
    POST /call/incoming                {"from": "+41..."} or {"client": ref}
                                       Pushes the call briefing to every /ws subscriber.
    POST /ask                          {"client": ref, "question": "..."}: the facts that answer it
    POST /transcribe                   multipart "file" (audio) [+ "client"]: text via ElevenLabs Scribe, plus answers
    GET  /lookup?q=waldo               clients matching a typed name, company or number
    GET  /prepare?q=waldo              the prepared briefing for that client (or the matches to pick from)
    GET  /profile/{ref}                the client's profile (temperament, wants, cash needs), each with its note
    GET  /call/{ref}/audio             the call briefing spoken (audio/mpeg, ElevenLabs Flash, cached)
    GET  /briefing/{ref}/audio         the 60-second briefing spoken
    POST /followup/send                {"client", "kind": "email"|"note", "body"}: send the approved draft (Gmail)
    POST /call/answered                the phone's Answer button (lets a recorded demo call proceed)
    GET  /demo/scripts                 recorded demo scripts, whether a saved run exists, email mode
    POST /demo/run                     {"script": "walter", "mode": "pipeline"|"replay"}; POST /demo/stop (End call)
    POST /demo/next                    the advisor finished their turn: the recorded client may speak again
    WS   /ws                           pushes {"type": "incoming_call" | "market" | "transcript" | "answer" |
                                       "listening" | "listening_stopped" | "listener_error", ...} events
    WS   /listen?client=REF            browser microphone (16 kHz PCM16 frames) -> live transcript + answers on /ws
    GET  /phone/                       the advisor phone app (web/phone)
    GET  /dashboard/                   the one-click 60-second briefing dashboard (web/dashboard)
    GET  /shared/*                     CSS tokens and DOM helpers shared by both web apps (web/shared)

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
from starlette.responses import FileResponse, JSONResponse, RedirectResponse, Response
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

from . import answers, briefing, callmode, demo, lookup, reasoning, excustody, listener, mailer, profiles, voice
from .data import ROOT, env, load
from .facts import client_name, compute, risk_profile
from .market import MarketState, load_scenario, scenarios

PHONEBOOK = ROOT / 'data' / 'phonebook.json'
PHONE_APP = ROOT / 'web' / 'phone'
DASHBOARD_APP = ROOT / 'web' / 'dashboard'
SHARED_APP = ROOT / 'web' / 'shared'


class State:
    def __init__(self):
        self.store = load()
        excustody.load_external(self.store)   # EXT-01..10, read from the side-challenge custody PDFs
        self.market = MarketState()
        self.phrased = {}           # ref -> briefing phrased by the LLM
        self.pending = set()        # refs being phrased right now
        self.demo_task = None       # the recorded demo call in progress, if any
        self.demo_answered = asyncio.Event()
        self.demo_stop = asyncio.Event()
        self.demo_next = asyncio.Event()   # the advisor has finished their turn
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
    """JSON or form body as a dict."""
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
             'currency': c.get('ReportingCurrency'), 'risk_profile': risk_profile(c),
             # Ex-custody clients came from a PDF statement, not from clients.json.
             'external': (c.get('ExternalSource') or {}).get('bank')}
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
    """The facts that best answer a question (backend/answers.py). Never new text."""
    facts, _ = callmode.call_facts(client, state.store, state.market)
    facts += [f for f in compute(client, state.store) if f.slot != 'who']
    graph = reasoning.build(client, state.store, state.market)
    return answers.answer(facts, question, use_llm=state.use_llm, graph=graph)


async def find_clients(request):
    """GET /lookup?q=waldo: clients matching a name, part of one, a company or a number."""
    matches = lookup.find(state.store, request.query_params.get('q', ''))
    return JSONResponse({'query': request.query_params.get('q', ''), 'matches': matches,
                         'best': lookup.best(matches)})


async def prepare(request):
    """GET /prepare?q=waldo: the prepared briefing for the client the advisor typed.

    Returns the 60-second briefing (Apertus-phrased once ready), the briefing for a call
    under the current market, and the profile — or just the matches when the name is
    ambiguous, so the advisor can pick.
    """
    query = request.query_params.get('q', '')
    matches = lookup.find(state.store, query)
    ref = request.query_params.get('client') or lookup.best(matches)
    if ref is None:
        return JSONResponse({'query': query, 'matches': matches, 'client': None},
                            status_code=200 if matches else 404)
    client, err = client_or_404(ref)
    if err:
        return err
    if ref in state.phrased:
        brief = {**state.phrased[ref], 'phrasing': 'ready'}
    else:
        brief = {**briefing.build(state.store, ref, use_llm=False), 'phrasing': 'pending' if state.use_llm else 'off'}
        if state.use_llm:
            state.precompute([ref])
    return JSONResponse({'query': query, 'matches': matches, 'client': ref, 'name': client_name(client),
                         'briefing': brief, 'call': callmode.build_call(state.store, ref, state.market),
                         'profile': profiles.get(client)})


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


async def call_answered(request):
    """The phone's Answer button: lets a recorded demo call start talking."""
    state.demo_answered.set()
    return JSONResponse({'ok': True})


async def send_followup(request):
    """Send the advisor-approved follow-up email or call note (Gmail, or data/outbox/ without settings)."""
    data = await body(request)
    if data is None or data.get('kind') not in ('email', 'note') or not (data.get('body') or '').strip():
        return error(400, 'expected {"client": ref, "kind": "email" | "note", "body": "...", "subject"?}')
    client, err = client_or_404(data.get('client'))
    if err:
        return err
    if len(data['body']) > 20000:
        return error(413, 'body too long')
    name = client_name(client)
    subject = (data.get('subject') or '').strip() or (
        f'Follow-up to our call today, {name}' if data['kind'] == 'email' else f'Call note: {name} ({client["ClientRef"]})')
    try:
        result = await run_in_threadpool(mailer.send, subject, data['body'])
    except Exception as e:  # tell the advisor it did not go out; never a 500
        return error(502, f'email not sent: {type(e).__name__}: {e}')
    await state.broadcast({'type': 'email_sent', 'client': client['ClientRef'], 'kind': data['kind'], **result})
    return JSONResponse({'kind': data['kind'], 'subject': subject, **result})


def _demo_running():
    return state.demo_task is not None and not state.demo_task.done()


def _set_market(name):
    state.market = load_scenario(name)
    return market_json()


async def demo_scripts(request):
    names = demo.scripts()
    runs = {name: (demo.RUNS_DIR / f'{name}-latest.json').is_file() for name in names}
    # Who each script calls as, so the phone does not need the client in its URL.
    callers = {}
    for name in names:
        try:
            callers[name] = demo.load_script(name).get('client')
        except (KeyError, ValueError):
            callers[name] = None
    who = {ref: client_name(state.store.clients[ref]) for ref in set(callers.values())
           if ref in state.store.clients}
    return JSONResponse({'scripts': names, 'replayable': runs, 'clients': callers, 'names': who,
                         'running': _demo_running(),
                         'email': 'gmail' if mailer.configured() else 'outbox'})


async def demo_run(request):
    """{"script": "golf", "mode": "pipeline" | "replay"}: a recorded call through the real
    listener, or a saved run pushed again with no network."""
    data = await body(request) or {}
    name, mode = data.get('script') or 'golf', data.get('mode') or 'pipeline'
    if name not in demo.scripts():
        return error(404, f'unknown script {name}; known: {", ".join(demo.scripts())}')
    if mode not in ('pipeline', 'replay'):
        return error(400, 'mode must be "pipeline" or "replay"')
    if mode == 'replay' and not (demo.RUNS_DIR / f'{name}-latest.json').is_file():
        return error(409, 'no saved run yet: run the pipeline once first')
    if _demo_running():
        # Starting a call always ends the one before it: stop it, let it close, then start.
        # A demo is retried many times; it must never refuse because an old call is still up.
        state.demo_stop.set()
        state.demo_answered.set()
        state.demo_next.set()
        try:
            await asyncio.wait_for(asyncio.shield(state.demo_task), 8)
        except (asyncio.TimeoutError, Exception):
            state.demo_task.cancel()
    state.demo_stop.clear()
    state.demo_next.clear()
    if mode == 'pipeline':
        coro = demo.run(
            name, broadcast=state.broadcast,
            ring=lambda ref: callmode.build_call(state.store, ref, state.market),
            make_session=lambda ref, on_event: listener.Session(
                ref, on_event, lambda text: answer(state.store.clients[ref], text), fmt='pcm_16000', source='recorded'),
            set_market=_set_market, answered=state.demo_answered, stop=state.demo_stop,
            audio_url=lambda path: f'/demo/audio/{path.name}', next_turn=state.demo_next)
    else:
        # A replay pushes the saved events, which carry their own market; without this the
        # server would still hold whatever scenario was loaded before, so a question typed
        # during the replayed call would be answered against the wrong market.
        scenario = (demo.load_script(name) or {}).get('scenario')
        if scenario:
            _set_market(scenario)
        coro = demo.replay(name, broadcast=state.broadcast, answered=state.demo_answered, stop=state.demo_stop,
                           next_turn=state.demo_next)
    state.demo_task = asyncio.create_task(coro)
    return JSONResponse({'started': name, 'mode': mode})


async def home(request):
    """The bare host is what someone types on the day; send them to the dashboard
    rather than a 404."""
    return RedirectResponse('/dashboard/')


async def demo_next(request):
    """The advisor finished speaking (or pressed Continue): the client may talk again."""
    state.demo_next.set()
    return JSONResponse({'ok': True})


async def demo_stop(request):
    """End call on the phone: stop the demo call now, so it can be run again."""
    state.demo_stop.set()
    state.demo_answered.set()   # release a run still waiting for Answer
    state.demo_next.set()       # or waiting for the advisor's turn
    return JSONResponse({'stopping': _demo_running()})


async def demo_audio(request):
    name = request.path_params['name']
    path = demo.AUDIO_DIR / name
    if not re.fullmatch(r'[0-9a-f]{20}\.mp3', name) or not path.is_file():
        return error(404, 'no such audio')
    return FileResponse(path, media_type='audio/mpeg')


async def websocket(ws):
    await ws.accept()
    state.sockets.add(ws)
    await ws.send_json({'type': 'hello', 'market': market_json()})
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        state.sockets.discard(ws)


def _session(ref, client, fmt, source):
    return listener.Session(ref, state.broadcast, lambda text: answer(client, text), fmt=fmt, source=source)


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
        Route('/', home),
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
        Route('/lookup', find_clients),
        Route('/prepare', prepare),
        Route('/call/{ref}/audio', call_audio),
        Route('/briefing/{ref}/audio', briefing_audio),
        WebSocketRoute('/ws', websocket),
        WebSocketRoute('/listen', listen),
        Route('/call/answered', call_answered, methods=['POST']),
        Route('/followup/send', send_followup, methods=['POST']),
        Route('/demo/scripts', demo_scripts),
        Route('/demo/run', demo_run, methods=['POST']),
        Route('/demo/stop', demo_stop, methods=['POST']),
        Route('/demo/next', demo_next, methods=['POST']),
        Route('/demo/audio/{name}', demo_audio),
        Mount('/phone', StaticFiles(directory=PHONE_APP, html=True), name='phone'),
        Mount('/dashboard', StaticFiles(directory=DASHBOARD_APP, html=True), name='dashboard'),
        Mount('/shared', StaticFiles(directory=SHARED_APP), name='shared'),
    ],
    middleware=[Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])],
    lifespan=lifespan,
)
