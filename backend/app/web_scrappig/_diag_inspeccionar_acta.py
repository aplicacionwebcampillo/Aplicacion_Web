"""Diagnóstico puntual: navega la RFAF igual que scraper.py hasta la ficha
de una jornada, y vuelca el HTML crudo de la fila de un partido ya jugado
(con resultado), para localizar el enlace/icono de la ficha del partido
(acta). Se borra después de usarlo."""
import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

CODIGO_CLUB = "28701965"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(
            headless=True,
            args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
            timeout=60000,
        )
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        url = f"https://www.rfaf.es/pnfg/NPcd/NFG_VerClub?cod_primaria=1000118&codigo_club={CODIGO_CLUB}"
        print(f"[INFO] Abriendo {url}", flush=True)
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_load_state("networkidle")

        await page.click(
            'a[href*="NFG_VisCompeticiones_Club?cod_primaria=1000123&codclub=28701965&codtemporada="]'
        )
        await page.wait_for_load_state("networkidle")

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")
        primera_tabla = soup.select_one(".table-bordered")
        if not primera_tabla:
            print("[ERROR] No se encontró la tabla de competiciones", flush=True)
            await browser.close()
            return

        # Coge la primera competición con un enlace válido.
        fila_competicion = None
        for row in primera_tabla.select("tbody tr"):
            cols = row.select("td")
            if len(cols) >= 4 and cols[0].find("a"):
                fila_competicion = row
                break

        if not fila_competicion:
            print("[ERROR] No se encontró ninguna competición con enlace", flush=True)
            await browser.close()
            return

        categoria = fila_competicion.select("td")[1].get_text(strip=True)
        enlace = fila_competicion.select("td")[0].find("a")
        from urllib.parse import urljoin

        url_categoria = urljoin(page.url, enlace["href"])
        print(f"[INFO] Categoría: {categoria} -> {url_categoria}", flush=True)
        await page.goto(url_categoria, wait_until="networkidle")

        content_categoria = await page.content()
        soup_categoria = BeautifulSoup(content_categoria, "html.parser")
        tabla_jornadas = soup_categoria.select_one(".table-bordered")
        if not tabla_jornadas:
            print("[ERROR] No se encontró tabla de jornadas", flush=True)
            await browser.close()
            return

        # Busca una jornada YA JUGADA (normalmente las primeras filas son las
        # más recientes/pasadas); prueba varias hasta encontrar un resultado.
        filas_jornada = [
            row for row in tabla_jornadas.select("tbody tr") if len(row.select("td")) >= 6
        ]
        print(f"[INFO] {len(filas_jornada)} jornadas encontradas", flush=True)

        for row in filas_jornada[:5]:
            cols = row.select("td")
            enlace_ficha = cols[5].find("a")
            if not (enlace_ficha and enlace_ficha.has_attr("href")):
                continue
            url_ficha = urljoin(page.url, enlace_ficha["href"])
            print(f"[INFO] Probando ficha de jornada: {url_ficha}", flush=True)
            await page.goto(url_ficha, wait_until="networkidle")
            content_jornada = await page.content()
            soup_jornada = BeautifulSoup(content_jornada, "html.parser")
            tabla_partidos = soup_jornada.select_one(
                "table.table.table-bordered.table-striped.table-hover"
            )
            if not tabla_partidos:
                print("[AVISO] Sin tabla de partidos en esta jornada", flush=True)
                continue

            for fila_partido in tabla_partidos.select("tbody tr"):
                columnas = fila_partido.select("td")
                if len(columnas) < 3:
                    continue
                resultado_info = columnas[2].find_all("b")
                if len(resultado_info) >= 2:
                    print("[INFO] Fila de partido CON resultado encontrada:", flush=True)
                    print(f"[INFO] Número total de columnas (td): {len(columnas)}", flush=True)
                    for i, col in enumerate(columnas):
                        print(f"--- columna {i} ---", flush=True)
                        print(col.prettify()[:1500], flush=True)
                    await browser.close()
                    return

        print("[AVISO] No se encontró ninguna fila con resultado en las jornadas probadas", flush=True)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
