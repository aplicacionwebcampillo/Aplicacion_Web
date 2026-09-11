import requests

resp = requests.get("https://aplicacion-web-m5oa.onrender.com/jugadores/?skip=0&limit=500")
print(resp.status_code)
jugadores = resp.json()
porteros = [j for j in jugadores if "portero" in (j.get("posicion") or "").lower()]
print(f"Porteros encontrados: {len(porteros)}")
for j in porteros:
    print(f"  {j.get('nombre')!r} posicion={j.get('posicion')!r} goles={j.get('goles')} id_equipo={j.get('id_equipo')}")
