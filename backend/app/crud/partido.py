from sqlalchemy.orm import Session
from sqlalchemy import text

def actualizar_resultado(db: Session, nombre_competicion: str, temporada: str, local: str, visitante: str, resultado: str):
    db.execute(text("SELECT actualizar_resultado_partido(:nombre_competicion, :temporada, :local, :visitante, :resultado)"), {
        "nombre_competicion": nombre_competicion,
        "temporada": temporada,
        "local": local,
        "visitante": visitante,
        "resultado": resultado
    })
    db.commit()

