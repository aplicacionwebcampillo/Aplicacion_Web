from sqlalchemy.orm import Session
from app import models, schemas
from app.models.equipo import Equipo
from app.schemas.equipo import EquipoCreate, EquipoUpdate

def create_equipo(db: Session, equipo: EquipoCreate):
    db_equipo = Equipo(**equipo.dict())
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

def get_equipos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Equipo).offset(skip).limit(limit).all()

def get_equipo(db: Session, id_equipo: int):
    return db.query(Equipo).filter(Equipo.id_equipo == id_equipo).first()

def update_equipo(db: Session, id_equipo: int, equipo_update: EquipoUpdate):
    equipo = db.query(Equipo).filter(Equipo.id_equipo == id_equipo).first()
    if not equipo:
        return None
    for key, value in equipo_update.dict(exclude_unset=True).items():
        setattr(equipo, key, value)
    db.commit()
    db.refresh(equipo)
    return equipo

def delete_equipo(db: Session, id_equipo: int):
    equipo = db.query(Equipo).filter(Equipo.id_equipo == id_equipo).first()
    if not equipo:
        return None
    db.delete(equipo)
    db.commit()
    return equipo
