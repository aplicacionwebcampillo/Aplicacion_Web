"""Diagnostico puntual: probar la URL de NFG_CmpJornada (distinta de
NFG_VisCompeticiones_Grupo) que el usuario dice que SI tiene el enlace del
acta para partidos de copa. Se borra tras usarlo."""
import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL_JORNADA = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"
    "&CodCompeticion=48829832&CodGrupo=48829872&CodTemporada=22&CodJornada=2"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(60000)
        try:
            await page.goto(URL_JORNADA, wait_until="networkidle")
            content = await page.content()
        finally:
            await browser.close()

    soup = BeautifulSoup(content, "html.parser")
    print(f"longitud HTML: {len(content)}", flush=True)
    total_filas = 0
    filas_con_link = 0
    for fila in soup.select("tbody tr"):
        celdas = fila.select("td")
        if len(celdas) < 3:
            continue
        total_filas += 1
        enlaces = fila.find_all("a")
        texto = fila.get_text(" ", strip=True)[:150]
        if enlaces:
            filas_con_link += 1
            print(f"[CON LINK] {texto!r} -> {[a.get('href') for a in enlaces]}", flush=True)
        else:
            print(f"[sin link] {texto!r}", flush=True)
    print(f"\nTotal filas: {total_filas}, con link: {filas_con_link}", flush=True)

    if total_filas == 0:
        print("\n--- No se encontraron filas tbody tr. Volcando primeros 3000 caracteres del HTML ---", flush=True)
        print(content[:3000], flush=True)


if __name__ == "__main__":
    asyncio.run(main())
