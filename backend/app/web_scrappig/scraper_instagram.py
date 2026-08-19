"""Importa las últimas publicaciones de Instagram del club como Noticias.

No usa la Graph API oficial (requiere cuenta Business/Creator y acceso que
no tenemos); usa `instaloader` para leer el perfil público. Es una solución
de mejor esfuerzo: Instagram puede bloquear o limitar el acceso anónimo, por
eso el workflow que ejecuta este script corre con una frecuencia baja
(ver .github/workflows/scraper_instagram.yml) en vez de a diario.

Solo depende de `instaloader` y `requests` (no de app.database ni del resto
del backend): habla con la API pública igual que scraper.py, así no necesita
credenciales de base de datos.

Variables de entorno requeridas:
  IG_TARGET_USERNAME   usuario de Instagram del club (sin @)
  NOTICIA_ADMIN_DNI    DNI de un administrador ya existente en la BD,
                        se usará como autor de las noticias importadas

Variables opcionales:
  IG_LOGIN_USER / IG_LOGIN_PASS  credenciales de una cuenta de Instagram
                        para autenticar la sesión (mejora la fiabilidad,
                        pero esa cuenta también puede ser limitada/baneada
                        si Instagram detecta scraping)
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
    login_user = os.environ.get("IG_LOGIN_USER")
    login_pass = os.environ.get("IG_LOGIN_PASS")
    max_posts = int(os.environ.get("IG_MAX_POSTS", "5"))

    loader = instaloader.Instaloader(
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
    )

    if login_user and login_pass:
        try:
            loader.login(login_user, login_pass)
            print(f"[INFO] Sesión iniciada como {login_user}")
        except Exception as e:
            print(f"[AVISO] No se pudo iniciar sesión en Instagram, se continúa sin login: {e}")
    else:
        print("[INFO] Sin credenciales de Instagram: acceso anónimo (más propenso a bloqueos)")

    perfil = instaloader.Profile.from_username(loader.context, ig_target)

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
