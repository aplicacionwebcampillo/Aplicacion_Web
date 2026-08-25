"""Sincroniza la plantilla (Jugador) a partir de las publicaciones de
Instagram del club que anuncian fichajes, renovaciones o bajas -- tanto de
jugadores como de cuerpo técnico (entrenador, segundo entrenador, preparador
físico, entrenador de porteros, delegado de equipo; ver SIGLAS_CUERPO_TECNICO
más abajo). Se guardan en la misma tabla Jugador, con un dorsal reservado
(26-30) por cargo para que el frontend los distinga de los jugadores.

Reutiliza la obtención de publicaciones de scraper_instagram.py (sesión de
Playwright ya autenticada). Para cada publicación candidata (cuyo pie de
foto contiene palabras como "HERE WE GO", "NUEVA INCORPORACIÓN", "FICHAJE",
"RENOVADO" o "GRACIAS"), se envía el texto y la imagen a una IA con visión
para clasificarla y extraer los datos:

  - El TEXTO del pie de foto indica el tipo de publicación y el nombre de
    la persona.
  - El DORSAL (jugadores) o la SIGLA del cargo (cuerpo técnico) solo
    aparece en la IMAGEN (el gráfico del fichaje/renovación), en el mismo
    hueco del gráfico, así que se extrae con visión.
  - La foto se sube a Cloudinary (la imagen completa de la publicación, no
    un recorte) para que no dependa de la URL temporal de Instagram.

Como la cuota gratuita de cada proveedor de IA es limitada (incluso por
DÍA, no solo por minuto), se usa una CASCADA de proveedores: Gemini →
Mistral, en ese orden. En cuanto un proveedor agota su cuota, el resto de
la ejecución sigue automáticamente con el siguiente, sin intervención
humana — así una sola ejecución puede llegar a cubrir todo lo pendiente en
vez de depender de la cuota de uno solo. Solo se usan los proveedores cuya
clave esté configurada (basta con GEMINI_API_KEY para que funcione;
MISTRAL_API_KEY es opcional, para ampliar la cascada). Si TODOS los
proveedores configurados se quedan sin cuota en la misma ejecución, se
para limpio y se retoma en la siguiente.

(Se probó también Groq como tercer proveedor, pero ninguno de los modelos
disponibles en una cuenta gratuita tiene visión: se descartó.)

Reglas de negocio (indicadas por el club):
  - Si no se puede determinar el dorsal, el jugador NO se guarda (ni se crea
    ni se actualiza) hasta que una publicación posterior lo aclare.
  - fecha_nacimiento no se rellena aquí (ninguna de las dos fuentes la da de
    forma fiable): queda como se definió en otro sitio (opcional).
  - Una publicación tipo "Gracias <nombre>" se interpreta como baja: se
    elimina al jugador si existe.

El emparejamiento con jugadores ya existentes se hace por nombre
normalizado (sin acentos, en minúsculas, y aceptando apodos si comparten
alguna palabra con un jugador que ya tenga ese mismo dorsal), igual que ya
hace la API (los endpoints de jugador están indexados por nombre).

Hace falta recordar qué publicaciones ya se clasificaron: se guarda en
data/instagram_jugadores_procesados.json (fuera de backend/, para no
disparar un redespliegue del backend) para no volver a gastar cuota
reclasificando lo mismo en cada ejecución. El workflow de GitHub Actions
hace commit de ese fichero tras cada ejecución. Una publicación NO se marca
como procesada si el fallo es recuperable (fallo de red, límite de cuota, o
un dorsal ya usado por OTRO jugador que requiere revisión manual): esas se
reintentan en la siguiente ejecución.

Variables de entorno requeridas:
  IG_TARGET_USERNAME    usuario de Instagram del club (sin @)
  IG_STORAGE_STATE_FILE ruta al fichero de sesión (ver
                         instagram_generar_sesion.py)
  GEMINI_API_KEY        clave gratuita de la API de Gemini (Google AI
                         Studio: https://ai.google.dev). Primer proveedor
                         de la cascada.

Variables opcionales:
  MISTRAL_API_KEY           clave gratuita de Mistral (https://console.mistral.ai).
                             Segundo proveedor de la cascada, si está
                             configurada.
  MISTRAL_MODEL              modelo de Mistral a usar. Por defecto
                             mistral-small-latest.
  IG_JUGADORES_FECHA_DESDE  publicaciones anteriores a esta fecha
                            (YYYY-MM-DD) se ignoran. Por defecto 2025-12-30.
  ID_EQUIPO_SENIOR          id_equipo al que pertenecen los jugadores
                            creados. Por defecto 1 (primer equipo Sénior).
  IG_JUGADORES_ESTADO_FILE  ruta del fichero de progreso (publicaciones ya
                            procesadas). Por defecto
                            data/instagram_jugadores_procesados.json.
"""

