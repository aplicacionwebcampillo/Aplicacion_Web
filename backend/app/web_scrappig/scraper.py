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


def extraer_acta(fila, base_url):
    """Busca el enlace a la ficha/acta del partido dentro de la fila. Se
    identifica por el propio endpoint de la RFAF (NFG_CmpPartido con
    CodActa=), no por clases CSS, que varían según la plantilla de la
    página (confirmado con una ficha real: div.div_icono_resultados > a
    con href a NFG_CmpPartido). Devuelve None si el partido aún no tiene
    acta publicada."""
    enlace_acta = fila.find("a", href=re.compile(r"NFG_CmpPartido.*CodActa=\d+"))
    if enlace_acta and enlace_acta.get("href"):
        return urljoin(base_url, enlace_acta["href"])
    return None


#***********************************************************************************************
async def scrape_competiciones(codigo_club: str):
    async with async_playwright() as p:       
        browser = await p.firefox.launch(
    headless=True,
    args=[
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--no-sandbox'
    ],
    timeout=60000
)
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        page.set_default_timeout(120000)

        url = f"https://www.rfaf.es/pnfg/NPcd/NFG_VerClub?cod_primaria=1000118&codigo_club={codigo_club}"
        await page.goto(url, wait_until='networkidle')
        await page.wait_for_load_state("networkidle")
        
        await page.click('a[href*="NFG_VisCompeticiones_Club?cod_primaria=1000123&codclub=28701965&codtemporada="]') # Ficha de Competición
        await page.wait_for_load_state("networkidle")
        
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        session = SessionLocal()
        now = datetime.now()
        url_api = "https://aplicacion-web-m5oa.onrender.com/competiciones/"
        
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
        browser = await p.firefox.launch(
    headless=True,
    args=[
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--no-sandbox'
    ],
    timeout=60000
)
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
        url_api = "https://aplicacion-web-m5oa.onrender.com/competiciones/"
        
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

                                    url_get = f"https://aplicacion-web-m5oa.onrender.com/clasificaciones/{nombre_competicion}/{temporada}/{equipo}"
                                    response = requests.get(url_get)

                                    if response.status_code == 404:
                                        res = requests.post("https://aplicacion-web-m5oa.onrender.com/clasificaciones/", json=data)
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
    url_base = "https://aplicacion-web-m5oa.onrender.com"
    local = data["local"]
    visitante = data["visitante"]
    nombre = data["nombre_competicion"]
    temporada = data["temporada_competicion"]

    async with httpx.AsyncClient() as client:
        response_get = await client.get(f"{url_base}/partidos/{nombre}/{temporada}/{local}/{visitante}")
        if response_get.status_code == 404:
            # No existe con este local/visitante exacto, pero puede que ya
            # existiera con otro rival en la MISMA jornada (p.ej. un cruce de
            # copa listado como "Descansa" a la espera del sorteo, que ahora
            # ya tiene rival real). Si es así, es el mismo partido con datos
            # antiguos: se borra antes de crear el nuevo para no dejar un
            # partido fantasma duplicado.
            jornada = data.get("jornada")
            if jornada:
                resp_lista = await client.get(
                    f"{url_base}/partidos/",
                    params={"nombre_competicion": nombre, "temporada_competicion": temporada},
                )
                if resp_lista.status_code == 200:
                    for p in resp_lista.json():
                        if p.get("jornada") != jornada:
                            continue
                        if p.get("local") == local and p.get("visitante") == visitante:
                            continue
                        if local in (p.get("local"), p.get("visitante")) or visitante in (p.get("local"), p.get("visitante")):
                            resp_del = await client.delete(
                                f"{url_base}/partidos/{nombre}/{temporada}/{p['local']}/{p['visitante']}"
                            )
                            if resp_del.status_code == 204:
                                print(f"Partido obsoleto eliminado (misma jornada, rival distinto): {p['local']} vs {p['visitante']}")

            response = await client.post(f"{url_base}/partidos/", json=data)
            if response.status_code == 201:
                print(f"Partido creado: {local} vs {visitante}")
            else:
                print(f"Error al crear partido: {response.status_code} - {response.text}")
        else:
            # Algunas competiciones (p.ej. copas/trofeos) no enlazan el acta
            # desde la ficha de jornada aunque ya este publicada -- se ha
            # comprobado que ni siquiera aparece con JavaScript activado, asi
            # que a veces se rellena a mano. Si esta vez no se ha encontrado
            # enlace pero el partido ya tenia un acta guardada, no se borra.
            nueva_acta = (data.get("acta") or "").strip()
            if not nueva_acta:
                actual = response_get.json()
                acta_actual = (actual.get("acta") or "").strip()
                if acta_actual:
                    data = {**data, "acta": actual["acta"]}

            response = await client.put(f"{url_base}/partidos/{nombre}/{temporada}/{local}/{visitante}", json=data)
            if response.status_code == 200:
                print(f"Partido actualizado: {local} vs {visitante}")
            else:
                print(f"Error al actualizar partido: {response.status_code} - {response.text}")


