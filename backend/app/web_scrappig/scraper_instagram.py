"""Importa las últimas publicaciones de Instagram del club como Noticias.

No usa la Graph API oficial (requiere cuenta Business/Creator y acceso que
no tenemos); usa `instaloader` para leer el perfil público. Es una solución
de mejor esfuerzo: Instagram puede bloquear o limitar el acceso, por eso el
workflow que ejecuta este script corre con una frecuencia baja (ver
.github/workflows/scraper_instagram.yml) en vez de a diario.

El script NUNCA hace login con usuario/contraseña por su cuenta: eso es lo
que dispara los bloqueos de Instagram. En su lugar reutiliza una sesión ya
autenticada manualmente en un navegador real (ver
docs/instagram_session_setup.md para los pasos exactos) y exportada con:

    instaloader --load-cookies firefox --login <usuario>

Solo depende de `instaloader` y `requests` (no de app.database ni del resto
del backend): habla con la API pública igual que scraper.py, así no necesita
credenciales de base de datos.

Variables de entorno requeridas:
  IG_TARGET_USERNAME   usuario de Instagram del club (sin @)
  NOTICIA_ADMIN_DNI    DNI de un administrador ya existente en la BD,
                        se usará como autor de las noticias importadas

Variables opcionales:
  IG_SESSION_USERNAME  usuario de Instagram cuya sesión guardada se reutiliza
  IG_SESSION_FILE       ruta al fichero de sesión exportado con
                        `instaloader --load-cookies firefox --login`
                        (sin estas dos variables, el script cae a acceso
                        anónimo, mucho más propenso a bloqueos)
  IG_MAX_POSTS          nº máximo de publicaciones a revisar por ejecución
                        (por defecto 5)
"""

import html
import os

import instaloader
import requests

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
        print(f"[OK] Noticia creada: {titular}")
    else:
        print(f"[ERROR] {resp.status_code} al crear noticia '{titular}': {resp.text}")


def main():
    ig_target = os.environ["IG_TARGET_USERNAME"]
    admin_dni = os.environ["NOTICIA_ADMIN_DNI"]
    session_username = os.environ.get("IG_SESSION_USERNAME")
    session_file = os.environ.get("IG_SESSION_FILE")
    max_posts = int(os.environ.get("IG_MAX_POSTS", "5"))

    print("[INFO] Arrancando importador de Instagram", flush=True)

    loader = instaloader.Instaloader(
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        max_connection_attempts=1,  # fallar rápido en vez de reintentar ~11 min contra un bloqueo de IP
    )

    # No se hace login por usuario/contraseña desde el script: eso es justo lo
    # que Instagram detecta y bloquea. En su lugar se reutiliza una sesión ya
    # autenticada manualmente (ver README junto a este archivo / instrucciones
    # del workflow) exportada con `instaloader --load-cookies firefox --login`.
    if session_username and session_file:
        try:
            loader.load_session_from_file(session_username, filename=session_file)
            print(f"[INFO] Sesión cargada para {session_username}", flush=True)
        except Exception as e:
            print(f"[AVISO] No se pudo cargar la sesión guardada, se continúa sin login: {e}", flush=True)
    else:
        print("[INFO] Sin sesión configurada: acceso anónimo (más propenso a bloqueos)", flush=True)

    perfil = instaloader.Profile.from_username(loader.context, ig_target)
    print(f"[INFO] Perfil {ig_target} obtenido correctamente", flush=True)

    noticias_existentes = obtener_noticias_existentes()
    titulares_existentes = {n.get("titular") for n in noticias_existentes}

    revisados = 0
    creados = 0
    for post in perfil.get_posts():
        if revisados >= max_posts:
            break
        revisados += 1

        if ya_importado(post.shortcode, noticias_existentes):
            print(f"[SKIP] Ya importado: {post.shortcode}")
            continue

        try:
            img_resp = requests.get(post.url, timeout=30)
            img_resp.raise_for_status()
            imagen_url = subir_a_cloudinary(img_resp.content)
        except Exception as e:
            print(f"[ERROR] No se pudo procesar la imagen de {post.shortcode}: {e}")
            continue

        titular = generar_titular(post.caption, post.shortcode, titulares_existentes)
        contenido = construir_contenido(post.caption, post.shortcode)

        crear_noticia(titular, imagen_url, contenido, admin_dni)
        titulares_existentes.add(titular)
        creados += 1

    print(f"[FIN] Revisadas {revisados} publicaciones, {creados} noticias nuevas creadas.")


if __name__ == "__main__":
    main()