import base64
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

GEMINI_MODEL = "gemini-3.5-flash"
MISTRAL_MODEL_DEFAULT = "mistral-small-latest"
FECHA_DESDE_DEFAULT = "2025-12-30"
ID_EQUIPO_SENIOR_DEFAULT = 1
POSICION_DEFAULT = "Sin especificar"

# Filtro previo por palabras clave: evita gastar llamadas a la IA en
# publicaciones que no son de fichajes/renovaciones/bajas (partidos,
# patrocinadores, etc.). La clasificación fina (fichaje/renovación/baja/
# otro) la hace después la IA con el texto completo.
PALABRAS_ALTA = [
    "here we go",
    "nueva incorporacion",
    "fichaje",
    "renovado",
    "renovacion",
]

# En una primera prueba real, filtrar solo por "gracias" en cualquier
# parte del texto disparó falsos positivos constantes (agradecimientos a
# patrocinadores, aficionados...), así que la baja solo se detecta si la
# publicación EMPIEZA por "gracias".

# Cada proveedor gratuito tiene su propio límite por minuto: se espera
# entre llamadas para no agotarlo de entrada. Gemini es el más estricto
# (5 peticiones/minuto observadas); para el resto, un margen prudente
# mientras no se demuestre lo contrario con uso real.
PAUSA_POR_PROVEEDOR = {"Gemini": 13, "Mistral": 3}
PAUSA_POR_DEFECTO = 5

REINTENTOS_LIMITE_CUOTA = 3
ESPERA_TRAS_LIMITE_SEGUNDOS = 35

# Fuera de backend/ y frontend/ a propósito: Render vigila esas carpetas
# para redesplegar automáticamente, y este fichero de estado (que el
# workflow actualiza y sube en cada ejecución) no debería disparar un
# redespliegue del backend cada vez.
ESTADO_FILE = os.environ.get("IG_JUGADORES_ESTADO_FILE", "data/instagram_jugadores_procesados.json")


class ProveedorAgotado(Exception):
    """La cuota gratuita del proveedor de IA actual (por minuto o por día)
    se ha agotado: hay que pasar al siguiente proveedor de la cascada."""


class TodosLosProveedoresAgotados(Exception):
    """Se han agotado las cuotas de TODOS los proveedores configurados:
    no queda nada que hacer hasta que alguna cuota se libere."""


def _cargar_procesados():
    try:
        with open(ESTADO_FILE, encoding="utf-8") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def _guardar_procesados(procesados):
    os.makedirs(os.path.dirname(ESTADO_FILE) or ".", exist_ok=True)
    with open(ESTADO_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(procesados), f, ensure_ascii=False, indent=2)
        f.write("\n")


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


# Las publicaciones de cuerpo técnico usan el mismo hueco de la imagen que
# el dorsal, pero con una sigla del cargo en vez de un número. El dorsal
# "reservado" de cada sigla es el mismo que ya usa la ficha de cada uno en
# la BD (ver DORSALES_CUERPO_TECNICO en JugadorDetalle.tsx), para que el
# frontend siga ocultándoles el dorsal/estadísticas de jugador.
SIGLAS_CUERPO_TECNICO = {
    "E": (26, "Entrenador"),
    "2E": (27, "Segundo Entrenador"),
    "PF": (28, "Preparador Físico"),
    "EP": (29, "Entrenador de Porteros"),
    "DE": (30, "Delegado de Equipo"),
}