BASE_URL = "https://rfaf.es"
tasks = []


def _texto_visible(tag):
    """Concatena solo el texto realmente visible dentro de tag, ignorando
    nodos con estilo inline display:none y el contenido de <style>/<script>
    -- RFAF inyecta en el marcador digitos señuelo ocultos (p.ej. un
    <span style="display:none">4</span> pegado justo detras del digito
    real) y pequeños scripts (ver _extraer_tabla_ntype) para dificultar el
    scraping ingenuo del resultado."""
    partes = []
    for nodo in tag.descendants:
        if not isinstance(nodo, str):
            continue
        padre = nodo.parent
        oculto = False
        while padre is not None and padre is not tag.parent:
            if padre.name in ("style", "script"):
                oculto = True
                break
            estilo = padre.get("style", "") if hasattr(padre, "get") else ""
            if re.search(r"display\s*:\s*none", estilo):
                oculto = True
                break
            padre = padre.parent
        if not oculto:
            partes.append(str(nodo))
    return "".join(partes)


def _extraer_tabla_ntype(soup):
    """Busca en toda la página el script empaquetado (formato "packer" de
    Dean Edwards) que define la función ntype(id,n,i,f) -- usada para
    "desordenar" un dígito del marcador cambiando la clase de su icono
    según una tabla de permutación, distinta en cada carga de página. No
    hace falta desempaquetar el script entero: los números de la tabla no
    se tocan en el empaquetado (solo se sustituyen tokens de una letra), y
    el multiplicador de la fórmula es un único token cuyo índice en la
    lista de palabras clave es directamente su valor en base 36. Devuelve
    (tabla, multiplicador) o (None, None) si no se encuentra."""
    for script in soup.find_all("script"):
        texto = script.string or script.get_text() or ""
        if "eval(function(p,a,c,k,e,d)" not in texto:
            continue
        m = re.search(
            r'\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*\d+\s*,\s*\d+\s*,\s*"((?:[^"\\]|\\.)*)"\.split\("\|"\)',
            texto,
        )
        if not m:
            continue
        packed, keywords_raw = m.group(1), m.group(2)
        keywords = keywords_raw.split("|")

        m_tabla = re.search(r"\[\s*([\d,\s]+)\]", packed)
        m_formula = re.search(r"\(\s*i\s*\*\s*(\w)\s*\)\s*\+\s*n", packed)
        if not (m_tabla and m_formula):
            continue
        try:
            multiplicador = int(keywords[int(m_formula.group(1), 36)])
        except (ValueError, IndexError):
            continue
        tabla = [int(x) for x in m_tabla.group(1).split(",")]
        return tabla, multiplicador
    return None, None


