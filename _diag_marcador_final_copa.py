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

        texto_completo = soup.get_text(" ", strip=True)
        idx = texto_completo.find("NAVAS")
        print(f"[DIAG] indice 'NAVAS' en texto: {idx}", flush=True)
        print(f"[DIAG] contexto alrededor de NAVAS: {texto_completo[max(0, idx-200):idx+800]!r}", flush=True)

        # También buscar cualquier tabla/celda con clase relacionada al marcador
        for tag in soup.select("[class*=resultado], [class*=marcador], .fa-solid"):
            print(f"[DIAG] elemento relevante: <{tag.name} class={tag.get('class')}> texto={tag.get_text(' ', strip=True)!r}", flush=True)

        await browser.close()


asyncio.run(main())