class ClasificacionPost(BaseModel):
    tipo: Literal["fichaje", "renovacion", "baja", "otro"]
    nombre_jugador: Optional[str] = None
    dorsal: Optional[int] = None
    sigla: Optional[Literal["E", "2E", "PF", "EP", "DE"]] = None
    posicion: Optional[str] = None


def _construir_instrucciones(caption):
    return (
        "Esta es una publicación de Instagram del club de fútbol amateur "
        "Campillo del Río CF. El pie de foto (texto) suele indicar de qué "
        "jugador o miembro del cuerpo técnico se trata y si es un fichaje, "
        "una renovación o una despedida (baja), con palabras como \"HERE "
        "WE GO\", \"NUEVA INCORPORACIÓN\", \"FICHAJE\", \"RENOVADO\" "
        "(fichaje/renovación) o \"Gracias <nombre>\" (baja). En el mismo "
        "hueco del gráfico donde normalmente va el DORSAL (número de "
        "camiseta) de un jugador, las publicaciones de cuerpo técnico "
        "muestran en su lugar una SIGLA de su cargo: \"E\" (Entrenador), "
        "\"2E\" (Segundo Entrenador), \"PF\" (Preparador Físico), \"EP\" "
        "(Entrenador de Porteros) o \"DE\" (Delegado de Equipo). Mira ese "
        "hueco con atención: si hay un número, es el dorsal de un jugador; "
        "si hay una de esas siglas, es un miembro del cuerpo técnico (no "
        "un jugador, no lleva dorsal).\n\n"
        f"Texto de la publicación:\n{caption or '(sin texto)'}\n\n"
        "Clasifica la publicación y responde ÚNICAMENTE con un objeto JSON "
        "con esta forma exacta, sin texto ni bloques de código alrededor:\n"
        '{"tipo": "fichaje"|"renovacion"|"baja"|"otro", '
        '"nombre_jugador": string|null, "dorsal": integer|null, '
        '"sigla": "E"|"2E"|"PF"|"EP"|"DE"|null, "posicion": string|null}\n\n'
        "- tipo: \"fichaje\" (nueva incorporación), \"renovacion\" (persona "
        "que ya estaba y renueva), \"baja\" (despedida) u \"otro\" (no "
        "trata sobre una persona concreta, ej. resultado de partido, "
        "publicidad...).\n"
        "- nombre_jugador: el nombre de la persona (jugador o miembro del "
        "cuerpo técnico) tal y como aparece en el texto o la imagen (null "
        "si tipo es \"otro\").\n"
        "- dorsal: el número de dorsal que se ve en la imagen (null si en "
        "su lugar hay una sigla de cuerpo técnico, si no se ve ningún "
        "número, o si tipo es \"baja\"/\"otro\").\n"
        "- sigla: la sigla del cuerpo técnico que se ve en la imagen en "
        "vez de un número de dorsal (null si en su lugar hay un dorsal "
        "numérico, si no se ve ninguna sigla, o si tipo es "
        "\"baja\"/\"otro\").\n"
        "- posicion: la demarcación del jugador si se menciona o se ve en "
        "la imagen (ej. \"Portero\", \"Defensa\", \"Centrocampista\", "
        "\"Delantero\"), o null si no aparece o es cuerpo técnico."
    )


