# Ejecutar la sincronización de lapreferente.com desde el móvil

`lapreferente_estadisticas_sync.py` no puede lanzarse desde GitHub Actions:
lapreferente.com está protegido por Cloudflare y solo responde bien desde
una conexión "de confianza" (no un runner en un datacenter), y el script usa
un navegador real (Playwright + Firefox) para leer la página, no peticiones
HTTP sueltas. Por eso hay que ejecutarlo a mano, desde tu propia red.

El problema en Android: Termux por sí solo no puede ejecutar los binarios de
Firefox que descarga Playwright (están compilados para glibc, y Termux usa
la libc de Android, incompatible). La solución es instalar un Linux de
verdad dentro de Termux con **proot-distro**.

Esto solo hay que configurarlo una vez.

## 1. Instala Termux y proot-distro

Instala **Termux** desde F-Droid (la versión de Google Play está
descontinuada y no recibe actualizaciones). Luego:

```bash
pkg update && pkg install proot-distro
proot-distro install debian
proot-distro login debian
```

El último comando te mete dentro del Debian instalado (a partir de ahora,
todo se ejecuta ahí dentro; `proot-distro login debian` para volver a entrar
en sesiones futuras).

## 2. Instala Python y Playwright dentro del Debian

```bash
apt update && apt install -y python3 python3-pip python3-venv git
git clone --depth 1 https://github.com/aplicacionwebcampillo/Aplicacion_Web.git
cd Aplicacion_Web
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4 playwright
playwright install --with-deps firefox
```

`playwright install --with-deps firefox` puede tardar varios minutos
(descarga el navegador y sus librerías). Si `--with-deps` falla por algún
paquete que `apt` no encuentra, prueba solo `playwright install firefox` —
en Debian suele bastar.

## 3. Cada vez que quieras sincronizar

1. En **Firefox para Android** (con la extensión **Cookie-Editor**
   instalada desde addons.mozilla.org), entra en
   `https://www.lapreferente.com/E38004/cd-campillo-del-rio-cf` y espera a
   que cargue del todo la tabla de la plantilla (Cloudflare puede tardar
   unos segundos o pedir marcar una casilla).
2. Toca el icono de Cookie-Editor → **Export** → **Export as JSON**. Copia
   ese JSON.
3. En Termux, entra en el Debian y pega el JSON en un fichero:
   ```bash
   proot-distro login debian
   cd Aplicacion_Web && source .venv/bin/activate
   nano cookies_lapreferente.json   # pega el JSON, Ctrl+O para guardar, Ctrl+X para salir
   ```
4. Lanza la sincronización:
   ```bash
   bash backend/app/web_scrappig/actualizar_lapreferente_movil.sh cookies_lapreferente.json
   ```
5. Borra el fichero de cookies al terminar (da acceso a esa sesión, aunque
   dura solo unas horas):
   ```bash
   rm cookies_lapreferente.json
   ```

Si el script vuelve a fallar con un aviso de Cloudflare, repite los pasos
1-4 — la cookie `cf_clearance` caduca en horas, no en días.

## Alternativa sin proot-distro (menos recomendable)

Si prefieres no instalar Debian, también puedes conectarte por SSH a tu
propio ordenador desde el móvil (con **Termux + `ssh`**, o cualquier cliente
SSH) y ejecutar ahí `actualizar_lapreferente.sh` de siempre — el ordenador
sí tiene Playwright ya instalado. En ese caso no hace falta nada de esta
guía, solo tener el ordenador encendido y accesible en la red.
