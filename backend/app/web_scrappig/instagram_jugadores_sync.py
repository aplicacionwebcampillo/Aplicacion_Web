"""Sincroniza la plantilla (Jugador) a partir de las publicaciones de
Instagram del club que anuncian fichajes, renovaciones o bajas.

Reutiliza la obtención de publicaciones de scraper_instagram.py (sesión de
Playwright ya autenticada). Para cada publicación candidata (cuyo pie de
foto contiene palabras como "HERE WE GO", "NUEVA INCORPORACIÓN", "FICHAJE",
"RENOVADO" o "GRACIAS"), se envía el texto y la imagen a la API gratuita de
Gemini (Google) para clasificarla y extraer los datos:

  - El TEXTO del pie de foto indica el tipo de publicación y el nombre del
    jugador.
  - El DORSAL solo aparece en la IMAGEN (el gráfico del fichaje/renovación),
    así que se extrae con visión.
  - La foto del jugador es la imagen completa de la publicación (no un
    recorte), subida a Cloudinary para que no dependa de la URL temporal de
    Instagram.

Reglas de negocio (indicadas por el club):
  - Si no se puede determinar el dorsal, el jugador NO se guarda (ni se crea
    ni se actualiza) hasta que una publicación posterior lo aclare.
  - fecha_nacimiento no se rellena aquí (ninguna de las dos fuentes la da de
    forma fiable): queda como se definió en otro sitio (opcional).
  - Una publicación tipo "Gracias <nombre>" se interpreta como baja: se
    elimina al jugador si existe.

El emparejamiento con jugadores ya existentes se hace por nombre
normalizado (sin acentos, en minúsculas), igual que ya hace la API (los
endpoints de jugador están indexados por nombre). Por eso no hace falta
guardar una marca de "ya procesado" por publicación: si se vuelve a
procesar la misma publicación, el resultado converge al mismo estado
(alta/actualización si el jugador no existe o ya existe con esos mismos
datos; baja si el jugador ya no existe, no hace nada).

Variables de entorno requeridas:
  IG_TARGET_USERNAME    usuario de Instagram del club (sin @)
  IG_STORAGE_STATE_FILE ruta al fichero de sesión (ver
                         instagram_generar_sesion.py)
  GEMINI_API_KEY        clave gratuita de la API de Gemini (Google AI
                         Studio: https://ai.google.dev), usada para leer
                         las imágenes de fichaje/renovación

Variables opcionales:
  IG_JUGADORES_FECHA_DESDE  publicaciones anteriores a esta fecha
                            (YYYY-MM-DD) se ignoran. Por defecto 2025-12-30.
  ID_EQUIPO_SENIOR          id_equipo al que pertenecen los jugadores
                            creados. Por defecto 1 (primer equipo Sénior).
"""

import json
import os
import sys
import time
import unicodedata
from datetime import datetime, timezone
from typing import Literal, Optional

import requests
from google import genai
from google.genai import types
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(__file__))
from scraper_instagram import (  # noqa: E402
    API_BASE,
    obtener_posts_del_perfil,
    subir_a_cloudinary,
)

MODEL = "gemini-3.5-flash"
FECHA_DESDE_DEFAULT = "2025-12-30"
ID_EQUIPO_SENIOR_DEFAULT = 1
POSICION_DEFAULT = "Sin especificar"

# Filtro previo por palabras clave: evita gastar llamadas a Gemini en
# publicaciones que no son de fichajes/renovaciones/bajas (partidos,
# patrocinadores, etc.). La clasificación fina (fichaje/renovación/baja/
# otro) la hace después Gemini con el texto completo.
PALABRAS_ALTA = [
    "here we go",
    "nueva incorporacion",
    "fichaje",
    "renovado",
    "renovacion",
]

# La cuota gratuita de Gemini es de solo 5 peticiones/minuto: hay que
# espaciar las llamadas y reintentar con espera cuando se agota. En una
# primera prueba real, filtrar solo por "gracias" en cualquier parte del
# texto disparó falsos positivos constantes (agradecimientos a
# patrocinadores, aficionados...), así que la baja solo se detecta si la
# publicación EMPIEZA por "gracias".
RATE_LIMIT_SLEEP_SECONDS = 13
REINTENTOS_LIMITE_CUOTA = 3
ESPERA_TRAS_LIMITE_SEGUNDOS = 35


def _normalizar(texto):
    if not texto:
        return ""
    sin_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return " ".join(sin_acentos.lower().split())


