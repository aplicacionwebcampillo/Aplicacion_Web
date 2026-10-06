import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

CODIGO_EQUIPO_FEM = "32996393"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        url = f"https://www.rfaf.es/pnfg/NPcd/NFG_VisEquipos?cod_primaria=1000119&Codigo_Equipo={CODIGO_EQUIPO_FEM}"
        await page.goto(url, wait_until="networkidle")
        print(f"[DIAG] Titulo pagina equipo femenino: {await page.title()}", flush=True)

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        tabla = soup.select_one(".table-bordered")
        if not tabla:
            print("[DIAG] No se encontro tabla de competiciones en la pagina del equipo", flush=True)
        else:
            for row in tabla.select("tbody tr"):
                cols = row.select("td")
                print(f"[DIAG] fila equipo (n={len(cols)}): {[c.get_text(strip=True) for c in cols]}", flush=True)
                if len(cols) >= 6:
                    enlace_ficha = cols[5].find("a")
                    print(f"[DIAG]   enlace ficha (col 5): {enlace_ficha.get('href') if enlace_ficha else None}", flush=True)
                if cols:
                    enlace_comp = cols[0].find("a")
                    print(f"[DIAG]   enlace competicion (col 0): {enlace_comp.get('href') if enlace_comp else None}", flush=True)

        await browser.close()


asyncio.run(main())
