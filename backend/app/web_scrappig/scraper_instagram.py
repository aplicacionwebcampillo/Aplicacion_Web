"""Importa las últimas publicaciones de Instagram del club como Noticias.

No usa la Graph API oficial (requiere cuenta Business/Creator y acceso que
no tenemos). Tampoco usa `instaloader`: se probó con sesión de cookies
válida y seguía siendo bloqueado (429), porque un cliente HTTP "en crudo"
como `requests` tiene una huella (TLS, cabeceras, ausencia de JavaScript)
que el sistema anti-bot de Instagram distingue de un navegador real, aunque
las cookies sean legítimas.

En su lugar usa Playwright (el mismo motor que ya usáis para el scraper de
RFAF) con una sesión ya autenticada manualmente en un navegador real, y lee
los datos interceptando la respuesta que el propio navegador recibe al
cargar la página del perfil — igual que haría un humano navegando.

Genera esa sesión una sola vez con instagram_generar_sesion.py (ver
docs/instagram_session_setup.md para los pasos completos).

Solo depende de `playwright` y `requests` (no de app.database ni del resto
del backend): habla con la API pública igual que scraper.py, así no necesita
credenciales de base de datos.

Variables de entorno requeridas:
  IG_TARGET_USERNAME    usuario de Instagram del club (sin @)
  NOTICIA_ADMIN_DNI     DNI de un administrador ya existente en la BD,
                         se usará como autor de las noticias importadas
  IG_STORAGE_STATE_FILE ruta al fichero de sesión generado con
                         instagram_generar_sesion.py

El script recorre todas las publicaciones del perfil (haciendo scroll para
que Instagram las vaya cargando) y crea noticias por las que aún no existan
(deduplicadas por shortcode); las siguientes ejecuciones solo procesan las
publicaciones nuevas.

Variables opcionales:
  IG_MAX_POSTS           límite opcional de publicaciones a procesar por
                         ejecución, empezando por las más antiguas de las
                         vistas (sin límite por defecto)
"""

import html
import json
import os
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from playwright.sync_api import sync_playwright

API_BASE = "https://aplicacion-web-m5oa.onrender.com"
CLOUDINARY_URL = "https://api.cloudinary.com/v1_1/dft3xbtrl/image/upload"
CLOUDINARY_UPLOAD_PRESET = "Aplicacion_Web"
CATEGORIA = "Noticias del Club"


def obtener_noticias_existentes():
    resp = requests.get(f"{API_BASE}/noticias/?skip=0&limit=500", timeout=30)
    resp.raise_for_status()
    return resp.json()


def ya_importado(shortcode, noticias_existentes):
    marca = f"<!-- ig:{shortcode} -->"
    return any(marca in (n.get("contenido") or "") for n in noticias_existentes)