def _digito_via_ntype(elemento, tabla_ntype):
    """Técnica 3: un <script>ntype("id",n,i,"fa-X")</script> dentro del
    elemento indica que hay que sustituir la clase por 'fa-'+tabla[i*mult+n]
    -- solo se aplica si se ejecuta JavaScript. Se calcula aquí sin
    ejecutar nada, usando la tabla ya extraída de la página."""
    if not tabla_ntype or tabla_ntype[0] is None:
        return None
    tabla, multiplicador = tabla_ntype
    script = elemento.find("script")
    if not script:
        return None
    texto = script.string or script.get_text() or ""
    m = re.search(r'ntype\("[^"]+",\s*(\d+),\s*(\d+),\s*"fa-\d+"\)', texto)
    if not m:
        return None
    n, i = int(m.group(1)), int(m.group(2))
    idx = i * multiplicador + n
    if 0 <= idx < len(tabla):
        return str(tabla[idx])
    return None


def _digito_via_after(elemento):
    """Técnica 2: un <span id="X"></span> vacío cuyo dígito real se
    inyecta mediante CSS generated content (#X:after{content:"\\HHHH"}) en
    vez de como texto -- invisible para un lector de texto normal, pero no
    oculto con display:none, así que sí es el dígito real (a diferencia de
    la técnica 3, que si no se ejecuta JavaScript muestra la clase sin
    intercambiar)."""
    span_id = elemento.find(attrs={"id": True})
    if not span_id:
        return None
    id_ = span_id["id"]
    style = elemento.find("style")
    if not style:
        return None
    texto_estilo = style.string or style.get_text() or ""
    m = re.search(re.escape(f"#{id_}:after") + r"\s*\{([^}]*)\}", texto_estilo)
    if not m:
        return None
    bloque = m.group(1)
    if re.search(r"display\s*:\s*none", bloque):
        return None
    m_content = re.search(r'content\s*:\s*"((?:\\.|[^"\\])*)"', bloque)
    if not m_content:
        return None
    contenido = re.sub(
        r"\\([0-9a-fA-F]{1,6})\s?", lambda m: chr(int(m.group(1), 16)), m_content.group(1)
    )
    digitos = re.sub(r"\D", "", contenido)
    return digitos or None


def _extraer_digito(elemento, tabla_ntype):
    """Prueba, en orden, las tres técnicas de ofuscación del marcador
    vistas en rfaf.es para un único dígito (el <i class="fa-solid"> de un
    lado del resultado): texto visible con un dígito señuelo oculto al
    lado, contenido CSS ::after en un span vacío, y el script ntype()."""
    visible = re.sub(r"\D", "", _texto_visible(elemento))
    if visible:
        return visible
    return _digito_via_after(elemento) or _digito_via_ntype(elemento, tabla_ntype)


def extraer_marcador_widget(celda, soup_pagina):
    """Extrae el resultado (local, visitante) de la celda central de una
    fila con el formato "widget" de NFG_CmpJornada. Devuelve (None, None)
    si el partido aun no se ha jugado o no se pudo leer el marcador.

    RFAF ofusca cada dígito del marcador con una de al menos tres técnicas
    distintas (ver _extraer_digito), aparentemente elegidas al azar en
    cada carga de página -- se comprobó con un partido real que un mismo
    marcador puede mezclar dos técnicas distintas, una para cada dígito."""
    spans = celda.select("span.wid2_resultado_cerrada")
    if len(spans) < 2:
        return None, None

    i_local = spans[0].find("i", class_="fa-solid")
    i_visitante = spans[1].find("i", class_="fa-solid")
    if not i_local or not i_visitante:
        return None, None

    tabla_ntype = _extraer_tabla_ntype(soup_pagina)
    local = _extraer_digito(i_local, tabla_ntype)
    visitante = _extraer_digito(i_visitante, tabla_ntype)
    if not local or not visitante:
        return None, None
    return local, visitante


def _norm_ascii(texto):
    if not texto:
        return ""
    sin_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return " ".join(sin_acentos.lower().split())


