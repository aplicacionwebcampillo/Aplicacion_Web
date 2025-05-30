#!/usr/bin/env bash
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Instalar navegadores (como Firefox) y sus dependencias
python -m playwright install --with-deps

