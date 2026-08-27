"""Diagnostico puntual: probar NFG_CmpJornada SIN el parametro CodJornada,
para ver si lista todas las jornadas/rondas con sus enlaces de acta, lo que
permitiria automatizar esto sin tener que adivinar CodJornada. Se borra
tras usarlo."""
import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL_SIN_JORNADA = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"
    "&CodCompeticion=48829832&CodGrupo=48829872&CodTemporada=22"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(60000)
        try:
            await page.goto(URL_SIN_JORNADA, wait_until="networkidle")
            print(f"URL final: {page.url}", flush=True)
            content = await page.content()
        finally:
            await browser.close()

    soup = BeautifulSoup(content, "html.parser")
    total = 0
    con_link = 0
    for fila in soup.select("tbody tr"):
        celdas = fila.select("td")
        if len(celdas) < 3:
            continue
        total += 1
        enlaces = fila.find_all("a")
        texto = fila.get_text(" ", strip=True)[:150]
        if enlaces:
            con_link += 1
            print(f"[CON LINK] {texto!r} -> {[a.get('href') for a in enlaces]}", flush=True)
        else:
            print(f"[sin link] {texto!r}", flush=True)
    print(f"\nTotal filas: {total}, con link: {con_link}", flush=True)

    # Tambien buscamos cualquier <select> o enlace que permita elegir jornada
    selects = soup.find_all("select")
    print(f"\nTotal <select> en la pagina: {len(selects)}", flush=True)
    for s in selects:
        print(f"  select name={s.get('name')!r} id={s.get('id')!r}", flush=True)
        for opt in s.find_all("option")[:20]:
            print(f"    option value={opt.get('value')!r} texto={opt.get_text(strip=True)!r}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