def _clasificar_gemini(api_key, caption, imagen_bytes, media_type):
    client = genai.Client(api_key=api_key)
    instrucciones = _construir_instrucciones(caption)

    for intento in range(1, REINTENTOS_LIMITE_CUOTA + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
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
            mensaje = str(e)
            if "PerDay" in mensaje:
                # Cuota DIARIA agotada: reintentar con espera no tiene
                # sentido (no se libera hasta el día siguiente).
                raise ProveedorAgotado(mensaje) from e
            limite_alcanzado = "RESOURCE_EXHAUSTED" in mensaje or "429" in mensaje
            if not limite_alcanzado:
                raise
            if intento == REINTENTOS_LIMITE_CUOTA:
                raise ProveedorAgotado(mensaje) from e
            print(
                f"[INFO] Límite de peticiones de Gemini alcanzado (intento {intento}/"
                f"{REINTENTOS_LIMITE_CUOTA}), esperando {ESPERA_TRAS_LIMITE_SEGUNDOS}s...",
                flush=True,
            )
            time.sleep(ESPERA_TRAS_LIMITE_SEGUNDOS)


def _segundos_de_reintento(resp):
    valor = resp.headers.get("Retry-After") or resp.headers.get("retry-after")
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def _clasificar_openai_compatible(url, api_key, modelo, caption, imagen_bytes, media_type):
    """Mistral expone una API de chat compatible con el formato de OpenAI
    (mensajes con bloques de texto + image_url en base64). Se usa request
    directo en vez de instalar el SDK propio, para no depender de una
    sintaxis de cliente que no se puede verificar aquí. Escrita de forma
    genérica (recibe la URL) por si en el futuro se añade otro proveedor
    compatible."""
    imagen_b64 = base64.standard_b64encode(imagen_bytes).decode("utf-8")
    instrucciones = _construir_instrucciones(caption)
    payload = {
        "model": modelo,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": instrucciones},
                {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{imagen_b64}"}},
            ],
        }],
    }

    for intento in range(1, REINTENTOS_LIMITE_CUOTA + 1):
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        if resp.status_code == 429:
            if intento == REINTENTOS_LIMITE_CUOTA:
                raise ProveedorAgotado(resp.text)
            espera = _segundos_de_reintento(resp) or ESPERA_TRAS_LIMITE_SEGUNDOS
            print(
                f"[INFO] 429 recibido (intento {intento}/{REINTENTOS_LIMITE_CUOTA}), "
                f"esperando {espera}s...",
                flush=True,
            )
            time.sleep(espera)
            continue
        resp.raise_for_status()
        contenido = resp.json()["choices"][0]["message"]["content"]
        return ClasificacionPost(**json.loads(contenido))


class Clasificador:
    """Cascada de proveedores de IA con visión: se prueba con el primero
    configurado y, en cuanto agota su cuota, se pasa automáticamente al
    siguiente para el resto de la ejecución (no se vuelve a intentar el
    proveedor agotado hasta la siguiente ejecución)."""

    def __init__(self):
        self._proveedores = []

        gemini_key = os.environ.get("GEMINI_API_KEY")
        if gemini_key:
            self._proveedores.append(("Gemini", lambda c, b, m: _clasificar_gemini(gemini_key, c, b, m)))

        mistral_key = os.environ.get("MISTRAL_API_KEY")
        if mistral_key:
            mistral_modelo = os.environ.get("MISTRAL_MODEL", MISTRAL_MODEL_DEFAULT)
            self._proveedores.append((
                "Mistral",
                lambda c, b, m: _clasificar_openai_compatible(
                    "https://api.mistral.ai/v1/chat/completions", mistral_key, mistral_modelo, c, b, m
                ),
            ))

        if not self._proveedores:
            raise RuntimeError(
                "No hay ninguna clave de proveedor configurada (GEMINI_API_KEY / MISTRAL_API_KEY)"
            )

        self._indice = 0
        print(
            f"[INFO] Cascada de proveedores configurada: {[n for n, _ in self._proveedores]}",
            flush=True,
        )

    def proveedor_actual(self):
        return self._proveedores[self._indice][0]

    def clasificar(self, caption, imagen_bytes, media_type):
        while self._indice < len(self._proveedores):
            nombre, funcion = self._proveedores[self._indice]
            try:
                return funcion(caption, imagen_bytes, media_type)
            except ProveedorAgotado:
                print(f"[INFO] Cuota de {nombre} agotada: pasando al siguiente proveedor...", flush=True)
                self._indice += 1
        raise TodosLosProveedoresAgotados()


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


