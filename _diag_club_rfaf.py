import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

CODIGO_CLUB = "28701965"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        url = f"https://www.rfaf.es/pnfg/NPcd/NFG_VerClub?cod_primaria=1000118&codigo_club={CODIGO_CLUB}"
        await page.goto(url, wait_until="networkidle")

        print(f"[DIAG] Titulo pagina club: {await page.title()}", flush=True)
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        # Dump de todos los enlaces de la pagina del club para ver que
        # secciones/equipos distintos ofrece (masculino, femenino, etc.)
        print("[DIAG] --- Enlaces en la pagina del club ---", flush=True)
        vistos = set()
        for a in soup.find_all("a", href=True):
            texto = a.get_text(strip=True)
            href = a["href"]
            clave = (texto, href)
            if texto and clave not in vistos:
                vistos.add(clave)
                print(f"[DIAG] enlace: texto={texto!r} href={href!r}", flush=True)

        await page.click('a[href*="NFG_VisCompeticiones_Club?cod_primaria=1000123&codclub=28701965&codtemporada="]')
        await page.wait_for_load_state("networkidle")

        content2 = await page.content()
        soup2 = BeautifulSoup(content2, "html.parser")

        print("[DIAG] --- Todas las competiciones listadas (todas las tablas) ---", flush=True)
        for i, table in enumerate(soup2.select(".table-bordered")):
            rows = table.select("tbody tr")
            print(f"[DIAG] tabla #{i} con {len(rows)} filas", flush=True)
            for row in rows:
                cols = row.select("td")
                if len(cols) < 3:
                    continue
                print(f"[DIAG]   fila: {[c.get_text(strip=True) for c in cols]}", flush=True)

        await browser.close()


asyncio.run(main())
