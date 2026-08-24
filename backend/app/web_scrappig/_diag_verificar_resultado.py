"""Acción puntual: el resultado guardado para la final (C.D. CANENA ATLETICO
X-Y C.D. CAMPILLO DEL RÍO C.F.) se extrajo con JavaScript deshabilitado, y el
marcador de esta ficha se pinta mediante iconos de fuente ofuscados que solo
se resuelven ejecutando JS (ver el <script>ntype(...)</script> en el HTML).
Sin JS el texto extraído no es fiable. Esta vez se activa JS, se espera a que
el marcador se pinte, y se hace una captura de pantalla de esa zona para leer
el resultado real a simple vista (en vez de fiarnos de un parseo de texto que
ya ha demostrado ser poco fiable). Se borra tras usarlo."""
import asyncio
import base64
import sys

sys.path.insert(0, "backend/app/web_scrappig")

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
        # JS habilitado (por defecto) para que se resuelva el marcador ofuscado.
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(URL_FINAL, wait_until="load")
        await page.wait_for_timeout(4000)

        locator = page.locator("table.table-bordered.table-striped").first
        png_bytes = await locator.screenshot()
        b64 = base64.b64encode(png_bytes).decode("ascii")
        print(f"[INFO] Tamaño captura: {len(png_bytes)} bytes", flush=True)
        print("[INFO] BASE64_START", flush=True)
        # Trocear en líneas para que no se corte en los logs
        for i in range(0, len(b64), 200):
            print(b64[i:i + 200], flush=True)
        print("[INFO] BASE64_END", flush=True)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
