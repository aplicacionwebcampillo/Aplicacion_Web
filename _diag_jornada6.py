import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

CODIGO_CLUB = "28701965"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        url = f"https://www.rfaf.es/pnfg/NPcd/NFG_VerClub?cod_primaria=1000118&codigo_club={CODIGO_CLUB}"
        await page.goto(url, wait_until="networkidle")
        await page.click('a[href*="NFG_VisCompeticiones_Club?cod_primaria=1000123&codclub=28701965&codtemporada="]')
        await page.wait_for_load_state("networkidle")

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")
        tablas = soup.select(".table-bordered")
        print(f"[DIAG] tablas: {len(tablas)}", flush=True)
        primera_tabla = tablas[0]

        for i, row in enumerate(primera_tabla.select("tbody tr")):
            cols = row.select("td")
            enlace0 = cols[0].find("a") if len(cols) > 0 else None
            enlace3 = cols[3].find("a") if len(cols) > 3 else None
            print(
                f"[DIAG] fila #{i} ({len(cols)} cols): {[c.get_text(' ', strip=True) for c in cols]} "
                f"| href0={enlace0.get('href') if enlace0 else None} "
                f"| href3={enlace3.get('href') if enlace3 else None}",
                flush=True,
            )

        await browser.close()


asyncio.run(main())
