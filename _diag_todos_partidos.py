import requests

resp = requests.get("https://aplicacion-web-m5oa.onrender.com/partidos/?skip=0&limit=1000")
print(resp.status_code)
partidos = resp.json()
campillo = [p for p in partidos if "campillo" in (p.get("local","")+p.get("visitante","")).lower()]
print(f"Total partidos Campillo: {len(campillo)}")
por_competicion = {}
for p in campillo:
    por_competicion.setdefault(p.get("nombre_competicion"), []).append(p)

for comp, lista in por_competicion.items():
    print(f"\n=== {comp} ({len(lista)} partidos) ===")
    for p in sorted(lista, key=lambda x: (x.get("dia") or "9999")):
        print(f"  jornada={p.get('jornada')!r} dia={p.get('dia')} hora={p.get('hora')} {p.get('local')} vs {p.get('visitante')} res={p.get('resultado_local')}-{p.get('resultado_visitante')} acta={'SI' if (p.get('acta') or '').strip() else 'NO'}")