async def buscar_datos_via_jornada(page, cod_competicion, cod_grupo, cod_temporada, equipo_local, equipo_visitante, nombre_jornada):
    """Contraste fiable para un partido concreto contra NFG_CmpJornada:
    devuelve (acta, resultado_local, resultado_visitante), con None en lo
    que no se encuentre.

    Sirve para dos cosas:
    1) Respaldo para cuando la ficha de jornada "clásica"
       (NFG_VisCompeticiones_Grupo) no trae el enlace del acta inline --
       confirmado que pasa en algunas competiciones de copa/trofeo, con o
       sin JavaScript.
    2) Fuente fiable del marcador: esa misma ficha clásica guarda el
       resultado en <b> tal cual, vulnerable al mismo truco de ofuscación
       del marcador que la ficha de jornada de las ligas -- confirmado con
       un partido real (una final de copa) que llegó a leerse "2-1" cuando
       el resultado real era "6-2". NFG_CmpJornada usa el formato "widget"
       que extraer_marcador_widget ya sabe decodificar correctamente.

    Necesita el CodJornada exacto; se busca primero en el desplegable de
    jornadas de esa misma competición/grupo/temporada la que coincide con
    el nombre de la jornada (p.ej. "Cuartos")."""
    base = (
        f"{BASE_URL}/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"
        f"&CodCompeticion={cod_competicion}&CodGrupo={cod_grupo}&CodTemporada={cod_temporada}"
    )
    try:
        await page.goto(base, wait_until="networkidle")
        soup = BeautifulSoup(await page.content(), "html.parser")

        objetivo_jornada = _norm_ascii(nombre_jornada)
        cod_jornada = None
        select_jornada = soup.find("select", {"name": "jornada"})
        if select_jornada and objetivo_jornada:
            # Coincidencia de palabra completa, no subcadena: "final" es
            # subcadena literal de "semifinales" (sin separador entre
            # "semi" y "final"), así que una comprobación con "in" hacía
            # que buscar "Final" encontrara antes "Semifinales" en la
            # lista -- confirmado con un partido real.
            patron_jornada = re.compile(rf"\b{re.escape(objetivo_jornada)}\b")
            for opt in select_jornada.find_all("option"):
                if patron_jornada.search(_norm_ascii(opt.get_text())):
                    cod_jornada = opt.get("value")
                    break

        if cod_jornada and cod_jornada != "0":
            await page.goto(f"{base}&CodJornada={cod_jornada}", wait_until="networkidle")
            soup = BeautifulSoup(await page.content(), "html.parser")

        objetivo_local = _norm_ascii(equipo_local)
        objetivo_visitante = _norm_ascii(equipo_visitante)

        # La misma fila puede aparecer duplicada a distinta profundidad (un
        # <tr> envoltorio con una <table> anidada dentro, y esa tabla con la
        # fila real de 3 columnas) -- el acta se acepta de cualquiera de las
        # dos (la búsqueda de <a> funciona igual en ambas), pero el
        # marcador solo se lee de la fila real de 3 columnas.
        acta = None
        fila_marcador = None
        for fila in soup.select("tbody tr"):
            texto_fila = _norm_ascii(fila.get_text(" "))
            if objetivo_local not in texto_fila or objetivo_visitante not in texto_fila:
                continue
            if not acta:
                acta = extraer_acta(fila, BASE_URL)
            celdas = fila.select("td")
            if fila_marcador is None and len(celdas) == 3:
                fila_marcador = fila

        resultado_local = resultado_visitante = None
        if fila_marcador is not None:
            celda_resultado = fila_marcador.select("td")[1]
            resultado_local, resultado_visitante = extraer_marcador_widget(celda_resultado, soup)

        return acta, resultado_local, resultado_visitante
    except Exception as e:
        print(f"[AVISO] No se pudo buscar los datos via NFG_CmpJornada: {e}", flush=True)
        return None, None, None


