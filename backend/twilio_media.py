"""Twilio incoming-call webhook and media stream: the real telephony path.

UNTESTED END TO END. No Twilio account, phone number or live call was
available in this environment to verify any of this against Twilio's actual
webhook or media-stream traffic — it is written strictly from Twilio's public
TwiML and Media Streams documentation, not exercised against a real call.
Test against a real Twilio number before relying on it for a demo; the
fallback in docs/PLAN.md (a second device dialling POST /call/incoming, which
does not depend on any of this) is the path that is actually verified.

Setup (see docs/PLAN.md "Twilio tonight"): a paid Twilio account, a UK/US
number (Swiss numbers need an address bundle), and the number's "A call comes
in" webhook set to POST https://<your-host>/twilio/incoming. A tunnel
(ngrok/cloudflared) is needed so Twilio can reach this server during
development.

Environment: ADVISOR_NUMBER (E.164, e.g. "+41791234567") — where the call is
forwarded. Twilio Media Streams audio is 8kHz mono mu-law; ElevenLabs'
realtime STT (backend/listener.py) wants 16kHz PCM16, so every frame is
decoded and resampled with the stdlib `audioop` module. `audioop` was removed
in Python 3.13 — this needs Python <= 3.12 or a replacement (e.g. `audioop-lts`).
"""

from xml.sax.saxutils import escape

import os


def twiml_response(ref, host):
    """TwiML for the incoming-call webhook: start a media stream to our
    listener (only if we resolved the caller to a client) then forward the
    call to ADVISOR_NUMBER. Never invents a client if the caller is unknown."""
    advisor = (os.getenv('ADVISOR_NUMBER') or '').strip()
    if not advisor:
        return ('<?xml version="1.0" encoding="UTF-8"?><Response>'
                '<Say>The advisor number is not configured.</Say></Response>')
    stream = f'<Start><Stream url="wss://{escape(host)}/call/{escape(ref)}/twilio-media" /></Start>' if ref else ''
    return (f'<?xml version="1.0" encoding="UTF-8"?><Response>{stream}'
            f'<Dial>{escape(advisor)}</Dial></Response>')


def mulaw8k_to_pcm16k(payload, rate_state):
    """One Twilio media frame (8kHz mono mu-law bytes) -> 16kHz PCM16 bytes.

    rate_state is audioop.ratecv's continuation state; pass None on the first
    call for a stream, then thread back what this returns so consecutive
    frames resample as one continuous signal rather than clicking at frame
    boundaries. Returns (pcm16_bytes, new_rate_state).
    """
    import audioop
    pcm16_8k = audioop.ulaw2lin(payload, 2)
    pcm16_16k, rate_state = audioop.ratecv(pcm16_8k, 2, 1, 8000, 16000, rate_state)
    return pcm16_16k, rate_state
