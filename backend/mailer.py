"""Send the approved follow-up email and call note.

Gmail over SMTP with an app password (myaccount.google.com/apppasswords). Settings in
.env, never committed:

    SMTP_USER=you@gmail.com
    SMTP_PASSWORD=<16-character app password>
    EMAIL_TO=where the demo mail should arrive
    EMAIL_FROM=optional, defaults to SMTP_USER
    SMTP_HOST / SMTP_PORT=optional, default smtp.gmail.com / 587

Without SMTP_USER, SMTP_PASSWORD and EMAIL_TO the message is written to data/outbox/
instead, so the demo never breaks on a missing password.
"""

import os
import smtplib
import time
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

from dotenv import load_dotenv

from .data import ROOT

load_dotenv(ROOT / '.env')

OUTBOX = ROOT / 'data' / 'outbox'


def _env(name, default=''):
    return (os.getenv(name) or default).strip().strip('"\'')


def configured():
    return all(_env(k) for k in ('SMTP_USER', 'SMTP_PASSWORD', 'EMAIL_TO'))


def masked(address):
    """'jo***@gmail.com' — enough to recognise the inbox without printing the address."""
    name, _, domain = address.partition('@')
    return f'{name[:2]}***@{domain}' if domain else '***'


def build(subject, body, to=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = _env('EMAIL_FROM') or _env('SMTP_USER') or 'advisor-copilot@localhost'
    msg['To'] = to or _env('EMAIL_TO') or 'outbox@localhost'
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid(domain='advisor-copilot')
    msg.set_content(body)
    return msg


def send(subject, body, to=None, timeout=20):
    """Send, or save to the outbox when no SMTP settings exist.

    Returns {'sent': True, 'to': masked} or {'sent': False, 'outbox': path}. SMTP errors
    raise, so the caller can tell the advisor the mail did not go out.
    """
    msg = build(subject, body, to)
    if not configured():
        OUTBOX.mkdir(parents=True, exist_ok=True)
        path = OUTBOX / f'{time.strftime("%Y%m%d-%H%M%S")}-{abs(hash(subject)) % 10000:04d}.eml'
        path.write_bytes(bytes(msg))
        return {'sent': False, 'outbox': str(path.relative_to(ROOT))}
    with smtplib.SMTP(_env('SMTP_HOST', 'smtp.gmail.com'), int(_env('SMTP_PORT', '587')), timeout=timeout) as smtp:
        smtp.starttls()
        smtp.login(_env('SMTP_USER'), _env('SMTP_PASSWORD'))
        smtp.send_message(msg)
    return {'sent': True, 'to': masked(msg['To'])}
