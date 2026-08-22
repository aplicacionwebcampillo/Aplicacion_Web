"""Diagnóstico temporal: prueba rápida (sin Instagram de por medio) de que
las claves de Groq y Mistral funcionan para peticiones con imagen, usando
los mismos modelos/endpoints que usará el sincronizador real."""

import os

import requests

PIXEL_ROJO_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def probar(nombre, url, api_key, modelo):
    if not api_key:
        print(f"[SKIP] {nombre}: no hay clave configurada", flush=True)
        return
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
        url, headers={"Authorization": f"Bearer {api_key}"}, json=payload, timeout=30
    )
    print(f"[INFO] {nombre} ({modelo}) -> status {resp.status_code}", flush=True)
    print(f"[INFO] cuerpo: {resp.text[:1000]}", flush=True)


probar(
    "Groq",
    "https://api.groq.com/openai/v1/chat/completions",
    os.environ.get("GROQ_API_KEY"),
    os.environ.get("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
)
print()
probar(
    "Mistral",
    "https://api.mistral.ai/v1/chat/completions",
    os.environ.get("MISTRAL_API_KEY"),
    os.environ.get("MISTRAL_MODEL", "pixtral-large-latest"),
)
