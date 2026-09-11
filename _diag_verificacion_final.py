from urllib.parse import quote

import requests

BASE = "https://aplicacion-web-m5oa.onrender.com/partidos"
TEMPORADA = quote("Temporada 2026-2027", safe="")


def get(nombre_comp, local, visitante):
    url = f"{BASE}/{quote(nombre_comp, safe='')}/{TEMPORADA}/{quote(local, safe='')}/{quote(visitante, safe='')}"
    resp = requests.get(url)
    return resp.status_code, resp.json() if resp.status_code == 200 else resp.text


print("=== Jornada 2 Liga (Cazorla vs Campillo) ===")
print(get("1ª Andaluza Sénior (Jaén)", "U.D. CAZORLA", 'C.D. CAMPILLO DEL RÍO C.F. "CD"'))

print("\n=== Final Copa (Navas 2006 vs Campillo) ===")
print(get("Trofeo Copa Presidente Diputación (Jaén)", "C.D. NAVAS 2006", 'C.D. CAMPILLO DEL RÍO C.F. "CD"'))

print("\n=== Cuartos Copa (Arjonilla vs Campillo, ya tenia acta) ===")
print(get("Trofeo Copa Presidente Diputación (Jaén)", "CLUB ATLETICO ARJONILLA", 'C.D. CAMPILLO DEL RÍO C.F. "CD"'))

print("\n=== Semifinales Copa (Hispania vs Campillo, ya tenia acta) ===")
print(get("Trofeo Copa Presidente Diputación (Jaén)", "C.D. HISPANIA DE TORREDELCAMPO", 'C.D. CAMPILLO DEL RÍO C.F. "CD"'))
