"""Acción puntual: localizar el nombre de la competición (h5) y el enlace al
acta (NFG_CmpPartido...CodActa=) en la ficha de la final de Copa de la
temporada pasada, para poder construir a mano los datos del partido (la
tabla de esta ficha usa una plantilla de "partido único" distinta a la de
listado de jornada que espera procesar_jornada, así que no se puede reusar
esa función tal cual). Se borra tras usarlo."""
import asyncio
import re
import sys

sys.path.insert(0, "backend/app/web_scrappig")

from bs4 import BeautifulSoup  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

URL_FINAL = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_CmpJornada"
    "?cod_primaria=1000120&CodCompeticion=48316372&CodGrupo=48316374"
    "&CodTemporada=21&CodJornada=6"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(
            headless=True,
            args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
            timeout=60000,
        )
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(URL_FINAL, wait_until="load")
        await page.wait_for_timeout(3000)
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        h5 = soup.find("h5")
        print(f"[INFO] h5 stripped_strings={list(h5.stripped_strings)!r}", flush=True)

        print("[INFO] Enlaces <a> que apuntan a NFG_CmpPartido...CodActa= en TODA la página:", flush=True)
        enlaces = soup.find_all("a", href=re.compile(r"NFG_CmpPartido.*CodActa=\d+"))
        for a in enlaces:
            print(f"    href={a.get('href')!r} texto={a.get_text(strip=True)!r} class={a.get('class')!r}", flush=True)
        if not enlaces:
            print("    (ninguno encontrado)", flush=True)

        print("[INFO] Buscando cualquier <a> cuyo href contenga 'CmpPartido' (por si el patrón de CodActa no coincide):", flush=True)
        enlaces2 = soup.find_all("a", href=re.compile(r"CmpPartido"))
        for a in enlaces2:
            print(f"    href={a.get('href')!r} texto={a.get_text(strip=True)!r} class={a.get('class')!r}", flush=True)
        if not enlaces2:
            print("    (ninguno encontrado)", flush=True)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
