from urllib.parse import quote

import requests

BASE = "https://aplicacion-web-m5oa.onrender.com/partidos"
NOMBRE = quote('1ª Andaluza Sénior (Jaén)', safe="")
TEMPORADA = quote("Temporada 2026-2027", safe="")

resp = requests.get(f"{BASE}/", params={"nombre_competicion": '1ª Andaluza Sénior (Jaén)', "temporada_competicion": "Temporada 2026-2027"})
print(resp.status_code)
partidos = resp.json()
campillo = [p for p in partidos if "campillo" in (p.get("local","")+p.get("visitante","")).lower()]
for p in sorted(campillo, key=lambda x: x.get("jornada","")):
    print(p)
