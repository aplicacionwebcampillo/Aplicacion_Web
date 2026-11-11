"""Diagnostico: muestra TODOS los partidos de '1a Andaluza Senior (Jaen)'
temporada 2026-2027 (liga actual del primer equipo tras el ascenso),
ordenados por jornada, para ver si el resultado de las ultimas jornadas
ya jugadas esta guardado correctamente en la tabla partido."""

import requests

API_BASE = "https://aplicacion-web-m5oa.onrender.com"


def main():
    resp = requests.get(
        f"{API_BASE}/partidos/",
        params={
            "nombre_competicion": "1ª Andaluza Sénior (Jaén)",
            "temporada_competicion": "Temporada 2026-2027",
        },
        timeout=30,
    )
    print(f"status={resp.status_code}", flush=True)
    partidos = resp.json()
    print(f"{len(partidos)} partidos", flush=True)

    def clave(p):
        try:
            return int(p.get("jornada"))
        except (TypeError, ValueError):
            return 9999

    for p in sorted(partidos, key=clave):
        print(f"  J{p.get('jornada')}: {p.get('local')} {p.get('resultado_local')}-{p.get('resultado_visitante')} {p.get('visitante')} ({p.get('dia')} {p.get('hora')}) acta={p.get('acta')!r}", flush=True)


if __name__ == "__main__":
    main()
