"""Voice for the briefing: ElevenLabs text-to-speech and speech-to-text.

    python -m backend.voice brief CASE-043 --scenario tech-selloff   # speak the call briefing, time it
    python -m backend.voice say "Waldo is calling." --out waldo.mp3
    python -m backend.voice transcribe call.mp3

Speech is cached in data/voice-cache/ by (model, voice, text), so a briefing that
has been spoken once replays instantly.
"""

import argparse
import hashlib
import os
import re
import sys
import time

import requests
from dotenv import load_dotenv

from .data import ROOT

load_dotenv(ROOT / '.env')

API = 'https://api.elevenlabs.io/v1'
CACHE_DIR = ROOT / 'data' / 'voice-cache'
# A premade voice: clear, professional, British English.
DEFAULT_VOICE = 'Xb7hH8MSUJpSbSDYk0k2'
DEFAULT_VOICE_NAME = 'Alice - Clear, Engaging Educator'
FAST_MODEL = 'eleven_flash_v2_5'
STT_MODEL = 'scribe_v1'
# Streaming speech-to-text for the call listener (tested: full transcript ~0.1 s after speech ends).
# Send {"message_type": "input_audio_chunk", "audio_base_64": <16 kHz PCM>, "sample_rate": 16000,
# "commit": false} every ~100 ms; receive partial_transcript / committed_transcript messages.
REALTIME_URL = ('wss://api.elevenlabs.io/v1/speech-to-text/realtime'
                '?model_id=scribe_v2_realtime&audio_format=pcm_16000&commit_strategy=vad')

CURRENCY_WORDS = {'CHF': 'francs', 'EUR': 'euros', 'USD': 'dollars', 'GBP': 'pounds'}
SCALE_WORDS = {'k': ' thousand', 'm': ' million', '': ''}
MONEY = re.compile(r'(?:([−+-])\s?)?\b(CHF|EUR|USD|GBP) (\d+(?:\.\d+)?)(k|m)?\b')
SIGNED_NUMBER = re.compile(r'(?<![\w.])([−+])(\d)')
RANGE = re.compile(r'(\d| percent)\s?[–—]\s?(\d)')


class VoiceUnavailable(RuntimeError):
    pass


def _key():
    key = (os.getenv('ELEVENLABS_KEY') or '').strip().strip('"\'')
    if not key:
        raise VoiceUnavailable('ELEVENLABS_KEY is not set')
    return key


def spoken(text):
    """One sentence as it should be read aloud. Every number keeps its digits and value;
    only signs, units and scales become words ('−CHF 12k' -> 'minus 12 thousand francs')."""
    def money(m):
        sign = {'−': 'minus ', '-': 'minus ', '+': 'plus '}.get(m.group(1) or '', '')
        return f'{sign}{m.group(3)}{SCALE_WORDS[m.group(4) or ""]} {CURRENCY_WORDS[m.group(2)]}'
    text = MONEY.sub(money, text)
    text = SIGNED_NUMBER.sub(lambda m: ('minus ' if m.group(1) == '−' else 'plus ') + m.group(2), text)
    text = text.replace('%', ' percent').replace('·', ',').replace('×', 'times')
    text = RANGE.sub(r'\1 to \2', text)
    return re.sub(r'\s+', ' ', text).strip()


def briefing_script(sentences):
    """Sentences (strings or {'text': ...} dicts) joined into one script to read aloud."""
    parts = [spoken(s['text'] if isinstance(s, dict) else s) for s in sentences]
    return ' '.join(p if p.endswith(('.', '!', '?', '"')) else p + '.' for p in parts if p)


def _cache_path(*parts):
    return CACHE_DIR / (hashlib.sha256('|'.join(parts).encode('utf-8')).hexdigest()[:24] + '.mp3')


def speak(text, voice_id=None, model=FAST_MODEL, timeout=60):
    """MP3 bytes for text, from the cache or ElevenLabs. Returns (audio, seconds to first byte or None)."""
    voice_id = voice_id or DEFAULT_VOICE
    path = _cache_path(model, voice_id, text)
    if path.exists():
        return path.read_bytes(), None
    started = time.perf_counter()
    try:
        resp = requests.post(f'{API}/text-to-speech/{voice_id}/stream',
                             params={'output_format': 'mp3_44100_128'},
                             headers={'xi-api-key': _key(), 'Content-Type': 'application/json'},
                             data=_json({'model_id': model, 'text': text}), stream=True, timeout=timeout)
        resp.raise_for_status()
        chunks, first = [], None
        for chunk in resp.iter_content(chunk_size=4096):
            if chunk:
                first = first if first is not None else time.perf_counter() - started
                chunks.append(chunk)
    except requests.RequestException as e:
        raise VoiceUnavailable(f'text-to-speech failed: {e}') from e
    audio = b''.join(chunks)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio)
    return audio, round(first, 3)


def transcribe(audio_bytes, model=STT_MODEL, language=None, filename='audio.mp3', timeout=60):
    """Text of an audio clip via ElevenLabs Scribe (batch). Returns (text, seconds)."""
    started = time.perf_counter()
    data = {'model_id': model}
    if language:
        data['language_code'] = language
    try:
        resp = requests.post(f'{API}/speech-to-text', headers={'xi-api-key': _key()}, data=data,
                             files={'file': (filename, audio_bytes, 'audio/mpeg')}, timeout=timeout)
        resp.raise_for_status()
        text = resp.json().get('text', '')
    except (requests.RequestException, ValueError) as e:
        raise VoiceUnavailable(f'speech-to-text failed: {e}') from e
    return text.strip(), round(time.perf_counter() - started, 2)


def _json(obj):
    import json
    return json.dumps(obj, ensure_ascii=False).encode('utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('brief')
    b.add_argument('ref')
    b.add_argument('--scenario', default='tech-selloff')
    s = sub.add_parser('say')
    s.add_argument('text')
    s.add_argument('--out', default='say.mp3')
    t = sub.add_parser('transcribe')
    t.add_argument('file')
    args = parser.parse_args(argv)

    if args.cmd == 'brief':
        from .callmode import build_call
        from .data import load
        from .market import load_scenario
        call = build_call(load(), args.ref, load_scenario(args.scenario))
        script = briefing_script(call['sentences'])
        audio, first = speak(script)
        print(f'{len(script.split())} words, {len(audio) // 1024} KB, first byte '
              f'{first if first is not None else "cached"} s -> {_cache_path(FAST_MODEL, DEFAULT_VOICE, script)}')
        print(script)
    elif args.cmd == 'say':
        audio, first = speak(args.text)
        with open(args.out, 'wb') as f:
            f.write(audio)
        print(f'wrote {args.out}, first byte {first} s')
    else:
        with open(args.file, 'rb') as f:
            text, secs = transcribe(f.read(), filename=os.path.basename(args.file))
        print(f'{secs} s: {text}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
