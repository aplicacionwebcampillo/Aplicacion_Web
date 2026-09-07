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

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")
        tablas = soup.select(".table-bordered")
        print(f"[DIAG] tablas en pagina de club: {len(tablas)}", flush=True)
        primera_tabla = tablas[0]

        objetivo = None
        for row in primera_tabla.select("tbody tr"):
            cols = row.select("td")
            if len(cols) < 4:
                continue
            categoria = cols[1].get_text(strip=True)
            print(f"[DIAG] categoria fila: {categoria!r}", flush=True)
            if "andaluza" in categoria.lower() and "1" in categoria:
                objetivo = row
                break

        if objetivo is None:
            print("[DIAG] No se encontro fila de 1a Andaluza", flush=True)
            await browser.close()
            return

        cols = objetivo.select("td")
        enlace = cols[0].find("a")
        url_categoria = urljoin(page.url, enlace["href"])
        print(f"[DIAG] URL categoria 1a Andaluza: {url_categoria}", flush=True)

        await page.goto(url_categoria, wait_until="networkidle")
        content_cat = await page.content()
        soup_cat = BeautifulSoup(content_cat, "html.parser")

        tablas_cat = soup_cat.select(".table-bordered")
        print(f"[DIAG] tablas .table-bordered en pagina categoria: {len(tablas_cat)}", flush=True)

        for i, tabla in enumerate(tablas_cat):
            filas = tabla.select("tbody tr")
            texto_tabla = tabla.get_text(" ", strip=True)[:150]
            contiene_linares = "linares" in tabla.get_text(" ", strip=True).lower()
            print(f"[DIAG] tabla #{i}: {len(filas)} filas, contiene_linares={contiene_linares}, preview={texto_tabla!r}", flush=True)

        # Dump completo de la tabla que el codigo actual usa (la primera)
        print("[DIAG] === Contenido tabla #0 (la que usa procesar_competiciones) ===", flush=True)
        for row in tablas_cat[0].select("tbody tr"):
            cols = row.select("td")
            textos = [c.get_text(" ", strip=True) for c in cols]
            print(f"[DIAG] fila: {textos}", flush=True)

        # Buscar cualquier enlace en toda la pagina que apunte a NFG_CmpJornada o similar
        print("[DIAG] === Enlaces relevantes en la pagina de categoria ===", flush=True)
        for a in soup_cat.find_all("a", href=True):
            href = a["href"]
            if "jornada" in href.lower() or "calendario" in href.lower() or "cmppartido" in href.lower():
                print(f"[DIAG] enlace: {href} texto={a.get_text(strip=True)!r}", flush=True)

        await browser.close()


asyncio.run(main())
