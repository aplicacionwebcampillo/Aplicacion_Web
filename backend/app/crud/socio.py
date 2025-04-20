from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.socio import Socio
from app.schemas.socio import SocioCreate

def create_socio(db: Session, socio: SocioCreate):
    db.execute(text("SELECT registrar_socio(:dni, :num_socio, :foto_perfil, :tipo_membresia, :estado)"), socio.dict())
    db.commit()
    return get_socio(db, socio.dni)

def get_socio(db: Session, dni: str):
    return db.query(Socio).filter(Socio.dni == dni).first()

