from sqlalchemy.orm import Session
from app.models.predice import Predice
from app.schemas.predice import PrediceCreate

def create_prediccion(db: Session, predice: PrediceCreate):
    db_predice = Predice(**predice.dict())
    db.add(db_predice)
    db.commit()
    db.refresh(db_predice)
    return db_predice

def get_predicciones_por_usuario(db: Session, dni: str):
    return db.query(Predice).filter(Predice.dni == dni).all()

