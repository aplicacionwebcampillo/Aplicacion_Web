from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.resultado import Resultado

router = APIRouter(prefix="/resultados", tags=["resultados"])

@router.get("/")
def get_resultados(categoria: str = Query(...), db: Session = Depends(get_db)):
    # Obtener la fecha de scrapeo más reciente
    ultima_fecha = db.query(func.max(Resultado.fetched_at)).filter(Resultado.categoria == categoria).scalar()

    if not ultima_fecha:
        return {"jornada": None, "partidos": []}

    # Traer solo los partidos de la última ejecución
    partidos = db.query(Resultado).filter(
        Resultado.categoria == categoria,
        Resultado.fetched_at == ultima_fecha
    ).all()

    # Convertir a dict para enviar al frontend
    return {
        "jornada": partidos[0].jornada if partidos else None,
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

