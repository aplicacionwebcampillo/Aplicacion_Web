"""Diagnóstico puntual: reutiliza la misma URL que ya usa con éxito
scraper_jornada.py (con partidos reales, a diferencia del grupo de la
temporada 2026-27 que aún no tiene jornadas) y vuelca el HTML crudo de la
celda de resultado de un partido ya jugado, para localizar el enlace/icono
de la ficha del partido (acta). Se borra después de usarlo."""
import requests
from bs4 import BeautifulSoup

URL = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion"
    "?cod_primaria=1000120&codgrupo=48466095&codcompeticion=48466094"
)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def main():
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    print(f"[INFO] GET {URL} -> {resp.status_code}", flush=True)
    soup = BeautifulSoup(resp.text, "html.parser")

    filas = soup.select("table.table-striped tbody tr")
    print(f"[INFO] {len(filas)} filas encontradas en table.table-striped", flush=True)

    for fila in filas:
        td_marcador = fila.select_one("td:nth-child(2)")
        if not td_marcador:
            continue
        b_tags = td_marcador.select("b")
        if len(b_tags) == 2 and b_tags[0].get_text(strip=True) and b_tags[1].get_text(strip=True):
            print("[INFO] Fila CON resultado encontrada. HTML de las 3 columnas:", flush=True)
            for i, td in enumerate(fila.select("td")):
                print(f"--- columna {i} ---", flush=True)
                print(td.prettify()[:2000], flush=True)
            return

    print("[AVISO] No se encontró ninguna fila con marcador de 2 números en esta tabla.", flush=True)
    # Vuelca las primeras 2 filas tal cual, por si el patrón de b_tags no aplica.
    for fila in filas[:2]:
        print("--- fila cruda (fallback) ---", flush=True)
        print(fila.prettify()[:2500], flush=True)


if __name__ == "__main__":
    main()
