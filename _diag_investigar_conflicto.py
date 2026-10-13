import requests

BASE = "https://aplicacion-web-m5oa.onrender.com"

resp = requests.get(f"{BASE}/jugadores/?skip=0&limit=500")
resp.raise_for_status()
jugadores = resp.json()

print("=== Jugadoras femenino (id_equipo=2) con dorsal ===")
femenino = [j for j in jugadores if j.get("id_equipo") == 2]
for j in sorted(femenino, key=lambda j: j.get("dorsal") or 0):
    print(f"dorsal={j.get('dorsal')!s:>4} | {j.get('nombre')!r} | posicion={j.get('posicion')!r} | "
          f"nombre_corto={j.get('nombre_corto')!r} | nombre_completo={j.get('nombre_completo')!r} | "
          f"estado_fichaje={j.get('estado_fichaje')!r} | fecha_nacimiento={j.get('fecha_nacimiento')!r}")

print(f"\nTotal femenino: {len(femenino)}")

print("\n=== Registro completo de MARIA GOMEZ GARRIDO ===")
maria = next((j for j in jugadores if j.get("nombre") == "MARIA GOMEZ GARRIDO"), None)
print(maria)

print("\n=== Buscando 'Bruno' en TODOS los jugadores (cualquier equipo) ===")
for j in jugadores:
    campos = " ".join(str(j.get(k, "")) for k in ("nombre", "nombre_corto", "nombre_completo"))
    if "bruno" in campos.lower():
        print(j)
