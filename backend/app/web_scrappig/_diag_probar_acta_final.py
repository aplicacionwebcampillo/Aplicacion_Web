"""Acción puntual: el partido de la final de Copa (C.D. CANENA ATLETICO 1-5
C.D. CAMPILLO DEL RÍO C.F., 14-06-2026) ya existía en la BD bajo la
competición real "Fase Final Trofeo Copa Subdelegado del Gobierno (Jaén)"
(no "Copa Andalucía" como se supuso al principio), con acta=" " sin
completar todavía. Este script solo actualiza ese registro existente con el
enlace real al acta, usando la función de producción
guardar_o_actualizar_partido de scraper.py. Se borra tras usarlo."""
import asyncio
import sys

sys.path.insert(0, "backend/app/web_scrappig")

from scraper import guardar_o_actualizar_partido  # noqa: E402

data = {
    "nombre_competicion": "Fase Final Trofeo Copa Subdelegado del Gobierno (Jaén)",
    "temporada_competicion": "Temporada 2025-2026",
    "local": "C.D. CANENA ATLETICO",
    "visitante": "C.D. CAMPILLO DEL RÍO C.F.",
    "dia": "2026-06-14",
    "hora": "20:00:00",
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
