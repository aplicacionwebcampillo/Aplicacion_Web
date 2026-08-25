"""Acción puntual: Javi Salazar, Diego Merlo y Juanjo Mendoza (cuerpo
técnico) se crearon a mano sin foto ni biografía -- sus publicaciones de
Instagram nunca pasaron por el sincronizador (probablemente porque son
anteriores a IG_JUGADORES_FECHA_DESDE). Este script busca sus publicaciones
sin el filtro de fecha, las clasifica con la misma IA (ya con reconocimiento
de siglas) y actualiza directamente su foto/biografía. No toca el fichero de
progreso: es un backfill puntual, no una ejecución normal. Se borra tras
usarlo."""
import os
import sys

sys.path.insert(0, "backend/app/web_scrappig")

import requests  # noqa: E402
from scraper_instagram import obtener_posts_del_perfil, subir_a_cloudinary  # noqa: E402
from instagram_jugadores_sync import (  # noqa: E402
    Clasificador,
    _media_type,
    _normalizar,
    actualizar_jugador,
)

NOMBRES_OBJETIVO = ["javi salazar", "diego merlo", "juanjo mendoza"]

# Nombre exacto en la ficha (para el PUT) + dorsal reservado que YA tienen
# correctamente en la BD (no se toca: solo se rellenan foto/biografia).
FICHA_POR_OBJETIVO = {
    "javi salazar": ("Javi Salazar", 27),
    "diego merlo": ("Diego Merlo", 28),
    "juanjo mendoza": ("Juanjo Mendoza", 29),
}


def main():
    ig_target = os.environ["IG_TARGET_USERNAME"]
    session_file = os.environ["IG_STORAGE_STATE_FILE"]

    print("[INFO] Descargando TODAS las publicaciones del perfil (sin filtro de fecha)...", flush=True)
    posts = obtener_posts_del_perfil(ig_target, session_file)
    print(f"[INFO] {len(posts)} publicaciones totales", flush=True)

    candidatas = [
        p for p in posts
        if any(nombre in _normalizar(p.get("caption")) for nombre in NOMBRES_OBJETIVO)
    ]
    print(f"[INFO] {len(candidatas)} publicaciones mencionan a alguno de los 3 objetivos", flush=True)

    clasificador = Clasificador()

    for post in candidatas:
        shortcode = post.get("shortcode")
        caption = post.get("caption", "")
        display_url = post.get("display_url")
        print(f"\n[INFO] --- {shortcode} ---", flush=True)
        print(f"[INFO] Caption: {caption[:200]!r}", flush=True)

        try:
            img_resp = requests.get(display_url, timeout=30)
            img_resp.raise_for_status()
        except Exception as e:
            print(f"[ERROR] No se pudo descargar la imagen: {e}", flush=True)
            continue

        clasificacion = clasificador.clasificar(
            caption, img_resp.content, _media_type(img_resp.headers.get("Content-Type"))
        )
        print(f"[INFO] Clasificación: {clasificacion}", flush=True)

        if not clasificacion.nombre_jugador:
            print("[SKIP] Sin nombre_jugador", flush=True)
            continue

        objetivo = next(
            (n for n in NOMBRES_OBJETIVO if n in _normalizar(clasificacion.nombre_jugador)
             or _normalizar(clasificacion.nombre_jugador) in n),
            None,
        )
        if not objetivo:
            print(
                f"[SKIP] '{clasificacion.nombre_jugador}' no coincide claramente con ninguno de los 3 objetivos",
                flush=True,
            )
            continue

        try:
            foto_url = subir_a_cloudinary(img_resp.content)
        except Exception as e:
            print(f"[ERROR] No se pudo subir la imagen a Cloudinary: {e}", flush=True)
            continue

        # Los 3 objetivos ya existen en la BD con el nombre y dorsal exactos
        # que figuran en su ficha (ver diagnóstico previo): se actualiza ESE
        # nombre exacto y se reenvía el MISMO dorsal que ya tenían (no None:
        # el campo es NOT NULL en la BD), sin tocar la posición.
        nombre_ficha, dorsal_actual = FICHA_POR_OBJETIVO[objetivo]

        actualizar_jugador(nombre_ficha, None, dorsal_actual, foto_url, biografia=caption)


if __name__ == "__main__":
    main()
