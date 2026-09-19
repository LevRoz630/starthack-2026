"""What a sentence heard on a call is, when it is more than a question with an answer.

Most of a real call is not a clean question. Each finished sentence is sorted, in order:

    small_talk   "How's the golf?"                     -> nothing
    instruction  "Sell the Novartis."                  -> noted, flagged: confirm in writing
    request      "Can you send me the tax statement?"  -> a to-do for after the call
    question     "How much did today cost me?"         -> an answer card (or a follow-up if
                                                          nothing in the data answers it)
    info         "We're buying a house next spring."   -> noted for the call note
    other        anything else                          -> nothing

Nothing here ever acts: instructions and requests only reach the call note, for the
advisor to confirm. Review what a live call did with `python -m backend.utterance review`.
"""

import json
import re
import sys
from pathlib import Path

from .answers import small_talk_only
from .data import ROOT

SESSIONS = ROOT / 'data' / 'sessions'

# A question that asks for advice is a question, even with "sell" in it.
ADVICE = re.compile(r"^\s*(?:so\s+)?(?:should|shall|would|could|do|does|is|are|can) (?:i|we|it|you think)\b", re.I)
INSTRUCTION = re.compile(
    r"\b(?:sell|buy|liquidate|cash out|get (?:me )?out of|dump|switch (?:into|to)|move (?:everything|it all|my money|\w+) (?:into|to)"
    r"|put (?:\w+ ){0,3}(?:into|in)|invest (?:\w+ ){0,3}in|transfer (?:\w+ ){0,3}to|stop the standing order)\b", re.I)
IMPERATIVE = re.compile(r"^\s*(?:please\s+|ok(?:ay)?,?\s+|right,?\s+|then\s+|and\s+)?"
                        r"(?:sell|buy|liquidate|dump|switch|move|put|invest|transfer|stop)\b"
                        r"|\bi (?:want|would like|'d like|need) (?:you )?to (?:sell|buy|liquidate|switch|move|put|invest|transfer|get out)\b"
                        r"|\b(?:just |please )(?:sell|buy)\b", re.I)
REQUEST = re.compile(
    r"\b(?:can|could|would|will) you (?:please )?(?:send|email|e-mail|mail|forward|prepare|check|look into|call|ring|book|"
    r"set up|arrange|find out|get back|put together|share|update)\b"
    r"|\bplease (?:send|email|forward|call|book|check|prepare|arrange)\b"
    r"|\b(?:send|email|forward) me\b|\bi(?:'d| would) like (?:a|the|to (?:get|see|have|receive))\b"
    r"|\blet me know\b|\bget back to me\b|\bcall me (?:back|tomorrow|later|next)\b"
    r"|\bwhen (?:should|shall|can|could) we (?:meet|talk|speak)\b|\b(?:let'?s|can we|could we) (?:meet|schedule|book)\b",
    re.I)
INFO = re.compile(
    r"\b(?:retir\w*|pension|house|property|flat|apartment|mortgage|inherit\w*|wedding|divorc\w*|baby|grandchild\w*|"
    r"school|university|tuition|new job|lost my job|my (?:company|business)|selling the (?:house|company|business)|"
    r"mov(?:e|ing) to|relocat\w*|tax\w*|medical|surgery|hospital|donat\w*|foundation|charity|sustainab\w*|esg|"
    r"don'?t want|prefer|worried|nervous|concerned|scared|anxious|need (?:the )?(?:money|cash|liquidity)|"
    r"next (?:year|month|spring|summer|autumn|winter)|in (?:a|two|three|\d+) (?:years?|months?))\b", re.I)
QUESTION_START = re.compile(r"^\s*(?:and |so |but |ok(?:ay)? |right,? |hm+,? )*(?:how|what|why|when|where|which|who|is|are|"
                            r"am|was|were|did|do|does|can|could|should|will|would|have|has|tell me|explain)\b", re.I)

LABELS = {'instruction': 'Instruction, confirm in writing', 'request': 'To do', 'info': 'Noted',
          'follow_up': 'To follow up'}


def classify(text):
    """'small_talk' | 'instruction' | 'request' | 'question' | 'info' | 'other'."""
    text = (text or '').strip()
    if not re.search(r'[a-zA-Z]{2,}', text) or small_talk_only(text):
        return 'small_talk'
    is_q = text.rstrip().endswith('?') or bool(QUESTION_START.search(text))
    if not ADVICE.search(text) and (IMPERATIVE.search(text) or (INSTRUCTION.search(text) and not is_q)):
        return 'instruction'
    if REQUEST.search(text):
        return 'request'
    if is_q:
        return 'question'
    if INFO.search(text):
        return 'info'
    return 'other'


class SessionLog:
    """Every finished sentence of a live call and what was done with it, one JSON line each,
    in data/sessions/ (gitignored: these are real conversations)."""

    def __init__(self, client, source, started):
        SESSIONS.mkdir(parents=True, exist_ok=True)
        stamp = started.strftime('%Y%m%d-%H%M%S')
        self.path = SESSIONS / f'{stamp}-{client}-{source}.jsonl'

    def write(self, **entry):
        try:
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        except OSError:
            pass   # logging must never break a call


def review(paths):
    """Print what each logged call heard and did, so misfires are easy to spot."""
    for path in paths:
        print(f'== {Path(path).name}')
        with open(path, encoding='utf-8') as f:
            for line in f:
                e = json.loads(line)
                shown = e.get('shown') or ''
                print(f"  {e.get('kind', ''):12} {e.get('decision', ''):12} {e.get('text', '')[:70]:72} {shown[:60]}")


def main(argv=None):
    args = argv if argv is not None else sys.argv[1:]
    if args[:1] == ['classify'] and len(args) > 1:
        print(classify(' '.join(args[1:])))
        return 0
    if args[:1] == ['review']:
        paths = args[1:] or sorted(str(p) for p in SESSIONS.glob('*.jsonl'))[-1:]
        if not paths:
            print('no sessions logged yet (data/sessions/)')
            return 1
        review(paths)
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
