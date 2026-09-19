"""Turns ffmpeg's silencedetect output into the ranges of the call worth keeping.

    ffmpeg -i mix.wav -af silencedetect=... -f null - 2>&1 | python3 gaps.py <args>

Reads the log on stdin, prints two lines: the video select expression and the audio
one, over the same ranges, so the picture and the sound stay together.

A pause under KEEP is left alone -- speech needs room to breathe. A longer one is
trimmed back to KEEP, split either side of the cut so neither phrase loses its edge.
Nothing after PROTECT is touched: that is the call note and the follow-up email, which
are silent on purpose.
"""
import re
import sys


def ranges(log, duration, keep, protect):
    silences = []
    start = None
    for line in log.splitlines():
        m = re.search(r'silence_start: (-?[\d.]+)', line)
        if m:
            start = float(m.group(1))
        m = re.search(r'silence_end: ([\d.]+)', line)
        if m and start is not None:
            silences.append((start, float(m.group(1))))
            start = None
    if start is not None:
        silences.append((start, duration))

    keeps, at = [], 0.0
    for s, e in silences:
        s, e = max(s, 0.0), min(e, duration)
        if s >= protect or e - s <= keep:
            continue
        cut_from = s + keep / 2
        cut_to = e - keep / 2
        if cut_to <= cut_from:
            continue
        keeps.append((at, cut_from))
        at = cut_to
    keeps.append((at, duration))
    return [(a, b) for a, b in keeps if b - a > 0.04]


def main():
    duration, keep, protect = (float(a) for a in sys.argv[1:4])
    keeps = ranges(sys.stdin.read(), duration, keep, protect)
    expr = '+'.join(f'between(t,{a:.3f},{b:.3f})' for a, b in keeps)
    print(expr)
    print(f'{sum(b - a for a, b in keeps):.2f}', file=sys.stderr)


if __name__ == '__main__':
    main()
