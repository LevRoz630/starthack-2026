# The demo film

`demo.mp4` is the cut: the advisor answering the phone, then the call itself on
screen with both voices over it. 1080x1920, so it plays full-bleed on a phone and
drops into a slide without letterboxing at the sides.

## The pieces

| File | What it is |
| --- | --- |
| `media/advisor-broll.mp4` | 13s, shot in the room: the advisor takes the call. |
| `media/phone-screen.mp4` | 3m screen recording of the live Walter call against the deployed box. **Silent** — the phone's mic fed the app, nothing was recorded into the file. |
| `media/advisor-voice.m4a` | The room recording of that same run: the advisor answering, start to finish. |
| `media/walter-voice.m4a` | Walter's eight lines, recorded separately, in the order `data/demo/walter.json` has them. |

## How the three tracks line up

The advisor's take is already in step with the screen recording, so it goes down at
offset zero. The anchor is the card at 2:00, which shows his own sentence — "which
is not — really not risky for a general portfolio that you're holding" — and that
sentence ends at 122.4s in the audio as well. `ADVISOR_END` cuts the take before the
room chatter at the end of it.

Walter was recorded separately, so each of his lines is placed to end `LEAD` seconds
before the card it produces. The advisor answered straight through without leaving
gaps his questions fit into, so the advisor's track ducks under Walter's wherever
they meet.

## Re-cutting it

```
bash docs/demo/assemble.sh            # writes docs/demo/demo.mp4
bash docs/demo/assemble.sh out.mp4    # somewhere else
```

`CARDS` at the top of the script is when Walter's cards appear on screen. If a
question lands early or late, change its number there and re-run.
