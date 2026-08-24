"""Diagnóstico puntual: lista la plantilla actual (equipo 1) tal cual está
guardada en la BD, para confirmar nombres exactos antes de crear/borrar/
actualizar registros a mano. Se borra después de usarlo."""
import requests

API_BASE = "https://aplicacion-web-m5oa.onrender.com"

resp = requests.get(f"{API_BASE}/jugadores/?skip=0&limit=200", timeout=30)
print(f"[INFO] GET /jugadores/ -> {resp.status_code}", flush=True)
jugadores = resp.json()
jugadores_equipo1 = [j for j in jugadores if j.get("id_equipo") == 1]
jugadores_equipo1.sort(key=lambda j: (j.get("dorsal") is None, j.get("dorsal")))
for j in jugadores_equipo1:
    print(
        f"dorsal={j.get('dorsal')!r} nombre={j.get('nombre')!r} "
        f"posicion={j.get('posicion')!r} fecha_nacimiento={j.get('fecha_nacimiento')!r}",
        flush=True,
    )
print(f"[INFO] Total equipo 1: {len(jugadores_equipo1)}", flush=True)
