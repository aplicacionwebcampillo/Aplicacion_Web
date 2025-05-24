from playwright.async_api import async_playwright
from app.database import SessionLocal
from app.models.competicion import Competicion
from app.models.clasificacion import Clasificacion
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from urllib.parse import urljoin
import re
import unicodedata
from typing import Tuple, Optional
import httpx
import asyncio
import json
from dotenv import load_dotenv
import os
from weasyprint import HTML
import aiohttp


def inferir_id_equipo(nombre_competicion: str) -> int:
    nombre = nombre_competicion.lower()
    if "juvenil" in nombre:
        return 3
    elif "femenin" in nombre:
        return 2
    else:
        return 1

def inferir_formato(nombre_competicion: str) -> str:
    nombre = nombre_competicion.lower()
    if "fase final" in nombre:
        return "Copa"
    if "trofeo copa subdelegado del gobierno" in nombre:
        return "Liga"
    if "copa" in nombre:
        return "Copa"
    return "Liga"

def inferir_temporada(mes: int, anio: int) -> str:
    if mes >= 8:
        inicio = anio
        fin = anio + 1
    else:
        inicio = anio - 1
        fin = anio

    return f"Temporada {inicio}-{fin}"

def normalizar_fecha(fecha_str):
    if not fecha_str:
        return None
    return "-".join(reversed(fecha_str.strip().split("-")))

def normalizar_hora(hora_str):
    if not hora_str:
        return None
    return hora_str.strip() + ":00"

def limpiar_texto(texto):
    if not texto or not isinstance(texto, str):
        return ""
    texto = texto.strip()
    texto = re.sub(r"\s+", " ", texto)
    texto = re.sub(r"[^\x20-\x7E]", "", texto)
    return texto


#***********************************************************************************************
async def scrape_competiciones(codigo_club: str):
    async with async_playwright() as p:       
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()


        url = f"https://www.rfaf.es/pnfg/NPcd/NFG_VerClub?cod_primaria=1000118&codigo_club={codigo_club}"
        await page.goto(url, wait_until='networkidle')
        await page.wait_for_load_state("networkidle")
        
        await page.click('a[href*="NFG_VisCompeticiones_Club?cod_primaria=1000123&codclub=28701965&codtemporada="]') # Ficha de Competición
        await page.wait_for_load_state("networkidle")
        
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        session = SessionLocal()
        now = datetime.now()
        url_api = "http://127.0.0.1:8000/competiciones/"
        
        for table in soup.select(".table-bordered"):
            rows = table.select("tbody tr")
            for row in rows:
                cols = row.select("td")
                if len(cols) < 3:
                    continue
                nombre_competicion = cols[2].get_text(strip=True)
                
                competicion = Competicion(
                    nombre=nombre_competicion,
                    temporada = inferir_temporada(now.month, now.year),
                    id_equipo=inferir_id_equipo(nombre_competicion),
                    formato=inferir_formato(nombre_competicion),
                )

                # Verificar si ya existe para evitar duplicados
                if not session.query(Competicion).filter_by(nombre=competicion.nombre, temporada=competicion.temporada).first():
                    data = {
                        "nombre": competicion.nombre,
                        "temporada": competicion.temporada,
                        "formato": competicion.formato,
                        "id_equipo": competicion.id_equipo,
                    }
                    response = requests.post(url_api, json=data)
                    if response.status_code == 200:
                        print("Competición creada vía API con éxito.")
                    else:
                        print(f"Error al crear competición vía API: {response.status_code} - {response.text}")
                else:
                    print("La competición ya existe en la base de datos.")

        session.commit()
        session.close()
                
        await page.wait_for_timeout(2000)
        await browser.close()

