from playwright.async_api import async_playwright
from app.database import SessionLocal
from app.models.competicion import Competicion

def inferir_id_equipo(nombre_competicion: str) -> int:
    nombre = nombre_competicion.lower()
    if "juvenil" in nombre:
        return 2
    elif "femenin" in nombre:
        return 3
    else:
        return 1

async def scrape_competiciones(codigo_club: str):
    async with async_playwright() as p:
        #browser = await p.firefox.launch(headless=False)
        #page = await browser.new_page()
        
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()


        url = f"https://www.rfaf.es/pnfg/NPcd/NFG_VerClub?cod_primaria=1000118&codigo_club={codigo_club}"
        await page.goto(url, wait_until='networkidle')
        
        #await page.click("#cmpbntyestxt") # Aceptar cookies
        #await page.wait_for_load_state("networkidle")
        
        await page.wait_for_timeout(2000) # Ficha de Competición
        await page.click('a[href*="NFG_VisCompeticiones_Club?cod_primaria=1000123&codclub=28701965&codtemporada=20"]')
                
        await page.wait_for_timeout(60000)
        await browser.close()

