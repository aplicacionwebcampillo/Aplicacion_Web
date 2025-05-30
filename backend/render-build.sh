#!/usr/bin/env bash
set -o errexit

# Instalar dependencias de Python
pip install -r requirements.txt

# Instalar navegadores de Playwright en una ruta persistente
PLAYWRIGHT_BROWSERS_PATH=0 python -m playwright install

