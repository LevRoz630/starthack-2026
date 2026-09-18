"""Voice for the briefing: ElevenLabs text-to-speech and speech-to-text.

    python -m backend.voice brief CASE-043 --scenario tech-selloff   # speak the call briefing, time it
    python -m backend.voice say "Waldo is calling." --out waldo.mp3
    python -m backend.voice transcribe call.mp3
    python -m backend.voice brief CASE-043 --dialect gsw-u-sd-chzh   # Zurich German (untested live)

Speech is cached in data/voice-cache/ by (model, voice, language, text), so a
briefing that has been spoken once replays instantly.

Swiss German (--dialect): no ElevenLabs voice speaks dialect natively, so per
docs/PLAN.md we translate the English script to a gsw dialect through Supertext
(backend/translate.py) and have ElevenLabs read it with language_code='de' — a
German voice reading dialect text. Untested end-to-end: needs a native speaker
to judge whether it actually sounds right before it goes on stage.
"""

import argparse
import hashlib
import os
import re
import sys
import time

import requests

from .data import ROOT, env

API = 'https://api.elevenlabs.io/v1'
CACHE_DIR = ROOT / 'data' / 'voice-cache'
# A premade voice: clear, professional, British English.
DEFAULT_VOICE = 'Xb7hH8MSUJpSbSDYk0k2'
DEFAULT_VOICE_NAME = 'Alice - Clear, Engaging Educator'
FAST_MODEL = 'eleven_flash_v2_5'
STT_MODEL = 'scribe_v1'

CURRENCY_WORDS = {'CHF': 'francs', 'EUR': 'euros', 'USD': 'dollars', 'GBP': 'pounds'}
SCALE_WORDS = {'k': ' thousand', 'm': ' million', '': ''}
MONEY = re.compile(r'(?:([−+-])\s?)?\b(CHF|EUR|USD|GBP) (\d+(?:\.\d+)?)(k|m)?\b')
SIGNED_NUMBER = re.compile(r'(?<![\w.])([−+])(\d)')
RANGE = re.compile(r'(\d| percent)\s?[–—]\s?(\d)')


class VoiceUnavailable(RuntimeError):
    pass


def _key():
    key = env('ELEVENLABS_KEY')
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


def dialect_script(sentences, dialect='gsw-u-sd-chzh'):
    """The briefing script translated into a Swiss German dialect via Supertext.

    Numbers are spelled out in English first (spoken()), then the whole script is
    translated — never the other way round, or the dialect pass would translate
    around English number-words it doesn't recognise as numbers. Falls back to the
    English script unchanged if Supertext is unavailable, so a missing/expired key
    degrades to an English voice rather than breaking the briefing.
    """
    from .translate import TranslationUnavailable, translate
    script = briefing_script(sentences)
    try:
        return translate([script], source='en', target=dialect)[0]
    except TranslationUnavailable:
        return script


def _cache_path(*parts):
    return CACHE_DIR / (hashlib.sha256('|'.join(parts).encode('utf-8')).hexdigest()[:24] + '.mp3')


def speak(text, voice_id=None, model=FAST_MODEL, timeout=60, language_code=None):
    """MP3 bytes for text, from the cache or ElevenLabs. Returns (audio, seconds to first byte or None).

    language_code tells ElevenLabs which language the voice should read in (e.g.
    'de' for a German voice reading Swiss German dialect text from dialect_script)."""
    voice_id = voice_id or DEFAULT_VOICE
    path = _cache_path(model, voice_id, language_code or '', text)
    if path.exists():
        return path.read_bytes(), None
    started = time.perf_counter()
    body = {'model_id': model, 'text': text}
    if language_code:
        body['language_code'] = language_code
    try:
        resp = requests.post(f'{API}/text-to-speech/{voice_id}/stream',
                             params={'output_format': 'mp3_44100_128'},
                             headers={'xi-api-key': _key(), 'Content-Type': 'application/json'},
                             data=_json(body), stream=True, timeout=timeout)
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
    b.add_argument('--dialect', help="e.g. gsw-u-sd-chzh (Zurich) or gsw-u-sd-chbe (Bern); untested live")
    s = sub.add_parser('say')
    s.add_argument('text')
    s.add_argument('--out', default='say.mp3')
    s.add_argument('--dialect', help="translate text to this Supertext target before speaking")
    t = sub.add_parser('transcribe')
    t.add_argument('file')
    args = parser.parse_args(argv)

    if args.cmd == 'brief':
        from .callmode import build_call
        from .data import load
        from .market import load_scenario
        call = build_call(load(), args.ref, load_scenario(args.scenario))
        if args.dialect:
            script = dialect_script(call['sentences'], args.dialect)
            audio, first = speak(script, language_code='de')
        else:
            script = briefing_script(call['sentences'])
            audio, first = speak(script)
        print(f'{len(script.split())} words, {len(audio) // 1024} KB, first byte '
              f'{first if first is not None else "cached"} s')
        print(script)
    elif args.cmd == 'say':
        text = args.text
        language_code = None
        if args.dialect:
            from .translate import TranslationUnavailable, translate
            try:
                text = translate([text], source='en', target=args.dialect)[0]
                language_code = 'de'
            except TranslationUnavailable as e:
                print(f'translation unavailable ({e}); speaking English text', file=sys.stderr)
        audio, first = speak(text, language_code=language_code)
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
