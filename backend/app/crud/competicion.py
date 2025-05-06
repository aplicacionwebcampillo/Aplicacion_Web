from sqlalchemy.orm import Session
from app.models.competicion import Competicion
from app.schemas.competicion import CompeticionCreate, CompeticionUpdate


def get_competicion(db: Session, nombre: str, temporada: str):
    return db.query(Competicion).filter_by(nombre=nombre, temporada=temporada).first()


def get_competiciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Competicion).offset(skip).limit(limit).all()


def create_competicion(db: Session, competicion: CompeticionCreate):
    db_competicion = Competicion(
        nombre=competicion.nombre,
        temporada=competicion.temporada,
        estado=competicion.estado,
        fecha_inicio=competicion.fecha_inicio,
        fecha_fin=competicion.fecha_fin,
        id_equipo=competicion.id_equipo
    )
    db.add(db_competicion)
    db.commit()
    db.refresh(db_competicion)
    return db_competicion


def update_competicion(db: Session, nombre: str, temporada: str, competicion_update: CompeticionUpdate):
    db_competicion = get_competicion(db, nombre, temporada)
    if not db_competicion:
        return None

    update_data = competicion_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_competicion, field, value)

    db.commit()
    db.refresh(db_competicion)
    return db_competicion


def delete_competicion(db: Session, nombre: str, temporada: str):
    db_competicion = get_competicion(db, nombre, temporada)
    if not db_competicion:
        return None

    db.delete(db_competicion)
    db.commit()
    return db_competicion

