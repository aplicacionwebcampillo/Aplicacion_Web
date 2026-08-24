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

SESSION_FILE="$(mktemp -t lapreferente_storage_state.XXXXXX)"
trap 'rm -f "$SESSION_FILE"' EXIT

echo "== 1/2: Generando sesión de lapreferente.com (se abrirá una ventana de Firefox) =="
python "$SCRIPT_DIR/lapreferente_generar_sesion.py" "$SESSION_FILE"

echo
echo "== 2/2: Sincronizando estadísticas con la base de datos =="
python "$SCRIPT_DIR/lapreferente_estadisticas_sync.py" "$SESSION_FILE"

echo
echo "[OK] Sincronización de lapreferente completada."