def _es_posible_baja(caption):
    lineas = [l for l in (caption or "").splitlines() if l.strip()]
    if not lineas:
        return False
    return _normalizar(lineas[0]).startswith("gracias")


def es_candidata(caption):
    caption_norm = _normalizar(caption)
    return any(palabra in caption_norm for palabra in PALABRAS_ALTA) or _es_posible_baja(caption)


class ClasificacionPost(BaseModel):
    tipo: Literal["fichaje", "renovacion", "baja", "otro"]
    nombre_jugador: Optional[str] = None
    dorsal: Optional[int] = None
    posicion: Optional[str] = None


def clasificar_post(client, caption, imagen_bytes, content_type):
    media_type = content_type.split(";")[0].strip() if content_type else "image/jpeg"
    if not media_type.startswith("image/"):
        media_type = "image/jpeg"

    instrucciones = (
        "Esta es una publicación de Instagram del club de fútbol amateur "
        "Campillo del Río CF. El pie de foto (texto) suele indicar de qué "
        "jugador se trata y si es un fichaje, una renovación o una "
        "despedida (baja), con palabras como \"HERE WE GO\", \"NUEVA "
        "INCORPORACIÓN\", \"FICHAJE\", \"RENOVADO\" (fichaje/renovación) o "
        "\"Gracias <nombre>\" (baja). El DORSAL (número de camiseta) casi "
        "siempre solo aparece en la imagen, no en el texto: míralo con "
        "atención en el gráfico.\n\n"
        f"Texto de la publicación:\n{caption or '(sin texto)'}\n\n"
        "Clasifica la publicación:\n"
        "- tipo: \"fichaje\" (nuevo jugador), \"renovacion\" (jugador que ya "
        "estaba y renueva), \"baja\" (despedida de un jugador) u \"otro\" "
        "(no trata sobre un jugador concreto, ej. resultado de partido, "
        "publicidad...).\n"
        "- nombre_jugador: el nombre del jugador tal y como aparece en el "
        "texto o la imagen (null si tipo es \"otro\").\n"
        "- dorsal: el número de dorsal que se ve en la imagen (null si no "
        "se ve ningún número o tipo es \"baja\"/\"otro\").\n"
        "- posicion: la demarcación del jugador si se menciona o se ve en "
        "la imagen (ej. \"Portero\", \"Defensa\", \"Centrocampista\", "
        "\"Delantero\"), o null si no aparece."
    )

    for intento in range(1, REINTENTOS_LIMITE_CUOTA + 1):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=[
                    instrucciones,
                    types.Part.from_bytes(data=imagen_bytes, mime_type=media_type),
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_json_schema=ClasificacionPost.model_json_schema(),
                ),
            )
            return ClasificacionPost(**json.loads(response.text))
        except Exception as e:
            limite_alcanzado = "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e)
            if not limite_alcanzado or intento == REINTENTOS_LIMITE_CUOTA:
                raise
            print(
                f"[INFO] Límite de peticiones de Gemini alcanzado (intento {intento}/"
                f"{REINTENTOS_LIMITE_CUOTA}), esperando {ESPERA_TRAS_LIMITE_SEGUNDOS}s...",
                flush=True,
            )
            time.sleep(ESPERA_TRAS_LIMITE_SEGUNDOS)


def obtener_jugadores_existentes():
    resp = requests.get(f"{API_BASE}/jugadores/?skip=0&limit=500", timeout=30)
    resp.raise_for_status()
    return resp.json()


def buscar_jugador(nombre_buscado, jugadores):
    objetivo = _normalizar(nombre_buscado)
    if not objetivo:
        return None
    for jugador in jugadores:
        candidato = _normalizar(jugador.get("nombre"))
        if not candidato:
            continue
        if candidato == objetivo or candidato in objetivo or objetivo in candidato:
            return jugador
    return None


def crear_jugador(nombre, posicion, dorsal, foto, id_equipo):
    data = {
        "nombre": nombre,
        "posicion": posicion or POSICION_DEFAULT,
        "fecha_nacimiento": None,
        "foto": foto,
        "biografia": None,
        "dorsal": dorsal,
        "id_equipo": id_equipo,
    }
    resp = requests.post(f"{API_BASE}/jugadores/", json=data, timeout=30)
    if resp.status_code in (200, 201):
        print(f"[OK] Jugador creado: {nombre} (dorsal {dorsal})", flush=True)
    else:
        print(f"[ERROR] {resp.status_code} al crear jugador '{nombre}': {resp.text}", flush=True)


