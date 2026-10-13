import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL = "https://www.rfaf.es/pnfg/NPcd/NFG_VisEquipos?cod_primaria=1000119&Codigo_Equipo=32996393"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(URL, wait_until="networkidle")
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        tablas = soup.select(".table-bordered")
        tabla_jugadoras = tablas[0]

        print("[DIAG] HTML completo de la tabla de jugadoras:", flush=True)
        print(str(tabla_jugadoras)[:6000], flush=True)

        # Tambien volcar el contexto alrededor de la tabla (titulo/cabecera)
        print("\n[DIAG] --- Elemento anterior a la tabla (posible titulo) ---", flush=True)
        anterior = tabla_jugadoras.find_previous(["h3", "h4", "h5", "strong", "b"])
        print(str(anterior)[:500] if anterior else None, flush=True)

        await browser.close()


asyncio.run(main())
