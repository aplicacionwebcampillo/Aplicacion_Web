"""Acción puntual: primero inspecciona la estructura real de tablas de la
ficha de la final de Copa de la temporada pasada (para confirmar si el
selector de producción `table.table.table-bordered.table-striped.table-hover`
la encuentra), y después ejecuta la extracción real de producción
(procesar_jornada, de scraper.py) contra esa misma ficha, para comprobar de
extremo a extremo que la extracción del acta y el guardado en la BD
funcionan. Se borra tras usarlo."""
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

        tablas = soup.find_all("table")
        print(f"[INFO] Tablas encontradas en la página: {len(tablas)}", flush=True)
        for i, t in enumerate(tablas):
            print(f"  - Tabla {i}: class={t.get('class')} id={t.get('id')} filas={len(t.select('tr'))}", flush=True)

        selector_produccion = soup.select_one("table.table.table-bordered.table-striped.table-hover")
        print(
            f"[INFO] ¿El selector de producción encuentra una tabla? "
            f"{'SÍ' if selector_produccion else 'NO'}",
            flush=True,
        )

        print("[INFO] Ejecutando procesar_jornada (producción) contra la misma URL...", flush=True)
        await procesar_jornada(page, URL_FINAL)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
