import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

BASE = (
    "https://rfaf.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"
    "&CodCompeticion=48466094&CodGrupo=48466095&CodTemporada=22"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(BASE, wait_until="networkidle")
        print(f"[DIAG] URL final tras cargar sin CodJornada: {page.url}", flush=True)
        soup = BeautifulSoup(await page.content(), "html.parser")

        select_jornada = soup.find("select", {"name": "jornada"})
        print(f"[DIAG] select encontrado: {select_jornada is not None}", flush=True)
        if select_jornada:
            valores = []
            for opt in select_jornada.find_all("option"):
                print(f"[DIAG] option value={opt.get('value')!r} texto={opt.get_text(strip=True)!r} selected={opt.has_attr('selected')}", flush=True)
                v = opt.get("value")
                if v and v.isdigit():
                    valores.append(int(v))
            print(f"[DIAG] max value numerico: {max(valores) if valores else None}", flush=True)

        await browser.close()


asyncio.run(main())
