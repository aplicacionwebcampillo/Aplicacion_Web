from sqlalchemy.orm import Session
from app.models.socio_abono import SocioAbono
from app.schemas.socio_abono import SocioAbonoCreate, SocioAbonoUpdate
from app.models.abono import Abono
import datetime
from fastapi import HTTPException
from app.crud.abono import get_abono
from datetime import date
from app.models.socio import Socio


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

def renovar_socio_abono(db: Session, dni: str, id_abono_actual: int, id_abono_nuevo: int):
    socio_abono_actual = db.query(SocioAbono).filter(
        SocioAbono.dni == dni, SocioAbono.id_abono == id_abono_actual
    ).first()

    if not socio_abono_actual:
        raise HTTPException(status_code=404, detail="Abono actual no encontrado")
    
    abono_actual = db.query(Abono).filter(Abono.id_abono == id_abono_actual).first()
    if not abono_actual:
        raise HTTPException(status_code=404, detail="Abono actual no encontrado")
    
    nuevo_socio_abono = SocioAbono(
        dni=dni,
        id_abono=id_abono_nuevo,
        fecha_compra=date.today(),
        pagado=False
    )

    db.add(nuevo_socio_abono)
    db.commit()
    db.refresh(nuevo_socio_abono)

    return nuevo_socio_abono


def get_abono_digital(db: Session, dni: str):
    socio = (
        db.query(Socio)
        .filter(Socio.dni == dni, Socio.estado == 'activo')
        .first()
    )

    if not socio:
        return None

    socio_abono = (
        db.query(SocioAbono)
        .filter(SocioAbono.dni == dni, SocioAbono.pagado == True)
        .order_by(SocioAbono.fecha_compra.desc())
        .first()
    )

    if not socio_abono:
        return None

    abono = (
        db.query(Abono)
        .filter(Abono.id_abono == socio_abono.id_abono)
        .first()
    )

    if not abono:
        return None

    return {
        "dni": socio.dni,
        "num_socio": socio.num_socio,
        "foto_perfil": socio.foto_perfil,
        "tipo_membresia": socio.tipo_membresia,
        "temporada": abono.temporada,
        "fecha_inicio": abono.fecha_inicio,
        "fecha_fin": abono.fecha_fin
    }

def validar_pago_socio_abono(db: Session, dni: str):
    socio = db.query(Socio).filter(Socio.dni == dni).first()
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")

    socio_abono = (
        db.query(SocioAbono)
        .filter(SocioAbono.dni == socio.dni)
        .order_by(SocioAbono.fecha_compra.desc())
        .first()
    )

    if not socio_abono:
        raise HTTPException(status_code=404, detail="No se encontró abono para este socio")

    socio_abono.pagado = True
    db.commit()
    db.refresh(socio_abono)
    return {"message": "Pago validado correctamente para abono", "id": socio_abono.id_abono}

