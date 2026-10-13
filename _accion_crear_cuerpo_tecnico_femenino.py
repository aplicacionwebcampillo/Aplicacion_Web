"""Accion unica: crea al entrenador del equipo femenino, usando el mismo
patron que el cuerpo tecnico senior (fila en la tabla jugador con un
dorsal reservado que el frontend traduce a un cargo), pero con el rango
reservado propio del femenino (56-60) para no chocar con dorsales reales
de jugadoras (ver Plantilla.tsx / JugadorDetalle.tsx)."""

import requests

API_BASE = "https://aplicacion-web-m5oa.onrender.com"

CUERPO_TECNICO_FEMENINO = [
    {"nombre": "ALVARO MARTINEZ MORAL", "posicion": "Entrenador", "dorsal": 56},
]

ID_EQUIPO_FEMENINO = 2


def main():
    for datos in CUERPO_TECNICO_FEMENINO:
        payload = {
            "nombre": datos["nombre"],
            "id_equipo": ID_EQUIPO_FEMENINO,
            "posicion": datos["posicion"],
            "dorsal": datos["dorsal"],
            "foto": "",
            "biografia": "",
        }
        resp = requests.post(f"{API_BASE}/jugadores/", json=payload, timeout=30)
        if resp.status_code in (200, 201):
            print(f"[OK] Creado {datos['nombre']} ({datos['posicion']}, dorsal {datos['dorsal']})", flush=True)
        else:
            print(f"[ERROR] {resp.status_code} al crear '{datos['nombre']}': {resp.text}", flush=True)

    print("\n[INFO] Cuerpo tecnico + plantilla actual del femenino (id_equipo=2):", flush=True)
    resp = requests.get(f"{API_BASE}/jugadores/?skip=0&limit=500", timeout=30)
    resp.raise_for_status()
    femeninas = sorted(
        [j for j in resp.json() if j.get("id_equipo") == ID_EQUIPO_FEMENINO],
        key=lambda j: j.get("dorsal") or 0,
    )
    for j in femeninas:
        print(f"  - #{j.get('dorsal')} {j.get('nombre')} (posicion='{j.get('posicion')}')", flush=True)


if __name__ == "__main__":
    main()
