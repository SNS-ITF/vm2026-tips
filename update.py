"""
VM 2026 - Opdater kampresultater
Kører via GitHub Actions hvert 30. minut.
Henter fra openfootball. Manglende resultater hardkodet herunder.
TILFØJ NYE RESULTATER under MANUAL_RESULTS efterhånden som kampe spilles.
"""
import urllib.request, json, sys
from datetime import datetime, timezone

# ─── TILFØJ MANUELLE RESULTATER HER ────────────────────────────────────────
# Format: kamp_nummer: (mål_hjemme, mål_ude)
# Bruges når openfootball ikke har opdateret endnu.
# Tidligere kampe slettes ikke – de overskrives bare af openfootball når den opdaterer.
MANUAL_RESULTS = {
    16: (1, 1),   # Belgium 1-1 Egypt         (15-jun)
    14: (0, 0),   # Spain 0-0 Cape Verde       (15-jun)
    # 13: (?, ?), # Saudi Arabia vs Uruguay    (16-jun)
    # 15: (?, ?), # IR Iran vs New Zealand     (16-jun)
}
# ────────────────────────────────────────────────────────────────────────────

MATCH_MAP = {
    ('Mexico', 'South Africa'): 1,
    ('South Korea', 'Czech Republic'): 2,
    ('Canada', 'Bosnia & Herzegovina'): 3,
    ('USA', 'Paraguay'): 4,
    ('Haiti', 'Scotland'): 5,
    ('Australia', 'Turkey'): 6,
    ('Brazil', 'Morocco'): 7,
    ('Qatar', 'Switzerland'): 8,
    ('Ivory Coast', 'Ecuador'): 9,
    ('Germany', 'Curaçao'): 10,
    ('Netherlands', 'Japan'): 11,
    ('Sweden', 'Tunisia'): 12,
    ('Saudi Arabia', 'Uruguay'): 13,
    ('Spain', 'Cape Verde'): 14,
    ('IR Iran', 'New Zealand'): 15,
    ('Iran', 'New Zealand'): 15,
    ('Belgium', 'Egypt'): 16,
    ('France', 'Senegal'): 17,
    ('Iraq', 'Norway'): 18,
    ('Argentina', 'Algeria'): 19,
    ('Austria', 'Jordan'): 20,
    ('Ghana', 'Panama'): 21,
    ('England', 'Croatia'): 22,
    ('Portugal', 'DR Congo'): 23,
    ('Uzbekistan', 'Colombia'): 24,
    ('Czech Republic', 'South Africa'): 25,
    ('Switzerland', 'Bosnia & Herzegovina'): 26,
    ('Canada', 'Qatar'): 27,
    ('Mexico', 'South Korea'): 28,
    ('Brazil', 'Haiti'): 29,
    ('Scotland', 'Morocco'): 30,
    ('Turkey', 'Paraguay'): 31,
    ('USA', 'Australia'): 32,
    ('Germany', 'Ivory Coast'): 33,
    ('Ecuador', 'Curaçao'): 34,
    ('Netherlands', 'Sweden'): 35,
    ('Tunisia', 'Japan'): 36,
    ('Uruguay', 'Cape Verde'): 37,
    ('Spain', 'Saudi Arabia'): 38,
    ('Belgium', 'IR Iran'): 39,
    ('Belgium', 'Iran'): 39,
    ('New Zealand', 'Egypt'): 40,
    ('Norway', 'Senegal'): 41,
    ('France', 'Iraq'): 42,
    ('Argentina', 'Austria'): 43,
    ('Jordan', 'Algeria'): 44,
    ('England', 'Ghana'): 45,
    ('Panama', 'Croatia'): 46,
    ('Portugal', 'Uzbekistan'): 47,
    ('Colombia', 'DR Congo'): 48,
    ('Scotland', 'Brazil'): 49,
    ('Morocco', 'Haiti'): 50,
    ('Switzerland', 'Canada'): 51,
    ('Bosnia & Herzegovina', 'Qatar'): 52,
    ('Czech Republic', 'Mexico'): 53,
    ('South Africa', 'South Korea'): 54,
    ('Curaçao', 'Ivory Coast'): 55,
    ('Ecuador', 'Germany'): 56,
    ('Japan', 'Sweden'): 57,
    ('Tunisia', 'Netherlands'): 58,
    ('Turkey', 'USA'): 59,
    ('Paraguay', 'Australia'): 60,
    ('Norway', 'France'): 61,
    ('Senegal', 'Iraq'): 62,
    ('Egypt', 'IR Iran'): 63,
    ('Egypt', 'Iran'): 63,
    ('New Zealand', 'Belgium'): 64,
    ('Cape Verde', 'Saudi Arabia'): 65,
    ('Uruguay', 'Spain'): 66,
    ('Panama', 'England'): 67,
    ('Croatia', 'Ghana'): 68,
    ('Algeria', 'Austria'): 69,
    ('Jordan', 'Argentina'): 70,
    ('Colombia', 'Portugal'): 71,
    ('DR Congo', 'Uzbekistan'): 72,
}