def actualizar_jugador(nombre_actual, posicion, dorsal, foto):
    data = {"dorsal": dorsal, "foto": foto}
    if posicion:
        data["posicion"] = posicion
    resp = requests.put(f"{API_BASE}/jugadores/{nombre_actual}", json=data, timeout=30)
    if resp.status_code == 200:
        print(f"[OK] Jugador actualizado: {nombre_actual} (dorsal {dorsal})", flush=True)
    else:
        print(f"[ERROR] {resp.status_code} al actualizar jugador '{nombre_actual}': {resp.text}", flush=True)


def eliminar_jugador(nombre_actual):
    resp = requests.delete(f"{API_BASE}/jugadores/{nombre_actual}", timeout=30)
    if resp.status_code == 200:
        print(f"[OK] Jugador dado de baja: {nombre_actual}", flush=True)
    else:
        print(f"[ERROR] {resp.status_code} al dar de baja a '{nombre_actual}': {resp.text}", flush=True)


def main():
    ig_target = os.environ["IG_TARGET_USERNAME"]
    session_file = os.environ["IG_STORAGE_STATE_FILE"]
    id_equipo = int(os.environ.get("ID_EQUIPO_SENIOR", ID_EQUIPO_SENIOR_DEFAULT))

    fecha_desde_str = os.environ.get("IG_JUGADORES_FECHA_DESDE", FECHA_DESDE_DEFAULT)
    fecha_desde_ts = datetime.strptime(fecha_desde_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()

    print("[INFO] Arrancando sincronizador de plantilla desde Instagram", flush=True)

    posts = obtener_posts_del_perfil(ig_target, session_file)
    if not posts:
        return

    posts = [p for p in posts if (p.get("taken_at") or 0) >= fecha_desde_ts]
    posts.sort(key=lambda p: p.get("taken_at") or 0)
    candidatas = [p for p in posts if es_candidata(p.get("caption"))]
    print(f"[INFO] {len(candidatas)} publicaciones candidatas de {len(posts)} en rango", flush=True)
    if not candidatas:
        return

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    for indice, post in enumerate(candidatas):
        if indice > 0:
            # La cuota gratuita de Gemini es de solo 5 peticiones/minuto:
            # espaciamos las llamadas para no agotarla de entrada.
            time.sleep(RATE_LIMIT_SLEEP_SECONDS)

        shortcode = post.get("shortcode")
        caption = post.get("caption", "")
        display_url = post.get("display_url")

        try:
            img_resp = requests.get(display_url, timeout=30)
            img_resp.raise_for_status()
        except Exception as e:
            print(f"[ERROR] No se pudo descargar la imagen de {shortcode}: {e}", flush=True)
            continue

        try:
            clasificacion = clasificar_post(
                client, caption, img_resp.content, img_resp.headers.get("Content-Type")
            )
        except Exception as e:
            print(f"[ERROR] No se pudo clasificar {shortcode}: {e}", flush=True)
            continue

        print(f"[INFO] {shortcode}: {clasificacion}", flush=True)

        if clasificacion.tipo == "otro" or not clasificacion.nombre_jugador:
            continue

        # Se recarga en cada iteración para reflejar altas/bajas ya hechas
        # en publicaciones anteriores de esta misma ejecución.
        jugadores_existentes = obtener_jugadores_existentes()
        jugador_existente = buscar_jugador(clasificacion.nombre_jugador, jugadores_existentes)

        if clasificacion.tipo == "baja":
            if jugador_existente:
                eliminar_jugador(jugador_existente["nombre"])
            else:
                print(f"[SKIP] Baja de '{clasificacion.nombre_jugador}': no hay jugador con ese nombre", flush=True)
            continue

        # fichaje o renovación
        if clasificacion.dorsal is None:
            print(
                f"[SKIP] '{clasificacion.nombre_jugador}': sin dorsal legible en la imagen, "
                "no se guarda hasta que se conozca",
                flush=True,
            )
            continue

        try:
            foto_url = subir_a_cloudinary(img_resp.content)
        except Exception as e:
            print(f"[ERROR] No se pudo subir la imagen de {shortcode} a Cloudinary: {e}", flush=True)
            continue

        if jugador_existente:
            actualizar_jugador(
                jugador_existente["nombre"], clasificacion.posicion, clasificacion.dorsal, foto_url
            )
        else:
            crear_jugador(
                clasificacion.nombre_jugador, clasificacion.posicion, clasificacion.dorsal, foto_url, id_equipo
            )

    print("[FIN] Sincronización de plantilla completada.", flush=True)


if __name__ == "__main__":
    main()
