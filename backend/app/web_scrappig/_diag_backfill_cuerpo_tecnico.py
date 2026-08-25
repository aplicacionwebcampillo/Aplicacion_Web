"""Acción puntual (segunda pasada): el backfill anterior no ordenaba las
publicaciones por fecha antes de procesarlas (a diferencia del
sincronizador real), así que para quienes tenían más de una publicación
(fichaje + renovación) se guardó la más antigua en vez de la más reciente.
Esta vez se procesan las 5 fichas del cuerpo técnico (no solo 3) ordenadas
por fecha ascendente, para que la última publicación de cada uno sea la que
quede guardada. Se borra tras usarlo."""
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

# Nombre exacto en la ficha (para el PUT) + dorsal reservado que ya tiene
# cada uno en la BD (no se toca: solo se rellenan foto/biografia) + sigla
# esperada de su cargo. La sigla es la comprobación clave: Sergio Silva, por
# ejemplo, tiene una publicación antigua (nov. 2024) de cuando fichó como
# JUGADOR, antes de ser entrenador -- coincide por nombre pero no lleva la
# sigla "E", así que se descarta en vez de pisar sus datos de entrenador.
FICHA_POR_OBJETIVO = {
    "sergio silva": ("SERGIO SILVA JIMENEZ", 26, "E"),
    "javi salazar": ("Javi Salazar", 27, "2E"),
    "diego merlo": ("Diego Merlo", 28, "PF"),
    "juanjo mendoza": ("Juanjo Mendoza", 29, "EP"),
    "christian cortes": ("CHRISTIAN CORTES HERRANZ", 30, "DE"),
}


def main():
    ig_target = os.environ["IG_TARGET_USERNAME"]
    session_file = os.environ["IG_STORAGE_STATE_FILE"]

    print("[INFO] Descargando TODAS las publicaciones del perfil (sin filtro de fecha)...", flush=True)
    posts = obtener_posts_del_perfil(ig_target, session_file)
    print(f"[INFO] {len(posts)} publicaciones totales", flush=True)

    candidatas = [
        p for p in posts
        if any(nombre in _normalizar(p.get("caption")) for nombre in FICHA_POR_OBJETIVO)
    ]
    # Igual que el sincronizador real: se procesan de más antigua a más
    # reciente, así la última publicación de cada persona es la que
    # queda guardada al final (no la primera que se encuentre).
    candidatas.sort(key=lambda p: p.get("taken_at") or 0)
    print(f"[INFO] {len(candidatas)} publicaciones mencionan a alguno de los 5 objetivos, en orden cronológico", flush=True)

    clasificador = Clasificador()

    for post in candidatas:
        shortcode = post.get("shortcode")
        caption = post.get("caption", "")
        display_url = post.get("display_url")
        print(f"\n[INFO] --- {shortcode} (taken_at={post.get('taken_at')}) ---", flush=True)
        print(f"[INFO] Caption: {caption[:200]!r}", flush=True)

        try:
            img_resp = requests.get(display_url, timeout=30)
            img_resp.raise_for_status()
        except Exception as e:
            print(f"[ERROR] No se pudo descargar la imagen: {e}", flush=True)
            continue

        try:
            clasificacion = clasificador.clasificar(
                caption, img_resp.content, _media_type(img_resp.headers.get("Content-Type"))
            )
        except Exception as e:
            print(f"[ERROR] No se pudo clasificar {shortcode}: {e}", flush=True)
            continue
        print(f"[INFO] Clasificación: {clasificacion}", flush=True)

        if not clasificacion.nombre_jugador:
            print("[SKIP] Sin nombre_jugador", flush=True)
            continue

        objetivo = next(
            (n for n in FICHA_POR_OBJETIVO if n in _normalizar(clasificacion.nombre_jugador)
             or _normalizar(clasificacion.nombre_jugador) in n),
            None,
        )
        if not objetivo:
            print(
                f"[SKIP] '{clasificacion.nombre_jugador}' no coincide claramente con ninguno de los 5 objetivos",
                flush=True,
            )
            continue

        nombre_ficha, dorsal_actual, sigla_esperada = FICHA_POR_OBJETIVO[objetivo]

        if clasificacion.sigla != sigla_esperada:
            print(
                f"[SKIP] '{clasificacion.nombre_jugador}' coincide por nombre pero la sigla detectada "
                f"({clasificacion.sigla!r}) no es la esperada para su cargo ({sigla_esperada!r}); "
                "probablemente una publicación de otra época (ej. como jugador antes de ser cuerpo "
                "técnico), se descarta.",
                flush=True,
            )
            continue

        try:
            foto_url = subir_a_cloudinary(img_resp.content)
        except Exception as e:
            print(f"[ERROR] No se pudo subir la imagen a Cloudinary: {e}", flush=True)
            continue

        actualizar_jugador(nombre_ficha, None, dorsal_actual, foto_url, biografia=caption)


if __name__ == "__main__":
    main()
