"""Actualiza partidos_jugados y goles de la plantilla desde la Tabla de
Goleadores pública de la RFAF (sin Cloudflare, sin JavaScript: se puede
ejecutar en un workflow programado sin intervención humana).

La RFAF no publica tarjetas, minutos ni titularidades por jugador (al menos
no se ha encontrado esa información de forma accesible), así que esos
campos solo se actualizan a mano con scraper_lapreferente_estadisticas.py.

No crea jugadores nuevos: solo actualiza a los que ya existen en la BD
(emparejados por nombre, igual que el resto de scripts de esta carpeta).

Variables de entorno:
  URL_GRUPO_RFAF   URL de la página de clasificación del grupo (de donde se
                   saca el enlace real a la Tabla de Goleadores). Por
                   defecto, el grupo Sénior del club.
"""

import os
import re
import unicodedata

import requests
from bs4 import BeautifulSoup

API_BASE = "https://aplicacion-web-m5oa.onrender.com"

URL_GRUPO_DEFAULT = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion"
    "?cod_primaria=1000120&codgrupo=48466095&codcompeticion=48466094"
)
BASE_RFAF = "https://www.rfaf.es"

# Subcadena (sin acentos, en minúsculas) para reconocer las filas del CLUB
# dentro de la tabla de goleadores, que lista jugadores de todo el grupo.
NOMBRE_EQUIPO_RFAF = os.environ.get("NOMBRE_EQUIPO_RFAF", "campillo")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


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


def obtener_url_goleadores(url_grupo):
    resp = requests.get(url_grupo, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    enlace = soup.find("a", string=re.compile("Tabla Goleadores", re.I))
    if not enlace or not enlace.get("href"):
        raise RuntimeError("No se encontró el enlace 'Tabla Goleadores' en la página del grupo")
    href = enlace["href"]
    return href if href.startswith("http") else f"{BASE_RFAF}/pnfg/NPcd/{href.lstrip('/')}"


def obtener_goleadores_del_equipo(url_goleadores):
    resp = requests.get(url_goleadores, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    tabla = None
    indices = {}
    for candidata in soup.select("table"):
        cabecera = candidata.find("tr")
        if not cabecera:
            continue
        etiquetas = [c.get_text(" ", strip=True) for c in cabecera.select("td, th")]
        etiquetas_norm = [_normalizar(e) for e in etiquetas]
        if "goles" in etiquetas_norm and any("partidos" in e for e in etiquetas_norm):
            tabla = candidata
            indices = {etiqueta: i for i, etiqueta in enumerate(etiquetas_norm)}
            break

    if tabla is None:
        raise RuntimeError("No se encontró la tabla de goleadores (cabecera con 'Goles'/'Partidos')")

    idx_jugador = indices.get("jugador", 0)
    idx_equipo = next((i for e, i in indices.items() if "equipo" in e), None)
    idx_pj = next((i for e, i in indices.items() if "partidos" in e), None)
    idx_goles = next((i for e, i in indices.items() if e == "goles"), indices.get("goles"))

    resultados = []
    for fila in tabla.select("tr")[1:]:
        celdas = [c.get_text(" ", strip=True) for c in fila.select("td, th")]
        if not celdas or idx_jugador >= len(celdas):
            continue
        nombre = celdas[idx_jugador].strip()
        if not nombre:
            continue
        equipo = celdas[idx_equipo].strip() if idx_equipo is not None and idx_equipo < len(celdas) else ""
        if NOMBRE_EQUIPO_RFAF not in _normalizar(equipo):
            continue
        resultados.append({
            "nombre": nombre,
            "partidos_jugados": _a_entero(celdas[idx_pj]) if idx_pj is not None and idx_pj < len(celdas) else 0,
            "goles": _a_entero(celdas[idx_goles]) if idx_goles is not None and idx_goles < len(celdas) else 0,
        })
    return resultados


def obtener_jugadores_existentes():
    resp = requests.get(f"{API_BASE}/jugadores/?skip=0&limit=500", timeout=30)
    resp.raise_for_status()
    return resp.json()


def buscar_jugador(nombre_buscado, jugadores):
    objetivo = _normalizar(nombre_buscado)
    if not objetivo:
        return None
    for jugador in jugadores:
        for candidato_nombre in (jugador.get("nombre"), jugador.get("nombre_corto"), jugador.get("nombre_completo")):
            candidato = _normalizar(candidato_nombre)
            if not candidato:
                continue
            if candidato == objetivo or candidato in objetivo or objetivo in candidato:
                return jugador
    return None


def actualizar_estadisticas(jugador, partidos_jugados, goles):
    resp = requests.put(
        f"{API_BASE}/jugadores/{jugador['nombre']}",
        json={"partidos_jugados": partidos_jugados, "goles": goles},
        timeout=30,
    )
    if resp.status_code == 200:
        print(f"[OK] {jugador['nombre']}: {partidos_jugados} PJ, {goles} goles", flush=True)
    else:
        print(f"[ERROR] {resp.status_code} al actualizar '{jugador['nombre']}': {resp.text}", flush=True)


def main():
    url_grupo = os.environ.get("URL_GRUPO_RFAF", URL_GRUPO_DEFAULT)

    print("[INFO] Buscando la Tabla de Goleadores...", flush=True)
    url_goleadores = obtener_url_goleadores(url_grupo)
    print(f"[INFO] URL: {url_goleadores}", flush=True)

    goleadores = obtener_goleadores_del_equipo(url_goleadores)
    print(f"[INFO] {len(goleadores)} jugadores del club en la tabla de goleadores", flush=True)
    if not goleadores:
        return

    jugadores_existentes = obtener_jugadores_existentes()

    for dato in goleadores:
        jugador = buscar_jugador(dato["nombre"], jugadores_existentes)
        if not jugador:
            print(f"[SKIP] '{dato['nombre']}': no hay jugador con ese nombre en la plantilla", flush=True)
            continue
        actualizar_estadisticas(jugador, dato["partidos_jugados"], dato["goles"])

    print("[FIN] Actualización de estadísticas desde la RFAF completada.", flush=True)


if __name__ == "__main__":
    main()
