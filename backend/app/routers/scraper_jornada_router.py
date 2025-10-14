from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.resultado import Resultado

router = APIRouter(prefix="/resultados", tags=["resultados"])

@router.get("/")
def get_resultados(categoria: str = Query(...), db: Session = Depends(get_db)):

    # Obtener la última jornada scrapeada para esta categoría
    ultima_jornada = db.query(Resultado.jornada) \
                       .filter(Resultado.categoria == categoria) \
                       .order_by(Resultado.fetched_at.desc()) \
                       .limit(1) \
                       .scalar()

    if not ultima_jornada:
        return {"jornada": None, "partidos": []}

    # Traer todos los partidos de esa última jornada
    partidos = db.query(Resultado).filter(
        Resultado.categoria == categoria,
        Resultado.jornada == ultima_jornada
    ).all()

    return {
        "jornada": ultima_jornada,
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

