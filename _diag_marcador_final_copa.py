import asyncio
import sys

sys.path.insert(0, "backend")

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.web_scrappig.scraper import (
    BASE_URL,
    _norm_ascii,
    _extraer_tabla_ntype,
    _extraer_digito,
    extraer_acta,
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
        if select_jornada:
            import re
            patron_jornada = re.compile(rf"\b{re.escape(objetivo_jornada)}\b")
            for opt in select_jornada.find_all("option"):
                if patron_jornada.search(_norm_ascii(opt.get_text())):
                    cod_jornada = opt.get("value")
                    break

        if cod_jornada and cod_jornada != "0":
            await page.goto(f"{base}&CodJornada={cod_jornada}", wait_until="networkidle")
            soup = BeautifulSoup(await page.content(), "html.parser")

        # Cuantos scripts "packer" (eval(function(p,a,c,k,e,d)...)) hay en
        # TODA la pagina -- si hay mas de uno, cada widget de marcador puede
        # traer su propia tabla de permutacion distinta, y usar siempre la
        # PRIMERA de toda la pagina para decodificar todos los digitos
        # seria incorrecto.
        total_scripts_packer = sum(
            1 for s in soup.find_all("script") if "eval(function(p,a,c,k,e,d)" in (s.string or s.get_text() or "")
        )
        print(f"[DIAG] total scripts packer en toda la pagina: {total_scripts_packer}", flush=True)

        objetivo_local = _norm_ascii(EQUIPO_LOCAL)
        objetivo_visitante = _norm_ascii(EQUIPO_VISITANTE)

        for fila in soup.select("tbody tr"):
            texto_fila = _norm_ascii(fila.get_text(" "))
            if objetivo_local not in texto_fila or objetivo_visitante not in texto_fila:
                continue
            celdas = fila.select("td")
            if len(celdas) != 3:
                continue
            celda = celdas[1]
            spans = celda.select("span.wid2_resultado_cerrada")
            if len(spans) < 2:
                print("[DIAG] no se encontraron los dos spans esperados", flush=True)
                continue

            i_local = spans[0].find("i", class_="fa-solid")
            i_visitante = spans[1].find("i", class_="fa-solid")

            tabla_global = _extraer_tabla_ntype(soup)
            tabla_local_scope = _extraer_tabla_ntype(spans[0])
            tabla_visitante_scope = _extraer_tabla_ntype(spans[1])
            print(f"[DIAG] tabla global (pagina completa): {tabla_global}", flush=True)
            print(f"[DIAG] tabla con ambito span local: {tabla_local_scope}", flush=True)
            print(f"[DIAG] tabla con ambito span visitante: {tabla_visitante_scope}", flush=True)

            digito_local_global = _extraer_digito(i_local, tabla_global)
            digito_visitante_global = _extraer_digito(i_visitante, tabla_global)
            print(f"[DIAG] digitos con tabla global: local={digito_local_global} visitante={digito_visitante_global}", flush=True)

            digito_local_scoped = _extraer_digito(i_local, tabla_local_scope)
            digito_visitante_scoped = _extraer_digito(i_visitante, tabla_visitante_scope)
            print(f"[DIAG] digitos con tabla por-span: local={digito_local_scoped} visitante={digito_visitante_scoped}", flush=True)

        await browser.close()


asyncio.run(main())
