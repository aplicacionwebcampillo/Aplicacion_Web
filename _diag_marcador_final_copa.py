import asyncio

from playwright.async_api import async_playwright

BASE = (
    "https://rfaf.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"
    "&CodCompeticion=48829832&CodGrupo=48829872&CodTemporada=22&CodJornada=4"
)


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"])
        # Con JavaScript HABILITADO esta vez: dejamos que el propio navegador
        # ejecute ntype() de verdad, en vez de reimplementar la logica de
        # ofuscacion a mano (que ha dado 3 lecturas distintas segun la
        # fuente: "2-1" decodificando la tabla, "6-2"/"3-0" leyendo texto
        # crudo). Así vemos el DOM tal cual lo veria un usuario real.
        context = await browser.new_context(java_script_enabled=True)
        page = await context.new_page()
        page.set_default_timeout(120000)

        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(2000)

        resultado = await page.evaluate(
            """
            () => {
                const spans = Array.from(document.querySelectorAll('span.wid2_resultado_cerrada'));
                return spans.map(span => {
                    const i = span.querySelector('i.fa-solid i[id]');
                    return i ? { id: i.id, className: i.className } : null;
                });
            }
            """
        )
        print(f"[DIAG] clases tras ejecutar JS real: {resultado}", flush=True)

        texto_filas = await page.evaluate(
            """
            () => {
                const filas = Array.from(document.querySelectorAll('tbody tr'));
                return filas
                    .filter(f => f.innerText.includes('NAVAS') && f.innerText.includes('CAMPILLO'))
                    .map(f => f.innerText.replace(/\\s+/g, ' ').trim());
            }
            """
        )
        print(f"[DIAG] innerText (post-JS) de filas con Navas/Campillo: {texto_filas}", flush=True)

        await browser.close()


asyncio.run(main())
