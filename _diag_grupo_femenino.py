import asyncio
import re

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from urllib.parse import urljoin

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

        soup = BeautifulSoup(await page.content(), "html.parser")
        tabla = soup.select(".table-bordered")[0]

        fila_femenino = None
        for row in tabla.select("tbody tr"):
            cols = row.select("td")
            if len(cols) < 4:
                continue
            if "femenina" in cols[2].get_text(strip=True).lower():
                fila_femenino = row
                print(f"[DIAG] fila femenino encontrada: {[c.get_text(strip=True) for c in cols]}", flush=True)
                break

        if not fila_femenino:
            print("[DIAG] NO se encontro ninguna fila femenina en la ficha de competicion", flush=True)
            await browser.close()
            return

        cols = fila_femenino.select("td")
        enlace_grupo = cols[3].find("a")
        print(f"[DIAG] enlace grupo (col 3): {enlace_grupo.get('href') if enlace_grupo else None}", flush=True)

        if not enlace_grupo:
            await browser.close()
            return

        url_grupo = urljoin(page.url, enlace_grupo["href"])
        await page.goto(url_grupo, wait_until="networkidle")
        soup_grupo = BeautifulSoup(await page.content(), "html.parser")

        enlace_cmp_jornada = soup_grupo.find("a", href=re.compile(r"NFG_CmpJornada\?.*CodCompeticion=", re.IGNORECASE))
        print(f"[DIAG] enlace NFG_CmpJornada: {enlace_cmp_jornada.get('href') if enlace_cmp_jornada else None}", flush=True)

        if not enlace_cmp_jornada:
            print("[DIAG] NO se encontro enlace a NFG_CmpJornada -- volcando enlaces de la pagina de grupo", flush=True)
            for a in soup_grupo.find_all("a", href=True):
                print(f"[DIAG]   enlace: texto={a.get_text(strip=True)!r} href={a['href']!r}", flush=True)
            await browser.close()
            return

        url_sin_jornada = re.sub(r"[?&]CodJornada=\d+", "", urljoin(page.url, enlace_cmp_jornada["href"]), flags=re.IGNORECASE)
        await page.goto(url_sin_jornada, wait_until="networkidle")
        soup_cal = BeautifulSoup(await page.content(), "html.parser")

        select_jornada = soup_cal.find("select", {"name": "jornada"})
        print(f"[DIAG] select jornada encontrado: {select_jornada is not None}", flush=True)
        if select_jornada:
            for opt in select_jornada.find_all("option"):
                print(f"[DIAG]   opcion: value={opt.get('value')!r} texto={opt.get_text(strip=True)!r} selected={opt.has_attr('selected')}", flush=True)

        print(f"[DIAG] URL calendario sin jornada: {page.url}", flush=True)
        # Volcar las filas con "campillo" tal cual se ven por defecto (sin elegir jornada)
        for fila in soup_cal.select("tbody tr"):
            texto = fila.get_text(" ", strip=True)
            if "campillo" in texto.lower():
                print(f"[DIAG] fila con campillo (vista por defecto): {texto[:200]!r}", flush=True)

        await browser.close()


asyncio.run(main())