def tip(s1, s2):
    if s1 > s2: return '1'
    if s1 == s2: return 'X'
    return '2'

results = {}

# Start med manuelle resultater
for num, (s1, s2) in MANUAL_RESULTS.items():
    results[str(num)] = {'score': f'{s1}–{s2}', 'tip': tip(s1, s2)}
print(f"Manuelle resultater: {len(results)}", file=sys.stderr)

# Hent fra openfootball og overskriv manuelle hvis de har data
try:
    url = 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json'
    req = urllib.request.Request(url, headers={'User-Agent': 'vm2026-tips/1.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode())
    found = 0
    for m in data.get('matches', []):
        ft = m.get('score', {}).get('ft')
        if not ft:
            continue
        t1, t2 = m.get('team1', ''), m.get('team2', '')
        num = MATCH_MAP.get((t1, t2))
        if num:
            s1, s2 = int(ft[0]), int(ft[1])
            results[str(num)] = {'score': f'{s1}–{s2}', 'tip': tip(s1, s2)}
            found += 1
    print(f"Openfootball: {found} resultater", file=sys.stderr)
except Exception as e:
    print(f"Openfootball fejlede: {e}", file=sys.stderr)

print(f"Total: {len(results)} resultater", file=sys.stderr)
# Sorter efter kampnummer
sorted_results = dict(sorted(results.items(), key=lambda x: int(x[0])))
out = {
    'results': sorted_results,
    'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'count': len(sorted_results)
}
print(json.dumps(out, ensure_ascii=False, indent=2))


# ─── Gem resultater direkte i Supabase ──────────────────────────────────────
import urllib.request as urlreq

SUPABASE_URL = 'https://fttdvrfibkxqzfljyhoj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ0dGR2cmZpYmt4cXpmbGp5aG9qIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE1NTAzNDQsImV4cCI6MjA5NzEyNjM0NH0.juD8gL9wk_TRZMSRKtC4pQQ1WPTTBP3e8cRTByAxjEo'

# Gem i korrekt format:
# results: {"1": "1", "2": "X", ...}  <- kun tip-værdi (1/X/2)
# live:    {"1": {"score": "2-0"}, ...} <- score til visning
results_flat = {k: v['tip'] for k, v in sorted_results.items()}
live = {k: {'score': v['score']} for k, v in sorted_results.items()}

payload = json.dumps({
    'id': 'results',
    'data': json.dumps({'results': results_flat, 'live': live}),
    'updated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
}).encode()

req = urlreq.Request(
    f'{SUPABASE_URL}/rest/v1/tipskonkurrence',
    data=payload,
    method='POST',
    headers={
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'apikey': SUPABASE_KEY,
        'Content-Type': 'application/json',
        'Prefer': 'resolution=merge-duplicates'
    }
)
try:
    with urlreq.urlopen(req, timeout=10) as r:
        print(f"Supabase opdateret: HTTP {r.status}", file=sys.stderr)
except Exception as e:
    print(f"Supabase fejl: {e}", file=sys.stderr)
