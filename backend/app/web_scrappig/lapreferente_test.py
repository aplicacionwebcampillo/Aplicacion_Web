"""Prueba local: extrae la tabla de la plantilla de lapreferente.com.

NO escribe nada en la base de datos ni en la API — solo imprime lo que
consigue extraer, para comprobar que el enfoque funciona y ver el formato
real de los datos antes de conectarlo con el resto del sistema.

Requiere una sesión generada con lapreferente_generar_sesion.py.

Uso:
    python backend/app/web_scrappig/lapreferente_test.py [ruta_sesion]
"""

import sys
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.lapreferente.com"
URL = f"{BASE_URL}/E38004/cd-campillo-del-rio-cf"
SESSION_FILE = sys.argv[1] if len(sys.argv) > 1 else "lapreferente_storage_state.json"


def cargar(page, url):
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3000)
    return page.title(), page.content()


with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    context = browser.new_context(storage_state=SESSION_FILE)
    page = context.new_page()

    title, html = cargar(page, URL)
    print(f"[INFO] Título de la página: {title}")

    if "moment" in title.lower() or "just a" in title.lower():
        print("[ERROR] Sigue mostrando el reto de Cloudflare. Regenera la sesión.")
        sys.exit(1)

    soup = BeautifulSoup(html, "html.parser")

    # Esta vez buscamos la tabla MÁS PEQUEÑA/interna que ya contenga la
    # cabecera "Porteros (" (sección de la plantilla), no la tabla
    # envoltorio de toda la página.
    candidatas = [t for t in soup.select("table") if "Porteros (" in t.get_text(" ", strip=True)]
    tabla_plantilla = min(candidatas, key=lambda t: len(t.get_text())) if candidatas else None

    if not tabla_plantilla:
        print("[ERROR] No se encontró la tabla de la plantilla. Guardando HTML completo en lapreferente_debug.html")
        with open("lapreferente_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        sys.exit(1)

    print(f"\n[INFO] Tabla encontrada (longitud texto: {len(tabla_plantilla.get_text())})\n")

    primer_enlace_jugador = None
    for fila in tabla_plantilla.select("tr"):
        celdas = fila.select("td, th")
        if not celdas:
            continue
        textos = [c.get_text(" ", strip=True) for c in celdas]
        print(textos)

        enlace = fila.select_one("a[href]")
        if enlace and "href" in enlace.attrs:
            href = enlace["href"]
            print("   -> enlace:", href)
            if primer_enlace_jugador is None and ".html" in href:
                primer_enlace_jugador = href

        # Mostramos el HTML crudo de la celda del nombre (normalmente la
        # 3ª celda) para ver cómo separar nombre corto / nombre completo.
        if len(celdas) >= 3:
            print("   -> HTML celda nombre:", str(celdas[2])[:500])

    # Visitamos la ficha de un jugador para ver si trae la fecha de
    # nacimiento exacta (mejor que dejarlo siempre vacío).
    if primer_enlace_jugador:
        url_jugador = urljoin(URL + "/", primer_enlace_jugador)
        print(f"\n[INFO] Visitando ficha de jugador de ejemplo: {url_jugador}")
        titulo_jugador, html_jugador = cargar(page, url_jugador)
        print(f"[INFO] Título ficha jugador: {titulo_jugador}")
        soup_jugador = BeautifulSoup(html_jugador, "html.parser")
        texto_jugador = soup_jugador.get_text(" ", strip=True)
        idx = texto_jugador.lower().find("nacimiento")
        if idx != -1:
            print("[INFO] Contexto alrededor de 'nacimiento':")
            print(texto_jugador[max(0, idx - 100) : idx + 150])
        else:
            print("[INFO] No se encontró la palabra 'nacimiento' en la ficha del jugador.")
        with open("lapreferente_jugador_debug.html", "w", encoding="utf-8") as f:
            f.write(html_jugador)
        print("[INFO] HTML completo de la ficha guardado en lapreferente_jugador_debug.html")

    browser.close()
