"""Diagnóstico temporal: ¿funciona GitHub Models (gratis, usa el propio
GITHUB_TOKEN de Actions, sin secret nuevo) para peticiones con imagen?"""

import base64
import os

import requests

TOKEN = os.environ["GITHUB_TOKEN"]
ENDPOINT = "https://models.github.ai/inference/chat/completions"

# Imagen mínima 1x1 px roja, en base64, solo para probar que la llamada
# con contenido de tipo imagen funciona de extremo a extremo.
PIXEL_ROJO_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)

payload = {
    "model": "openai/gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "¿De qué color es esta imagen? Responde solo con el color."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{PIXEL_ROJO_PNG_B64}"}},
            ],
        }
    ],
}

resp = requests.post(
    ENDPOINT,
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    json=payload,
    timeout=30,
)
print(f"[INFO] status {resp.status_code}", flush=True)
print(f"[INFO] cuerpo: {resp.text[:1500]}", flush=True)
