import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL_JORNADA2 = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"
    "&CodCompeticion=48466094&CodGrupo=48466095&CodTemporada=22&CodJornada=2"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(URL_JORNADA2, wait_until="networkidle")
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        for fila in soup.find_all("tr"):
            celdas = fila.select("td")
            if len(celdas) != 3:
                continue
            texto = fila.get_text(" ", strip=True)
            if "campillo" in texto.lower():
                print("[DIAG] fila cruda Campillo jornada 2:", flush=True)
                print(str(fila)[:4000], flush=True)

        await browser.close()


asyncio.run(main())
