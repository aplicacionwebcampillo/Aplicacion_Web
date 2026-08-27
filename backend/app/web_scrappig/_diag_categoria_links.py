"""Diagnostico puntual: reproducir la navegacion real (abrir_pagina_club ->
categoria "1a ANDALUZA SENIOR") y volcar TODOS los enlaces de CADA columna
de la fila de esa categoria (no solo el que ya usamos), para ver si hay un
enlace hermano que ya lleve directamente a NFG_CmpJornada con todos los
parametros (CodCompeticion, CodGrupo, CodTemporada, CodJornada). Se borra
tras usarlo."""
import asyncio
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.web_scrappig.scraper import abrir_pagina_club


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(60000)
        try:
            await abrir_pagina_club(page, "28701965")
            print(f"URL tras abrir_pagina_club: {page.url}", flush=True)
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
                print(f"\n{'=' * 20} Categoria: {categoria!r} {'=' * 20}", flush=True)
                print(f"URL categoria: {url_categoria}", flush=True)

                await page.goto(url_categoria, wait_until="networkidle")
                content2 = await page.content()
                soup2 = BeautifulSoup(content2, "html.parser")
                tabla_jornadas = soup2.select_one(".table-bordered")
                if not tabla_jornadas:
                    print("  No se encontro tabla de jornadas.", flush=True)
                    continue
                for row2 in tabla_jornadas.select("tbody tr"):
                    cols2 = row2.select("td")
                    if len(cols2) < 6:
                        continue
                    print(f"  Fila con {len(cols2)} columnas:", flush=True)
                    for i, c in enumerate(cols2):
                        enlaces = c.find_all("a", href=True)
                        for a in enlaces:
                            full = urljoin(page.url, a["href"])
                            print(f"    col[{i}] href={a['href']!r} -> {full}", flush=True)
                break  # solo la primera categoria SENIOR, para no tardar
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
