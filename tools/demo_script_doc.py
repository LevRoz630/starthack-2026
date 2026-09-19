import json, pathlib
WHO = {
 'walter': ("Walter White", "CASE-045",
   "A former chemistry teacher. His file says he runs a small family car-wash business on the "
   "side and occasionally asks about reinvesting its proceeds, prefers to settle smaller amounts "
   "in cash where possible, and values discretion -- minimal written correspondence about "
   "portfolio specifics. Recent health concerns have prompted a review of estate and succession "
   "planning. He is 63% health care through Novartis and BB Biotech, and Novartis alone is 41% "
   "of his book."),
 'buzz': ("Buzz Lightyear", "CASE-027",
   "Very enthusiastic about space travel; his file records that he follows private spaceflight "
   "companies with great interest and has asked for more detail on how that exposure could be "
   "expanded further. He prefers forward-looking, high-conviction positions over defensive ones. "
   "He is 97.9% industrials, SpaceX alone is 68.5% of his book, and his volatility is running "
   "above the ceiling for his profile."),
}
ORDER = [('walter', 'Call 1 — the silent one, for filming'), ('buzz', 'Call 2 — the voiced one')]
out = ["# The two demo calls", "",
       "Generated from the recorded runs in `data/demo/runs/`, so this is what actually happens on",
       "the phone rather than what was intended. The client's lines are in `data/demo/*.json`.", "",
       "Every number an advisor says out loud must be on the card above it. If a card does not",
       "come, say the thing without the number.", ""]
for name, heading in ORDER:
    run = json.loads(pathlib.Path(f'data/demo/runs/{name}-latest.json').read_text(encoding='utf-8'))
    script = json.loads(pathlib.Path(f'data/demo/{name}.json').read_text(encoding='utf-8'))
    who, ref, blurb = WHO[name]
    first = who.split()[0].upper()
    answers = [x['event'] for x in run['events'] if x['event']['type'] == 'answer']
    out += ['---', '', f'## {heading}: {who} ({ref})', '', f'**Who.** {blurb}', '',
            f"**Market.** {script['scenario']}.  **Length.** {run['events'][-1]['t']:.0f} seconds, "
            f"{len(answers)} answered questions.", '']
    for i, e in enumerate(answers, 1):
        out += [f'### {i}', '', f"**{first}:** {e['question']}", '']
        out += [f"> {a['text']}" for a in e.get('answers', [])]
        out += ['']
    out += ['### Sign-off', '', f"**{first}:** {script['lines'][-1]['text']}", '',
            '*No card. It is not a question, and the system knows that.*', '']
out += ['---', '', '## For whoever plays the client', '',
        '- Say the lines as written. The speech-to-text is listening for these words.',
        '- **End every line on the question.** A line that finishes with a statement is committed as',
        '  a statement and gets no card.',
        '- Leave the gap. The advisor is answering the client in it.',
        '- The last line is a sign-off, not a question. Do not turn it into one.', '',
        '## For the advisor', '',
        '- Look at the card, then look up. Do not read it off the screen word for word.',
        '- Never say a number that is not on the card in front of you.', '']
pathlib.Path('docs/DEMO-SCRIPT.md').write_text('\n'.join(out), encoding='utf-8')
print('regenerated')
