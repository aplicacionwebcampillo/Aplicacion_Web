from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.patrocinador import Patrocinador
from app.schemas.patrocinador import PatrocinadorCreate

def create_patrocinador(db: Session, patrocinador: PatrocinadorCreate):
    db.execute(text("SELECT agregar_patrocinador(:nombre, :tipo, :email, :telefono, :logo, :fecha_inicio, :fecha_fin, :dni_administrador)"), patrocinador.dict())
    db.commit()

def delete_patrocinador(db: Session, id_patrocinador: int):
    db.execute(text("SELECT eliminar_patrocinador(:id_patrocinador)"), {"id_patrocinador": id_patrocinador})
    db.commit()

