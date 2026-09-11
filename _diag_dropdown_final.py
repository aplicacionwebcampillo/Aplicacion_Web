import asyncio
import re
import unicodedata

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

BASE = (
    "https://rfaf.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"
    "&CodCompeticion=48829832&CodGrupo=48829872&CodTemporada=22"
)


def _norm_ascii(texto):
    if not texto:
        return ""
    sin_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return " ".join(sin_acentos.lower().split())


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(BASE, wait_until="networkidle")
        soup = BeautifulSoup(await page.content(), "html.parser")

        select_jornada = soup.find("select", {"name": "jornada"})
        print(f"[DIAG] select encontrado: {select_jornada is not None}", flush=True)
        if select_jornada:
            for opt in select_jornada.find_all("option"):
                texto = opt.get_text()
                print(f"[DIAG] option value={opt.get('value')!r} texto={texto!r} norm={_norm_ascii(texto)!r} contiene_final={'final' in _norm_ascii(texto)}", flush=True)

        # Tambien probar sin CodJornada que filas trae por defecto
        for fila in soup.select("tbody tr"):
            texto = _norm_ascii(fila.get_text(" "))
            if "navas" in texto or "campillo" in texto:
                print(f"[DIAG] fila por defecto (sin CodJornada) con navas/campillo: {texto[:200]!r}", flush=True)

        await browser.close()


asyncio.run(main())
