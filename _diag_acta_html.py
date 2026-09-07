import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL_ACTA = (
    "https://rfaf.es/pnfg/NPcd/NFG_CmpPartido?cod_primaria=1000120"
    "&CodActa=2666060&cod_acta=2666060"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(URL_ACTA, wait_until="networkidle")
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        h2 = soup.select_one("h2.ntype")
        print(f"[DIAG] h2 HTML crudo:\n{h2}", flush=True)

        # Contexto mas amplio: el contenedor padre
        contenedor = h2.parent
        print(f"[DIAG] contenedor padre HTML crudo:\n{contenedor}", flush=True)

        await browser.close()


asyncio.run(main())
