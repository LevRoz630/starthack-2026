"""Realtime speech-to-text for the call listener.

UNTESTED END TO END. Written from the protocol documented as a comment on
voice.REALTIME_URL (latency-tested there against a canned audio file, not
against a live call). No Twilio account or live microphone was available in
this environment to verify it against real audio — review and test with real
audio before relying on it for a demo. Needs `websockets` (requirements.txt)
and a working ELEVENLABS_KEY.

    -> {"message_type": "input_audio_chunk", "audio_base_64": <16kHz PCM16>,
        "sample_rate": 16000, "commit": false}
    <- {"message_type": "partial_transcript" | "committed_transcript", "text": ...}
"""

import base64
import json

from .voice import REALTIME_URL, VoiceUnavailable, _key


class ListenerUnavailable(RuntimeError):
    pass


async def stream_to_elevenlabs(audio_chunks, on_transcript):
    """Relay raw 16kHz PCM16 audio to ElevenLabs' realtime STT and await
    on_transcript(text) for each committed transcript, in order.

    audio_chunks: an async iterator of raw PCM16 bytes (~100ms each).
    on_transcript: an async callable, awaited once per committed transcript.
    Returns when audio_chunks is exhausted or the connection drops.
    """
    try:
        import websockets
    except ImportError as e:
        raise ListenerUnavailable('the "websockets" package is not installed') from e
    try:
        key = _key()
    except VoiceUnavailable as e:
        raise ListenerUnavailable(str(e)) from e

    try:
        async with websockets.connect(REALTIME_URL, additional_headers={'xi-api-key': key}) as ws:
            async def sender():
                async for chunk in audio_chunks:
                    await ws.send(json.dumps({
                        'message_type': 'input_audio_chunk',
                        'audio_base_64': base64.b64encode(chunk).decode('ascii'),
                        'sample_rate': 16000,
                        'commit': False,
                    }))
                await ws.send(json.dumps({
                    'message_type': 'input_audio_chunk', 'audio_base_64': '',
                    'sample_rate': 16000, 'commit': True,
                }))

            import asyncio
            send_task = asyncio.create_task(sender())
            try:
                async for raw in ws:
                    try:
                        msg = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    if msg.get('message_type') == 'committed_transcript' and (msg.get('text') or '').strip():
                        await on_transcript(msg['text'].strip())
            finally:
                send_task.cancel()
    except Exception as e:  # noqa: BLE001 - any transport failure ends the listener, never the call
        raise ListenerUnavailable(f'realtime speech-to-text failed: {e}') from e
