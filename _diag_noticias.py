import requests

BASE = "https://aplicacion-web-m5oa.onrender.com"

resp = requests.get(f"{BASE}/noticias/?skip=0&limit=200")
print(resp.status_code)
data = resp.json()
print(f"Total noticias: {len(data)}")

import re


def clave(n):
    m = re.search(r"\((\d{2})/(\d{2})/(\d{4})\)\s*$", n.get("titular", ""))
    if m:
        dd, mm, yyyy = m.groups()
        from datetime import datetime
        return datetime(int(yyyy), int(mm), int(dd))
    return None

noticias_con_fecha = [(clave(n), n) for n in data]
noticias_con_fecha_validas = [(f, n) for f, n in noticias_con_fecha if f]
noticias_con_fecha_validas.sort(key=lambda x: x[0], reverse=True)

print("\n=== Top 5 por fecha extraida del titular ===")
for f, n in noticias_con_fecha_validas[:5]:
    print(f, "|", n.get("id_noticia"), "|", n.get("titular"))

print(f"\nNoticias SIN fecha en el titular: {len(noticias_con_fecha) - len(noticias_con_fecha_validas)}")
sin_fecha = [n for f, n in noticias_con_fecha if not f]
for n in sin_fecha[:10]:
    print(n.get("id_noticia"), "|", n.get("titular"))

print("\n=== Top 5 por id_noticia (orden de insercion) ===")
try:
    ordenadas_id = sorted(data, key=lambda n: int(n.get("id_noticia", 0)), reverse=True)
except Exception as e:
    print("error ordenando por id:", e)
    ordenadas_id = []
for n in ordenadas_id[:5]:
    print(n.get("id_noticia"), "|", n.get("titular"))
