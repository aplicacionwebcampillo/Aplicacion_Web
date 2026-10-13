"""Diagnostico: comprueba si YA existen dorsales repetidos entre distintos
equipos en la BD actual. Si los hay, confirma que validar_dorsal_unico es
por equipo (no global), y entonces es seguro ignorar colisiones con el
equipo senior (id_equipo=1) al actualizar el femenino (id_equipo=2)."""

import requests
from collections import defaultdict

API_BASE = "https://aplicacion-web-m5oa.onrender.com"


def main():
    resp = requests.get(f"{API_BASE}/jugadores/?skip=0&limit=500", timeout=30)
    resp.raise_for_status()
    jugadores = resp.json()

    por_dorsal = defaultdict(list)
    for j in jugadores:
        por_dorsal[j.get("dorsal")].append((j.get("id_equipo"), j.get("nombre")))

    repetidos_entre_equipos = {
        d: entradas for d, entradas in por_dorsal.items()
        if len({e[0] for e in entradas}) > 1
    }

    if repetidos_entre_equipos:
        print("[CONFIRMADO] Hay dorsales repetidos ENTRE equipos distintos ya en la BD:", flush=True)
        for d, entradas in sorted(repetidos_entre_equipos.items()):
            print(f"  dorsal {d}: {entradas}", flush=True)
        print("\n=> El trigger validar_dorsal_unico es POR EQUIPO, no global.", flush=True)
    else:
        print("[AVISO] No hay dorsales repetidos entre equipos distintos actualmente.", flush=True)
        print("No se puede confirmar si el trigger es global o por equipo solo con esto.", flush=True)

    # Intento directo: probamos a crear un jugador de prueba con un dorsal
    # que YA usa el equipo senior pero en el equipo femenino, y vemos si el
    # servidor lo rechaza o lo acepta (lo borramos despues si se crea).
    print("\n[INFO] Probando si el equipo femenino puede usar un dorsal ya usado en el senior...", flush=True)
    dorsal_prueba = 4  # usado por ENRIQUE RODRIGUEZ RUIZ en id_equipo=1
    nombre_prueba = "ZZZ JUGADOR PRUEBA TEMPORAL"
    payload = {"nombre": nombre_prueba, "id_equipo": 2, "posicion": "", "dorsal": dorsal_prueba}
    resp = requests.post(f"{API_BASE}/jugadores/", json=payload, timeout=30)
    if resp.status_code in (200, 201):
        print(f"[OK] Se permite: dorsal {dorsal_prueba} coexiste en equipo 1 y equipo 2 (trigger por equipo).", flush=True)
        # limpiar
        del_resp = requests.delete(f"{API_BASE}/jugadores/{nombre_prueba}", timeout=30)
        print(f"[INFO] Jugador de prueba eliminado (status {del_resp.status_code}).", flush=True)
    else:
        print(f"[BLOQUEADO] status {resp.status_code}: {resp.text}", flush=True)
        print("=> El trigger validar_dorsal_unico parece ser GLOBAL.", flush=True)


if __name__ == "__main__":
    main()
