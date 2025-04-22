from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.socio import Socio
from app.schemas.socio import SocioCreate, SocioUpdate
from app.models.usuario import Usuario

def create_socio(db: Session, socio: SocioCreate):
    db.execute(text("""
        CALL registrar_socio(
            :p_dni, :p_nombre, :p_apellidos, :p_telefono,
            :p_fecha_nacimiento, :p_email, :p_contrasena, :p_tipo_membresia
        )
    """), {
        "p_dni": socio.dni,
        "p_nombre": socio.nombre,
        "p_apellidos": socio.apellidos,
        "p_telefono": socio.telefono,
        "p_fecha_nacimiento": socio.fecha_nacimiento,
        "p_email": socio.email,
        "p_contrasena": socio.contrasena,
        "p_tipo_membresia": socio.tipo_membresia
    })

    db.commit()
    return db.query(Socio).filter(Socio.dni == socio.dni).first()

def get_socio(db: Session, dni: str):
    return db.query(Socio).filter(Socio.dni == dni).first()
    
def get_socios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Socio).offset(skip).limit(limit).all()

def update_socio(db: Session, dni: str, socio_update: SocioUpdate):
    socio = db.query(Socio).filter(Socio.dni == dni).first()
    if not socio:
        return None
    for key, value in socio_update.dict(exclude_unset=True).items():
        setattr(socio, key, value)    
    db.commit()
    db.refresh(socio)
    return socio

def delete_socio(db: Session, dni: str):
    socio = db.query(Socio).filter(Socio.dni == dni).first()
    usuario = db.query(Usuario).filter(Usuario.dni == dni).first()
    if socio:
        db.delete(socio)
    if usuario:
        db.delete(usuario)
    db.commit()
    return True

