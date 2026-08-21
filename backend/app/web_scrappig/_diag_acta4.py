"""Diagnóstico temporal (v4): la 'Tabla Goleadores' de la RFAF resultó ser
un enlace normal (no JavaScript): NFG_CMP_Goleadores. La pedimos
directamente con requests (sin navegador) y volcamos su estructura."""

import requests
from bs4 import BeautifulSoup

URL_GOLEADORES = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_CMP_Goleadores"
    "?cod_primaria=1000120&CodJornada=1&codcompeticion=48466094"
    "&codtemporada=22&codgrupo=48466095"
)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

resp = requests.get(URL_GOLEADORES, headers=headers, timeout=30)
print(f"[INFO] status {resp.status_code}, {len(resp.text)} bytes", flush=True)

soup = BeautifulSoup(resp.text, "html.parser")
texto = soup.get_text(" ", strip=True)
print(f"[INFO] Longitud texto visible: {len(texto)}", flush=True)
print("[INFO] Primeros 3000 caracteres:", flush=True)
print(texto[:3000], flush=True)

print("\n[INFO] Tablas encontradas y sus primeras filas:", flush=True)
for i, tabla in enumerate(soup.select("table")):
    filas = tabla.select("tr")
    print(f"--- Tabla {i}: {len(filas)} filas ---", flush=True)
    for fila in filas[:8]:
        celdas = [c.get_text(" ", strip=True) for c in fila.select("td, th")]
        if celdas:
            print(f"   {celdas}", flush=True)
