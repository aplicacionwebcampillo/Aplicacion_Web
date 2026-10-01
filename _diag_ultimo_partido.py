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


from datetime import date

HOY = date.today().isoformat()

print("=== Todos los partidos (buscando los ya jugados mas recientes) ===")
status, data = get("/partidos/")
print(status)
if isinstance(data, list):
    def parse_fecha(p):
        return p.get("dia") or ""
    partidos_campillo = [
        p for p in data
        if "campillo" in (p.get("local", "") + p.get("visitante", "")).lower()
    ]
    jugados = [p for p in partidos_campillo if parse_fecha(p) and parse_fecha(p) <= HOY]
    futuros = [p for p in partidos_campillo if parse_fecha(p) and parse_fecha(p) > HOY]
    jugados.sort(key=parse_fecha)
    futuros.sort(key=parse_fecha)
    print(f"Total partidos del Campillo: {len(partidos_campillo)}, jugados hasta hoy ({HOY}): {len(jugados)}")
    print("--- ultimos 6 jugados ---")
    for p in jugados[-6:]:
        print(p)
    print("--- proximos 3 ---")
    for p in futuros[:3]:
        print(p)
else:
    print(data)