#**********************************************************************************************        
async def scrape_clasificacion(codigo_club: str):
    async with async_playwright() as p:       
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()


        url = f"https://www.rfaf.es/pnfg/NPcd/NFG_VerClub?cod_primaria=1000118&codigo_club={codigo_club}"
        await page.goto(url, wait_until='networkidle')
        await page.wait_for_load_state("networkidle")
        
        await page.click('a[href*="NFG_VisCompeticiones_Club?cod_primaria=1000123&codclub=28701965&codtemporada="]') # Ficha de Competición
        await page.wait_for_load_state("networkidle")
        
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        session = SessionLocal()
        now = datetime.now()
        url_api = "http://127.0.0.1:8000/competiciones/"
        
        for table in soup.select(".table-bordered"):
            rows = table.select("tbody tr")
            for row in rows:
                cols = row.select("td")
                if len(cols) < 4:
                    continue

                nombre_competicion = cols[2].get_text(strip=True)
                formato_competicion = inferir_formato(nombre_competicion)

                if formato_competicion == "Liga":
                    # Extraer enlace de la cuarta columna
                    enlace = cols[3].find("a")
                    if enlace and enlace.has_attr("href"):
                        href = enlace["href"]
                        url_completa = urljoin(page.url, href)
                        await page.goto(url_completa, wait_until="networkidle") # Navegar al enlace
                        print(f"Visitando competición Liga: {nombre_competicion}")
                        
                        await page.click('a.btn.btn_cab_wid.la_roja_regular:has-text("Ver Clasificación")') # Ir a clasificación
                        await page.wait_for_load_state("networkidle")
                                                
                        # Guardar la clasificación
                        
                        html = await page.content()
                        clasificacion_soup = BeautifulSoup(html, "html.parser")
                        tabla = clasificacion_soup.select_one('.table-bordered')
                        
                        temporada = inferir_temporada(now.month, now.year)
                        
                        if tabla:
                            for fila in tabla.select("tbody tr"):
                                celdas = fila.select("td")
                                if len(celdas) >= 4:
                                    posicion = int(celdas[1].get_text(strip=True))
                                    equipo = celdas[2].get_text(strip=True)
                                    puntos = int(celdas[3].get_text(strip=True))

                                    data = {
                                        "nombre_competicion": nombre_competicion,
                                        "temporada_competicion": temporada,
                                        "equipo": equipo,
                                        "posicion": posicion,
                                        "puntos": puntos
                                    }

                                    url_get = f"http://127.0.0.1:8000/clasificaciones/{nombre_competicion}/{temporada}/{equipo}"
                                    response = requests.get(url_get)

                                    if response.status_code == 404:
                                        res = requests.post("http://127.0.0.1:8000/clasificaciones/", json=data)
                                        print(f"Creada: {res.status_code} {data}")
                                    else:
                                        res = requests.put(url_get, json={"posicion": posicion, "puntos": puntos})
                                        print(f"Actualizada: {res.status_code} {data}")

                        
                        await page.go_back(wait_until="networkidle")
                        await page.go_back(wait_until="networkidle")
                    else:
                        print(f"No se encontró enlace en la 4a columna para {nombre_competicion}")

        session.commit()
        session.close()
                
        await page.wait_for_timeout(2000)
        await browser.close()
        
#**********************************************************************************************
async def guardar_o_actualizar_partido(data):
    url_base = "http://127.0.0.1:8000"
    local = data["local"]
    visitante = data["visitante"]
    nombre = data["nombre_competicion"]
    temporada = data["temporada_competicion"]

    async with httpx.AsyncClient() as client:
        response_get = await client.get(f"{url_base}/partidos/{nombre}/{temporada}/{local}/{visitante}")
        if response_get.status_code == 404:
            response = await client.post(f"{url_base}/partidos/", json=data)
            if response.status_code == 201:
                print(f"Partido creado: {local} vs {visitante}")
            else:
                print(f"Error al crear partido: {response.status_code} - {response.text}")
        else:
            response = await client.put(f"{url_base}/partidos/{nombre}/{temporada}/{local}/{visitante}", json=data)
            if response.status_code == 200:
                print(f"Partido actualizado: {local} vs {visitante}")
            else:
                print(f"Error al actualizar partido: {response.status_code} - {response.text}")


BASE_URL = "https://rfaf.es"
tasks = []

