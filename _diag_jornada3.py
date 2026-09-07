import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL_CALENDARIO = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_VisCalendario_Vis?cod_primaria=1000120"
    "&codtemporada=22&codcompeticion=48466094&codgrupo=48466095"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(URL_CALENDARIO, wait_until="networkidle")
        print(f"[DIAG] URL final: {page.url}", flush=True)

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        tablas = soup.select(".table-bordered")
        print(f"[DIAG] tablas .table-bordered: {len(tablas)}", flush=True)

        for i, tabla in enumerate(tablas):
            filas = tabla.select("tbody tr")
            print(f"[DIAG] tabla #{i}: {len(filas)} filas", flush=True)
            if filas:
                primera = filas[0]
                cols = primera.select("td")
                print(f"[DIAG]   primera fila: {len(cols)} columnas: {[c.get_text(' ', strip=True) for c in cols]}", flush=True)
                enlace = None
                for c in cols:
                    a = c.find("a")
                    if a and a.has_attr("href"):
                        enlace = a["href"]
                        break
                print(f"[DIAG]   primer enlace en la fila: {enlace}", flush=True)

        # Buscar especificamente la fila con Linares
        print("[DIAG] === Buscando fila con 'linares' en cualquier tabla ===", flush=True)
        for i, tabla in enumerate(tablas):
            for fila in tabla.select("tbody tr"):
                texto = fila.get_text(" ", strip=True)
                if "linares" in texto.lower():
                    cols = fila.select("td")
                    print(f"[DIAG] tabla #{i} fila con Linares ({len(cols)} cols): {[c.get_text(' ', strip=True) for c in cols]}", flush=True)
                    for c in cols:
                        a = c.find("a")
                        if a and a.has_attr("href"):
                            print(f"[DIAG]   enlace en columna: {a['href']}", flush=True)

        await browser.close()


asyncio.run(main())
