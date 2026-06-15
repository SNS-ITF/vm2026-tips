import urllib.request
import json
import sys

URL = 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json'

try:
    with urllib.request.urlopen(URL, timeout=15) as r:
        raw = json.loads(r.read().decode())
except Exception as e:
    print(f"Fejl ved hentning: {e}", file=sys.stderr)
    sys.exit(1)

# Byg simpel lookup: match_num -> {score, tip}
results = {}
for rnd in raw.get('rounds', []):
    for m in rnd.get('matches', []):
        num = m.get('num')
        s1  = m.get('score1')
        s2  = m.get('score2')
        if num and s1 is not None and s2 is not None:
            if   s1 > s2: tip = '1'
            elif s1 == s2: tip = 'X'
            else:          tip = '2'
            results[str(num)] = {'score': f'{s1}–{s2}', 'tip': tip}

out = {'results': results, 'source': 'openfootball/worldcup.json'}
print(json.dumps(out, ensure_ascii=False, indent=2))
