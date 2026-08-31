"""Convierte cookies exportadas de un navegador ya logueado/verificado en
lapreferente.com al formato de sesión (storage_state) que usa
lapreferente_estadisticas_sync.py.

Por qué existe: lapreferente_generar_sesion.py abre una ventana de Firefox
local para pasar el chequeo de Cloudflare a mano, pero eso requiere una
pantalla (no vale en Termux/servidor sin GUI). Este script permite generar
la misma sesión a partir de cookies ya exportadas de un navegador real donde
el chequeo de Cloudflare ya se ha superado (por ejemplo Firefox para
Android, tras entrar normal en la web del club).

Uso:
    1. En un navegador real, entra en
       https://www.lapreferente.com/E38004/cd-campillo-del-rio-cf y espera a
       que cargue la tabla de la plantilla (Cloudflare puede tardar unos
       segundos o pedir marcar una casilla).
    2. Exporta las cookies del sitio con una extensión como "Cookie-Editor"
       (botón "Export" -> "Export as JSON"). Guarda ese JSON en un fichero,
       por ejemplo cookies_lapreferente.json.
    3. Ejecuta:
           python backend/app/web_scrappig/lapreferente_cookies_a_sesion.py \
               cookies_lapreferente.json lapreferente_storage_state.json
    4. Usa lapreferente_storage_state.json con
       lapreferente_estadisticas_sync.py como siempre.

Aviso: la cookie de verificación de Cloudflare (cf_clearance) suele durar
solo unas horas, no días. Hay que repetir este proceso cada vez que se
quiera sincronizar la plantilla.
"""

import json
import sys

SAMESITE_MAP = {
    "strict": "Strict",
    "lax": "Lax",
    "no_restriction": "None",
    "none": "None",
    "unspecified": "Lax",
}


def convertir_cookie(cookie_extension):
    dominio = cookie_extension.get("domain", "")
    if dominio and not dominio.startswith("."):
        dominio = "." + dominio if "lapreferente.com" in dominio else dominio

    es_sesion = cookie_extension.get("session", False)
    expira = cookie_extension.get("expirationDate")
    expires = -1 if es_sesion or expira is None else int(expira)

    same_site_original = str(cookie_extension.get("sameSite", "unspecified")).lower()

    return {
        "name": cookie_extension["name"],
        "value": cookie_extension["value"],
        "domain": dominio,
        "path": cookie_extension.get("path", "/"),
        "expires": expires,
        "httpOnly": bool(cookie_extension.get("httpOnly", False)),
        "secure": bool(cookie_extension.get("secure", True)),
        "sameSite": SAMESITE_MAP.get(same_site_original, "Lax"),
    }


def main():
    if len(sys.argv) != 3:
        print(
            "Uso: python lapreferente_cookies_a_sesion.py <cookies_exportadas.json> <salida_storage_state.json>",
            flush=True,
        )
        sys.exit(1)

    ruta_entrada, ruta_salida = sys.argv[1], sys.argv[2]

    with open(ruta_entrada, encoding="utf-8") as f:
        cookies_extension = json.load(f)

    cookies_lapreferente = [
        c for c in cookies_extension if "lapreferente.com" in c.get("domain", "")
    ]
    if not cookies_lapreferente:
        print(
            "[ERROR] No se encontró ninguna cookie de lapreferente.com en el fichero. "
            "Asegúrate de exportar las cookies estando en la pestaña de lapreferente.com.",
            flush=True,
        )
        sys.exit(1)

    nombres = {c["name"] for c in cookies_lapreferente}
    if "cf_clearance" not in nombres:
        print(
            "[AVISO] No se encontró la cookie 'cf_clearance' entre las exportadas: "
            "sin ella es probable que Cloudflare vuelva a mostrar el chequeo. "
            "Revisa que la tabla de la plantilla cargó del todo antes de exportar.",
            flush=True,
        )

    storage_state = {
        "cookies": [convertir_cookie(c) for c in cookies_lapreferente],
        "origins": [],
    }

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(storage_state, f)

    print(f"[OK] Sesión generada en {ruta_salida} a partir de {len(cookies_lapreferente)} cookies.", flush=True)
    print(
        "Recuerda: esta sesión caduca en unas horas (cf_clearance), no días.",
        flush=True,
    )


if __name__ == "__main__":
    main()
