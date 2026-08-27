"""Diagnostico puntual: ejecuta el scraping real de partidos (igual que
main.py) pero con extraer_acta parcheado para volcar el HTML crudo de la
fila del partido Arjonilla-Campillo en cuanto la encuentre, y asi ver si
la RFAF ya publico el enlace del acta y por que no lo estamos cogiendo.
Se borra tras usarlo."""
import asyncio

from app.web_scrappig import scraper as scraper_module

original_extraer_acta = scraper_module.extraer_acta


def debug_extraer_acta(fila, base_url):
    texto = fila.get_text(" ", strip=True)
    if "arjonilla" in texto.lower():
        print("=" * 20 + " FILA ARJONILLA ENCONTRADA " + "=" * 20, flush=True)
        print(f"texto fila: {texto!r}", flush=True)
        enlaces = fila.find_all("a")
        print(f"num enlaces <a> en la fila: {len(enlaces)}", flush=True)
        for a in enlaces:
            print(f"  <a href={a.get('href')!r}> texto={a.get_text(strip=True)!r}", flush=True)
        print("--- HTML crudo de la fila (hasta 4000 caracteres) ---", flush=True)
        print(str(fila)[:4000], flush=True)
        print("=" * 60, flush=True)
    resultado = original_extraer_acta(fila, base_url)
    if "arjonilla" in texto.lower():
        print(f"resultado de extraer_acta: {resultado!r}", flush=True)
    return resultado


scraper_module.extraer_acta = debug_extraer_acta


async def main():
    await scraper_module.scrape_partidos("28701965")


if __name__ == "__main__":
    asyncio.run(main())