async def procesar_jornada(page, url_jornada: str, cod_competicion=None, cod_temporada=None):
    """Devuelve el numero de partidos realmente guardados, para que quien
    llama pueda distinguir una ficha vacia/rota (enlace presente pero sin
    tabla de partidos aprovechable) de una ficha que de verdad se proceso."""
    await page.goto(url_jornada, wait_until="networkidle")
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")

    print(f"[INFO] Procesando ficha")

    h5 = soup.find('h5')
    if not h5:
        print("[AVISO] No se encontró título (h5) en la ficha de jornada.")
        return 0
    lineas = list(h5.stripped_strings)
    if not lineas:
        return 0

    nombre_competicion = lineas[0]

    now = datetime.now()
    temporada = inferir_temporada(now.month, now.year)

    # Algunas fichas (p.ej. finales de copa) usan "table-light" en vez de
    # "table-hover" para la misma tabla de partidos, así que no exigimos esa
    # clase concreta.
    tabla_partidos = soup.select_one("table.table-bordered.table-striped")
    if not tabla_partidos:
        print("[AVISO] No se encontró tabla de partidos en la jornada.")
        return 0

    partidos_guardados = 0
    for row in tabla_partidos.select("tbody tr"):
        columnas = row.select("td")
        if len(columnas) < 3:
            continue

        jornada = columnas[0].get_text(strip=True)

        #equipos_info = columnas[1].find_all('h5')
        equipos_info = list(columnas[1].stripped_strings)

        # Algunas fichas (p.ej. partido único de una final) generan filas con
        # una estructura de columnas totalmente distinta a la habitual
        # (jornada/equipos+fecha/resultado); en vez de fallar o guardar
        # basura, se descarta la fila si no tiene la forma esperada.
        if len(equipos_info) < 3:
            continue

        #if len(equipos_info) < 3:
           #equipo_local = equipos_info[0].get_text(strip=True)
           #equipo_visitante = "Descansa"
           #fecha_hora_texto = equipos_info[1].get_text(strip=True)
        #else:
        equipo_local = equipos_info[0]
        equipo_visitante = equipos_info[1]

        # Los nombres de equipo reales siempre tienen varios caracteres; si
        # alguno es demasiado corto (p.ej. "1" o "-"), es que esta fila viene
        # de una plantilla distinta que reparte los datos en otras columnas,
        # no un partido real.
        if len(equipo_local) < 3 or len(equipo_visitante) < 3:
            continue
        fecha_hora_texto = equipos_info[2]
        print(f"Partido Revisar: {equipo_local} vs {equipo_visitante}")
        
        
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

        acta = extraer_acta(row, BASE_URL)

        # Esta ficha "clásica" guarda el resultado en <b> tal cual,
        # vulnerable al mismo truco de ofuscación del marcador que la ficha
        # de jornada de las ligas -- confirmado con un partido real (una
        # final de copa) que se leyó "2-1" cuando el resultado real era
        # "6-2". Para el partido del Campillo se contrasta siempre contra
        # NFG_CmpJornada (que también sirve de respaldo para el acta si esta
        # ficha no la enlaza), y se usa lo que encuentre ahí en vez de lo de
        # aquí cuando lo encuentra.
        if cod_competicion and cod_temporada and (
            "campillo" in equipo_local.lower() or "campillo" in equipo_visitante.lower()
        ):
            cod_grupo_match = re.search(r"codgrupo=(\d+)", url_jornada, re.IGNORECASE)
            if cod_grupo_match:
                acta_fiable, res_local_fiable, res_visitante_fiable = await buscar_datos_via_jornada(
                    page, cod_competicion, cod_grupo_match.group(1), cod_temporada,
                    equipo_local, equipo_visitante, jornada,
                )
                if acta_fiable:
                    acta = acta_fiable
                if res_local_fiable is not None:
                    resultado_local, resultado_visitante = res_local_fiable, res_visitante_fiable
        acta = acta or " "

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
            "acta": acta,
        }
        await guardar_o_actualizar_partido(data)
        partidos_guardados += 1

    return partidos_guardados


