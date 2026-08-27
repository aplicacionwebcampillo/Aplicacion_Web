"""Diagnostico puntual: comprobar si el enlace del acta solo aparece con
JavaScript activado. scrape_partidos() usa java_script_enabled=False; si el
enlace se inserta por JS, con JS desactivado nunca lo veriamos (aunque la
RFAF ya lo haya publicado), lo cual explicaria por que el acta de ayer no
se ha capturado pese a estar ya publicada. Se borra tras usarlo."""
import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.web_scrappig.scraper import abrir_pagina_club, BASE_URL
from urllib.parse import urljoin


async def buscar_fila(page):
    """Reproduce procesar_competiciones/procesar_jornada hasta encontrar la
    fila de Arjonilla-Campillo, sin escribir en la BD."""
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")
    tablas = soup.select(".table-bordered")
    primera_tabla = tablas[0]
    for row in primera_tabla.select("tbody tr"):
        cols = row.select("td")
        if len(cols) < 4:
            continue
        categoria = cols[1].get_text(strip=True)
        if "SENIOR" not in categoria.upper():
            continue
        enlace = cols[0].find("a")
        if not (enlace and enlace.has_attr("href")):
            continue
        url_categoria = urljoin(page.url, enlace["href"])
        await page.goto(url_categoria, wait_until="networkidle")
        content_categoria = await page.content()
        soup_categoria = BeautifulSoup(content_categoria, "html.parser")
        tabla_jornadas = soup_categoria.select_one(".table-bordered")
        if not tabla_jornadas:
            continue
        for row2 in tabla_jornadas.select("tbody tr"):
            cols2 = row2.select("td")
            if len(cols2) < 6:
                continue
            enlace_ficha = cols2[5].find("a")
            if not (enlace_ficha and enlace_ficha.has_attr("href")):
                continue
            url_ficha = urljoin(page.url, enlace_ficha["href"])
            await page.goto(url_ficha, wait_until="networkidle")
            await page.wait_for_timeout(1500)
            content_ficha = await page.content()
            soup_ficha = BeautifulSoup(content_ficha, "html.parser")
            for fila in soup_ficha.select("tbody tr"):
                if "arjonilla" in fila.get_text(" ", strip=True).lower():
                    return page.url, fila
    return None, None


async def probar(js_enabled: bool):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=js_enabled)
        page = await context.new_page()
        page.set_default_timeout(120000)
        try:
            await abrir_pagina_club(page, "28701965")
            url, fila = await buscar_fila(page)
        finally:
            await browser.close()
    print(f"\n{'=' * 20} JS enabled={js_enabled} {'=' * 20}", flush=True)
    if fila is None:
        print("  No se encontro la fila de Arjonilla.", flush=True)
        return
    print(f"  url ficha: {url}", flush=True)
    enlaces = fila.find_all("a")
    print(f"  num enlaces <a>: {len(enlaces)}", flush=True)
    for a in enlaces:
        print(f"    <a href={a.get('href')!r}> texto={a.get_text(strip=True)!r}", flush=True)
    print(f"  HTML crudo: {str(fila)[:3000]}", flush=True)


async def main():
    await probar(js_enabled=False)
    await probar(js_enabled=True)


if __name__ == "__main__":
    asyncio.run(main())
