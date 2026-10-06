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


print("=== Partidos Liga Femenina 2026-2027 ===")
status, data = get(f"/partidos/?nombre_competicion={quote(COMP, safe='')}&temporada_competicion={quote(TEMPORADA, safe='')}")
print(status)
if isinstance(data, list):
    print(f"Total: {len(data)}")
    for p in data:
        print(p)
else:
    print(data)

print("\n=== Clasificacion Liga Femenina 2026-2027 ===")
status, data = get(f"/clasificaciones/?nombre_competicion={quote(COMP, safe='')}&temporada_competicion={quote(TEMPORADA, safe='')}")
print(status)
print(data)

print("\n=== Jugadoras (id_equipo=2) completas ===")
status, data = get("/jugadores/")
print(status)
if isinstance(data, list):
    for j in data:
        if j.get("id_equipo") == 2:
            print(j)
