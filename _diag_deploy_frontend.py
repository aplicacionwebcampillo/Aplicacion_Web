import re
import requests

URL = "https://campillodelriocf.es/"

resp = requests.get(URL, timeout=20)
print("status index:", resp.status_code)
html = resp.text

# Buscar los <script type="module" src="...">
scripts = re.findall(r'<script[^>]+src="([^"]+)"', html)
print("scripts encontrados:", scripts)

for src in scripts:
    url_js = src if src.startswith("http") else f"https://campillodelriocf.es{src}"
    try:
        r = requests.get(url_js, timeout=20)
        contiene = "Fútbol 11" in r.text or "Futbol 11" in r.text
        print(f"{url_js} -> status={r.status_code} contiene 'Futbol 11'={contiene} tam={len(r.text)}")
    except Exception as e:
        print(f"{url_js} -> error: {e}")
