import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL_JORNADA = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"
    "&CodCompeticion=48466094&CodGrupo=48466095&CodTemporada=22&CodJornada=1"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(URL_JORNADA, wait_until="networkidle")
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        tabla = soup.select_one("table.table-bordered.table-striped")
        filas = tabla.select("tr")
        print(f"[DIAG] total filas <tr> (no solo tbody): {len(filas)}", flush=True)

        for i, fila in enumerate(filas):
            texto = fila.get_text(" ", strip=True)
            if "campillo" in texto.lower():
                print(f"[DIAG] === fila #{i} con campillo, HTML crudo ===", flush=True)
                print(str(fila)[:3000], flush=True)

        await browser.close()


asyncio.run(main())
