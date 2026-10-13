import requests

BASE = "https://aplicacion-web-m5oa.onrender.com"
NOMBRE = "MARIA GOMEZ GARRIDO"

print("=== Antes ===")
antes = requests.get(f"{BASE}/jugadores/{NOMBRE}")
print(antes.status_code, antes.json())

payload = {
    "nombre_corto": None,
    "nombre_completo": None,
    "estado_fichaje": None,
}
r = requests.put(f"{BASE}/jugadores/{NOMBRE}", json=payload)
print("\n=== Resultado PUT ===")
print(r.status_code, r.json())

print("\n=== Despues ===")
despues = requests.get(f"{BASE}/jugadores/{NOMBRE}")
print(despues.status_code, despues.json())