def subir_a_cloudinary(imagen_bytes):
    resp = requests.post(
        CLOUDINARY_URL,
        files={"file": ("instagram.jpg", imagen_bytes)},
        data={"upload_preset": CLOUDINARY_UPLOAD_PRESET},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["secure_url"]


def _formatear_fecha(taken_at):
    if not taken_at:
        return None
    try:
        return datetime.fromtimestamp(taken_at, tz=timezone.utc).strftime("%d/%m/%Y")
    except (OSError, ValueError, OverflowError, TypeError):
        return None


def generar_titular(caption, shortcode, taken_at, titulares_existentes):
    primera_linea = ""
    if caption and caption.strip():
        primera_linea = caption.strip().splitlines()[0]
    base = primera_linea[:170].strip() or "Publicación de Instagram"

    # La fecha va siempre en el titular (no solo para desambiguar): el
    # modelo de Noticia no tiene columna de fecha, así que el frontend
    # ordena la lista de noticias extrayendo esta fecha del titular.
    fecha_txt = _formatear_fecha(taken_at)
    sufijo_fecha = f" ({fecha_txt})" if fecha_txt else ""
    titular = (base[: 200 - len(sufijo_fecha)] + sufijo_fecha)[:200]

    if titular not in titulares_existentes:
        return titular

    # Coincide incluso con la fecha (misma publicación el mismo día, poco
    # probable) -> el shortcode como último recurso para garantizar unicidad.
    sufijo = f" ({shortcode})"
    return base[: 200 - len(sufijo)] + sufijo


def construir_contenido(caption, shortcode):
    texto = html.escape((caption or "").strip())
    parrafos = "".join(f"<p>{linea}</p>" for linea in texto.splitlines() if linea.strip())
    enlace = (
        f'<p><a href="https://www.instagram.com/p/{shortcode}/" '
        'target="_blank" rel="noopener noreferrer">Ver publicación en Instagram</a></p>'
    )
    marca = f"<!-- ig:{shortcode} -->"
    # Todo el texto va en un único <div>: el contenedor donde se pinta
    # contenido usa CSS flex para centrar, así que si dejamos varios <p>
    # sueltos como hijos directos cada uno se convierte en su propia
    # "celda" flex (se ve como una tabla rota) en vez de apilarse como
    # párrafos normales.
    return f"<div>{parrafos}{enlace}</div>{marca}"


def crear_noticia(titular, imagen_url, contenido, admin_dni):
    data = {
        "titular": titular,
        "imagen": imagen_url,
        "contenido": contenido,
        "categoria": CATEGORIA,
        "dni_administrador": admin_dni,
    }
    resp = requests.post(f"{API_BASE}/noticias/", json=data, timeout=30)
    if resp.status_code in (200, 201):
        print(f"[OK] Noticia creada: {titular}", flush=True)
    else:
        print(f"[ERROR] {resp.status_code} al crear noticia '{titular}': {resp.text}", flush=True)


def _parsear_json_tolerante(texto):
    """Devuelve una lista de objetos JSON encontrados en un cuerpo de
    respuesta, tolerando el formato "streaming" de Meta: varias líneas,
    cada una con su propio JSON, a veces con un prefijo anti-hijacking
    tipo `for (;;);` delante."""
    texto = (texto or "").strip()
    if texto.startswith("for (;;);"):
        texto = texto[len("for (;;);"):]

    objetos = []
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        try:
            objetos.append(json.loads(linea))
        except Exception:
            continue

    if not objetos:
        try:
            objetos.append(json.loads(texto))
        except Exception:
            pass

    return objetos


TIMELINE_CONNECTION_KEY = "xdt_api__v1__feed__user_timeline_graphql_connection"


def _normalizar_post(node):
    shortcode = node.get("shortcode") or node.get("code")
    if not shortcode:
        return None

    display_url = node.get("display_url")
    if not display_url:
        candidatos = ((node.get("image_versions2") or {}).get("candidates")) or []
        if candidatos:
            display_url = candidatos[0].get("url")
    if not display_url:
        return None

    caption = ""
    caption_edges = (node.get("edge_media_to_caption") or {}).get("edges") or []
    if caption_edges:
        caption = caption_edges[0].get("node", {}).get("text", "")
    elif isinstance(node.get("caption"), dict):
        caption = node["caption"].get("text", "") or ""
    elif isinstance(node.get("caption"), str):
        caption = node["caption"]

    # taken_at: fecha real de publicación. Instagram pone las publicaciones
    # FIJADAS primero en la cuadrícula del perfil aunque sean antiguas; si
    # no tenemos esto en cuenta, una fijada de hace un año se importaría
    # como si fuera la más reciente. La usamos para procesar/crear las
    # noticias en orden cronológico real, no en el orden de la cuadrícula.
    taken_at = node.get("taken_at")
    if taken_at is None:
        caption_obj = node.get("caption")
        if isinstance(caption_obj, dict):
            taken_at = caption_obj.get("created_at")
    taken_at = taken_at or 0

    if not taken_at:
        print(
            f"[DEBUG] Sin fecha para {shortcode}, claves del nodo: "
            + json.dumps(sorted(node.keys()), ensure_ascii=False),
            flush=True,
        )

    return {
        "shortcode": shortcode,
        "display_url": display_url,
        "caption": caption,
        "taken_at": taken_at,
    }


def _buscar_timeline_del_perfil(obj):
    """Busca específicamente la conexión con la cuadrícula de publicaciones
    del PERFIL visitado (TIMELINE_CONNECTION_KEY) dentro de un payload.

    A propósito NO se hace una búsqueda genérica de "cualquier objeto con
    shortcode" en toda la respuesta: la misma carga de página incluye otras
    secciones (feed de inicio, sugerencias de cuentas...) con publicaciones
    de OTRAS personas, y mezclarlas metería noticias que no son del club."""
    if isinstance(obj, dict):
        if TIMELINE_CONNECTION_KEY in obj:
            return obj[TIMELINE_CONNECTION_KEY]
        # Variante antigua de la API, por si Instagram revierte el cambio.
        if "edge_owner_to_timeline_media" in obj:
            return obj["edge_owner_to_timeline_media"]
        for valor in obj.values():
            resultado = _buscar_timeline_del_perfil(valor)
            if resultado is not None:
                return resultado
    elif isinstance(obj, list):
        for item in obj:
            resultado = _buscar_timeline_del_perfil(item)
            if resultado is not None:
                return resultado
    return None


def _extraer_posts_de_timeline(timeline):
    posts = []
    for edge in (timeline or {}).get("edges") or []:
        post = _normalizar_post(edge.get("node") or {})
        if post:
            posts.append(post)
    return posts


def obtener_posts_del_perfil(ig_target, session_file):
    """Abre el perfil con un navegador real (sesión ya autenticada) y
    busca publicaciones en cualquiera de las respuestas JSON que el propio
    navegador reciba mientras carga la página (no se asume un endpoint
    concreto, porque Instagram cambia esto con frecuencia)."""
    encontrados = []
    vistos = set()
    respuestas_con_datos = 0
    capturas_debug = []  # (url, longitud, nº objetos JSON, fragmento)

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(storage_state=session_file)
        page = context.new_page()

        def al_recibir_respuesta(response):
            nonlocal respuestas_con_datos
            if response.status != 200:
                return
            # Nos fijamos en el dominio, no en el content-type: los endpoints
            # de datos de Instagram (ajax/bz, api/graphql, graphql/query)
            # no siempre declaran "application/json". Descartamos el CDN de
            # imágenes/vídeo (cdninstagram.com) para no perder tiempo
            # intentando parsear binarios.
            host = urlparse(response.url).hostname or ""
            if host not in ("www.instagram.com", "i.instagram.com"):
                return
            try:
                texto = response.text()
            except Exception:
                return
            objetos = _parsear_json_tolerante(texto)
            if objetos:
                respuestas_con_datos += 1

            antes = len(encontrados)
            for objeto in objetos:
                timeline = _buscar_timeline_del_perfil(objeto)
                if timeline is None:
                    continue
                for post in _extraer_posts_de_timeline(timeline):
                    if post["shortcode"] not in vistos:
                        vistos.add(post["shortcode"])
                        encontrados.append(post)

            if len(encontrados) == antes:
                capturas_debug.append((response.url, len(texto), len(objetos), texto[:1500]))

        page.on("response", al_recibir_respuesta)
        page.goto(f"https://www.instagram.com/{ig_target}/", wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(3000)

        # Instagram solo carga ~12 publicaciones de golpe; el resto se pide
        # por bloques al hacer scroll (paginación infinita). Vamos bajando
        # hasta que dos scrolls seguidos no traigan publicaciones nuevas, con
        # un tope de seguridad para no quedarnos colgados indefinidamente.
        sin_novedades = 0
        for _ in range(60):
            antes = len(encontrados)
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(2000)
            if len(encontrados) == antes:
                sin_novedades += 1
                if sin_novedades >= 3:
                    break
            else:
                sin_novedades = 0

        if not encontrados:
            print(f"[DEBUG] URL final tras cargar: {page.url}", flush=True)
            try:
                print(f"[DEBUG] Título de la página: {page.title()}", flush=True)
            except Exception:
                pass
            print(f"[DEBUG] {respuestas_con_datos} respuestas parseadas como JSON, 0 publicaciones encontradas", flush=True)
            # Mostramos las respuestas más "grandes" (más probable que sean
            # las que llevan datos de verdad, no confirmaciones triviales).
            capturas_debug.sort(key=lambda c: c[1], reverse=True)
            for url, longitud, n_objetos, fragmento in capturas_debug[:6]:
                print(f"[DEBUG] --- {url} (len={longitud}, objetos_json={n_objetos}) ---", flush=True)
                print(f"[DEBUG] {fragmento}", flush=True)

        browser.close()

    if not encontrados:
        print(
            "[ERROR] No se encontraron publicaciones en ninguna respuesta "
            "(posible bloqueo, sesión caducada, o cambio de formato)",
            flush=True,
        )

    return encontrados


FECHA_DESDE_DEFAULT = "2025-12-30"


def main():
    ig_target = os.environ["IG_TARGET_USERNAME"]
    admin_dni = os.environ["NOTICIA_ADMIN_DNI"]
    session_file = os.environ["IG_STORAGE_STATE_FILE"]
    # Sin límite por defecto: se recorren todas las publicaciones vistas
    # dentro del rango de fechas (la deduplicación por shortcode hace que,
    # en ejecuciones posteriores, solo se creen noticias nuevas).
    max_posts_env = os.environ.get("IG_MAX_POSTS")
    max_posts = int(max_posts_env) if max_posts_env else None

    fecha_desde_str = os.environ.get("IG_FECHA_DESDE", FECHA_DESDE_DEFAULT)
    fecha_desde_ts = datetime.strptime(fecha_desde_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()

    print("[INFO] Arrancando importador de Instagram (Playwright)", flush=True)

    posts = obtener_posts_del_perfil(ig_target, session_file)
    if not posts:
        return

    antes_filtro = len(posts)
    posts = [p for p in posts if (p.get("taken_at") or 0) >= fecha_desde_ts]
    print(
        f"[INFO] {len(posts)} de {antes_filtro} publicaciones están dentro del rango "
        f"(desde {fecha_desde_str})",
        flush=True,
    )
    if not posts:
        return

    # Instagram devuelve primero las publicaciones FIJADAS, sin importar su
    # fecha real. Las procesamos en orden cronológico (más antigua primero)
    # para que las noticias se creen en el orden en que de verdad ocurrieron,
    # en vez de que una fijada antigua parezca la más reciente.
    posts.sort(key=lambda p: p.get("taken_at") or 0)

    print(f"[INFO] Perfil {ig_target} obtenido correctamente, {len(posts)} publicaciones vistas", flush=True)

    noticias_existentes = obtener_noticias_existentes()
    titulares_existentes = {n.get("titular") for n in noticias_existentes}

    revisados = 0
    creados = 0
    for post in (posts[:max_posts] if max_posts else posts):
        revisados += 1
        shortcode = post.get("shortcode")
        if not shortcode:
            continue

        if ya_importado(shortcode, noticias_existentes):
            print(f"[SKIP] Ya importado: {shortcode}", flush=True)
            continue

        display_url = post.get("display_url")
        caption = post.get("caption", "")

        try:
            img_resp = requests.get(display_url, timeout=30)
            img_resp.raise_for_status()
            imagen_url = subir_a_cloudinary(img_resp.content)
        except Exception as e:
            print(f"[ERROR] No se pudo procesar la imagen de {shortcode}: {e}", flush=True)
            continue

        titular = generar_titular(caption, shortcode, post.get("taken_at"), titulares_existentes)
        contenido = construir_contenido(caption, shortcode)

        crear_noticia(titular, imagen_url, contenido, admin_dni)
        titulares_existentes.add(titular)
        creados += 1

    print(f"[FIN] Revisadas {revisados} publicaciones, {creados} noticias nuevas creadas.", flush=True)


if __name__ == "__main__":
    main()
