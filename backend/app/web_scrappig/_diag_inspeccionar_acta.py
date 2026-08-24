"""Diagnóstico puntual: inspecciona la ficha de jornada real que dio el
club (temporada pasada, con partidos ya jugados) para localizar el
enlace/icono de la ficha de cada partido (acta). Esta vez vuelca TODAS las
tablas de la página (clase CSS + primeras filas), sin asumir un selector
concreto, porque el selector que usa procesar_jornada() no encontró nada
en esta página. Se borra después de usarlo."""
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_CmpJornada"
    "?cod_primaria=1000120&CodCompeticion=48316372&CodGrupo=48316374"
    "&CodTemporada=21&CodJornada=6"
)


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, wait_until="load", timeout=60000)
        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    tablas = soup.select("table")
    print(f"[INFO] {len(tablas)} tablas encontradas", flush=True)

    for i, tabla in enumerate(tablas):
        clases = tabla.get("class")
        filas = tabla.select("tr")
        print(f"=== Tabla {i}: class={clases!r}, {len(filas)} filas (tr) ===", flush=True)
        # Vuelca hasta 2 filas de cada tabla para ver la estructura real.
        for fila in filas[:2]:
            print(fila.prettify()[:2500], flush=True)

    # Además, busca cualquier <a> en TODA la página cuyo href contenga
    # patrones típicos de ficha/acta de partido, por si no está dentro de
    # una tabla estándar.
    print("=== Enlaces <a> en toda la página con pistas de 'acta'/'ficha'/'partido' ===", flush=True)
    for a in soup.select("a[href]"):
        href = a["href"]
        texto = a.get_text(strip=True)
        if any(p in href.lower() for p in ("acta", "ficha", "partido", "cmppartido", "vispartido")):
            print(f"href={href!r} texto={texto!r} html={str(a)[:300]}", flush=True)


if __name__ == "__main__":
    main()
