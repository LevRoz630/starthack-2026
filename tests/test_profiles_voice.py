import os
import re

import pytest

from backend import voice
from backend.data import load
from backend.profiles import (TEMPERAMENTS, WANTS, keyword_profile, load_cache, notes_of, playbook_angles,
                              validate)

NUMBER = re.compile(r'\d+(?:\.\d+)?')
network = pytest.mark.skipif(not os.getenv('RUN_NETWORK_TESTS'), reason='set RUN_NETWORK_TESTS=1 to call ElevenLabs')


@pytest.fixture(scope='module')
def store():
    return load()


def test_cached_profiles_only_quote_real_notes(store):
    cache = load_cache()
    assert set(cache) == set(store.clients)
    angles = set(playbook_angles())
    for ref, p in cache.items():
        notes = [n.rstrip('.') for n in notes_of(store.client(ref))]
        assert p['temperament'] in TEMPERAMENTS and p['wants'] in WANTS, ref
        assert p['source'] in ('apertus', 'keywords', 'no-notes'), ref
        for phrase in p['liquidity_needs'] + p['contact_preferences']:
            assert phrase in notes, (ref, phrase)
        for quoted in p['evidence'].values():
            assert all(q.rstrip('.') in notes for q in quoted), ref
        assert set(p['angles']) <= angles, ref


def test_keywords_match_whole_words():
    p = keyword_profile(['Extremely patient investor; unconcerned by short-term volatility, takes the long view.'])
    assert p['temperament'] == 'patient'      # not 'anxious' from "unconcerned"
    assert p['wants'] == 'unknown'            # not 'short' from "short-term"


def test_validation_rejects_what_the_notes_do_not_support():
    notes = ['Plans to buy a house next year.', 'Prefers email over calls.']
    known = playbook_angles()
    ok, why = validate({'temperament': 'unknown', 'wants': 'unknown', 'liquidity_needs': [1],
                        'contact_preferences': [2], 'angles': ['cash_need'], 'evidence': {}}, notes, known)
    assert why is None and ok['liquidity_needs'] == ['Plans to buy a house next year']
    assert validate({'temperament': 'furious', 'wants': 'unknown'}, notes, known)[0] is None
    assert validate({'temperament': 'unknown', 'wants': 'unknown', 'liquidity_needs': [3]}, notes, known)[0] is None
    assert validate({'temperament': 'unknown', 'wants': 'unknown', 'angles': ['invented']}, notes, known)[0] is None
    # A claim without a note behind it is dropped to unknown rather than trusted.
    ok, _ = validate({'temperament': 'anxious', 'wants': 'unknown', 'evidence': {}}, notes, known)
    assert ok['temperament'] == 'unknown'


def test_script_keeps_every_number():
    sentences = [{'text': 'Probably the market move: Information Technology −4.8% today, 9.6% of the book; '
                          'about −CHF 12k (−1.4%) overall.'},
                 'Liquidity at 100.0%, outside its 0.0%–60.0% band, target 3.0%.',
                 'Waldo is calling: Investor profile 6, CHF 891k across 1 portfolio.']
    script = voice.briefing_script(sentences)
    assert script == voice.briefing_script(sentences)
    source = ' '.join(s['text'] if isinstance(s, dict) else s for s in sentences)
    assert sorted(NUMBER.findall(script)) == sorted(NUMBER.findall(source))
    assert 'minus 12 thousand francs' in script and '0.0 percent to 60.0 percent' in script
    assert 'profile 6, 891 thousand francs' in script


def test_voice_without_a_key_fails_cleanly(monkeypatch, tmp_path):
    monkeypatch.setenv('ELEVENLABS_KEY', '')
    monkeypatch.setattr(voice, 'CACHE_DIR', tmp_path)
    with pytest.raises(voice.VoiceUnavailable):
        voice.speak('not cached')
    with pytest.raises(voice.VoiceUnavailable):
        voice.transcribe(b'')


@network
def test_round_trip_through_elevenlabs():
    question = 'How much have I lost on tech today?'
    audio, _ = voice.speak(question)
    text, _ = voice.transcribe(audio)
    assert 'tech' in text.lower()
