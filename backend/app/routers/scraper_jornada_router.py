from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.resultado import Resultado

router = APIRouter(prefix="/resultados", tags=["resultados"])


@router.get("/")
def get_resultados(categoria: str = Query(...), db: Session = Depends(get_db)):
    # La tabla "resultados" guarda, para cada categoría, la RONDA ENTERA
    # (todos los equipos) de la última jornada ya jugada -- a diferencia de
    # Partido, que por diseño solo guarda los partidos del propio club. La
    # rellena scraper.py (guardar_resultados_jornada_completa), calculando
    # dinámicamente el codgrupo/codcompeticion de cada temporada en vez de
    # usar unos fijos, así que siempre queda con la jornada y temporada
    # correctas con cada ejecución del scraping automático.
    ultima_fecha = (
        db.query(func.max(Resultado.fetched_at))
        .filter(Resultado.categoria == categoria)
        .scalar()
    )

    if not ultima_fecha:
        return {"jornada": None, "partidos": []}

    partidos = (
        db.query(Resultado)
        .filter(
            Resultado.categoria == categoria,
            Resultado.fetched_at == ultima_fecha,
        )
        .all()
    )

    if not partidos:
        return {"jornada": None, "partidos": []}

    jornada = partidos[0].jornada

    return {
        "jornada": jornada,
        "partidos": [
            {
                "local": p.local,
                "visitante": p.visitante,
                "goles_local": p.goles_local,
                "goles_visitante": p.goles_visitante,
                "fecha_texto": p.fecha,
                "hora_texto": p.hora,
            }
            for p in partidos
        ]
    }
