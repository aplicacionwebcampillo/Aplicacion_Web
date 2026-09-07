import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL_JORNADA = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"
    "&CodCompeticion=48466094&CodGrupo=48466095&CodTemporada=22&CodJornada=1"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(URL_JORNADA, wait_until="networkidle")
        print(f"[DIAG] URL final: {page.url}", flush=True)

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        h5 = soup.find("h5")
        print(f"[DIAG] h5: {list(h5.stripped_strings) if h5 else None}", flush=True)

        tabla_partidos = soup.select_one("table.table-bordered.table-striped")
        print(f"[DIAG] tabla.table-bordered.table-striped encontrada: {tabla_partidos is not None}", flush=True)

        if tabla_partidos:
            for row in tabla_partidos.select("tbody tr"):
                cols = row.select("td")
                print(f"[DIAG] fila ({len(cols)} cols): {[c.get_text(' ', strip=True) for c in cols]}", flush=True)
        else:
            print("[DIAG] === Todas las .table-bordered en la pagina ===", flush=True)
            for i, t in enumerate(soup.select(".table-bordered")):
                clases = t.get("class")
                filas = t.select("tbody tr")
                print(f"[DIAG] tabla #{i} clases={clases} filas={len(filas)}", flush=True)
                if filas:
                    print(f"[DIAG]   primera fila: {[c.get_text(' ', strip=True) for c in filas[0].select('td')]}", flush=True)

        await browser.close()


asyncio.run(main())
