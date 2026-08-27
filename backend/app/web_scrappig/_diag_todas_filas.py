"""Diagnostico puntual: volcar TODAS las filas de partidos de esta pagina
de grupo (no solo Arjonilla) para ver si el enlace del acta aparece en
otras filas de la MISMA pagina (partido de liga, por ejemplo) o si
realmente ninguna fila de esta pagina tiene enlace nunca. Se borra tras
usarlo."""
import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL_FICHA = "https://www.rfaf.es/pnfg/NPcd/NFG_VisCompeticiones_Grupo?&cod_primaria=1000123&codequipo=28796965&codgrupo=48829872"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(60000)
        try:
            await page.goto(URL_FICHA, wait_until="networkidle")
            content = await page.content()
        finally:
            await browser.close()

    soup = BeautifulSoup(content, "html.parser")
    total_filas = 0
    filas_con_link = 0
    for fila in soup.select("tbody tr"):
        celdas = fila.select("td")
        if len(celdas) < 3:
            continue
        total_filas += 1
        enlaces = fila.find_all("a")
        texto = fila.get_text(" ", strip=True)[:120]
        if enlaces:
            filas_con_link += 1
            print(f"[CON LINK] {texto!r} -> {[a.get('href') for a in enlaces]}", flush=True)
        else:
            print(f"[sin link] {texto!r}", flush=True)
    print(f"\nTotal filas de partido: {total_filas}, con link: {filas_con_link}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
