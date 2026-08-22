"""Actualiza la plantilla (posición, nombre corto/legal, estado de
fichaje/renovación, y TODAS las estadísticas de la temporada: partidos
jugados, titularidades, minutos, goles, tarjetas) desde la tabla de la
plantilla de lapreferente.com.

Se ejecuta A MANO, en tu ordenador (no en un workflow programado): la web
está protegida por Cloudflare, cuyo reto solo se puede pasar con un humano
delante, y la sesión que lo consigue caduca en horas. Genera esa sesión con
lapreferente_generar_sesion.py antes de ejecutar este script.

Este script NO crea jugadores nuevos: lapreferente no publica el dorsal, y
sin dorsal un jugador no se puede guardar (esa parte la cubre
instagram_jugadores_sync.py). Solo actualiza a los jugadores que ya existen
en la plantilla, emparejándolos por nombre.

Uso:
    python backend/app/web_scrappig/lapreferente_estadisticas_sync.py [ruta_sesion]
"""

import re
import sys
import unicodedata

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

API_BASE = "https://aplicacion-web-m5oa.onrender.com"
BASE_URL = "https://www.lapreferente.com"
URL_PLANTILLA = f"{BASE_URL}/E38004/cd-campillo-del-rio-cf"
SESSION_FILE_DEFAULT = "lapreferente_storage_state.json"


def _normalizar(texto):
    if not texto:
        return ""
    sin_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return " ".join(sin_acentos.lower().split())


def _a_entero(texto):
    try:
        return int(re.sub(r"[^\d-]", "", texto or "") or 0)
    except ValueError:
        return 0


def _estado_fichaje(celda_nombre):
    img = celda_nombre.find("img", title=True)
    if not img:
        return None
    titulo = img["title"].lower()
    if "renov" in titulo:
        return "Renovado"
    if "fichaje" in titulo or "incorporaci" in titulo:
        return "Fichaje"
    return None


def extraer_jugadores(html):
    """Recorre la tabla de la plantilla. Las columnas de estadísticas
    (Edad, PJ, PT, Min, Goles, TA, TR) se leen SIEMPRE como las 7 últimas
    celdas de la fila, en ese orden — así no depende de cuántas columnas
    haya antes (foto, nombre...), que sí varían."""
    soup = BeautifulSoup(html, "html.parser")
    candidatas = [t for t in soup.select("table") if "Porteros (" in t.get_text(" ", strip=True)]
    tabla = min(candidatas, key=lambda t: len(t.get_text())) if candidatas else None
    if tabla is None:
        return []

    jugadores = []
    for fila in tabla.select("tr"):
        celdas = fila.select("td")
        if len(celdas) < 7:
            continue

        div_nombre = fila.select_one('td div[style*="flex-direction:column"]')
        if not div_nombre:
            continue
        spans = div_nombre.find_all("span")
        if len(spans) < 2:
            continue
        nombre_corto = spans[0].get_text(strip=True)
        nombre_completo = spans[1].get_text(strip=True)
        if not nombre_corto and not nombre_completo:
            continue

        celda_nombre = div_nombre.find_parent("td")
        estado = _estado_fichaje(celda_nombre)

        indice_celda_nombre = next((i for i, c in enumerate(celdas) if c is celda_nombre), None)
        posicion = None
        if indice_celda_nombre is not None and indice_celda_nombre + 1 < len(celdas):
            posicion = celdas[indice_celda_nombre + 1].get_text(" ", strip=True) or None

        _edad, pj, pt, minutos, goles, ta, tr = (c.get_text(" ", strip=True) for c in celdas[-7:])

        jugadores.append({
            "nombre_corto": nombre_corto,
            "nombre_completo": nombre_completo,
            "posicion": posicion,
            "estado_fichaje": estado,
            "partidos_jugados": _a_entero(pj),
            "partidos_titular": _a_entero(pt),
            "minutos": _a_entero(minutos),
            "goles": _a_entero(goles),
            "tarjetas_amarillas": _a_entero(ta),
            "tarjetas_rojas": _a_entero(tr),
        })
    return jugadores


def obtener_jugadores_existentes():
    resp = requests.get(f"{API_BASE}/jugadores/?skip=0&limit=500", timeout=30)
    resp.raise_for_status()
    return resp.json()


def buscar_jugador(nombre_corto, nombre_completo, jugadores):
    objetivos = [o for o in (_normalizar(nombre_completo), _normalizar(nombre_corto)) if o]
    for jugador in jugadores:
        candidatos = [
            _normalizar(jugador.get("nombre")),
            _normalizar(jugador.get("nombre_corto")),
            _normalizar(jugador.get("nombre_completo")),
        ]
        for objetivo in objetivos:
            for candidato in candidatos:
                if candidato and (candidato == objetivo or candidato in objetivo or objetivo in candidato):
                    return jugador
    return None


def actualizar_jugador(jugador_actual, datos):
    payload = dict(datos)
    if not payload.get("posicion"):
        # posicion es obligatoria en el modelo: si lapreferente no la trae
        # esta vez, no se toca la que ya hubiera.
        payload.pop("posicion", None)
    resp = requests.put(f"{API_BASE}/jugadores/{jugador_actual['nombre']}", json=payload, timeout=30)
    if resp.status_code == 200:
        print(f"[OK] {jugador_actual['nombre']} actualizado: {datos}", flush=True)
    else:
        print(f"[ERROR] {resp.status_code} al actualizar '{jugador_actual['nombre']}': {resp.text}", flush=True)


def main():
    session_file = sys.argv[1] if len(sys.argv) > 1 else SESSION_FILE_DEFAULT

    print("[INFO] Cargando plantilla de lapreferente.com...", flush=True)
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(storage_state=session_file)
        page = context.new_page()
        page.goto(URL_PLANTILLA, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(3000)
        titulo = page.title()
        if "moment" in titulo.lower() or "just a" in titulo.lower():
            print(
                "[ERROR] Cloudflare sigue bloqueando: regenera la sesión con "
                "lapreferente_generar_sesion.py",
                flush=True,
            )
            browser.close()
            return
        html = page.content()
        browser.close()

    jugadores_lapreferente = extraer_jugadores(html)
    print(f"[INFO] {len(jugadores_lapreferente)} jugadores encontrados en lapreferente", flush=True)
    if not jugadores_lapreferente:
        print("[AVISO] No se encontró la tabla de la plantilla. ¿Ha cambiado la web?", flush=True)
        return

    jugadores_existentes = obtener_jugadores_existentes()

    for datos in jugadores_lapreferente:
        jugador = buscar_jugador(datos["nombre_corto"], datos["nombre_completo"], jugadores_existentes)
        if not jugador:
            print(
                f"[SKIP] '{datos['nombre_completo'] or datos['nombre_corto']}': no está en la plantilla "
                "(lapreferente no puede crear jugadores nuevos, falta el dorsal)",
                flush=True,
            )
            continue
        actualizar_jugador(jugador, datos)

    print("[FIN] Sincronización desde lapreferente completada.", flush=True)


if __name__ == "__main__":
    main()
