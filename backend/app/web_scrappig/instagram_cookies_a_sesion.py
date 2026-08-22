"""Convierte cookies exportadas de un navegador ya logueado en Instagram al
formato de sesión (storage_state) que usan los scripts de scraping.

Por qué existe: Instagram rechaza el login (mensaje falso de "contraseña
incorrecta") en cualquier navegador/contexto que no reconoce -- incógnito,
otro navegador, o una ventana nueva de Playwright -- aunque la contraseña
sea correcta. Solo confía en un navegador con historial ya establecido. Este
script evita tener que iniciar sesión de nuevo en ningún sitio "nuevo":
reutiliza la sesión que YA tienes autenticada en tu navegador de confianza.

Uso:
    1. En tu navegador de siempre (donde SÍ puedes entrar en Instagram),
       instala una extensión para exportar cookies, por ejemplo "Cookie-Editor"
       (disponible para Chrome y Firefox).
    2. Entra en https://www.instagram.com ya logueado, abre la extensión,
       y exporta las cookies del sitio en formato JSON (botón "Export" ->
       "Export as JSON" en Cookie-Editor). Guarda ese JSON en un fichero,
       por ejemplo cookies_instagram.json.
    3. Ejecuta:
           python backend/app/web_scrappig/instagram_cookies_a_sesion.py \
               cookies_instagram.json ig_storage_state.json
    4. Sigue desde el paso 3 de docs/instagram_session_setup.md (codificar
       en base64 y actualizar el secret IG_STORAGE_STATE_B64).
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
        dominio = "." + dominio if "instagram.com" in dominio else dominio

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
            "Uso: python instagram_cookies_a_sesion.py <cookies_exportadas.json> <salida_storage_state.json>",
            flush=True,
        )
        sys.exit(1)

    ruta_entrada, ruta_salida = sys.argv[1], sys.argv[2]

    with open(ruta_entrada, encoding="utf-8") as f:
        cookies_extension = json.load(f)

    cookies_instagram = [
        c for c in cookies_extension if "instagram.com" in c.get("domain", "")
    ]
    if not cookies_instagram:
        print(
            "[ERROR] No se encontró ninguna cookie de instagram.com en el fichero. "
            "Asegúrate de exportar las cookies estando en la pestaña de instagram.com.",
            flush=True,
        )
        sys.exit(1)

    nombres = {c["name"] for c in cookies_instagram}
    if "sessionid" not in nombres:
        print(
            "[AVISO] No se encontró la cookie 'sessionid' entre las exportadas: "
            "sin ella la sesión no estará realmente autenticada. Revisa que "
            "exportaste las cookies estando logueado en instagram.com.",
            flush=True,
        )

    storage_state = {
        "cookies": [convertir_cookie(c) for c in cookies_instagram],
        "origins": [],
    }

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(storage_state, f)

    print(f"[OK] Sesión generada en {ruta_salida} a partir de {len(cookies_instagram)} cookies.", flush=True)
    print(
        "Este fichero da acceso completo a esa cuenta de Instagram: trátalo "
        "como una contraseña, no lo subas al repositorio ni lo compartas.",
        flush=True,
    )


if __name__ == "__main__":
    main()
