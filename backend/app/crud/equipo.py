from sqlalchemy.orm import Session
from app.models.equipo import Equipo
from app.schemas.equipo import EquipoCreate

def create_equipo(db: Session, equipo: EquipoCreate):
    db_equipo = Equipo(**equipo.dict())
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

def get_equipo(db: Session, id_equipo: int):
    return db.query(Equipo).filter(Equipo.id_equipo == id_equipo).first()

