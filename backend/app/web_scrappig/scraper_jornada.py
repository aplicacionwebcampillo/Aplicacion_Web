from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import Tuple


def normalizar_marcador(texto: str) -> Tuple[str, str]:
    texto = texto.replace("–", "-").replace("—", "-")
    partes = [p.strip() for p in re.split(r"\s*-\s*", texto)]
    if len(partes) == 2 and all(p.isdigit() for p in partes):
        return partes[0], partes[1]
    return "0", "0"


def normalizar_fecha_hora(texto: str) -> Tuple[str, str]:
    fecha, hora = None, None
    match = re.search(r"(\d{1,2}-\d{1,2}-\d{4})", texto)
    if match:
        fecha = "-".join(reversed(match.group(1).split("-")))
    match_hora = re.search(r"(\d{1,2}:\d{2})", texto)
    if match_hora:
        hora = match_hora.group(1) + ":00"
    return fecha, hora


def obtener_resultados(url: str) -> dict:
    """
    Recibe la URL de la competición y devuelve resultados de la última jornada.
    Filtra partidos donde local o visitante sean None.
    """
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    jornada_node = soup.select_one("h3, h4, .titulo")
    jornada_text = jornada_node.get_text(strip=True) if jornada_node else "Última jornada"

    resultados = []

    filas = soup.select("table.table-striped tbody tr")
    for f in filas:
        td_local = f.select_one("td:nth-child(1)")
        td_marcador = f.select_one("td:nth-child(2)")
        td_visitante = f.select_one("td:nth-child(3)")

        # Local
        local_a = td_local.select_one("h4 a")
        local_span = td_local.select_one("h4 span")
        local = local_a.get_text(strip=True) if local_a else (local_span.get_text(strip=True) if local_span else None)

        # Visitante
        visitante_a = td_visitante.select_one("h4 a")
        visitante = visitante_a.get_text(strip=True) if visitante_a else None

        # Marcador
        b_tags = td_marcador.select("b")
        goles_local, goles_visitante = " ", " "
        if len(b_tags) == 2:
            goles_local = b_tags[0].get_text(strip=True)
            goles_visitante = b_tags[1].get_text(strip=True)

        fecha_texto, hora_texto = normalizar_fecha_hora(td_marcador.get_text(" ", strip=True))

        if local and visitante:
            resultados.append({
                "local": local,
                "visitante": visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "fecha_texto": fecha_texto,
                "hora_texto": hora_texto,
            })

    return {
        "jornada": jornada_text,
        "partidos": resultados,
        "fetched_at": datetime.utcnow().isoformat() + "Z"
    }

