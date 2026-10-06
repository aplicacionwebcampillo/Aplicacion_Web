from urllib.parse import quote

import requests

BASE = "https://aplicacion-web-m5oa.onrender.com"
COMP = "Liga Femenina Sénior Fútbol 7 (Jaén)"
TEMPORADA = "Temporada 2026-2027"


def get(path):
    resp = requests.get(f"{BASE}{path}")
    try:
        return resp.status_code, resp.json()
    except Exception:
        return resp.status_code, resp.text


print("=== Partidos Liga Femenina 2026-2027 (tras el fix) ===")
status, data = get(f"/partidos/?nombre_competicion={quote(COMP, safe='')}&temporada_competicion={quote(TEMPORADA, safe='')}")
print(status)
print(data)
