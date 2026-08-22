"""Diagnóstico temporal: confirma que el conflicto de dorsal ya devuelve
un 409 con mensaje claro, tras el fix de DBAPIError."""

import requests

API_BASE = "https://aplicacion-web-m5oa.onrender.com"

resp = requests.post(
    f"{API_BASE}/jugadores/",
    json={
        "nombre": "___TEST_DIAGNOSTICO___",
        "posicion": "Centrocampista",
        "dorsal": 1,
        "id_equipo": 1,
    },
    timeout=30,
)
print(f"[INFO] POST de prueba con dorsal duplicado -> {resp.status_code}", flush=True)
print(f"[INFO] Cuerpo de la respuesta: {resp.text[:500]}", flush=True)
