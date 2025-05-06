from sqlalchemy.orm import Session
from app.models.socio_abono import SocioAbono
from app.schemas.socio_abono import SocioAbonoCreate, SocioAbonoUpdate
from app.models.abono import Abono
import datetime
from fastapi import HTTPException


def create_socio_abono(db: Session, socio_abono: SocioAbonoCreate):
    nuevo = SocioAbono(**socio_abono.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def get_socio_abono(db: Session, dni: str, id_abono: int):
    return db.query(SocioAbono).filter(
        SocioAbono.dni == dni,
        SocioAbono.id_abono == id_abono
    ).first()

def get_all_socio_abonos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SocioAbono).offset(skip).limit(limit).all()

def update_socio_abono(db: Session, dni: str, id_abono: int, socio_abono_update: SocioAbonoUpdate):
    socio_abono_db = db.query(SocioAbono).filter_by(dni=dni, id_abono=id_abono).first()
    if not socio_abono_db:
        raise HTTPException(status_code=404, detail="Socio-Abono no encontrado")

    # Solo actualizamos campos que no implican renovación
    if socio_abono_update.pagado is not None:
        socio_abono_db.pagado = socio_abono_update.pagado

    db.commit()
    db.refresh(socio_abono_db)
    return socio_abono_db


def delete_socio_abono(db: Session, dni: str, id_abono: int):
    socio_abono = get_socio_abono(db, dni, id_abono)
    if not socio_abono:
        return False
    db.delete(socio_abono)
    db.commit()
    return True

