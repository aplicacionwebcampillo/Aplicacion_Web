"""Genera el fichero de sesión para lapreferente.com (para pasar el reto
de seguridad de Cloudflare).

Se ejecuta a mano, en tu propio ordenador (no en CI). Abre una ventana de
Firefox real y visible: espera a que la página cargue del todo (Cloudflare
puede tardar unos segundos comprobando que eres humano; a veces no hace
falta hacer nada, a veces pide marcar una casilla). Cuando veas la tabla de
la plantilla del equipo cargada, vuelve a la terminal y pulsa Enter para
guardar la sesión.

Aviso: la cookie de verificación de Cloudflare (cf_clearance) suele durar
solo unas horas, no días. Esta sesión habrá que regenerarla cada vez que
quieras sincronizar la plantilla, a diferencia de la de Instagram.

Uso:
    python backend/app/web_scrappig/lapreferente_generar_sesion.py [ruta_salida]

Requiere Playwright instalado con el navegador Firefox:
    pip install playwright
    playwright install firefox
"""

import sys

from playwright.sync_api import sync_playwright

URL = "https://www.lapreferente.com/E38004/cd-campillo-del-rio-cf"
OUTPUT = sys.argv[1] if len(sys.argv) > 1 else "lapreferente_storage_state.json"

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(URL)

    input(
        "\nEspera a que la página cargue del todo (Cloudflare puede tardar "
        "unos segundos comprobando que eres humano; si te pide marcar una "
        "casilla de verificación, hazlo).\n"
        "Cuando veas la tabla de la plantilla del equipo, vuelve aquí y "
        "pulsa Enter...\n"
    )

    context.storage_state(path=OUTPUT)
    browser.close()

print(f"[OK] Sesión guardada en {OUTPUT}")
print(
    "Recuerda: esta sesión caduca en unas horas. Si el script de prueba "
    "vuelve a mostrar el reto de Cloudflare, repite este paso."
)
