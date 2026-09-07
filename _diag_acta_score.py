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

        texto = soup.get_text(" ", strip=True)
        idx = texto.lower().find("campillo")
        print(f"[DIAG] texto alrededor de 'campillo': {texto[max(0,idx-200):idx+400]}", flush=True)

        # Buscar cualquier cosa con clase relacionada a resultado
        for el in soup.select("[class*=resultado], [class*=marcador], h2, h1, .fa-solid"):
            print(f"[DIAG] elemento: tag={el.name} clase={el.get('class')} texto={el.get_text(' ', strip=True)!r}", flush=True)

        await browser.close()


asyncio.run(main())
