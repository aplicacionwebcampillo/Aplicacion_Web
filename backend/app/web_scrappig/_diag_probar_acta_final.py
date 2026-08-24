"""Acción puntual: inspecciona fila a fila la tabla de partidos de la ficha
de la final de Copa de la temporada pasada (para entender por qué
procesar_jornada revienta con IndexError al extraer equipos_info), y luego
ejecuta la extracción real de producción (procesar_jornada, de scraper.py)
contra esa misma ficha. Se borra tras usarlo."""
import asyncio
import sys

sys.path.insert(0, "backend/app/web_scrappig")

from bs4 import BeautifulSoup  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402
from scraper import procesar_jornada  # noqa: E402

URL_FINAL = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_CmpJornada"
    "?cod_primaria=1000120&CodCompeticion=48316372&CodGrupo=48316374"
    "&CodTemporada=21&CodJornada=6"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(
            headless=True,
            args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
            timeout=60000,
        )
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        print("[INFO] Cargando página para inspección previa...", flush=True)
        await page.goto(URL_FINAL, wait_until="load")
        await page.wait_for_timeout(3000)
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        tabla_partidos = soup.select_one("table.table-bordered.table-striped")
        for i, row in enumerate(tabla_partidos.select("tbody tr")):
            columnas = row.select("td")
            print(f"[FILA {i}] num_columnas={len(columnas)}", flush=True)
            for j, col in enumerate(columnas):
                print(f"    col[{j}] stripped_strings={list(col.stripped_strings)!r}", flush=True)
            if not columnas:
                print(f"    (fila sin <td>) html={row!s}"[:600], flush=True)

        print("[INFO] Ejecutando procesar_jornada (producción) contra la misma URL...", flush=True)
        try:
            await procesar_jornada(page, URL_FINAL)
        except Exception as e:
            print(f"[ERROR] procesar_jornada falló: {e!r}", flush=True)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
