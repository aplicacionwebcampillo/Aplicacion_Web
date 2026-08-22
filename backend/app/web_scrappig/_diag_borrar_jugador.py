"""Acción puntual (no diagnóstico permanente): borra a un jugador que ya
no está en el club, indicado explícitamente por el club."""

import requests

API_BASE = "https://aplicacion-web-m5oa.onrender.com"
NOMBRE = "JUAN FRANCISCO MORAL MORENO"

resp = requests.delete(f"{API_BASE}/jugadores/{NOMBRE}", timeout=30)
print(f"[INFO] DELETE /jugadores/{NOMBRE} -> {resp.status_code}", flush=True)
print(f"[INFO] cuerpo: {resp.text[:500]}", flush=True)
