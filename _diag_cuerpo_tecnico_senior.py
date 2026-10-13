"""Diagnostico: muestra como esta guardado el cuerpo tecnico del equipo
senior (id_equipo=1) en la tabla jugador, usando los dorsales reservados
26-30 que el frontend (Plantilla.tsx) traduce a un cargo en vez de un
numero. Tambien comprueba si el dorsal 27 del equipo femenino (usado por
una jugadora real, Maria Jose Moreno Civantos) colisiona con esa misma
convencion."""

import requests
import json

API_BASE = "https://aplicacion-web-m5oa.onrender.com"

CARGOS = {26: "Entrenador", 27: "Segundo Entrenador", 28: "Preparador Fisico", 29: "Entrenador de Porteros", 30: "Delegado de Equipo"}


def main():
    resp = requests.get(f"{API_BASE}/jugadores/?skip=0&limit=500", timeout=30)
    resp.raise_for_status()
    jugadores = resp.json()

    print("[INFO] Cuerpo tecnico actual del equipo SENIOR (id_equipo=1, dorsal 26-30):", flush=True)
    for j in jugadores:
        if j.get("id_equipo") == 1 and j.get("dorsal") in CARGOS:
            print(json.dumps(j, ensure_ascii=False, indent=2), flush=True)

    print("\n[INFO] Jugadoras del FEMENINO con dorsal en el rango reservado 26-30:", flush=True)
    colision = False
    for j in jugadores:
        if j.get("id_equipo") == 2 and j.get("dorsal") in CARGOS:
            colision = True
            print(f"  - {j.get('nombre')} tiene dorsal {j.get('dorsal')} -> se mostraria como '{CARGOS[j.get('dorsal')]}' en vez de su dorsal real", flush=True)
    if not colision:
        print("  (ninguna)", flush=True)


if __name__ == "__main__":
    main()
