"""Diagnóstico temporal: lista los modelos disponibles en Groq y Mistral
con la clave configurada, para encontrar el ID real de un modelo con
visión (en vez de adivinarlo)."""

import os

import requests


def listar(nombre, url, api_key):
    if not api_key:
        print(f"[SKIP] {nombre}: no hay clave configurada", flush=True)
        return
    resp = requests.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
    print(f"[INFO] {nombre} -> status {resp.status_code}", flush=True)
    if resp.status_code != 200:
        print(f"[INFO] cuerpo: {resp.text[:500]}", flush=True)
        return
    datos = resp.json().get("data", [])
    ids = sorted(d.get("id", "") for d in datos)
    print(f"[INFO] {len(ids)} modelos disponibles:", flush=True)
    for id_modelo in ids:
        print(f"   {id_modelo}", flush=True)


listar("Groq", "https://api.groq.com/openai/v1/models", os.environ.get("GROQ_API_KEY"))
print()
listar("Mistral", "https://api.mistral.ai/v1/models", os.environ.get("MISTRAL_API_KEY"))
