#!/bin/bash
# Versión para móvil (Termux + proot-distro) de actualizar_lapreferente.sh.
#
# La diferencia: en vez de abrir una ventana de Firefox local para pasar el
# chequeo de Cloudflare (lapreferente_generar_sesion.py, necesita una
# pantalla), reutiliza cookies ya exportadas de un navegador real -- p.ej.
# Firefox para Android con la extensión Cookie-Editor -- donde ese chequeo
# ya se ha superado. Ver docs/lapreferente_movil.md para la puesta en
# marcha completa en el teléfono.
#
# Uso:
#   1. En Firefox (Android), entra en
#      https://www.lapreferente.com/E38004/cd-campillo-del-rio-cf y espera a
#      que cargue la tabla de la plantilla.
#   2. Exporta las cookies con Cookie-Editor -> Export -> Export as JSON, y
#      guarda ese JSON en un fichero, p.ej. cookies_lapreferente.json.
#   3. bash backend/app/web_scrappig/actualizar_lapreferente_movil.sh cookies_lapreferente.json

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Uso: bash actualizar_lapreferente_movil.sh <cookies_exportadas.json>" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COOKIES_FILE="$1"

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "No se ha encontrado ni 'python3' ni 'python' en el PATH. Instala Python 3." >&2
    exit 1
fi

SESSION_FILE="$(mktemp -t lapreferente_storage_state.XXXXXX)"
trap 'rm -f "$SESSION_FILE"' EXIT

echo "== 1/2: Convirtiendo cookies exportadas a sesión =="
"$PYTHON" "$SCRIPT_DIR/lapreferente_cookies_a_sesion.py" "$COOKIES_FILE" "$SESSION_FILE"

echo
echo "== 2/2: Sincronizando estadísticas con la base de datos =="
"$PYTHON" "$SCRIPT_DIR/lapreferente_estadisticas_sync.py" "$SESSION_FILE"

echo
echo "[OK] Sincronización de lapreferente completada."
