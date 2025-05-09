from sqlalchemy.orm import Session
from app.models.cesion_abono import CesionAbono
from app.schemas.cesion_abono import CesionAbonoCreate, CesionAbonoUpdate
from datetime import date
from app.models.abono import Abono

def create_cesion_abono(db: Session, cesion: CesionAbonoCreate):
    nueva_cesion = CesionAbono(**cesion.dict())
    db.add(nueva_cesion)
    db.commit()
    db.refresh(nueva_cesion)
    return nueva_cesion

def get_cesion_abono(db: Session, id_cesion: int):
    return db.query(CesionAbono).filter(CesionAbono.id_cesion == id_cesion).first()

def get_cesiones_abono(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CesionAbono).offset(skip).limit(limit).all()

def update_cesion_abono(db: Session, id_cesion: int, cesion_update: CesionAbonoUpdate):
    cesion = db.query(CesionAbono).filter(CesionAbono.id_cesion == id_cesion).first()
    if not cesion:
        return None
    for key, value in cesion_update.dict(exclude_unset=True).items():
        setattr(cesion, key, value)
    db.commit()
    db.refresh(cesion)
    return cesion

def delete_cesion_abono(db: Session, id_cesion: int):
    cesion = db.query(CesionAbono).filter(CesionAbono.id_cesion == id_cesion).first()
    if not cesion:
        return None
    db.delete(cesion)
    db.commit()
    return cesion


def get_cesion_activa(db: Session, dni_beneficiario: str):
    today = date.today()

    cesion = (
        db.query(CesionAbono, Abono)
        .join(Abono, CesionAbono.id_abono == Abono.id_abono)
        .filter(
            CesionAbono.dni_beneficiario == dni_beneficiario,
            CesionAbono.fecha_inicio <= today,
            CesionAbono.fecha_fin >= today
        )
        .order_by(CesionAbono.fecha_cesion.desc())
        .first()
    )

    if not cesion:
        return None

    cesion_abono, abono = cesion

    return {
        "dni_cedente": cesion_abono.dni_cedente,
        "dni_beneficiario": cesion_abono.dni_beneficiario,
        "fecha_inicio": cesion_abono.fecha_inicio,
        "fecha_fin": cesion_abono.fecha_fin,
        "fecha_cesion": cesion_abono.fecha_cesion,
        "temporada": abono.temporada,
        "fecha_inicio_abono": abono.fecha_inicio,
        "fecha_fin_abono": abono.fecha_fin,
    }
    
