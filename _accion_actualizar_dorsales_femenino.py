"""Accion unica: actualiza los dorsales de 9 jugadoras existentes y crea 4
jugadoras nuevas del equipo femenino (id_equipo=2), segun los dorsales reales
vistos en la alineacion de lapreferente.com que aporto el usuario.

Antes de tocar nada, imprime los dorsales actuales de TODOS los equipos para
comprobar que no hay colision con el nuevo conjunto de dorsales (por si el
trigger validar_dorsal_unico fuese global y no por equipo).
"""

import requests

API_BASE = "https://aplicacion-web-m5oa.onrender.com"

ACTUALIZACIONES = [
    ("ALMUDENA MARTIN SIERRA", 16),
    ("MARIA JIMENEZ LOPEZ", 8),
    ("OMAYMA FAGROUCH FAGROUCH", 4),
    ("YADIRA VANESSA SOTAMINGA CLAVON", 20),
    ("MARIA JOSE MORENO CIVANTOS", 27),
    ("MARIA DEL MAR CUEVAS CEACERO", 23),
    ("MARIA GOMEZ GARRIDO", 2),
    ("ANA DE AMO PEREZ", 7),
    ("SORAYA CASTILLO LOPEZ", 24),
]

NUEVAS = [
    {"nombre": "JIMENA CAMPOS PUJAZON", "dorsal": 11},
    {"nombre": "SILVIA ARANDA RODRIGUEZ", "dorsal": 12},
    {"nombre": "LOURDES MUÑOZ MORENO", "dorsal": 25},
    {"nombre": "AURORA PADILLA COETO", "dorsal": 22},
]

ID_EQUIPO_FEMENINO = 2


def main():
    print("[INFO] Comprobando dorsales actuales de TODOS los equipos...", flush=True)
    resp = requests.get(f"{API_BASE}/jugadores/?skip=0&limit=500", timeout=30)
    resp.raise_for_status()
    jugadores = resp.json()

    nuevos_dorsales = {d for _, d in ACTUALIZACIONES} | {j["dorsal"] for j in NUEVAS}
    nombres_actualizar = {n for n, _ in ACTUALIZACIONES}

    colisiones = [
        j for j in jugadores
        if j.get("dorsal") in nuevos_dorsales and j.get("nombre") not in nombres_actualizar
    ]
    if colisiones:
        print("[AVISO] Colisiones de dorsal detectadas con jugadores que NO se van a tocar:", flush=True)
        for j in colisiones:
            print(f"  - {j.get('nombre')} (id_equipo={j.get('id_equipo')}, dorsal={j.get('dorsal')})", flush=True)
        print("[ABORTAR] No se realiza ninguna actualizacion por seguridad.", flush=True)
        return
    else:
        print("[OK] No hay colisiones de dorsal con otros jugadores.", flush=True)

    print("\n[INFO] Actualizando dorsales de 9 jugadoras existentes...", flush=True)
    for nombre, dorsal in ACTUALIZACIONES:
        resp = requests.put(f"{API_BASE}/jugadores/{nombre}", json={"dorsal": dorsal}, timeout=30)
        if resp.status_code == 200:
            print(f"[OK] {nombre} -> dorsal {dorsal}", flush=True)
        else:
            print(f"[ERROR] {resp.status_code} al actualizar '{nombre}': {resp.text}", flush=True)

    print("\n[INFO] Creando 4 jugadoras nuevas...", flush=True)
    for datos in NUEVAS:
        payload = {
            "nombre": datos["nombre"],
            "id_equipo": ID_EQUIPO_FEMENINO,
            "posicion": "",
            "dorsal": datos["dorsal"],
        }
        resp = requests.post(f"{API_BASE}/jugadores/", json=payload, timeout=30)
        if resp.status_code in (200, 201):
            print(f"[OK] Creada {datos['nombre']} con dorsal {datos['dorsal']}", flush=True)
        else:
            print(f"[ERROR] {resp.status_code} al crear '{datos['nombre']}': {resp.text}", flush=True)

    print("\n[INFO] Estado final del equipo femenino (id_equipo=2):", flush=True)
    resp = requests.get(f"{API_BASE}/jugadores/?skip=0&limit=500", timeout=30)
    resp.raise_for_status()
    femeninas = sorted(
        [j for j in resp.json() if j.get("id_equipo") == ID_EQUIPO_FEMENINO],
        key=lambda j: j.get("dorsal") or 0,
    )
    for j in femeninas:
        print(f"  - #{j.get('dorsal')} {j.get('nombre')} (posicion='{j.get('posicion')}')", flush=True)
    print(f"\n[FIN] Total jugadoras femenino: {len(femeninas)}", flush=True)


if __name__ == "__main__":
    main()
