from fastapi import APIRouter, Query, HTTPException
from app.web_scrappig.scraper_jornada import obtener_resultados

router = APIRouter(prefix="/resultados", tags=["resultados"])

URLS_COMPETICIONES = {
    "Senior": "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion?cod_primaria=1000120&codgrupo=45293013&codcompeticion=44788639",
    "Femenino_7": "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion?cod_primaria=1000120&codgrupo=46575672&codcompeticion=46575570",
    "Femenino_11": "https://www.rfaf.es/pnfg/NPcd/NFG_VisClasificacion?cod_primaria=1000120&codgrupo=46573703&codcompeticion=46573611",
}

@router.get("/")
def get_resultados(categoria: str = Query("Senior")):
    """
    Devuelve los resultados de la última jornada según categoría.
    Filtra partidos donde local o visitante sean None.
    """
    url = URLS_COMPETICIONES.get(categoria)
    if not url:
        raise HTTPException(status_code=400, detail="Categoría no válida")

    try:
        return obtener_resultados(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

