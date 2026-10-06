from urllib.parse import quote

import requests

BASE = "https://aplicacion-web-m5oa.onrender.com"

LOCAL = "C.D. CAMPILLO DEL RÍO CF"
VISITANTE = 'CLUB DEPORTIVO ATLÉTICO BAILÉN 1808 "SE"'
NOMBRE_COMP = "Liga Femenina Sénior Fútbol 7 (Jaén)"
TEMPORADA = "Temporada 2026-2027"


def get(path):
    resp = requests.get(f"{BASE}{path}")
    try:
        return resp.status_code, resp.json()
    except Exception:
        return resp.status_code, resp.text


print("=== GET exacto (misma ruta que usa guardar_o_actualizar_partido) ===")
url = f"/partidos/{quote(NOMBRE_COMP, safe='')}/{quote(TEMPORADA, safe='')}/{quote(LOCAL, safe='')}/{quote(VISITANTE, safe='')}"
print("URL codificada correctamente:", url)
print(get(url))

print("\n=== GET SIN codificar (tal y como lo construye guardar_o_actualizar_partido) ===")
url_sin_codificar = f"/partidos/{NOMBRE_COMP}/{TEMPORADA}/{LOCAL}/{VISITANTE}"
print("URL cruda:", url_sin_codificar)
print(get(url_sin_codificar))

print("\n=== Todos los partidos que mencionen Bailen o Campillo del Rio CF (cualquier competicion/temporada) ===")
status, data = get("/partidos/")
print(status)
if isinstance(data, list):
    for p in data:
        texto = (p.get("local", "") + p.get("visitante", "")).upper()
        if "BAIL" in texto or "CAMPILLO DEL R" in texto:
            print(p)
