from urllib.parse import quote

import requests

BASE = "https://aplicacion-web-m5oa.onrender.com/partidos/"


def get(nombre_comp, temporada):
    url = f"{BASE}?nombre_competicion={quote(nombre_comp, safe='')}&temporada_competicion={quote(temporada, safe='')}"
    resp = requests.get(url)
    return resp.status_code, resp.json() if resp.status_code == 200 else resp.text


print("=== Tal cual lo pide el frontend (Partidos.tsx / Calendario.tsx) ===")
status, data = get("1ª Andaluza Sénior (Jaén)", "Temporada 2026-2027")
print(status)
if isinstance(data, list):
    print(f"Total partidos devueltos: {len(data)}")
    # Buscar cualquier fila que mencione Iliturgi o jornada 4
    for p in data:
        if "iliturgi" in (p.get("local", "") + p.get("visitante", "")).lower() or p.get("jornada") == "4":
            print(p)
else:
    print(data)
