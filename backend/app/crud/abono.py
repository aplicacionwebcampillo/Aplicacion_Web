from sqlalchemy.orm import Session
from app.models.abono import Abono
from app.schemas.abono import AbonoCreate, AbonoUpdate

def create_abono(db: Session, abono: AbonoCreate):
    nuevo_abono = Abono(**abono.dict())
    db.add(nuevo_abono)
    db.commit()
    db.refresh(nuevo_abono)
    return nuevo_abono

def get_abono(db: Session, id_abono: int):
    return db.query(Abono).filter(Abono.id_abono == id_abono).first()

def get_abonos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Abono).offset(skip).limit(limit).all()

def update_abono(db: Session, id_abono: int, abono_update: AbonoUpdate):
    abono = db.query(Abono).filter(Abono.id_abono == id_abono).first()
    if not abono:
        return None
    for key, value in abono_update.dict(exclude_unset=True).items():
        setattr(abono, key, value)
    db.commit()
    db.refresh(abono)
    return abono

def delete_abono(db: Session, id_abono: int):
    abono = db.query(Abono).filter(Abono.id_abono == id_abono).first()
    if not abono:
        return False
    db.delete(abono)
    db.commit()
    return True

