import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.database import engine
from app.database import Base
from app.models.competicion import Competicion
from app.web_scrappig.scraper import (scrape_competiciones, scrape_clasificacion, scrape_partidos)


def init_db():
    Base.metadata.create_all(bind=engine)

async def main():
    init_db()
    codigo_club = "28701965"
    await scrape_competiciones(codigo_club)
    await scrape_clasificacion(codigo_club)
    await scrape_partidos(codigo_club)

if __name__ == "__main__":
    asyncio.run(main())
