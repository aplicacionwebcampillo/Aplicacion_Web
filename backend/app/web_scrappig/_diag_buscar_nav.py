"""Diagnostico puntual: en la pagina NFG_VisCompeticiones_Grupo que ya
usamos (donde la fila del partido no tiene enlace), buscar SI existe algun
enlace en cualquier parte de la pagina hacia NFG_CmpJornada o similar --
para saber si se puede navegar automaticamente hasta la pagina que SI
tiene el acta, sin conocer sus IDs de antemano. Se borra tras usarlo."""
import asyncio
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL_GRUPO = "https://www.rfaf.es/pnfg/NPcd/NFG_VisCompeticiones_Grupo?&cod_primaria=1000123&codequipo=28796965&codgrupo=48829872"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(60000)
        try:
            await page.goto(URL_GRUPO, wait_until="networkidle")
            content = await page.content()
        finally:
            await browser.close()

    soup = BeautifulSoup(content, "html.parser")
    todos = soup.find_all("a", href=True)
    print(f"Total enlaces <a> en toda la pagina: {len(todos)}", flush=True)
    for a in todos:
        href = a["href"]
        texto = a.get_text(strip=True)
        interesante = "jornada" in href.lower() or "cmppartido" in href.lower() or "cmpjornada" in href.lower()
        marca = "[JORNADA/ACTA] " if interesante else ""
        print(f"{marca}href={href!r} texto={texto!r}", flush=True)
        if interesante:
            print(f"    url completa: {urljoin(page.url, href)}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
