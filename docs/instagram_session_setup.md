# Configurar la sesión de Instagram para el importador de noticias

La misma sesión de Instagram (`IG_STORAGE_STATE_B64` / `IG_TARGET_USERNAME`)
la usan dos workflows: el importador de noticias (`scraper_instagram.py`) y
el sincronizador de la plantilla (`instagram_jugadores_sync.py`). No hace
falta repetir esta configuración por separado para cada uno.

`scraper_instagram.py` usa Playwright (navegador real) con una sesión ya
autenticada a mano, en vez de hacer login por script. Se probó primero con
`instaloader` (incluso con cookies de sesión válidas) y Instagram lo seguía
bloqueando: un cliente HTTP "en crudo" tiene una huella distinta a la de un
navegador real y el sistema anti-bot lo detecta aunque la cookie sea
legítima. Por eso ahora se usa un navegador de verdad.

Esto solo hay que configurarlo una vez (y repetirlo si la sesión llega a
caducar/cerrarse).

## 1. Instala Playwright en tu entorno local

```bash
cd ~/Aplicacion_Web
source .venv_ig/bin/activate   # o el venv que uses
pip install playwright
playwright install firefox
```

## 2. Genera la sesión iniciando login manual

```bash
python backend/app/web_scrappig/instagram_generar_sesion.py ig_storage_state.json
```

Se abrirá una ventana de Firefox de verdad. Inicia sesión en Instagram con
normalidad ahí (resuelve cualquier verificación si te la pide). Cuando
tengas la sesión iniciada, vuelve a la terminal y pulsa Enter — se guardará
todo en `ig_storage_state.json`.

## 3. Codifica el fichero de sesión para guardarlo como secret

```bash
base64 -w0 ig_storage_state.json > /tmp/session_b64.txt
cat /tmp/session_b64.txt
```

Copia toda la salida (una única línea larga). **No la pegues en ningún
chat**: ese contenido da acceso completo a la cuenta de Instagram, igual
que la contraseña.

## 4. Configura los secrets en GitHub

En **Settings → Secrets and variables → Actions** del repositorio:

- `IG_STORAGE_STATE_B64`: pega el contenido de `/tmp/session_b64.txt`.
- `IG_TARGET_USERNAME`: usuario de Instagram del club (sin @), si no lo
  tienes ya configurado de antes.
- `NOTICIA_ADMIN_DNI`: DNI de un administrador existente en la BD.
- `GEMINI_API_KEY`: solo si vas a usar el sincronizador de plantilla
  (`instagram_jugadores_sync.py`), que necesita leer el dorsal en la imagen
  de los fichajes/renovaciones. Se obtiene gratis en
  https://ai.google.dev (API Keys), sin tarjeta de crédito.

Si tenías secrets antiguos de intentos anteriores (`IG_SESSION_USERNAME`,
`IG_SESSION_FILE_B64`, `IG_LOGIN_USER`, `IG_LOGIN_PASS`), puedes borrarlos:
ya no se usan.

## 5. Limpieza local

```bash
rm /tmp/session_b64.txt ig_storage_state.json
```

## 6. Probar

Lanza el workflow "Importar noticias desde Instagram" manualmente desde la
pestaña Actions. En el log deberías ver `[INFO] Perfil <usuario_del_club>
obtenido correctamente, N publicaciones vistas`.

## Cuándo repetir esto

Si la sesión caduca o Instagram la invalida, el script lo indicará con
`[ERROR] No se capturó la respuesta del perfil...`. Si pasa, repite los
pasos 2-4 para generar una sesión nueva.

## Alternativa: si Instagram rechaza el login en `instagram_generar_sesion.py`

A veces Instagram no deja iniciar sesión en ningún navegador "nuevo" que no
reconoce -- incógnito, otro navegador, o la ventana que abre Playwright --
mostrando un falso "contraseña incorrecta" aunque sea correcta, mientras que
en tu navegador de siempre (el que usas a diario) sí funciona. Esto no es un
bloqueo de la cuenta, es que Instagram solo confía en contextos de navegador
con historial ya establecido.

En ese caso, en vez de intentar iniciar sesión de nuevo en ningún sitio,
reutiliza la sesión que ya tienes autenticada en tu navegador de confianza:

1. En ese navegador, instala una extensión para exportar cookies, por
   ejemplo **Cookie-Editor** (Chrome/Firefox).
2. Con https://www.instagram.com abierto y logueado, abre la extensión y
   exporta las cookies del sitio como JSON (botón "Export" → "Export as
   JSON"). Guarda ese contenido en un fichero, por ejemplo
   `cookies_instagram.json`.
3. Conviértelo al formato que necesita el sincronizador:
   ```bash
   python backend/app/web_scrappig/instagram_cookies_a_sesion.py \
       cookies_instagram.json ig_storage_state.json
   ```
4. Sigue desde el paso 3 de más arriba (codificar en base64 y actualizar el
   secret `IG_STORAGE_STATE_B64`).
5. Borra `cookies_instagram.json` e `ig_storage_state.json` al terminar --
   dan acceso completo a la cuenta, igual que la contraseña.
