# Configurar la sesión de lapreferente.com para la sincronización automática

`lapreferente_estadisticas_sync.py` (posición, nombre corto/legal, estado de
fichaje/renovación y estadísticas de temporada) ya se puede lanzar desde
GitHub Actions (`scraper_lapreferente_estadisticas.yml`), igual que el
sincronizador de Instagram — pero con una diferencia importante: la cookie
de Cloudflare (`cf_clearance`) que hace falta para pasar su comprobación
**dura solo unas horas, no días**. Eso significa que hay que regenerar y
volver a subir la sesión antes de cada vez que quieras que la sincronización
tenga éxito — un cron semanal fijo fallará la mayoría de las semanas salvo
que refresques la sesión justo antes.

Cuando el secret está caducado, el propio workflow lo detecta y termina
limpio (avisando en el log), sin tocar la base de datos — no hay riesgo de
que una sesión vieja corrompa nada, simplemente no hace su trabajo esa vez.

## 1. Genera la sesión iniciando el navegador

```bash
cd ~/Aplicacion_Web
source .venv_ig/bin/activate   # o el venv que uses (necesita Playwright)
python backend/app/web_scrappig/lapreferente_generar_sesion.py lapreferente_storage_state.json
```

Se abrirá una ventana de Firefox real. Espera a que cargue del todo
(Cloudflare puede tardar unos segundos comprobando que eres humano; a veces
no hace falta hacer nada, a veces pide marcar una casilla). Cuando veas la
tabla de la plantilla del club, vuelve a la terminal y pulsa Enter.

## 2. Codifícala en base64

```bash
base64 -w0 lapreferente_storage_state.json > /tmp/session_b64.txt
```

## 3. Verifica que el base64 es correcto antes de subirlo

```bash
base64 -d /tmp/session_b64.txt > /tmp/test_decode.json \
  && python3 -m json.tool /tmp/test_decode.json > /dev/null \
  && echo "OK: es JSON válido"
```

## 4. Sube el secret (mejor con `gh`, evita el copy-paste manual)

```bash
gh secret set LAPREFERENTE_STORAGE_STATE_B64 --repo aplicacionwebcampillo/Aplicacion_Web < /tmp/session_b64.txt
```

Si prefieres pegarlo a mano en la web de GitHub (**Settings → Secrets and
variables → Actions**), usa el contenido de `cat /tmp/session_b64.txt`, pero
`gh secret set` evita el riesgo de que el pegado se corte o corrompa.

## 5. Limpieza local

```bash
rm lapreferente_storage_state.json /tmp/session_b64.txt /tmp/test_decode.json
```

## 6. Lanza el workflow

Desde la pestaña Actions, "Actualizar plantilla desde lapreferente.com" →
Run workflow. En el log, el paso "Restaurar sesión" debe mostrar `[OK] JSON
de sesión válido (N cookies)`, y el siguiente paso debe listar los jugadores
encontrados y actualizados (`[OK] <nombre> actualizado: {...}`).

## Cuándo repetir esto

Cada vez que quieras que la sincronización automática (manual o por el cron
semanal de los lunes) tenga éxito, si ya han pasado varias horas desde la
última vez que generaste la sesión. Si el log dice `[ERROR] Cloudflare
sigue bloqueando: regenera la sesión...`, repite los pasos 1-4.
