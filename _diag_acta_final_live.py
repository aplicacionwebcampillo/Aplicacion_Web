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
        primera_tabla = soup.select(".table-bordered")[0]

        fila_copa = None
        for row in primera_tabla.select("tbody tr"):
            cols = row.select("td")
            if len(cols) < 4:
                continue
            if "Trofeo Copa Presidente" in cols[2].get_text(strip=True):
                fila_copa = row
                break

        if not fila_copa:
            print("[DIAG] No se encontro la fila de la Copa", flush=True)
            await browser.close()
            return

        cols = fila_copa.select("td")
        enlace_grupo = cols[3].find("a")
        url_grupo = urljoin(page.url, enlace_grupo["href"])
        print(f"[DIAG] URL grupo copa: {url_grupo}", flush=True)

        await page.goto(url_grupo, wait_until="networkidle")
        soup_grupo = BeautifulSoup(await page.content(), "html.parser")

        for a in soup_grupo.find_all("a", href=True):
            if "NFG_CmpJornada" in a["href"] or "NFG_VisCalendario" in a["href"]:
                print(f"[DIAG] enlace: {a['href']!r} texto={a.get_text(strip=True)!r}", flush=True)

        enlace_ultima = soup_grupo.find("a", href=re.compile(r"NFG_CmpJornada\?.*CodJornada=\d+", re.IGNORECASE))
        if not enlace_ultima:
            print("[DIAG] no se encontro enlace a ultima jornada", flush=True)
            await browser.close()
            return

        url_ultima = urljoin(page.url, enlace_ultima["href"])
        print(f"[DIAG] URL ultima jornada copa: {url_ultima}", flush=True)

        await page.goto(url_ultima, wait_until="networkidle")
        soup_jornada = BeautifulSoup(await page.content(), "html.parser")

        h5 = soup_jornada.find("h5")
        print(f"[DIAG] h5: {list(h5.stripped_strings) if h5 else None}", flush=True)

        tabla_partidos = soup_jornada.select_one("table.table-bordered.table-striped")
        if tabla_partidos:
            for row in tabla_partidos.select("tbody tr"):
                cols = row.select("td")
                if len(cols) < 3:
                    continue
                texto = row.get_text(" ", strip=True)
                if "navas" in texto.lower() or "campillo" in texto.lower():
                    print(f"[DIAG] fila NAVAS/CAMPILLO: {[c.get_text(' ',strip=True) for c in cols]}", flush=True)
                    enlace_acta = row.find("a", href=re.compile(r"NFG_CmpPartido.*CodActa=\d+"))
                    print(f"[DIAG] enlace acta en esta fila: {enlace_acta}", flush=True)
        else:
            print("[DIAG] no se encontro tabla de partidos en la jornada", flush=True)

        await browser.close()


asyncio.run(main())
