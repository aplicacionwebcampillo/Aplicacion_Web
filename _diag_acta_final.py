from urllib.parse import quote

import requests

base = "https://aplicacion-web-m5oa.onrender.com/partidos"
nombre = quote("Trofeo Copa Presidente Diputación (Jaén)", safe="")
temporada = quote("Temporada 2026-2027", safe="")
local = quote("C.D. NAVAS 2006", safe="")
visitante = quote('C.D. CAMPILLO DEL RÍO C.F. "CD"', safe="")

url = f"{base}/{nombre}/{temporada}/{local}/{visitante}"
resp = requests.get(url)
print(resp.status_code)
print(resp.json())
