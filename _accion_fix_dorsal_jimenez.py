import requests

API_BASE = "https://aplicacion-web-m5oa.onrender.com"
NOMBRE = "MARIA JIMÉNEZ LÓPEZ"
DORSAL = 8

resp = requests.put(f"{API_BASE}/jugadores/{NOMBRE}", json={"dorsal": DORSAL}, timeout=30)
print(f"status={resp.status_code} body={resp.text}", flush=True)
