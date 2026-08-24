#!/bin/bash
# Genera una sesión nueva de Instagram y la sube directamente como secret de
# GitHub Actions (IG_STORAGE_STATE_B64), en un solo paso.
#
# Requiere: Playwright instalado (pip install playwright && playwright
# install firefox) y el CLI de GitHub autenticado (gh auth login).
#
# Uso:
#   bash backend/app/web_scrappig/actualizar_secret_instagram.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="aplicacionwebcampillo/Aplicacion_Web"

SESSION_FILE="$(mktemp -t ig_storage_state.XXXXXX)"
B64_FILE="$(mktemp -t ig_session_b64.XXXXXX)"
trap 'rm -f "$SESSION_FILE" "$B64_FILE"' EXIT

echo "== 1/3: Generando sesión de Instagram (se abrirá una ventana de Firefox) =="
python "$SCRIPT_DIR/instagram_generar_sesion.py" "$SESSION_FILE"

echo
echo "== 2/3: Codificando y verificando =="
base64 -w0 "$SESSION_FILE" > "$B64_FILE"
python3 -c "
import base64, json
with open('$B64_FILE') as f:
    raw = f.read()
data = json.loads(base64.b64decode(raw))
print(f\"[OK] JSON valido ({len(data.get('cookies', []))} cookies)\")
"

echo
echo "== 3/3: Subiendo el secret IG_STORAGE_STATE_B64 =="
gh secret set IG_STORAGE_STATE_B64 --repo "$REPO" < "$B64_FILE"

echo
echo "[OK] Secret de Instagram actualizado."