def buscar_jugador_por_dorsal(nombre_buscado, dorsal, id_equipo, jugadores):
    # Respaldo cuando el nombre completo no coincide (apodos tipo "Alex"
    # por "Alejandro", "Fran" por "Francisco", "Kike" por "Enrique"...): si
    # ese dorsal ya lo tiene otro jugador del mismo equipo Y comparten al
    # menos una palabra del nombre (normalmente el apellido), se trata de
    # la misma persona. Sin esa coincidencia de palabra NO se asume: podría
    # ser un dorsal reciclado de un jugador distinto que se fue sin que
    # capturáramos su baja.
    tokens_buscado = set(_normalizar(nombre_buscado).split())
    if not tokens_buscado:
        return None
    for jugador in jugadores:
        if jugador.get("dorsal") != dorsal or jugador.get("id_equipo") != id_equipo:
            continue
        tokens_candidato = set(_normalizar(jugador.get("nombre")).split())
        if tokens_buscado & tokens_candidato:
            return jugador
    return None


def _reportar_fallo(resp, accion, nombre):
    if resp.status_code == 409:
        # Conflicto real de datos (p.ej. dorsal ya usado por OTRO jugador):
        # no se reintenta solo, necesita revisión manual (¿el jugador
        # anterior con ese dorsal se ha ido y falta su baja? ¿Gemini leyó
        # mal el número?). Se deja sin marcar como procesado para que
        # siga apareciendo en cada ejecución hasta que se resuelva.
        print(f"[SKIP] Conflicto al {accion} '{nombre}', revisión manual necesaria: {resp.text}", flush=True)
    else:
        print(f"[ERROR] {resp.status_code} al {accion} '{nombre}': {resp.text}", flush=True)


def crear_jugador(nombre, posicion, dorsal, foto, id_equipo, biografia=None):
    data = {
        "nombre": nombre,
        "posicion": posicion or POSICION_DEFAULT,
        "fecha_nacimiento": None,
        "foto": foto,
        "biografia": biografia,
        "dorsal": dorsal,
        "id_equipo": id_equipo,
    }
    resp = requests.post(f"{API_BASE}/jugadores/", json=data, timeout=30)
    if resp.status_code in (200, 201):
        print(f"[OK] Jugador creado: {nombre} (dorsal {dorsal})", flush=True)
        return True
    _reportar_fallo(resp, "crear jugador", nombre)
    return False


def actualizar_jugador(nombre_actual, posicion, dorsal, foto, biografia=None):
    data = {"dorsal": dorsal, "foto": foto}
    if posicion:
        data["posicion"] = posicion
    if biografia:
        data["biografia"] = biografia
    resp = requests.put(f"{API_BASE}/jugadores/{nombre_actual}", json=data, timeout=30)
    if resp.status_code == 200:
        print(f"[OK] Jugador actualizado: {nombre_actual} (dorsal {dorsal})", flush=True)
        return True
    _reportar_fallo(resp, "actualizar jugador", nombre_actual)
    return False


