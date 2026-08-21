"""Diagnóstico temporal (v3): la página del grupo tiene un enlace/pestaña
"Tabla Goleadores" (y "Tabla Detallada", con la columna "Sanción" a nivel de
equipo). Vamos directos a por el href real de "Tabla Goleadores" y "Tabla
Detallada" para ver si dan estadísticas por JUGADOR (goles, tarjetas)."""

from playwright.sync_api import sync_playwright

URL_GRUPO = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion"
    "?cod_primaria=1000120&codgrupo=48466095&codcompeticion=48466094"
)

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(URL_GRUPO, wait_until="networkidle", timeout=60000)
    print(f"[INFO] Página cargada: {page.url}", flush=True)

    for etiqueta in ("Tabla Goleadores", "Tabla Detallada", "Ver Resultados", "Ver Calendario"):
        enlace = page.locator(f"a:has-text('{etiqueta}')").first
        if enlace.count() == 0:
            print(f"[AVISO] No se encontró enlace '{etiqueta}'", flush=True)
            continue
        href = enlace.get_attribute("href")
        onclick = enlace.get_attribute("onclick")
        print(f"[INFO] '{etiqueta}' -> href={href!r} onclick={onclick!r}", flush=True)

    print("\n[INFO] Navegando a 'Tabla Goleadores'...", flush=True)
    enlace_goleadores = page.locator("a:has-text('Tabla Goleadores')").first
    with page.expect_navigation(wait_until="networkidle", timeout=20000):
        enlace_goleadores.click()
    print(f"[INFO] URL tras clic: {page.url}", flush=True)

    texto = page.inner_text("body")
    print(f"[INFO] Longitud texto visible: {len(texto)}", flush=True)
    print("[INFO] Primeros 2000 caracteres del texto visible:", flush=True)
    print(texto[:2000], flush=True)

    with open("rfaf_goleadores_debug.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    print("\n[INFO] Navegando ahora a 'Tabla Detallada'...", flush=True)
    page.goto(URL_GRUPO, wait_until="networkidle", timeout=60000)
    enlace_detallada = page.locator("a:has-text('Tabla Detallada')").first
    if enlace_detallada.count() > 0:
        with page.expect_navigation(wait_until="networkidle", timeout=20000):
            enlace_detallada.click()
        print(f"[INFO] URL tras clic: {page.url}", flush=True)
        texto2 = page.inner_text("body")
        print(f"[INFO] Longitud texto visible: {len(texto2)}", flush=True)
        print("[INFO] Primeros 2000 caracteres del texto visible:", flush=True)
        print(texto2[:2000], flush=True)

    browser.close()
