"""Diagnóstico temporal: ¿la web de la RFAF (pnfg) publica actas de
partido con datos por jugador (goleadores, tarjetas)? Busca en la página
de calendario/resultados del grupo un enlace a un partido ya jugado, y
vuelca su HTML para inspeccionar la estructura."""

import re
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.rfaf.es"
URL_GRUPO = (
    "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion"
    "?cod_primaria=1000120&codgrupo=48466095&codcompeticion=48466094"
)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

resp = requests.get(URL_GRUPO, headers=headers, timeout=30)
print(f"[INFO] Clasificación: status {resp.status_code}, {len(resp.text)} bytes", flush=True)
soup = BeautifulSoup(resp.text, "html.parser")

# Buscamos cualquier enlace que huela a "partido" (acta, resultado, vs...).
enlaces = soup.select("a[href]")
candidatos = []
for a in enlaces:
    href = a["href"]
    texto = a.get_text(" ", strip=True)
    if re.search(r"partido|acta|resultado", href, re.I):
        candidatos.append((href, texto))

print(f"[INFO] {len(enlaces)} enlaces totales, {len(candidatos)} con pinta de partido/acta", flush=True)
for href, texto in candidatos[:30]:
    print(f"  -> {href}  |  {texto[:80]}", flush=True)

# También probamos la vista de "calendario" del mismo grupo, que en pnfg
# suele listar cada jornada con enlace al partido.
url_calendario = URL_GRUPO.replace("NFG_VisClasificacion", "NFG_VisResult")
resp2 = requests.get(url_calendario, headers=headers, timeout=30)
print(f"\n[INFO] NFG_VisResult: status {resp2.status_code}, {len(resp2.text)} bytes", flush=True)
soup2 = BeautifulSoup(resp2.text, "html.parser")
enlaces2 = soup2.select("a[href]")
candidatos2 = []
for a in enlaces2:
    href = a["href"]
    texto = a.get_text(" ", strip=True)
    if re.search(r"partido|acta", href, re.I):
        candidatos2.append((href, texto))
print(f"[INFO] {len(enlaces2)} enlaces totales, {len(candidatos2)} con pinta de partido/acta", flush=True)
for href, texto in candidatos2[:30]:
    print(f"  -> {href}  |  {texto[:80]}", flush=True)

primer_partido = candidatos2[0][0] if candidatos2 else (candidatos[0][0] if candidatos else None)
if primer_partido:
    url_partido = urljoin(BASE, primer_partido)
    print(f"\n[INFO] Visitando posible ficha de partido: {url_partido}", flush=True)
    resp3 = requests.get(url_partido, headers=headers, timeout=30)
    print(f"[INFO] status {resp3.status_code}, {len(resp3.text)} bytes", flush=True)
    texto_plano = BeautifulSoup(resp3.text, "html.parser").get_text(" ", strip=True)
    for palabra in ("goles", "goleador", "tarjeta", "amarilla", "roja", "minuto", "convocado"):
        idx = texto_plano.lower().find(palabra)
        estado = "SI" if idx != -1 else "no"
        print(f"  contiene '{palabra}': {estado}" + (f" (contexto: ...{texto_plano[max(0,idx-60):idx+100]}...)" if idx != -1 else ""), flush=True)
    with open("rfaf_partido_debug.html", "w", encoding="utf-8") as f:
        f.write(resp3.text)
    print("[INFO] HTML completo guardado en rfaf_partido_debug.html (no se sube, solo local al runner)", flush=True)
else:
    print("\n[AVISO] No se encontró ningún enlace de partido/acta en ninguna de las dos páginas.", flush=True)
    sys.exit(0)
