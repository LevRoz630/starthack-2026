"""Recorded demo pipeline: a scripted client call through the real listener.

A script (data/demo/<name>.json) names the client, the market scenario and the
client's lines. The lines are voiced once by ElevenLabs and cached (data/demo/audio/,
gitignored). A run then does what a live call does, with recorded audio in place of
the phone line:

1. load the script's market scenario and push it to the phones,
2. ring the advisor's phone with the call briefing,
3. wait for Answer (POST /call/answered), or give up after ring_timeout,
4. per line: tell the phone to play the client's voice, and stream the same audio in
   real time into the real speech-to-text session, so transcripts and answer cards
   appear as the words are heard,
5. hang up: push call_ended, and the phone shows the call note and follow-up email.

Every event of a run is saved to data/demo/runs/<name>-latest.json. `replay` pushes a
saved run again with its original timing and no network at all: the fallback if the
venue network fails during the pitch.

The live pipeline is the same listener fed by Twilio or the phone microphone; see
backend/listener.py.

    python -m backend.demo prepare golf        # voice the lines (needs ELEVENLABS_KEY)
"""

import asyncio
import hashlib
import json
import sys
import time

import requests

from .data import ROOT, env

DEMO_DIR = ROOT / 'data' / 'demo'
AUDIO_DIR = DEMO_DIR / 'audio'
RUNS_DIR = DEMO_DIR / 'runs'
TTS_URL = 'https://api.elevenlabs.io/v1/text-to-speech/{voice}'
TTS_MODEL = 'eleven_flash_v2_5'
PCM_BYTES_PER_SECOND = 32000       # 16 kHz, 16-bit mono: what the listener's pcm_16000 session takes
CHUNK_SECONDS = 0.1


def scripts():
    return sorted(p.stem for p in DEMO_DIR.glob('*.json'))


def load_script(name):
    path = DEMO_DIR / f'{name}.json'
    if not path.is_file():
        raise KeyError(f'unknown demo script {name!r}; known: {", ".join(scripts())}')
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def audio_path(voice, fmt, text):
    digest = hashlib.sha256(f'{TTS_MODEL}|{voice}|{fmt}|{text}'.encode('utf-8')).hexdigest()[:20]
    return AUDIO_DIR / f'{digest}.{"pcm" if fmt.startswith("pcm") else "mp3"}'


def tts(text, voice, fmt):
    """Audio for one line, from the cache or ElevenLabs (fmt: pcm_16000 or mp3_44100_128)."""
    path = audio_path(voice, fmt, text)
    if path.exists():
        return path
    resp = requests.post(TTS_URL.format(voice=voice), params={'output_format': fmt},
                         headers={'xi-api-key': env('ELEVENLABS_KEY'), 'Content-Type': 'application/json'},
                         data=json.dumps({'model_id': TTS_MODEL, 'text': text}).encode('utf-8'), timeout=60)
    resp.raise_for_status()
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    path.write_bytes(resp.content)
    return path


def prepare(script):
    """Voice every line; returns [{text, pause_before, pcm, mp3, seconds}]."""
    voice = script['client_voice']
    lines = []
    for line in script['lines']:
        pcm = tts(line['text'], voice, 'pcm_16000')
        mp3 = tts(line['text'], voice, 'mp3_44100_128')
        lines.append({**line, 'pcm': pcm, 'mp3': mp3, 'seconds': pcm.stat().st_size / PCM_BYTES_PER_SECOND})
    return lines