def _media_type(content_type):
    media_type = content_type.split(";")[0].strip() if content_type else "image/jpeg"
    if not media_type.startswith("image/"):
        media_type = "image/jpeg"
    return media_type


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

    procesados = _cargar_procesados()
    pendientes = [p for p in candidatas if p.get("shortcode") not in procesados]
    print(
        f"[INFO] {len(candidatas)} publicaciones candidatas de {len(posts)} en rango "
        f"({len(candidatas) - len(pendientes)} ya procesadas en ejecuciones anteriores, "
        f"{len(pendientes)} pendientes)",
        flush=True,
    )
    if not pendientes:
        return

    clasificador = Clasificador()

    for indice, post in enumerate(pendientes):
        if indice > 0:
            # Cada proveedor gratuito tiene su propio límite por minuto:
            # espaciamos las llamadas según cuál esté activo ahora mismo.
            pausa = PAUSA_POR_PROVEEDOR.get(clasificador.proveedor_actual(), PAUSA_POR_DEFECTO)
            time.sleep(pausa)

        shortcode = post.get("shortcode")
        caption = post.get("caption", "")
        display_url = post.get("display_url")
        terminado = False  # solo True si esta publicación no necesita reintentarse

        try:
            img_resp = requests.get(display_url, timeout=30)
            img_resp.raise_for_status()
        except Exception as e:
            print(f"[ERROR] No se pudo descargar la imagen de {shortcode}: {e}", flush=True)
            continue

        try:
            clasificacion = clasificador.clasificar(
                caption, img_resp.content, _media_type(img_resp.headers.get("Content-Type"))
            )
        except TodosLosProveedoresAgotados:
            print(
                "[FIN] Todos los proveedores de IA configurados han agotado su cuota: se "
                f"retoma en la siguiente ejecución programada. Procesadas {indice}/{len(pendientes)} "
                "publicaciones pendientes en esta ejecución.",
                flush=True,
            )
            break
        except Exception as e:
            print(f"[ERROR] No se pudo clasificar {shortcode}: {e}", flush=True)
            continue

        # La IA a veces devuelve el nombre con espacios de más al principio o
        # al final (p.ej. tras un salto de línea en la imagen): se recorta
        # aquí, en el único punto de entrada, para que ningún jugador se
        # guarde con un nombre "ROSENDO GALERA  " que luego rompa el enlace
        # a su ficha.
        if clasificacion.nombre_jugador:
            clasificacion.nombre_jugador = clasificacion.nombre_jugador.strip()
        if clasificacion.posicion:
            clasificacion.posicion = clasificacion.posicion.strip()

        if clasificacion.sigla:
            dorsal_reservado, posicion_por_defecto = SIGLAS_CUERPO_TECNICO[clasificacion.sigla]
            clasificacion.dorsal = dorsal_reservado
            clasificacion.posicion = clasificacion.posicion or posicion_por_defecto

        print(f"[INFO] {shortcode}: {clasificacion}", flush=True)

        if clasificacion.tipo == "otro" or not clasificacion.nombre_jugador:
            terminado = True
        else:
            # Se recarga en cada iteración para reflejar altas/bajas ya
            # hechas en publicaciones anteriores de esta misma ejecución.
            jugadores_existentes = obtener_jugadores_existentes()
            jugador_existente = buscar_jugador(clasificacion.nombre_jugador, jugadores_existentes)

            if (
                not jugador_existente
                and clasificacion.tipo in ("fichaje", "renovacion")
                and clasificacion.dorsal is not None
            ):
                por_dorsal = buscar_jugador_por_dorsal(
                    clasificacion.nombre_jugador, clasificacion.dorsal, id_equipo, jugadores_existentes
                )
                if por_dorsal:
                    print(
                        f"[INFO] '{clasificacion.nombre_jugador}' no coincide por nombre, pero el dorsal "
                        f"{clasificacion.dorsal} ya lo tiene '{por_dorsal['nombre']}': se trata como el "
                        "mismo jugador",
                        flush=True,
                    )
                    jugador_existente = por_dorsal

            if clasificacion.tipo == "baja":
                if jugador_existente:
                    eliminar_jugador(jugador_existente["nombre"])
                else:
                    print(
                        f"[SKIP] Baja de '{clasificacion.nombre_jugador}': no hay jugador con ese nombre",
                        flush=True,
                    )
                terminado = True

            elif clasificacion.dorsal is None:
                print(
                    f"[SKIP] '{clasificacion.nombre_jugador}': sin dorsal legible en la imagen, "
                    "no se guarda hasta que se conozca",
                    flush=True,
                )
                terminado = True

            else:
                try:
                    foto_url = subir_a_cloudinary(img_resp.content)
                except Exception as e:
                    print(f"[ERROR] No se pudo subir la imagen de {shortcode} a Cloudinary: {e}", flush=True)
                    foto_url = None

                if foto_url:
                    if jugador_existente:
                        terminado = actualizar_jugador(
                            jugador_existente["nombre"], clasificacion.posicion, clasificacion.dorsal, foto_url,
                            biografia=caption,
                        )
                    else:
                        terminado = crear_jugador(
                            clasificacion.nombre_jugador, clasificacion.posicion, clasificacion.dorsal,
                            foto_url, id_equipo, biografia=caption,
                        )

        if terminado:
            procesados.add(shortcode)
            _guardar_procesados(procesados)

    print("[FIN] Sincronización de plantilla completada.", flush=True)


if __name__ == "__main__":
    main()
