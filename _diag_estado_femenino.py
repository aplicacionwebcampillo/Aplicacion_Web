import requests

BASE = "https://aplicacion-web-m5oa.onrender.com"


def get(path):
    resp = requests.get(f"{BASE}{path}")
    try:
        return resp.status_code, resp.json()
    except Exception:
        return resp.status_code, resp.text


print("=== /competiciones/ ===")
status, data = get("/competiciones/?limit=500")
print(status)
if isinstance(data, list):
    print(f"Total: {len(data)}")
    for c in data:
        print(c)
else:
    print(data)

print("\n=== /jugadores/ (buscando id_equipo != 1) ===")
status, data = get("/jugadores/")
print(status)
if isinstance(data, list):
    from collections import Counter
    conteo = Counter(j.get("id_equipo") for j in data)
    print(f"Total jugadores: {len(data)}, por id_equipo: {dict(conteo)}")
    for j in data:
        if j.get("id_equipo") != 1:
            print(j)
else:
    print(data)
