from fastapi import APIRouter, Query, HTTPException
from app.database import SessionLocal
from app.models.resultado import Resultado

router = APIRouter(prefix="/resultados", tags=["resultados"])

@router.get("/")
def get_resultados(categoria: str = Query("Senior")):
    session = SessionLocal()
    try:
        resultados = (
            session.query(Resultado)
            .filter_by(categoria=categoria)
            .order_by(Resultado.fetched_at.desc())
            .all()
        )

        if not resultados:
            raise HTTPException(status_code=404, detail="No hay resultados guardados aún.")

        return [
            {
                "jornada": r.jornada,
                "local": r.local,
                "visitante": r.visitante,
                "goles_local": r.goles_local,
                "goles_visitante": r.goles_visitante,
                "fecha": r.fecha,
                "hora": r.hora,
            }
            for r in resultados
        ]
    finally:
        session.close()

