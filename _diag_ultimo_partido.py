from urllib.parse import quote

import requests

BASE = "https://aplicacion-web-m5oa.onrender.com"
TEMPORADA = "Temporada 2026-2027"


def get(path):
    url = f"{BASE}{path}"
    resp = requests.get(url)
    try:
        return resp.status_code, resp.json()
    except Exception:
        return resp.status_code, resp.text


print("=== Todos los partidos (buscando los mas recientes) ===")
status, data = get("/partidos/")
print(status)
if isinstance(data, list):
    import re
    def parse_fecha(p):
        return p.get("dia") or ""
    partidos_campillo = [
        p for p in data
        if "campillo" in (p.get("local", "") + p.get("visitante", "")).lower()
    ]
    partidos_campillo.sort(key=parse_fecha)
    print(f"Total partidos del Campillo: {len(partidos_campillo)}")
    for p in partidos_campillo[-8:]:
        print(p)
else:
    print(data)
