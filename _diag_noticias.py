import requests

BASE = "https://aplicacion-web-m5oa.onrender.com"

resp_total = requests.get(f"{BASE}/noticias/?skip=0&limit=1000")
total = resp_total.json()
print(f"Total noticias en BD: {len(total)}")

resp = requests.get(f"{BASE}/noticias/?skip=0&limit=100")
print(resp.status_code)
data = resp.json()
print(f"Noticias devueltas con el mismo fetch que usa el frontend (limit=100): {len(data)}")

ids = sorted((int(n["id_noticia"]) for n in data), reverse=True)
print(f"ID mas alto incluido: {ids[0] if ids else None}")

ids_totales = sorted(int(n["id_noticia"]) for n in total)
print(f"ID mas alto que existe en BD: {ids_totales[-1] if ids_totales else None}")

if ids and ids_totales and ids[0] == ids_totales[-1]:
    print("[OK] La noticia mas reciente SI esta incluida en el fetch de 100.")
else:
    print("[FALLO] La noticia mas reciente NO esta en el fetch de 100.")

for n in sorted(data, key=lambda n: int(n["id_noticia"]), reverse=True)[:3]:
    print(n["id_noticia"], "|", n["titular"])
