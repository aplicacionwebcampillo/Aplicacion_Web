import asyncio
import re
from urllib.parse import urljoin

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

        print(f"[DIAG] URL tras click Ficha de Competicion: {page.url}", flush=True)

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")
        tablas = soup.select(".table-bordered")
        print(f"[DIAG] tablas en pagina de club: {len(tablas)}", flush=True)

        objetivo_row = None
        for tabla in tablas:
            for row in tabla.select("tbody tr"):
                cols = row.select("td")
                if len(cols) < 4:
                    continue
                nombre_competicion = cols[2].get_text(strip=True)
                print(f"[DIAG] fila club: {[c.get_text(' ', strip=True) for c in cols]}", flush=True)
                if "1" in nombre_competicion.lower() and "andaluza" in nombre_competicion.lower():
                    objetivo_row = row
                    break
            if objetivo_row:
                break

        if objetivo_row is None:
            print("[DIAG] No se encontro fila de 1a Andaluza en ninguna tabla del club", flush=True)
            await browser.close()
            return

        cols = objetivo_row.select("td")
        enlace_clasif = cols[3].find("a") if len(cols) > 3 else None
        if not enlace_clasif or not enlace_clasif.has_attr("href"):
            print("[DIAG] La fila objetivo no tiene enlace en la 4a columna", flush=True)
            await browser.close()
            return

        url_grupo = urljoin(page.url, enlace_clasif["href"])
        print(f"[DIAG] URL grupo (columna 4, la que usa scrape_clasificacion): {url_grupo}", flush=True)

        await page.goto(url_grupo, wait_until="networkidle")
        print(f"[DIAG] URL final tras navegar: {page.url}", flush=True)

        content2 = await page.content()
        soup2 = BeautifulSoup(content2, "html.parser")

        print("[DIAG] === Botones/enlaces .btn en esta pagina ===", flush=True)
        for a in soup2.select("a.btn"):
            print(f"[DIAG] btn: href={a.get('href')!r} texto={a.get_text(strip=True)!r}", flush=True)

        print("[DIAG] === Todos los enlaces con calendario/jornada/partido en href o texto ===", flush=True)
        for a in soup2.find_all("a", href=True):
            href = a["href"]
            texto = a.get_text(strip=True)
            if any(k in href.lower() or k in texto.lower() for k in ["calendario", "jornada", "partido", "resultado"]):
                print(f"[DIAG] enlace: href={href!r} texto={texto!r}", flush=True)

        print(f"[DIAG] URL completa actual para extraer codcompeticion/codgrupo/codtemporada: {page.url}", flush=True)

        await browser.close()


asyncio.run(main())
