"""Diagnóstico temporal: ¿está el backend en Render ejecutando el código
más reciente? Comprueba si la respuesta de /jugadores/ ya incluye los
campos nuevos (nombre_corto, estado_fichaje...) y si un conflicto de
dorsal ya da el mensaje claro (409) en vez del 500 genérico antiguo."""

import requests

API_BASE = "https://aplicacion-web-m5oa.onrender.com"

resp = requests.get(f"{API_BASE}/jugadores/?skip=0&limit=1", timeout=30)
print(f"[INFO] GET /jugadores/?limit=1 -> {resp.status_code}", flush=True)
if resp.status_code == 200:
    datos = resp.json()
    if datos:
        claves = sorted(datos[0].keys())
        print(f"[INFO] Claves del primer jugador: {claves}", flush=True)
        print(f"[INFO] ¿Tiene 'nombre_corto'?: {'nombre_corto' in datos[0]}", flush=True)
        print(f"[INFO] ¿Tiene 'estado_fichaje'?: {'estado_fichaje' in datos[0]}", flush=True)
    else:
        print("[AVISO] La lista de jugadores está vacía", flush=True)

# Provocamos a propósito un conflicto de dorsal (dorsal 1, que ya existe)
# para ver si el backend ya devuelve el 409 con mensaje claro, o el 500
# genérico antiguo.
resp2 = requests.post(
    f"{API_BASE}/jugadores/",
    json={
        "nombre": "___TEST_DIAGNOSTICO___",
        "posicion": "Centrocampista",
        "dorsal": 1,
        "id_equipo": 1,
    },
    timeout=30,
)
print(f"\n[INFO] POST de prueba con dorsal duplicado -> {resp2.status_code}", flush=True)
print(f"[INFO] Cuerpo de la respuesta: {resp2.text[:500]}", flush=True)
