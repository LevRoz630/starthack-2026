"""Before the demo: is everything that the stage depends on actually working?

    python -m backend.preflight                 # checks, including the running server
    python -m backend.preflight --url http://localhost:8000

Each line says OK or what is wrong and what to do. Exit code 1 if anything that would
break the demo fails; warnings (email, ringtone) do not fail it.
"""

import argparse
import asyncio
import sys
import time

import requests

from .data import ROOT, env, load

OK, WARN, FAIL = 'OK  ', 'WARN', 'FAIL'
results = []


def report(status, what, detail=''):
    results.append(status)
    print(f'  [{status}] {what}' + (f': {detail}' if detail else ''))


def check_data():
    from .excustody import load_external
    store = load()
    load_external(store)
    n = len(store.clients)
    report(OK if n >= 57 else FAIL, 'client data', f'{n} clients (47 case + 10 custody PDFs)')
    return store


def check_keys():
    for key in ('ELEVENLABS_KEY', 'SWISSCOM_KEY'):
        report(OK if env(key) else FAIL, key, 'set' if env(key) else 'missing from .env')
    if env('OPENAI_API_KEY'):
        report(OK, 'OPENAI_API_KEY', 'set (fallback model)')
    email = all(env(k) for k in ('SMTP_USER', 'SMTP_PASSWORD', 'EMAIL_TO'))
    report(OK if email else WARN, 'email', 'Gmail configured' if email else
           'no SMTP_USER/SMTP_PASSWORD/EMAIL_TO: Approve saves to data/outbox/ instead of sending')


def check_apertus():
    from .llm import chat
    try:
        t = time.perf_counter()
        _, provider = chat([{'role': 'user', 'content': 'Reply with OK.'}], 0.0, 5, timeout=15)
        report(OK, 'language model', f'{provider}, {time.perf_counter() - t:.1f} s')
    except Exception as e:
        report(WARN, 'language model', f'{type(e).__name__}: answers fall back to rules and keywords')


def check_voice():
    key = env('ELEVENLABS_KEY')
    try:
        r = requests.get('https://api.elevenlabs.io/v1/user/subscription', headers={'xi-api-key': key}, timeout=10)
        left = r.json().get('character_limit', 0) - r.json().get('character_count', 0)
        report(OK if r.ok else FAIL, 'ElevenLabs account', f'{left:,} characters left' if r.ok else f'HTTP {r.status_code}')
    except Exception as e:
        report(FAIL, 'ElevenLabs account', f'{type(e).__name__}: no voice and no live listening')
        return

    async def stt():
        from . import listener
        events = []

        async def on_event(e):
            events.append(e)
        s = listener.Session('CASE-045', on_event, lambda q: {}, fmt='pcm_16000', source='preflight')
        s.log = None
        t = time.perf_counter()
        opened = await s.start()
        await s.close()
        return opened, time.perf_counter() - t, events
    try:
        opened, took, events = asyncio.run(stt())
        errors = [e.get('error') for e in events if e.get('type') == 'listener_error']
        report(OK if opened and not errors else FAIL, 'live speech-to-text',
               f'connected in {took:.1f} s' if opened and not errors else f'{errors or "did not connect"}')
    except Exception as e:
        report(FAIL, 'live speech-to-text', f'{type(e).__name__}: {e}')


def check_demo():
    from . import demo
    for name in demo.scripts():
        script = demo.load_script(name)
        missing = [line['text'][:30] for line in script['lines']
                   for fmt in ('pcm_16000', 'mp3_44100_128')
                   if not demo.audio_path(script['client_voice'], fmt, line['text']).exists()]
        report(OK if not missing else WARN, f'demo "{name}" voice',
               'all lines voiced' if not missing else
               f'{len(missing)} clips not cached yet: run python -m backend.demo prepare {name} (needs network)')
        saved = (demo.RUNS_DIR / f'{name}-latest.json').is_file()
        report(OK if saved else WARN, f'demo "{name}" offline replay', 'saved run present' if saved else
               'no saved run: play the voiced call once to create it')
    ringtone = (ROOT / 'web' / 'phone' / 'ringtone.mp3').is_file()
    report(OK if ringtone else WARN, 'ringtone', 'present' if ringtone else 'web/phone/ringtone.mp3 missing: the ring is silent')


def check_server(url):
    try:
        h = requests.get(f'{url}/health', timeout=5).json()
    except Exception:
        report(FAIL, 'server', f'not reachable at {url}: start it with  uvicorn backend.api:app --port 8000')
        return
    report(OK, 'server', f'{h.get("clients")} clients, phrased {h.get("phrased")}')
    market = h.get('market')
    report(OK if market and market != 'empty' else FAIL, 'market scenario',
           market if market and market != 'empty' else
           'none loaded: answers have no market move. POST /market/events {"scenario": "tech-selloff"}')
    for path in ('/phone/', '/dashboard/'):
        code = requests.get(f'{url}{path}', timeout=5).status_code
        report(OK if code == 200 else FAIL, f'page {path}', f'HTTP {code}')
    t = time.perf_counter()
    r = requests.post(f'{url}/ask', json={'client': 'CASE-043', 'question': 'How much did I lose today?'}, timeout=20)
    took = time.perf_counter() - t
    good = r.ok and r.json().get('found')
    report(OK if good else FAIL, 'answer engine', f'{took:.2f} s: {r.json()["answers"][0]["text"][:60]}' if good
           else f'HTTP {r.status_code}')
    print('\n  Microphone: the phone page must be opened on localhost (this laptop) or over HTTPS;'
          '\n  a phone on the Wi-Fi via http:// will not be allowed to use its microphone.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--url', default='http://localhost:8000')
    parser.add_argument('--no-server', action='store_true', help='skip the running-server checks')
    args = parser.parse_args(argv)
    print('Preflight')
    check_data()
    check_keys()
    check_apertus()
    check_voice()
    check_demo()
    if not args.no_server:
        check_server(args.url.rstrip('/'))
    failed = results.count(FAIL)
    print(f'\n{"READY" if not failed else f"NOT READY: {failed} failure(s)"}'
          f'{f", {results.count(WARN)} warning(s)" if results.count(WARN) else ""}')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
