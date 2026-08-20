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

Variables opcionales:
  IG_MAX_POSTS           nº máximo de publicaciones a revisar por ejecución
                         (por defecto 5)
"""

import html
import json
import os
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


def generar_titular(caption, shortcode, titulares_existentes):
    primera_linea = ""
    if caption and caption.strip():
        primera_linea = caption.strip().splitlines()[0]
    base = primera_linea[:180].strip() or f"Publicación de Instagram ({shortcode})"

    titular = base[:200]
    if titular in titulares_existentes:
        sufijo = f" ({shortcode})"
        titular = base[: 200 - len(sufijo)] + sufijo
    return titular


def construir_contenido(caption, shortcode):
    texto = html.escape((caption or "").strip())
    parrafos = "".join(f"<p>{linea}</p>" for linea in texto.splitlines() if linea.strip())
    enlace = (
        f'<p><a href="https://www.instagram.com/p/{shortcode}/" '
        'target="_blank" rel="noopener noreferrer">Ver publicación en Instagram</a></p>'
    )
    marca = f"<!-- ig:{shortcode} -->"
    return f"{parrafos}{enlace}{marca}"


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


def _normalizar_post(node):
    shortcode = node.get("shortcode")
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

    return {"shortcode": shortcode, "display_url": display_url, "caption": caption}


def _buscar_posts_recursivo(obj, encontrados, vistos):
    """Recorre cualquier estructura JSON buscando objetos que tengan
    pinta de publicación de Instagram (shortcode + imagen), sin asumir
    en qué campo exacto del payload están anidados. Así no depende de
    adivinar el esquema de GraphQL que Instagram use en cada momento."""
    if isinstance(obj, dict):
        if "shortcode" in obj:
            post = _normalizar_post(obj)
            if post and post["shortcode"] not in vistos:
                vistos.add(post["shortcode"])
                encontrados.append(post)
        for valor in obj.values():
            _buscar_posts_recursivo(valor, encontrados, vistos)
    elif isinstance(obj, list):
        for item in obj:
            _buscar_posts_recursivo(item, encontrados, vistos)


def obtener_posts_del_perfil(ig_target, session_file):
    """Abre el perfil con un navegador real (sesión ya autenticada) y
    busca publicaciones en cualquiera de las respuestas JSON que el propio
    navegador reciba mientras carga la página (no se asume un endpoint
    concreto, porque Instagram cambia esto con frecuencia)."""
    encontrados = []
    vistos = set()
    peticiones_vistas = []
    respuestas_con_datos = 0

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(storage_state=session_file)
        page = context.new_page()

        def al_recibir_respuesta(response):
            nonlocal respuestas_con_datos
            peticiones_vistas.append(f"{response.status} {response.url}")
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
            for objeto in objetos:
                _buscar_posts_recursivo(objeto, encontrados, vistos)

        page.on("response", al_recibir_respuesta)
        page.goto(f"https://www.instagram.com/{ig_target}/", wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(3000)

        if not encontrados:
            print(f"[DEBUG] URL final tras cargar: {page.url}", flush=True)
            try:
                print(f"[DEBUG] Título de la página: {page.title()}", flush=True)
            except Exception:
                pass
            print(f"[DEBUG] {respuestas_con_datos} respuestas JSON parseadas, 0 publicaciones encontradas en ellas", flush=True)
            interesantes = [u for u in peticiones_vistas if "instagram" in u or "graphql" in u]
            for u in interesantes[-30:]:
                print(f"[DEBUG]   {u}", flush=True)

        browser.close()

    if not encontrados:
        print(
            "[ERROR] No se encontraron publicaciones en ninguna respuesta "
            "(posible bloqueo, sesión caducada, o cambio de formato)",
            flush=True,
        )

    return encontrados


def main():
    ig_target = os.environ["IG_TARGET_USERNAME"]
    admin_dni = os.environ["NOTICIA_ADMIN_DNI"]
    session_file = os.environ["IG_STORAGE_STATE_FILE"]
    max_posts = int(os.environ.get("IG_MAX_POSTS", "5"))

    print("[INFO] Arrancando importador de Instagram (Playwright)", flush=True)

    posts = obtener_posts_del_perfil(ig_target, session_file)
    if not posts:
        return

    print(f"[INFO] Perfil {ig_target} obtenido correctamente, {len(posts)} publicaciones vistas", flush=True)

    noticias_existentes = obtener_noticias_existentes()
    titulares_existentes = {n.get("titular") for n in noticias_existentes}

    revisados = 0
    creados = 0
    for post in posts[:max_posts]:
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

        titular = generar_titular(caption, shortcode, titulares_existentes)
        contenido = construir_contenido(caption, shortcode)

        crear_noticia(titular, imagen_url, contenido, admin_dni)
        titulares_existentes.add(titular)
        creados += 1

    print(f"[FIN] Revisadas {revisados} publicaciones, {creados} noticias nuevas creadas.", flush=True)


if __name__ == "__main__":
    main()
