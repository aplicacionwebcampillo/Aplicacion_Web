"""Diagnóstico temporal (v2, con navegador real): la RFAF no tiene
Cloudflare, pero la navegación a resultados/actas de partido parece
depender de JavaScript (botones "Ver Resultados"), no de enlaces <a href>
planos, así que un simple requests.get no llega. Probamos con Playwright
(como ya hacemos con Instagram) para renderizar la página de verdad,
pulsar donde haga falta, y ver qué aparece."""

import re

from playwright.sync_api import sync_playwright

URL_GRUPO = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion"
    "?cod_primaria=1000120&codgrupo=48466095&codcompeticion=48466094"
)

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()

    urls_vistas = []

    def al_navegar(frame):
        if frame == page.main_frame:
            urls_vistas.append(page.url)

    page.on("framenavigated", al_navegar)

    page.goto(URL_GRUPO, wait_until="networkidle", timeout=60000)
    print(f"[INFO] Página cargada: {page.url}", flush=True)

    # Buscamos cualquier elemento clicable que suene a "resultados" o a un
    # partido ya jugado (marcador tipo "N - N").
    candidatos = page.locator("text=/Ver Resultados|Resultados/i")
    n = candidatos.count()
    print(f"[INFO] {n} elementos con texto 'Resultados'", flush=True)

    if n > 0:
        try:
            candidatos.first.click(timeout=10000)
            page.wait_for_timeout(3000)
            print(f"[INFO] Tras clic, URL: {page.url}", flush=True)
        except Exception as e:
            print(f"[ERROR] No se pudo hacer clic: {e}", flush=True)

    html = page.content()
    print(f"[INFO] HTML actual: {len(html)} bytes", flush=True)

    # Buscamos enlaces/botones a partidos concretos (marcadores N-N).
    marcadores = page.locator("text=/\\b\\d{1,2}\\s*-\\s*\\d{1,2}\\b/")
    print(f"[INFO] {marcadores.count()} posibles marcadores de resultado en pantalla", flush=True)

    if marcadores.count() > 0:
        try:
            marcadores.first.click(timeout=10000)
            page.wait_for_timeout(3000)
            print(f"[INFO] Tras clic en marcador, URL: {page.url}", flush=True)
            html = page.content()
            print(f"[INFO] HTML tras clic: {len(html)} bytes", flush=True)
        except Exception as e:
            print(f"[ERROR] No se pudo hacer clic en marcador: {e}", flush=True)

    texto_plano = page.inner_text("body")
    for palabra in ("goles", "goleador", "tarjeta", "amarilla", "roja", "minuto", "convocado", "alineaci"):
        idx = texto_plano.lower().find(palabra)
        estado = "SI" if idx != -1 else "no"
        print(
            f"  contiene '{palabra}': {estado}"
            + (f" (contexto: ...{texto_plano[max(0,idx-60):idx+120]}...)" if idx != -1 else ""),
            flush=True,
        )

    print(f"\n[INFO] URLs visitadas en el frame principal: {urls_vistas}", flush=True)

    with open("rfaf_partido_debug2.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[INFO] HTML guardado localmente en rfaf_partido_debug2.html", flush=True)

    browser.close()
