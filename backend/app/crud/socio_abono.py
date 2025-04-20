from sqlalchemy.orm import Session
from app.models.socio_abono import SocioAbono
from app.schemas.socio_abono import SocioAbonoCreate

def create_socio_abono(db: Session, socio_abono: SocioAbonoCreate):
    db_socio_abono = SocioAbono(**socio_abono.dict())
    db.add(db_socio_abono)
    db.commit()
    db.refresh(db_socio_abono)
    return db_socio_abono

def get_abonos_por_socio(db: Session, dni: str):
    return db.query(SocioAbono).filter(SocioAbono.dni == dni).all()

