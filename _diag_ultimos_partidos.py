"""Diagnostico: muestra los partidos mas recientes guardados en la BD
(tabla partido) para cada categoria, y tambien el contenido actual de la
tabla resultados (usada por 'Resultados - Ultima Jornada' en el
frontend), para comparar con lo que deberia mostrarse."""

import requests
from collections import defaultdict

API_BASE = "https://aplicacion-web-m5oa.onrender.com"


def main():
    resp = requests.get(f"{API_BASE}/partidos/?skip=0&limit=1000", timeout=30)
    print(f"[INFO] /partidos/ status={resp.status_code}", flush=True)
    if resp.status_code == 200:
        partidos = resp.json()
        print(f"[INFO] {len(partidos)} partidos en total", flush=True)
        por_categoria = defaultdict(list)
        for p in partidos:
            por_categoria[p.get("nombre_competicion")].append(p)
        for cat, lst in por_categoria.items():
            print(f"\n[CATEGORIA] {cat} ({len(lst)} partidos)", flush=True)
            def clave(p):
                return p.get("dia") or ""
            lst_ordenado = sorted(lst, key=clave)
            for p in lst_ordenado[-6:]:
                print(f"  {p}", flush=True)
    else:
        print(resp.text[:2000], flush=True)

    print("\n\n[INFO] Probando otras rutas conocidas...", flush=True)
    for categoria in ["Senior", "Femenino_7", "Femenino_11"]:
        r = requests.get(f"{API_BASE}/resultados/?categoria={categoria}", timeout=30)
        print(f"\n[RESULTADOS] categoria={categoria} status={r.status_code}", flush=True)
        print(f"  {r.text[:2000]}", flush=True)


if __name__ == "__main__":
    main()
