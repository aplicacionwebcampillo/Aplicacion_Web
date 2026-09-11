import asyncio
import sys

sys.path.insert(0, "backend")

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.web_scrappig.scraper import (
    BASE_URL,
    _norm_ascii,
    extraer_acta,
    extraer_marcador_widget,
)

COD_COMPETICION = "48829832"
COD_GRUPO = "48829872"
COD_TEMPORADA = "22"
EQUIPO_LOCAL = "C.D. NAVAS 2006"
EQUIPO_VISITANTE = 'C.D. CAMPILLO DEL RÍO C.F. "CD"'
NOMBRE_JORNADA = "Final"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        base = (
            f"{BASE_URL}/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"
            f"&CodCompeticion={COD_COMPETICION}&CodGrupo={COD_GRUPO}&CodTemporada={COD_TEMPORADA}"
        )
        await page.goto(base, wait_until="networkidle")
        soup = BeautifulSoup(await page.content(), "html.parser")

        objetivo_jornada = _norm_ascii(NOMBRE_JORNADA)
        cod_jornada = None
        select_jornada = soup.find("select", {"name": "jornada"})
        print(f"[DIAG] select_jornada encontrado: {select_jornada is not None}", flush=True)
        if select_jornada:
            import re
            patron_jornada = re.compile(rf"\b{re.escape(objetivo_jornada)}\b")
            for opt in select_jornada.find_all("option"):
                texto = _norm_ascii(opt.get_text())
                if patron_jornada.search(texto):
                    cod_jornada = opt.get("value")
                    print(f"[DIAG] opcion coincidente: value={cod_jornada!r} texto={opt.get_text()!r}", flush=True)
                    break

        if cod_jornada and cod_jornada != "0":
            await page.goto(f"{base}&CodJornada={cod_jornada}", wait_until="networkidle")
            soup = BeautifulSoup(await page.content(), "html.parser")

        objetivo_local = _norm_ascii(EQUIPO_LOCAL)
        objetivo_visitante = _norm_ascii(EQUIPO_VISITANTE)

        print(f"[DIAG] URL final: {page.url}", flush=True)

        filas_encontradas = 0
        for fila in soup.select("tbody tr"):
            texto_fila = _norm_ascii(fila.get_text(" "))
            if objetivo_local not in texto_fila or objetivo_visitante not in texto_fila:
                continue
            filas_encontradas += 1
            celdas = fila.select("td")
            print(f"[DIAG] fila #{filas_encontradas} con {len(celdas)} td(s)", flush=True)
            print(f"[DIAG]   texto fila: {texto_fila[:200]!r}", flush=True)
            acta_fila = extraer_acta(fila, BASE_URL)
            print(f"[DIAG]   acta en esta fila: {acta_fila!r}", flush=True)
            if len(celdas) == 3:
                celda_resultado = celdas[1]
                print(f"[DIAG]   HTML celda resultado: {str(celda_resultado)[:1000]!r}", flush=True)
                res_local, res_visitante = extraer_marcador_widget(celda_resultado, soup)
                print(f"[DIAG]   marcador decodificado: {res_local} - {res_visitante}", flush=True)

        print(f"[DIAG] total filas encontradas con ambos equipos: {filas_encontradas}", flush=True)

        await browser.close()


asyncio.run(main())
