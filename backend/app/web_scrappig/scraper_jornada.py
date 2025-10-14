from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
from app.database import SessionLocal
from app.models.resultado import Resultado
import re
from typing import Tuple
import os
import requests
from urllib.parse import urljoin
import unicodedata
from typing import Tuple, Optional
import httpx
import asyncio
import json
from dotenv import load_dotenv
from weasyprint import HTML
import aiohttp

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


def scrape_y_guardar(url: str, categoria: str = "Senior"):
    print(f"[INFO] Scrapeando resultados para {categoria}")

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    jornada_node = soup.select_one("h3, h4, .titulo")
    jornada_text = jornada_node.get_text(strip=True) if jornada_node else "Última jornada"

    filas = soup.select("table.table-striped tbody tr")
    session = SessionLocal()
    now = datetime.utcnow()

    for f in filas:
        td_local = f.select_one("td:nth-child(1)")
        td_marcador = f.select_one("td:nth-child(2)")
        td_visitante = f.select_one("td:nth-child(3)")

        local_a = td_local.select_one("h4 a")
        local_span = td_local.select_one("h4 span")
        local = local_a.get_text(strip=True) if local_a else (local_span.get_text(strip=True) if local_span else None)

        visitante_a = td_visitante.select_one("h4 a")
        visitante = visitante_a.get_text(strip=True) if visitante_a else None

        b_tags = td_marcador.select("b")
        goles_local, goles_visitante = " ", " "
        if len(b_tags) == 2:
            goles_local = b_tags[0].get_text(strip=True)
            goles_visitante = b_tags[1].get_text(strip=True)

        fecha_texto, hora_texto = normalizar_fecha_hora(td_marcador.get_text(" ", strip=True))

        if not local or not visitante:
            continue

        existente = (
            session.query(Resultado)
            .filter_by(local=local, visitante=visitante, jornada=jornada_text, categoria=categoria)
            .first()
        )

        if existente:
            existente.goles_local = goles_local
            existente.goles_visitante = goles_visitante
            existente.fecha = fecha_texto
            existente.hora = hora_texto
            existente.fetched_at = now
            print(f"[ACTUALIZADO] {local} vs {visitante}")
        else:
            nuevo = Resultado(
                jornada=jornada_text,
                local=local,
                visitante=visitante,
                goles_local=goles_local,
                goles_visitante=goles_visitante,
                fecha=fecha_texto,
                hora=hora_texto,
                categoria=categoria,
                fetched_at=now,
            )
            session.add(nuevo)
            print(f"[CREADO] {local} vs {visitante}")

    session.commit()
    session.close()
    print(f"[OK] Jornada '{jornada_text}' guardada en BD correctamente.")


if __name__ == "__main__":
    URLS = {
        "Senior": "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion?cod_primaria=1000120&codgrupo=45293013&codcompeticion=44788639",
        "Femenino_7": "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion?cod_primaria=1000120&codgrupo=46575672&codcompeticion=46575570",
        "Femenino_11": "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion?cod_primaria=1000120&codgrupo=46573703&codcompeticion=46573611",
    }

    for categoria, url in URLS.items():
        scrape_y_guardar(url, categoria)

