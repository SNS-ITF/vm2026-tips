"""
VM 2026 – Opdater kampresultater
Kører via GitHub Actions hver 30. minut.
Kendte resultater hardkodet, fremtidige kampe tilføjes løbende.
"""
import json, sys
from datetime import datetime, timezone

def tip(s1, s2):
    if s1 > s2: return '1'
    if s1 == s2: return 'X'
    return '2'

# Alle spillede resultater – opdateres manuelt i denne fil efterhånden
# Format: kamp_nummer: (score_hjemme, score_ude)
RESULTS = {
    # --- 11. juni ---
    1:  (2, 0),   # Mexico 2-0 South Africa
    # --- 12. juni ---
    2:  (2, 1),   # Rep. of Korea 2-1 Czech Rep.
    3:  (1, 1),   # Canada 1-1 Bosnia/Herzeg.
    4:  (4, 1),   # USA 4-1 Paraguay
    # --- 13. juni ---
    7:  (1, 1),   # Brazil 1-1 Morocco
    8:  (1, 1),   # Qatar 1-1 Switzerland
    5:  (0, 1),   # Haiti 0-1 Scotland
    6:  (2, 0),   # Australia 2-0 Turkey
    # --- 14. juni ---
    10: (7, 1),   # Germany 7-1 Curaçao
    11: (2, 2),   # Netherlands 2-2 Japan
    9:  (1, 0),   # Ivory Coast 1-0 Ecuador
    12: (5, 1),   # Sweden 5-1 Tunisia
    # --- 15. juni (aften endnu ikke spillet) ---
    # 14: Spain vs Cape Verde
    # 16: Belgium vs Egypt
    # 13: Saudi Arabia vs Uruguay
    # 15: IR Iran vs New Zealand
}

results = {}
for num, (s1, s2) in RESULTS.items():
    results[str(num)] = {
        'score': f'{s1}–{s2}',
        'tip': tip(s1, s2)
    }

out = {
    'results': results,
    'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'count': len(results)
}

print(json.dumps(out, ensure_ascii=False, indent=2))
