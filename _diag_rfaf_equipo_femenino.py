import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL = "https://www.rfaf.es/pnfg/NPcd/NFG_VisEquipos?cod_primaria=1000119&Codigo_Equipo=32996393"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(URL, wait_until="networkidle")
        print(f"[DIAG] Titulo pagina: {await page.title()}", flush=True)

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        print("[DIAG] --- Todas las tablas .table-bordered ---", flush=True)
        for i, tabla in enumerate(soup.select(".table-bordered")):
            filas = tabla.select("tbody tr")
            print(f"[DIAG] tabla #{i}: {len(filas)} filas", flush=True)
            for fila in filas[:3]:
                cols = fila.select("td")
                print(f"[DIAG]   fila ({len(cols)} cols): {[c.get_text(' ', strip=True)[:60] for c in cols]}", flush=True)

        print("[DIAG] --- Buscando palabras clave: plantilla, jugador, licencia ---", flush=True)
        texto_pagina = soup.get_text(" ", strip=True)
        for palabra in ["plantilla", "jugador", "licencia", "ficha de jugador", "staff"]:
            print(f"[DIAG] '{palabra}' aparece: {palabra.lower() in texto_pagina.lower()}", flush=True)

        print("[DIAG] --- Enlaces relevantes (jugador, persona, ficha) ---", flush=True)
        vistos = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            texto = a.get_text(strip=True)
            if any(p in href.lower() for p in ["jugador", "persona", "ficha"]) or "Persona_Mostrar" in str(a):
                clave = (texto, href)
                if clave not in vistos:
                    vistos.add(clave)
                    print(f"[DIAG] enlace: texto={texto!r} href={href!r}", flush=True)

        print("[DIAG] primeros 3000 chars de texto limpio de la pagina:", flush=True)
        print(texto_pagina[:3000], flush=True)

        await browser.close()


asyncio.run(main())
