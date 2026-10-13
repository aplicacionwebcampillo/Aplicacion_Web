import requests

BASE = "https://aplicacion-web-m5oa.onrender.com"

for categoria in ("Senior", "Femenino_7", "Femenino_11"):
    resp = requests.get(f"{BASE}/resultados/?categoria={categoria}")
    print(f"=== {categoria} ===")
    print(resp.status_code)
    print(resp.json())
    print()
