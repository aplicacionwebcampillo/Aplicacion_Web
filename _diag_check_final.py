from urllib.parse import quote

import requests

base = "https://aplicacion-web-m5oa.onrender.com/partidos"
nombre = quote('1ª Andaluza Sénior (Jaén)', safe="")
temporada = quote("Temporada 2026-2027", safe="")
local = quote('C.D. CAMPILLO DEL RÍO C.F. "CD"', safe="")
visitante = quote("LINARES DEPORTIVO", safe="")

url = f"{base}/{nombre}/{temporada}/{local}/{visitante}"
print(url)
resp = requests.get(url)
print(resp.status_code)
print(resp.json())
