"""Diagnostico puntual: probar la URL exacta de la ficha del grupo
(NFG_VisCompeticiones_Grupo, la que ya sabemos que contiene la fila del
Cuartos Arjonilla-Campillo) con JavaScript activado pero SIN esperar a
networkidle (que nunca se cumple en esta pagina con JS, de ahi que el
scraper real lo desactive) -- en su lugar, domcontentloaded + espera fija.
Se borra tras usarlo."""
import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL_FICHA = "https://www.rfaf.es/pnfg/NPcd/NFG_VisCompeticiones_Grupo?&cod_primaria=1000123&codequipo=28796965&codgrupo=48829872"


async def probar(js_enabled: bool):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=js_enabled)
        page = await context.new_page()
        page.set_default_timeout(60000)
        try:
            await page.goto(URL_FICHA, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            content = await page.content()
        finally:
            await browser.close()

    print(f"\n{'=' * 20} JS enabled={js_enabled} {'=' * 20}", flush=True)
    soup = BeautifulSoup(content, "html.parser")
    encontrada = False
    for fila in soup.select("tbody tr"):
        if "arjonilla" in fila.get_text(" ", strip=True).lower():
            encontrada = True
            enlaces = fila.find_all("a")
            print(f"  num enlaces <a>: {len(enlaces)}", flush=True)
            for a in enlaces:
                print(f"    <a href={a.get('href')!r}> texto={a.get_text(strip=True)!r}", flush=True)
            print(f"  HTML crudo: {str(fila)[:3000]}", flush=True)
    if not encontrada:
        print("  No se encontro la fila de Arjonilla en esta carga.", flush=True)
        print(f"  longitud HTML total: {len(content)}", flush=True)


async def main():
    await probar(js_enabled=False)
    await probar(js_enabled=True)


if __name__ == "__main__":
    asyncio.run(main())
