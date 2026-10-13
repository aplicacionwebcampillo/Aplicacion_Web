import requests

BASE = "https://aplicacion-web-m5oa.onrender.com"

A_ELIMINAR = [
    "CELIA MOLINA MORENO",
    "JULIA RUIZ ARANDA",
    "RAQUEL MORENO CIVANTOS",
    "SILVIA MORAL VEGA",
    "MARIA JOSE HOCES ARIAS",
    "ANA FERNANDEZ RAMOS",
]

resp = requests.get(f"{BASE}/jugadores/?skip=0&limit=500")
resp.raise_for_status()
jugadoras_femenino = [j for j in resp.json() if j.get("id_equipo") == 2]

print(f"Total jugadoras femenino actualmente: {len(jugadoras_femenino)}")
nombres_actuales = {j["nombre"] for j in jugadoras_femenino}

for nombre in A_ELIMINAR:
    if nombre not in nombres_actuales:
        print(f"[AVISO] '{nombre}' no esta en la BD (ya se elimino o cambio de nombre), se omite")
        continue
    r = requests.delete(f"{BASE}/jugadores/{nombre}")
    if r.status_code == 200:
        print(f"[OK] Eliminada: {nombre}")
    else:
        print(f"[ERROR] {r.status_code} al eliminar '{nombre}': {r.text}")

resp2 = requests.get(f"{BASE}/jugadores/?skip=0&limit=500")
resp2.raise_for_status()
restantes = [j["nombre"] for j in resp2.json() if j.get("id_equipo") == 2]
print(f"\nJugadoras femenino restantes ({len(restantes)}):")
for n in sorted(restantes):
    print(" -", n)
