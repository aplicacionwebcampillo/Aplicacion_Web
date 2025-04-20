from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.competicion import Competicion
from app.schemas.competicion import CompeticionCreate

def create_competicion(db: Session, competicion: CompeticionCreate):
    db.execute(text("SELECT agregar_competicion(:nombre, :temporada, :estado, :fecha_inicio, :fecha_fin)"), competicion.dict())
    db.commit()

def delete_competicion(db: Session, nombre: str, temporada: str):
    db.execute(text("SELECT eliminar_competicion(:nombre, :temporada)"), {"nombre": nombre, "temporada": temporada})
    db.commit()

