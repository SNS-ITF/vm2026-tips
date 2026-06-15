import urllib.request, json, sys
from datetime import datetime, timezone

MATCH_MAP = {
    ('Mexico', 'South Africa'):           1,
    ('South Korea', 'Czech Republic'):    2,
    ('Canada', 'Bosnia & Herzegovina'):   3,
    ('USA', 'Paraguay'):                  4,
    ('Haiti', 'Scotland'):                5,
    ('Australia', 'Turkey'):              6,
    ('Brazil', 'Morocco'):                7,
    ('Qatar', 'Switzerland'):             8,
    ('Ivory Coast', 'Ecuador'):           9,
    ('Germany', 'Curaçao'):              10,
    ('Netherlands', 'Japan'):            11,
    ('Sweden', 'Tunisia'):               12,
    ('Saudi Arabia', 'Uruguay'):         13,
    ('Spain', 'Cape Verde'):             14,
    ('IR Iran', 'New Zealand'):          15,
    ('Iran', 'New Zealand'):             15,
    ('Belgium', 'Egypt'):                16,
    ('France', 'Senegal'):               17,
    ('Iraq', 'Norway'):                  18,
    ('Argentina', 'Algeria'):            19,
    ('Austria', 'Jordan'):               20,
    ('Ghana', 'Panama'):                 21,
    ('England', 'Croatia'):              22,
    ('Portugal', 'DR Congo'):            23,
    ('Uzbekistan', 'Colombia'):          24,
    ('Czech Republic', 'South Africa'):  25,
    ('Switzerland', 'Bosnia & Herzegovina'): 26,
    ('Canada', 'Qatar'):                 27,
    ('Mexico', 'South Korea'):           28,
    ('Brazil', 'Haiti'):                 29,
    ('Scotland', 'Morocco'):             30,
    ('Turkey', 'Paraguay'):              31,
    ('USA', 'Australia'):                32,
    ('Germany', 'Ivory Coast'):          33,
    ('Ecuador', 'Curaçao'):             34,
    ('Netherlands', 'Sweden'):           35,
    ('Tunisia', 'Japan'):                36,
    ('Uruguay', 'Cape Verde'):           37,
    ('Spain', 'Saudi Arabia'):           38,
    ('Belgium', 'Iran'):                 39,
    ('Belgium', 'IR Iran'):              39,
    ('New Zealand', 'Egypt'):            40,
    ('Norway', 'Senegal'):               41,
    ('France', 'Iraq'):                  42,
    ('Argentina', 'Austria'):            43,
    ('Jordan', 'Algeria'):               44,
    ('England', 'Ghana'):                45,
    ('Panama', 'Croatia'):               46,
    ('Portugal', 'Uzbekistan'):          47,
    ('Colombia', 'DR Congo'):            48,
    ('Scotland', 'Brazil'):              49,
    ('Morocco', 'Haiti'):                50,
    ('Switzerland', 'Canada'):           51,
    ('Bosnia & Herzegovina', 'Qatar'):   52,
    ('Czech Republic', 'Mexico'):        53,
    ('South Africa', 'South Korea'):     54,
    ('Curaçao', 'Ivory Coast'):         55,
    ('Ecuador', 'Germany'):              56,
    ('Japan', 'Sweden'):                 57,
    ('Tunisia', 'Netherlands'):          58,
    ('Turkey', 'USA'):                   59,
    ('Paraguay', 'Australia'):           60,
    ('Norway', 'France'):                61,
    ('Senegal', 'Iraq'):                 62,
    ('Egypt', 'Iran'):                   63,
    ('Egypt', 'IR Iran'):                63,
    ('New Zealand', 'Belgium'):          64,
    ('Cape Verde', 'Saudi Arabia'):      65,
    ('Uruguay', 'Spain'):                66,
    ('Panama', 'England'):               67,
    ('Croatia', 'Ghana'):                68,
    ('Algeria', 'Austria'):              69,
    ('Jordan', 'Argentina'):             70,
    ('Colombia', 'Portugal'):            71,
    ('DR Congo', 'Uzbekistan'):          72,
}

def tip(s1, s2):
    if s1 > s2: return '1'
    if s1 == s2: return 'X'
    return '2'

url = 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'vm2026-tips/1.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode())
    print(f"Hentet {len(data.get('matches',[]))} kampe fra openfootball", file=sys.stderr)
except Exception as e:
    print(f"FEJL ved hentning: {e}", file=sys.stderr)
    sys.exit(1)

results = {}
for m in data.get('matches', []):
    ft = m.get('score', {}).get('ft')
    if not ft:
        continue
    t1, t2 = m.get('team1',''), m.get('team2','')
    num = MATCH_MAP.get((t1, t2))
    if num is None:
        print(f"Ikke matchet: {t1!r} vs {t2!r}", file=sys.stderr)
        continue
    s1, s2 = int(ft[0]), int(ft[1])
    # Ignorer 0-0 for kampe der ikke er startet endnu
    # (openfootball inkluderer af og til 0-0 som placeholder)
    results[str(num)] = {'score': f'{s1}–{s2}', 'tip': tip(s1, s2)}

print(f"Gemmer {len(results)} resultater", file=sys.stderr)
out = {
    'results': results,
    'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'count': len(results)
}
print(json.dumps(out, ensure_ascii=False, indent=2))
