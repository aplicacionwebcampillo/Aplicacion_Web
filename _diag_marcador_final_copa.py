import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

ACTA_URL = (
    "https://rfaf.es/pnfg/NPcd/NFG_CmpPartido?cod_primaria=1000120"
    "&CodActa=2646254&cod_acta=2646254"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(ACTA_URL, wait_until="networkidle")
        soup = BeautifulSoup(await page.content(), "html.parser")

        print(f"[DIAG] titulo pagina: {await page.title()}", flush=True)
        h5 = soup.find("h5")
        print(f"[DIAG] h5: {h5.get_text(' ', strip=True) if h5 else None}", flush=True)

        texto_completo = soup.get_text(" ", strip=True)
        print(f"[DIAG] primeros 2000 chars de texto (get_text, incluye ocultos): {texto_completo[:2000]!r}", flush=True)

        await browser.close()


asyncio.run(main())
