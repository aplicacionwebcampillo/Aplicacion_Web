"""Acción puntual: corrige el resultado guardado de la final de Copa. El
guardado anterior (1-5) se extrajo con JavaScript deshabilitado de una ficha
cuyo marcador se pinta mediante iconos de fuente ofuscados por JS, así que
era basura. Una captura de pantalla con JS habilitado confirma el resultado
real: 1-1 en el partido, con el Campillo ganando 3-5 en la tanda de
penaltis. Se borra tras usarlo."""
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
    "resultado_visitante": 1,
    "acta": "https://rfaf.es/pnfg/NPcd/NFG_CmpPartido?cod_primaria=1000120&CodActa=2634141&cod_acta=2634141",
}


async def main():
    print(f"[INFO] Guardando: {data}", flush=True)
    await guardar_o_actualizar_partido(data)


if __name__ == "__main__":
    asyncio.run(main())
