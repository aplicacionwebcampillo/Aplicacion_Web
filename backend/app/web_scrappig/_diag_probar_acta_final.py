"""Acción puntual: guarda en la BD la final de Copa de la temporada pasada
(C.D. CANENA ATLETICO 1-5 C.D. CAMPILLO DEL RÍO C.F., con acta ya publicada
en la RFAF) usando la función real de producción guardar_o_actualizar_partido
de scraper.py, para comprobar que el enlace de acta se ve en el sitio en
producción.

La ficha de un partido único de la RFAF (NFG_CmpJornada de una final) usa una
plantilla distinta a la de listado de jornada que espera procesar_jornada
(columnas y h5 distintos), así que en vez de forzar esa función se han
extraído a mano los datos, ya confirmados en diagnósticos previos contra la
URL real:
https://www.rfaf.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120&CodCompeticion=48316372&CodGrupo=48316374&CodTemporada=21&CodJornada=6

Se borra tras usarlo."""
import asyncio
import sys

sys.path.insert(0, "backend/app/web_scrappig")

from scraper import guardar_o_actualizar_partido, normalizar_fecha, normalizar_hora  # noqa: E402

data = {
    "nombre_competicion": "Copa Andalucía 1ª Andaluza Sénior (Jaén)",
    "temporada_competicion": "Temporada 2025-2026",
    "local": "C.D. CANENA ATLETICO",
    "visitante": "C.D. CAMPILLO DEL RÍO C.F.",
    "dia": normalizar_fecha("14-06-2026"),
    "hora": normalizar_hora("20:00"),
    "jornada": "Final",
    "resultado_local": 1,
    "resultado_visitante": 5,
    "acta": "https://rfaf.es/pnfg/NPcd/NFG_CmpPartido?cod_primaria=1000120&CodActa=2634141&cod_acta=2634141",
}


async def main():
    print(f"[INFO] Guardando: {data}", flush=True)
    await guardar_o_actualizar_partido(data)


if __name__ == "__main__":
    asyncio.run(main())
