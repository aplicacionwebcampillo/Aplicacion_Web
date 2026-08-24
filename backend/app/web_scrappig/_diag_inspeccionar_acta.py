"""Diagnóstico puntual: inspecciona la ficha de jornada real que dio el
club (temporada pasada, con partidos ya jugados) para localizar el
enlace/icono de la ficha de cada partido (acta). Prueba primero con
requests (rápido); si la tabla sale vacía, reintenta con Playwright por si
el contenido se carga con JavaScript. Se borra después de usarlo."""
import sys

import requests
from bs4 import BeautifulSoup

URL = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_CmpJornada"
    "?cod_primaria=1000120&CodCompeticion=48316372&CodGrupo=48316374"
    "&CodTemporada=21&CodJornada=6"
)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def volcar_tabla(html, origen):
    soup = BeautifulSoup(html, "html.parser")
    tabla = soup.select_one("table.table.table-bordered.table-striped.table-hover")
    if not tabla:
        print(f"[AVISO] ({origen}) No se encontró table.table-bordered.table-striped.table-hover", flush=True)
        # Vuelca cualquier tabla que haya, por si cambió la clase.
        todas = soup.select("table")
        print(f"[INFO] ({origen}) {len(todas)} tablas totales en la página", flush=True)
        return False

    filas = tabla.select("tbody tr")
    print(f"[INFO] ({origen}) {len(filas)} filas en la tabla de partidos", flush=True)
    if not filas:
        return False

    for fila in filas:
        columnas = fila.select("td")
        print(f"[INFO] ({origen}) Fila con {len(columnas)} columnas. HTML completo de la fila:", flush=True)
        print(fila.prettify()[:3000], flush=True)
    return True


def main():
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    print(f"[INFO] GET {URL} -> {resp.status_code}", flush=True)
    if volcar_tabla(resp.text, "requests"):
        return

    print("[INFO] Reintentando con Playwright (por si el contenido es dinámico)...", flush=True)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] Playwright no está instalado en este entorno de diagnóstico.", flush=True)
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle", timeout=60000)
        html = page.content()
        browser.close()

    volcar_tabla(html, "playwright")


if __name__ == "__main__":
    main()
