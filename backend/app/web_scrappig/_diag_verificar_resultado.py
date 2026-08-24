"""Acción puntual: el usuario dice que el resultado guardado para la final
(C.D. CANENA ATLETICO 1-5 C.D. CAMPILLO DEL RÍO C.F.) no es correcto.
Vuelca el HTML crudo de la celda de resultado de la ficha real para
verificar cuál es el marcador correcto, en vez de fiarnos del orden de
stripped_strings. Se borra tras usarlo."""
import asyncio
import sys

sys.path.insert(0, "backend/app/web_scrappig")

from bs4 import BeautifulSoup  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

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

        await page.goto(URL_FINAL, wait_until="load")
        await page.wait_for_timeout(3000)
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        tabla_partidos = soup.select_one("table.table-bordered.table-striped")
        filas = tabla_partidos.select("tbody tr")
        # FILA 1 (índice 1) es la fila de datos real: local | resultado | visitante
        fila_datos = filas[1]
        columnas = fila_datos.select("td")
        print(f"[INFO] num columnas fila de datos: {len(columnas)}", flush=True)
        for i, col in enumerate(columnas):
            print(f"--- col[{i}] HTML crudo ---", flush=True)
            print(str(col), flush=True)
            print(f"--- col[{i}] texto ---", flush=True)
            print(col.get_text(" | ", strip=True), flush=True)

        # También el texto completo visible de toda la fila 0 (el contenedor),
        # tal y como lo vería un humano en la página, para contexto.
        print("[INFO] Texto completo visible de la ficha (todas las filas):", flush=True)
        print(tabla_partidos.get_text(" | ", strip=True), flush=True)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