async def procesar_jornada(page, url_jornada: str):
    await page.goto(url_jornada, wait_until="networkidle")
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")

    print(f"[INFO] Procesando ficha")
    
    h5 = soup.find('h5')
    lineas = list(h5.stripped_strings)

    nombre_competicion = lineas[0]
    
    now = datetime.now()
    temporada = inferir_temporada(now.month, now.year)
    
    tabla_partidos = soup.select_one("table.table.table-bordered.table-striped.table-hover")
    if not tabla_partidos:
        print("[AVISO] No se encontró tabla de partidos en la jornada.")
        return

    for row in tabla_partidos.select("tbody tr"):
        columnas = row.select("td")
        if len(columnas) < 3:
            continue
        
        jornada = columnas[0].get_text(strip=True)
        
        equipos_info = columnas[1].find_all('h5')
        
        if len(equipos_info) < 3:
            equipo_local = equipos_info[0].get_text(strip=True)
            equipo_visitante = "Descansa"
            fecha_hora_texto = equipos_info[1].get_text(strip=True)
        else:
            equipo_local = equipos_info[0].get_text(strip=True)
            equipo_visitante = equipos_info[1].get_text(strip=True)
            fecha_hora_texto = equipos_info[2].get_text(strip=True)
        
        
        fecha_hora = fecha_hora_texto.split()

        fecha = fecha_hora[0] if len(fecha_hora) > 0 else "??-??-????"
        hora = fecha_hora[1] if len(fecha_hora) > 1 else "00:00"
        
        fecha = normalizar_fecha(fecha)
        hora = normalizar_hora(hora)

        
        resultado_info = columnas[2].find_all('b')
        
        if len(resultado_info) < 2:
            resultado_local = 0
            resultado_visitante = 0
        else:
            resultado_local = resultado_info[0].get_text(strip=True)
            resultado_visitante = resultado_info[1].get_text(strip=True)

        data = {
            "nombre_competicion": nombre_competicion,
            "temporada_competicion": temporada,
            "local": equipo_local,
            "visitante": equipo_visitante,
            "dia": fecha,
            "hora": hora,
            "jornada": jornada,
            "resultado_local": resultado_local,
            "resultado_visitante": resultado_visitante,
            "acta": " ",
        }
        await guardar_o_actualizar_partido(data)



async def procesar_competiciones(page):
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")

    categorias_visitadas = set()

    tablas = soup.select(".table-bordered")
    if not tablas:
        print("[AVISO] No se encontraron tablas con .table-bordered")
        return

    primera_tabla = tablas[0]

    for row in primera_tabla.select("tbody tr"):
        cols = row.select("td")
        if len(cols) < 4:
            continue

        categoria = cols[1].get_text(strip=True)

        # Saltar si ya visitamos esta categoría
        if categoria in categorias_visitadas:
            continue

        enlace = cols[0].find("a")
        if enlace and enlace.has_attr("href"):
            url_completa = urljoin(page.url, enlace["href"])
            await page.goto(url_completa, wait_until="networkidle")

            content_categoria = await page.content()
            soup_categoria = BeautifulSoup(content_categoria, "html.parser")

            tabla_jornadas = soup_categoria.select_one(".table-bordered")
            if not tabla_jornadas:
                print(f"[AVISO] No se encontró tabla de jornadas para: {categoria}")
                continue

            for row in tabla_jornadas.select("tbody tr"):
                cols = row.select("td")
                if len(cols) < 6:
                    continue
                
                enlace_ficha = cols[5].find("a")
                if enlace_ficha and enlace_ficha.has_attr("href"):
                    url_completa_ficha = urljoin(page.url, enlace_ficha["href"])
                    await procesar_jornada(page, url_completa_ficha)

            categorias_visitadas.add(categoria)
            print(f"Categoría visitada: {categoria}")



async def abrir_pagina_club(page, codigo_club: str):
    url = f"https://www.rfaf.es/pnfg/NPcd/NFG_VerClub?cod_primaria=1000118&codigo_club={codigo_club}"
    await page.goto(url, wait_until='networkidle')
    await page.wait_for_load_state("networkidle")

    await page.click('a[href*="NFG_VisCompeticiones_Club?cod_primaria=1000123&codclub=28701965&codtemporada="]')
    await page.wait_for_load_state("networkidle")


async def scrape_partidos(codigo_club: str):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()

        try:
            await abrir_pagina_club(page, codigo_club)
            await procesar_competiciones(page)
        finally:
            await page.wait_for_timeout(2000)
            await browser.close()

