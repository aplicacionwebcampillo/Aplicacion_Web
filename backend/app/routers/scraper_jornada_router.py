from datetime import date, datetime

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.partido import Partido

router = APIRouter(prefix="/resultados", tags=["resultados"])

# Misma correspondencia categoria -> competición que usa el frontend
# (Clasificacion.tsx). Antes este endpoint leía de una tabla aparte
# ("resultados") rellenada por scraper_jornada.py con el codgrupo/
# codcompeticion de la RFAF escritos a mano -- esos códigos cambian cada
# temporada, y los de categorías femeninas se quedaron desactualizados
# (apuntaban a la temporada anterior) porque nadie los volvió a tocar a
# mano. Se sustituye por una consulta sobre Partido, que scraper.py ya
# mantiene al día automáticamente temporada tras temporada sin códigos
# fijos.
COMPETICION_POR_CATEGORIA = {
    "Senior": "1ª Andaluza Sénior (Jaén)",
    "Femenino_7": "Liga Femenina Sénior Fútbol 7 (Jaén)",
    "Femenino_11": "2ª Andaluza Femenina Sénior (Jaén)",
}


def _temporada_actual() -> str:
    hoy = datetime.now()
    inicio = hoy.year if hoy.month >= 8 else hoy.year - 1
    return f"Temporada {inicio}-{inicio + 1}"


@router.get("/")
def get_resultados(categoria: str = Query(...), db: Session = Depends(get_db)):
    nombre_competicion = COMPETICION_POR_CATEGORIA.get(categoria)
    if not nombre_competicion:
        return {"jornada": None, "partidos": []}

    temporada_competicion = _temporada_actual()
    hoy = date.today()

    # Última jornada ya JUGADA: la fecha más reciente que no sea futura.
    ultima_fecha = (
        db.query(func.max(Partido.dia))
        .filter(
            Partido.nombre_competicion == nombre_competicion,
            Partido.temporada_competicion == temporada_competicion,
            Partido.dia <= hoy,
        )
        .scalar()
    )

    if not ultima_fecha:
        return {"jornada": None, "partidos": []}

    partido_referencia = (
        db.query(Partido)
        .filter(
            Partido.nombre_competicion == nombre_competicion,
            Partido.temporada_competicion == temporada_competicion,
            Partido.dia == ultima_fecha,
        )
        .first()
    )
    if not partido_referencia:
        return {"jornada": None, "partidos": []}

    # Se devuelven TODOS los partidos de esa misma jornada (no solo el de
    # esa fecha exacta): los partidos de una jornada se suelen repartir en
    # varios días del mismo fin de semana.
    partidos = (
        db.query(Partido)
        .filter(
            Partido.nombre_competicion == nombre_competicion,
            Partido.temporada_competicion == temporada_competicion,
            Partido.jornada == partido_referencia.jornada,
        )
        .all()
    )

    return {
        "jornada": f"Jornada {partido_referencia.jornada}",
        "partidos": [
            {
                "local": p.local,
                "visitante": p.visitante,
                "goles_local": p.resultado_local,
                "goles_visitante": p.resultado_visitante,
                "fecha_texto": p.dia.isoformat() if p.dia else None,
                "hora_texto": p.hora.isoformat() if p.hora else None,
            }
            for p in partidos
        ]
    }

