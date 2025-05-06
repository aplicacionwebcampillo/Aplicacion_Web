from sqlalchemy.orm import Session
from app.models.cesion_abono import CesionAbono
from app.schemas.cesion_abono import CesionAbonoCreate, CesionAbonoUpdate

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

