"""Diagnóstico temporal: prueba varios modelos candidatos de Mistral con
una imagen, para ver cuál acepta contenido de tipo image_url."""

import os

import requests

PIXEL_ROJO_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def probar(modelo, api_key):
    payload = {
        "model": modelo,
        "temperature": 0,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "¿De qué color es esta imagen? Responde solo con el color."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{PIXEL_ROJO_PNG_B64}"}},
            ],
        }],
    }
    resp = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=30,
    )
    print(f"[INFO] {modelo} -> status {resp.status_code}", flush=True)
    print(f"[INFO] cuerpo: {resp.text[:600]}", flush=True)
    print(flush=True)


api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    print("[SKIP] no hay MISTRAL_API_KEY configurada", flush=True)
else:
    for modelo in ("mistral-small-latest", "mistral-medium-latest", "mistral-large-latest"):
        probar(modelo, api_key)
