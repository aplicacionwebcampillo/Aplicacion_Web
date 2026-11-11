"""Diagnostico: reproduce la navegacion real de procesar_competiciones
hasta la pagina NFG_CmpJornada (formato "widget") de 1a Andaluza Senior,
y para las jornadas 10 y 11 (los dos ultimos partidos del Campillo, que
muestran 0-0 en la web) imprime el HTML crudo de la celda de resultado y
el resultado que devuelve extraer_marcador_widget, para ver por que falla
la decodificacion del marcador en esos dos casos concretos."""

import asyncio
import re
import sys
from urllib.parse import urljoin

sys.path.insert(0, "backend")

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.web_scrappig.scraper import (
    abrir_pagina_club,
    extraer_marcador_widget,
    _extraer_tabla_ntype,
)

CODIGO_CLUB = "28701965"
NOMBRE_COMPETICION_OBJETIVO = "1ª Andaluza Sénior (Jaén)"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"], timeout=60000)
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()

        await abrir_pagina_club(page, CODIGO_CLUB)
        soup = BeautifulSoup(await page.content(), "html.parser")

        tablas = soup.select(".table-bordered")
        primera_tabla = tablas[0]
        url_grupo = None
        for row in primera_tabla.select("tbody tr"):
            cols = row.select("td")
            if len(cols) < 4:
                continue
            nombre_competicion_fila = cols[2].get_text(strip=True)
            if nombre_competicion_fila != NOMBRE_COMPETICION_OBJETIVO:
                continue
            enlace_grupo = cols[3].find("a")
            if enlace_grupo and enlace_grupo.has_attr("href"):
                url_grupo = urljoin(page.url, enlace_grupo["href"])
            break

        print(f"[INFO] url_grupo = {url_grupo}", flush=True)
        if not url_grupo:
            print("[ERROR] No se encontro la fila de la competicion objetivo", flush=True)
            await browser.close()
            return

        await page.goto(url_grupo, wait_until="networkidle")
        soup_grupo = BeautifulSoup(await page.content(), "html.parser")
        enlace_cmp_jornada = soup_grupo.find("a", href=re.compile(r"NFG_CmpJornada\?.*CodCompeticion=", re.IGNORECASE))
        url_sin_jornada = re.sub(r"[?&]CodJornada=\d+", "", urljoin(page.url, enlace_cmp_jornada["href"]), flags=re.IGNORECASE)
        print(f"[INFO] url_sin_jornada = {url_sin_jornada}", flush=True)

        separador = "&" if "?" in url_sin_jornada else "?"
        for num_jornada in (10, 11):
            url_num = f"{url_sin_jornada}{separador}CodJornada={num_jornada}"
            print(f"\n[JORNADA {num_jornada}] {url_num}", flush=True)
            await page.goto(url_num, wait_until="networkidle")
            soup_jornada = BeautifulSoup(await page.content(), "html.parser")

            tabla_ntype = _extraer_tabla_ntype(soup_jornada)
            print(f"  tabla_ntype = {tabla_ntype}", flush=True)

            encontrado = False
            for fila in soup_jornada.find_all("tr"):
                celdas = fila.select("td")
                if len(celdas) != 3:
                    continue
                eq_local_tag = celdas[0].select_one("h4 a")
                eq_visit_tag = celdas[2].select_one("h4 a")
                if not eq_local_tag or not eq_visit_tag:
                    continue
                eq_local = eq_local_tag.get_text(strip=True)
                eq_visit = eq_visit_tag.get_text(strip=True)
                if "campillo" not in eq_local.lower() and "campillo" not in eq_visit.lower():
                    continue
                encontrado = True
                celda_resultado = celdas[1]
                print(f"  Partido: {eq_local} vs {eq_visit}", flush=True)
                print(f"  HTML crudo celda_resultado:\n{celda_resultado}", flush=True)
                resultado = extraer_marcador_widget(celda_resultado, soup_jornada)
                print(f"  extraer_marcador_widget -> {resultado}", flush=True)
            if not encontrado:
                print("  [AVISO] No se encontro fila del Campillo en esta jornada", flush=True)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
