#!/bin/bash
# Genera una sesión nueva de lapreferente.com y sincroniza la plantilla
# (posición, nombre corto/legal, estado de fichaje/renovación y estadísticas
# de temporada) directamente contra la base de datos en producción, en un
# solo paso.
#
# No sube ningún secret ni pasa por GitHub Actions: lapreferente.com está
# protegido por Cloudflare y solo se puede sincronizar ejecutándolo aquí, a
# mano, desde una conexión de confianza.
#
# Requiere: Playwright instalado (pip install playwright && playwright
# install firefox).
#
# Uso:
#   bash backend/app/web_scrappig/actualizar_lapreferente.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# En muchos sistemas (p.ej. Ubuntu/Debian recientes) solo existe "python3",
# no "python". Se detecta cuál hay disponible en vez de asumir uno fijo.
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

echo "== 1/2: Generando sesión de lapreferente.com (se abrirá una ventana de Firefox) =="
"$PYTHON" "$SCRIPT_DIR/lapreferente_generar_sesion.py" "$SESSION_FILE"

echo
echo "== 2/2: Sincronizando estadísticas con la base de datos =="
"$PYTHON" "$SCRIPT_DIR/lapreferente_estadisticas_sync.py" "$SESSION_FILE"

echo
echo "[OK] Sincronización de lapreferente completada."