async def procesar_jornada_widget(page, url_jornada: str, nombre_competicion: str):
    """Respaldo para competiciones (p.ej. 1ª Andaluza Sénior) cuya ficha de
    equipo ya no trae enlace a la jornada esta temporada: aqui se procesa
    directamente NFG_CmpJornada, que usa un formato de fila "widget"
    distinto al de la tabla de jornada clasica (procesar_jornada)."""
    await page.goto(url_jornada, wait_until="networkidle")
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")

    now = datetime.now()
    temporada = inferir_temporada(now.month, now.year)

    jornada_match = re.search(r"CodJornada=(\d+)", url_jornada, re.IGNORECASE)
    jornada = jornada_match.group(1) if jornada_match else ""

    for fila in soup.find_all("tr"):
        celdas = fila.select("td")
        if len(celdas) != 3:
            continue

        equipo_local_tag = celdas[0].select_one("h4 a")
        equipo_visitante_tag = celdas[2].select_one("h4 a")
        if not equipo_local_tag or not equipo_visitante_tag:
            continue

        equipo_local = equipo_local_tag.get_text(strip=True)
        equipo_visitante = equipo_visitante_tag.get_text(strip=True)
        if len(equipo_local) < 3 or len(equipo_visitante) < 3:
            continue

        # Esta ficha lista TODOS los partidos de la jornada de toda la
        # competición (todos los equipos, no solo el Campillo) -- aquí solo
        # interesa guardar el partido del propio club.
        if "campillo" not in equipo_local.lower() and "campillo" not in equipo_visitante.lower():
            continue

        celda_resultado = celdas[1]
        horarios = celda_resultado.select("span.horario")
        fecha = normalizar_fecha(horarios[0].get_text(strip=True)) if len(horarios) > 0 else None
        hora = normalizar_hora(horarios[1].get_text(strip=True)) if len(horarios) > 1 else None

        resultado_local, resultado_visitante = extraer_marcador_widget(celda_resultado, soup)
        acta = extraer_acta(fila, BASE_URL) or " "

        data = {
            "nombre_competicion": nombre_competicion,
            "temporada_competicion": temporada,
            "local": equipo_local,
            "visitante": equipo_visitante,
            "dia": fecha,
            "hora": hora,
            "jornada": jornada,
            "resultado_local": resultado_local if resultado_local is not None else 0,
            "resultado_visitante": resultado_visitante if resultado_visitante is not None else 0,
            "acta": acta,
        }
        await guardar_o_actualizar_partido(data)


