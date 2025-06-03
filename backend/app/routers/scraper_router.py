from fastapi import APIRouter
from app.web_scrappig.main import main as run_scraper

router = APIRouter()

@router.get("/run-scraper")
async def run_scraper_endpoint():
    await run_scraper()
    return {"status": "Scraping ejecutado correctamente"}

