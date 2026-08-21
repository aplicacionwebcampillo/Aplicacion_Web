"""Prueba local: extrae la tabla de la plantilla de lapreferente.com.

NO escribe nada en la base de datos ni en la API — solo imprime lo que
consigue extraer, para comprobar que el enfoque funciona y ver el formato
real de los datos antes de conectarlo con el resto del sistema.

Requiere una sesión generada con lapreferente_generar_sesion.py.

Uso:
    python backend/app/web_scrappig/lapreferente_test.py [ruta_sesion]
"""

import sys

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = "https://www.lapreferente.com/E38004/cd-campillo-del-rio-cf"
SESSION_FILE = sys.argv[1] if len(sys.argv) > 1 else "lapreferente_storage_state.json"

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    context = browser.new_context(storage_state=SESSION_FILE)
    page = context.new_page()
    page.goto(URL, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3000)
    title = page.title()
    html = page.content()
    browser.close()

print(f"[INFO] Título de la página: {title}")

if "moment" in title.lower() or "just a" in title.lower():
    print(
        "[ERROR] Sigue mostrando el reto de seguridad de Cloudflare. "
        "La sesión ha caducado o no llegó a resolverse. Vuelve a generarla "
        "con lapreferente_generar_sesion.py."
    )
    sys.exit(1)

soup = BeautifulSoup(html, "html.parser")

# Buscamos la tabla de la plantilla por su contenido (tiene que mencionar
# "Jugador" y "Demarcación" o "Edad" en algún punto de la tabla), sin
# asumir un id/clase concreto porque todavía no lo conocemos.
tabla_plantilla = None
for tabla in soup.select("table"):
    texto = tabla.get_text(" ", strip=True)
    if "Jugador" in texto and ("Demarcaci" in texto or "Edad" in texto):
        tabla_plantilla = tabla
        break

if not tabla_plantilla:
    print(
        "[ERROR] No se encontró la tabla de la plantilla. Guardando el "
        "HTML completo en lapreferente_debug.html para revisarlo."
    )
    with open("lapreferente_debug.html", "w", encoding="utf-8") as f:
        f.write(html)
    sys.exit(1)

print("[INFO] Tabla de plantilla encontrada. Filas (celdas de cada fila):\n")
for fila in tabla_plantilla.select("tr"):
    celdas = [c.get_text(" ", strip=True) for c in fila.select("td, th")]
    if celdas:
        print(celdas)

    # También sacamos el href del enlace del jugador (si lo hay), por si
    # hace falta entrar a su ficha para más datos (p.ej. la foto).
    enlace = fila.select_one("a[href]")
    if enlace:
        print("   -> enlace:", enlace["href"])
