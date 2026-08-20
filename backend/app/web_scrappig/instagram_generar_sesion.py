"""Genera el fichero de sesión de Instagram para el importador de noticias.

Se ejecuta UNA VEZ, a mano, en tu propio ordenador (no en CI). Abre una
ventana de Firefox real y visible: inicias sesión en Instagram con
normalidad ahí (resolviendo cualquier verificación), y al terminar se
guarda esa sesión (cookies + almacenamiento local) en un fichero que el
importador programado reutilizará.

Uso:
    python backend/app/web_scrappig/instagram_generar_sesion.py [ruta_salida]

Si no se indica ruta_salida, se guarda como ig_storage_state.json en el
directorio actual.

Requiere Playwright instalado con el navegador Firefox:
    pip install playwright
    playwright install firefox
"""

import sys

from playwright.sync_api import sync_playwright

OUTPUT = sys.argv[1] if len(sys.argv) > 1 else "ig_storage_state.json"

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.instagram.com/accounts/login/")

    input(
        "\nInicia sesión en Instagram en la ventana del navegador que se ha "
        "abierto (resuelve cualquier verificación si te la pide).\n"
        "Cuando hayas terminado y veas tu perfil/inicio cargado, vuelve "
        "aquí y pulsa Enter...\n"
    )

    context.storage_state(path=OUTPUT)
    browser.close()

print(f"[OK] Sesión guardada en {OUTPUT}")
print(
    "Este fichero da acceso completo a esa cuenta de Instagram: trátalo "
    "como una contraseña, no lo subas al repositorio ni lo compartas."
)