class Recorder:
    """Passes events on and keeps them, with their time since the start, for replay."""

    def __init__(self, broadcast):
        self.broadcast = broadcast
        self.started = time.monotonic()
        self.events = []

    async def __call__(self, event):
        self.events.append({'t': round(time.monotonic() - self.started, 3), 'event': event})
        if not event.get('type', '').startswith('_'):
            await self.broadcast(event)

    def save(self, name, meta, complete=True):
        """Keep every run; only a completed call replaces <name>-latest.json, the offline replay."""
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        data = {**meta, 'saved_at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'events': self.events}
        stamped = RUNS_DIR / f'{name}-{time.strftime("%Y%m%d-%H%M%S")}.json'
        paths = [stamped, RUNS_DIR / f'{name}-latest.json'] if complete else [stamped]
        for path in paths:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
        return paths[-1]


async def _stream(session, data, stop):
    """Send audio to the listener in real time, 100 ms at a time."""
    step = int(PCM_BYTES_PER_SECOND * CHUNK_SECONDS)
    for i in range(0, len(data), step):
        if stop.is_set():
            return
        await session.send_audio(data[i:i + step])
        await asyncio.sleep(CHUNK_SECONDS)


async def _silence(session, seconds, stop):
    # A live line never goes quiet at the byte level; the speech-to-text VAD needs silence to commit.
    await _stream(session, bytes(int(PCM_BYTES_PER_SECOND * seconds) & ~1), stop)


async def run(name, *, broadcast, ring, make_session, set_market, answered, stop, audio_url):
    """One recorded call through the real pipeline. Returns the path of the saved run.

    ring(ref) -> call briefing (pushed as incoming_call); make_session(ref, on_event) ->
    listener.Session in pcm_16000; set_market(scenario) -> market json; answered / stop:
    asyncio.Events set by the API; audio_url(path) -> URL the phone can play.
    """
    script = load_script(name)
    lines = await asyncio.to_thread(prepare, script)
    ref = script['client']
    rec = Recorder(broadcast)
    await rec({'type': 'demo_started', 'script': name, 'client': ref, 'mode': 'pipeline'})
    if script.get('scenario'):
        await rec({'type': 'market', 'market': set_market(script['scenario'])})
    answered.clear()    # before ringing: an Answer tapped right away must count
    await rec({'type': 'incoming_call', 'briefing': ring(ref), 'demo': name})

    try:
        await asyncio.wait_for(answered.wait(), script.get('ring_timeout', 45))
    except asyncio.TimeoutError:
        await rec({'type': 'demo_finished', 'client': ref, 'result': 'not answered'})
        return rec.save(name, {'script': name, 'client': ref}, complete=False)
    await rec({'type': '_answered', 'client': ref})

    session = make_session(ref, rec)
    await session.start()
    try:
        for line in lines:
            await _silence(session, line.get('pause_before', 1.0), stop)
            if stop.is_set():
                break
            await rec({'type': 'demo_audio', 'client': ref, 'url': audio_url(line['mp3']), 'text': line['text']})
            await _stream(session, line['pcm'].read_bytes(), stop)
        await _silence(session, 1.5, stop)
    finally:
        await session.close()
    await asyncio.sleep(script.get('hangup_after', 2.0))
    await rec({'type': 'call_ended', 'client': ref, 'demo': name})
    await rec({'type': 'demo_finished', 'client': ref, 'result': 'stopped' if stop.is_set() else 'done'})
    return rec.save(name, {'script': name, 'client': ref, 'scenario': script.get('scenario')},
                    complete=not stop.is_set())


async def replay(name, *, broadcast, answered, stop, answer_timeout=120):
    """Push a saved run again with its original timing; waits for Answer where the run did."""
    path = RUNS_DIR / f'{name}-latest.json'
    if not path.is_file():
        raise KeyError(f'no saved run for {name!r}; run the pipeline once first')
    with open(path, encoding='utf-8') as f:
        events = json.load(f)['events']
    base = time.monotonic()
    for item in events:
        if stop.is_set():
            return
        wait = item['t'] - (time.monotonic() - base)
        if wait > 0:
            await asyncio.sleep(wait)
        event = item['event']
        if event.get('type') == 'incoming_call':
            answered.clear()
        if event.get('type') == '_answered':
            # The recorded run waited for the advisor here; so does the replay.
            began = time.monotonic()
            try:
                await asyncio.wait_for(answered.wait(), answer_timeout)
            except asyncio.TimeoutError:
                return
            base += time.monotonic() - began
            continue
        await broadcast({**event, 'replayed': True})


def main(argv=None):
    args = argv if argv is not None else sys.argv[1:]
    if len(args) == 2 and args[0] == 'prepare':
        lines = prepare(load_script(args[1]))
        for line in lines:
            print(f'{line["seconds"]:5.1f}s  {line["text"]}')
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
