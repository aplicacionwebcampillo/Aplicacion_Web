from urllib.parse import quote

import requests

BASE = "https://aplicacion-web-m5oa.onrender.com/partidos"
NOMBRE = quote('1ª Andaluza Sénior (Jaén)', safe="")
TEMPORADA = quote("Temporada 2026-2027", safe="")

PARTIDOS_AJENOS = [
    ("C.D. VILLANUEVA", "BEGIJAR C.F."),
    ("C.D. VILCHES", "U.D. CAZORLA"),
    ("JAMILENA ATCO. C.D. DE FUTBOL", "C.D. TUGIA JUEGO LIMPIO ROMERO VERDE"),
    ("CAROLINENSE C.D.", "CLUB DEPORTIVO ATLÉTICO BAILÉN 1808"),
    ("JODAR C.F.", "INTER DE JAEN C.F. MOYZA"),
    ("C.D. TUCCITANA", 'REAL JAEN C.F., S.A.D. "B"'),
    ("C.D. JABALQUINTO", "C.D. CASTELLAR IBERO"),
]

for local, visitante in PARTIDOS_AJENOS:
    url = f"{BASE}/{NOMBRE}/{TEMPORADA}/{quote(local, safe='')}/{quote(visitante, safe='')}"
    resp = requests.delete(url)
    print(f"{local} vs {visitante}: {resp.status_code}")
