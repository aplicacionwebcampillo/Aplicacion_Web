from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.models.patrocinador import Patrocinador
from app.schemas.patrocinador import PatrocinadorCreate, PatrocinadorUpdate

def create_patrocinador(db: Session, patrocinador: PatrocinadorCreate):
    db.execute(text("""
        SELECT agregar_patrocinador(
            :p_nombre, :p_tipo, :p_email, :p_telefono, :p_logo, :p_fecha_inicio, :p_fecha_fin, :p_dni_administrador
        )
    """), {
        "p_nombre": patrocinador.nombre,
        "p_tipo": patrocinador.tipo,
        "p_email": patrocinador.email,
        "p_telefono": patrocinador.telefono,
        "p_logo": patrocinador.logo,
        "p_fecha_inicio": patrocinador.fecha_inicio,
        "p_fecha_fin": patrocinador.fecha_fin,
        "p_dni_administrador": patrocinador.dni_administrador
    })
    db.commit()
    return db.query(Patrocinador).filter(Patrocinador.nombre == Patrocinador.nombre).first()

def get_patrocinador(db: Session, nombre: str):
    return db.query(Patrocinador).filter(Patrocinador.nombre == nombre).first()

def get_patrocinadores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Patrocinador).offset(skip).limit(limit).all()

def update_patrocinador(db: Session, nombre: str, patrocinador_update: PatrocinadorUpdate):
    patrocinador = db.query(Patrocinador).filter(Patrocinador.nombre == nombre).first()
    if not patrocinador:
        return None
    for key, value in patrocinador_update.dict(exclude_unset=True).items():
        setattr(patrocinador, key, value)
    db.commit()
    db.refresh(patrocinador)
    return patrocinador

def delete_patrocinador(db: Session, nombre: str):
    patrocinador = db.query(Patrocinador).filter(Patrocinador.nombre == nombre).first()
    if patrocinador:
        db.delete(patrocinador)
    db.commit()
    return True


