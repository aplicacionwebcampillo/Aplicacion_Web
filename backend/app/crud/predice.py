from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models.predice import Predice
from app.schemas.predice import PrediceCreate, PrediceUpdate
from typing import List
from app.models.socio import Socio
from fastapi import HTTPException

def create_prediccion(db: Session, prediccion: PrediceCreate) -> Predice:
    db_predice = Predice(**prediccion.model_dump())
    db.add(db_predice)
    db.commit()
    db.refresh(db_predice)
    return db_predice


def get_prediccion(db: Session, dni: str, nombre_competicion: str, temporada_competicion: str, local: str, visitante: str) -> Predice:
    return db.query(Predice).filter_by(
        dni=dni,
        nombre_competicion=nombre_competicion,
        temporada_competicion=temporada_competicion,
        local=local,
        visitante=visitante
    ).first()


def get_predicciones(db: Session, skip: int = 0, limit: int = 100) -> List[Predice]:
    return db.query(Predice).offset(skip).limit(limit).all()


def update_prediccion(
    db: Session,
    dni: str,
    nombre_competicion: str,
    temporada_competicion: str,
    local: str,
    visitante: str,
    prediccion_update: PrediceUpdate
) -> Predice:
    db_predice = get_prediccion(db, dni, nombre_competicion, temporada_competicion, local, visitante)
    if not db_predice:
        raise NoResultFound("Predicción no encontrada")
    
    update_data = prediccion_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_predice, key, value)
    
    db.commit()
    db.refresh(db_predice)
    return db_predice


def delete_prediccion(db: Session, dni: str, nombre_competicion: str, temporada_competicion: str, local: str, visitante: str) -> bool:
    db_predice = get_prediccion(db, dni, nombre_competicion, temporada_competicion, local, visitante)
    if not db_predice:
        return False
    db.delete(db_predice)
    db.commit()
    return True


def validar_pago_predice(
    db: Session,
    dni: str,
    nombre_competicion: str,
    temporada_competicion: str,
    local: str,
    visitante: str,
    resultado_local: int,
    resultado_visitante: int
):
    socio = db.query(Socio).filter(Socio.dni == dni).first()
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")

    prediccion = (
        db.query(Predice)
        .filter(
            Predice.dni == socio.dni,
            Predice.nombre_competicion == nombre_competicion,
            Predice.temporada_competicion == temporada_competicion,
            Predice.local == local,
            Predice.visitante == visitante,
            Predice.resultado_local == resultado_local,
            Predice.resultado_visitante == resultado_visitante
        )
        .first()
    )

    if not prediccion:
        raise HTTPException(status_code=404, detail="No se encontró predicción que coincida")

    prediccion.pagado = True
    db.commit()
    db.refresh(prediccion)
    return {
        "message": "Pago validado correctamente para predicción",
        "resultado_local": prediccion.resultado_local,
        "resultado_visitante": prediccion.resultado_visitante
    }

