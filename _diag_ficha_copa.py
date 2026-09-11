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
        await page.click('a[href*="NFG_VisCompeticiones_Club?cod_primaria=1000123&codclub=28701965&codtemporada="]')
        await page.wait_for_load_state("networkidle")

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")
        primera_tabla = soup.select(".table-bordered")[0]

        fila_copa = None
        for row in primera_tabla.select("tbody tr"):
            cols = row.select("td")
            if len(cols) < 4:
                continue
            if "Trofeo Copa Presidente" in cols[2].get_text(strip=True):
                fila_copa = row
                break

        enlace_equipo = fila_copa.select("td")[0].find("a")
        url_equipo = enlace_equipo["href"]
        from urllib.parse import urljoin
        url_equipo = urljoin(page.url, url_equipo)
        print(f"[DIAG] URL equipo: {url_equipo}", flush=True)

        await page.goto(url_equipo, wait_until="networkidle")
        soup_equipo = BeautifulSoup(await page.content(), "html.parser")
        tabla_jornadas = soup_equipo.select_one(".table-bordered")

        for row_j in tabla_jornadas.select("tbody tr"):
            cols_j = row_j.select("td")
            if len(cols_j) < 6:
                continue
            nombre_fila = cols_j[0].get_text(strip=True)
            print(f"[DIAG] fila equipo: nombre={nombre_fila!r}", flush=True)
            if "Trofeo Copa Presidente" not in nombre_fila:
                continue
            enlace_ficha = cols_j[5].find("a")
            print(f"[DIAG]   enlace_ficha presente: {enlace_ficha is not None}", flush=True)
            if enlace_ficha:
                url_ficha = urljoin(page.url, enlace_ficha["href"])
                print(f"[DIAG]   URL ficha: {url_ficha}", flush=True)

                await page.goto(url_ficha, wait_until="networkidle")
                soup_ficha = BeautifulSoup(await page.content(), "html.parser")
                h5 = soup_ficha.find("h5")
                print(f"[DIAG]   h5 encontrado: {h5}", flush=True)
                print(f"[DIAG]   titulo pagina: {await page.title()}", flush=True)
                print(f"[DIAG]   primeros 500 chars body: {soup_ficha.get_text(' ', strip=True)[:500]!r}", flush=True)

        await browser.close()


asyncio.run(main())