async def procesar_competiciones(page):
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")

    cod_temporada_match = re.search(r"codtemporada=(\d+)", page.url, re.IGNORECASE)
    cod_temporada = cod_temporada_match.group(1) if cod_temporada_match else None

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

        nombre_competicion_fila = cols[2].get_text(strip=True)

        enlace = cols[0].find("a")
        if enlace and enlace.has_attr("href"):
            url_completa = urljoin(page.url, enlace["href"])
            await page.goto(url_completa, wait_until="networkidle")

            content_categoria = await page.content()
            soup_categoria = BeautifulSoup(content_categoria, "html.parser")

            tabla_jornadas = soup_categoria.select_one(".table-bordered")
            if not tabla_jornadas:
                print(f"[AVISO] No se encontró tabla de jornadas para: {categoria}")
            else:
                for row_jornada in tabla_jornadas.select("tbody tr"):
                    cols_jornada = row_jornada.select("td")
                    if len(cols_jornada) < 6:
                        continue

                    # La página de equipo lista TODAS las competiciones de
                    # ese equipo en una sola tabla compartida (no solo la de
                    # esta fila exterior) -- hay que quedarse solo con la
                    # fila cuya competición coincide, si no se reprocesa el
                    # enlace de una competición distinta.
                    if cols_jornada[0].get_text(strip=True) != nombre_competicion_fila:
                        continue

                    cod_competicion = None
                    enlace_competicion = cols_jornada[0].find("a")
                    if enlace_competicion and enlace_competicion.has_attr("href"):
                        m = re.search(r"codcompeticion=(\d+)", enlace_competicion["href"], re.IGNORECASE)
                        if m:
                            cod_competicion = m.group(1)

                    enlace_ficha = cols_jornada[5].find("a")
                    if enlace_ficha and enlace_ficha.has_attr("href"):
                        url_completa_ficha = urljoin(page.url, enlace_ficha["href"])
                        await procesar_jornada(
                            page, url_completa_ficha,
                            cod_competicion=cod_competicion, cod_temporada=cod_temporada,
                        )

        # Para las ligas (a diferencia de las copas), la ficha de equipo a
        # veces viene vacía y otras enlaza solo a una jornada suelta (se
        # comprobó: apuntaba nada más que a la última jugada, dejando fuera
        # la siguiente) -- así que para las ligas este respaldo se ejecuta
        # SIEMPRE, no solo si el camino de arriba no encontró nada. Entra
        # por la página de Grupo (columna 4, la misma que usa
        # scrape_clasificacion) hasta llegar a NFG_CmpJornada.
        if inferir_formato(nombre_competicion_fila) == "Liga" and len(cols) > 3:
            enlace_grupo = cols[3].find("a")
            if enlace_grupo and enlace_grupo.has_attr("href"):
                url_grupo = urljoin(page.url, enlace_grupo["href"])
                await page.goto(url_grupo, wait_until="networkidle")
                soup_grupo = BeautifulSoup(await page.content(), "html.parser")

                # Hay más de un enlace a NFG_CmpJornada en esta página: uno
                # genérico sin parámetros ("Calendarios y resultados", que
                # aparece antes en el HTML) y el de "Ver Última Jornada",
                # que sí lleva CodCompeticion/CodGrupo/CodTemporada -- hay
                # que exigir esos parámetros para no quedarse con el vacío.
                enlace_cmp_jornada = soup_grupo.find(
                    "a", href=re.compile(r"NFG_CmpJornada\?.*CodCompeticion=", re.IGNORECASE)
                )
                if enlace_cmp_jornada and enlace_cmp_jornada.has_attr("href"):
                    # Se entra sin CodJornada para leer el desplegable de
                    # jornadas -- lista TODA la temporada (jugada o no), a
                    # diferencia de "Ver Última Jornada", que solo apunta a
                    # la última ya JUGADA y deja fuera la siguiente
                    # (comprobado: con la jornada 1 jugada y la 2 por jugar,
                    # apuntaba solo a la 1). Recorrer hasta el valor más
                    # alto del desplegable sí cubre toda la temporada.
                    url_sin_jornada = re.sub(
                        r"[?&]CodJornada=\d+", "", urljoin(page.url, enlace_cmp_jornada["href"]), flags=re.IGNORECASE
                    )
                    await page.goto(url_sin_jornada, wait_until="networkidle")
                    soup_calendario = BeautifulSoup(await page.content(), "html.parser")

                    select_jornada = soup_calendario.find("select", {"name": "jornada"})
                    valores_jornada = [
                        int(opt["value"]) for opt in (select_jornada.find_all("option") if select_jornada else [])
                        if opt.get("value", "").isdigit()
                    ]
                    ultima_jornada = max(valores_jornada) if valores_jornada else None

                    if ultima_jornada:
                        separador = "&" if "?" in url_sin_jornada else "?"
                        for num_jornada in range(1, ultima_jornada + 1):
                            url_num = f"{url_sin_jornada}{separador}CodJornada={num_jornada}"
                            await procesar_jornada_widget(page, url_num, nombre_competicion_fila)
                    else:
                        print(f"[AVISO] No se encontró el desplegable de jornadas para: {categoria}")
                else:
                    print(f"[AVISO] No se encontró enlace a NFG_CmpJornada para: {categoria}")

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
        browser = await p.firefox.launch(
    headless=True,
    args=[
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--no-sandbox'
    ],
    timeout=60000
)
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()

        try:
            await abrir_pagina_club(page, codigo_club)
            await procesar_competiciones(page)
        finally:
            await page.wait_for_timeout(2000)
            await browser.close()
