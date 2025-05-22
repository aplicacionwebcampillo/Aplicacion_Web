from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional
from fastapi import HTTPException
from app.models.clasificacion import Clasificacion
from app.schemas.clasificacion import ClasificacionCreate, ClasificacionUpdate


def create_clasificacion(db: Session, clasificacion: ClasificacionCreate):
    db_clasificacion = Clasificacion(
        nombre_competicion=clasificacion.nombre_competicion,
        temporada_competicion=clasificacion.temporada_competicion,
        equipo=clasificacion.equipo,
        posicion=clasificacion.posicion,
        puntos=clasificacion.puntos, 
    )
    db.add(db_clasificacion)
    db.commit()
    db.refresh(db_clasificacion)
    return db_clasificacion

def get_clasificacion(
    db: Session,
    nombre_competicion: str,
    temporada_competicion: str,
    equipo: str
) -> Optional[Clasificacion]:
    return db.query(Clasificacion).filter_by(
        nombre_competicion=nombre_competicion,
        temporada_competicion=temporada_competicion,
        equipo=equipo
    ).first()


def get_clasificaciones(
    db: Session,
    nombre_competicion: Optional[str] = None,
    temporada_competicion: Optional[str] = None
) -> List[Clasificacion]:
    query = db.query(Clasificacion)
    
    if nombre_competicion:
        query = query.filter(Clasificacion.nombre_competicion == nombre_competicion)
    
    if temporada_competicion:
        query = query.filter(Clasificacion.temporada_competicion == temporada_competicion)
    
    return query.order_by(Clasificacion.posicion).all()


   
def update_clasificacion(
    db: Session,
    nombre_competicion: str,
    temporada_competicion: str,
    equipo: str,
    clasificacion_update: ClasificacionUpdate
): 
    db_clasificacion = get_clasificacion(db, nombre_competicion, temporada_competicion, equipo)
    if not db_clasificacion:
        raise HTTPException(status_code=404, detail="Clasificacion not found")

    update_data = clasificacion_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_clasificacion, field, value)

    db.commit()
    db.refresh(db_clasificacion)
    return db_clasificacion


def delete_clasificacion(
    db: Session,
    nombre_competicion: str,
    temporada_competicion: str,
    equipo: str
) -> bool:
    db_clasificacion = get_clasificacion(db, nombre_competicion, temporada_competicion, equipo)
    if not db_clasificacion:
        return False
    
    db.delete(db_clasificacion)
    db.commit()
    return True

