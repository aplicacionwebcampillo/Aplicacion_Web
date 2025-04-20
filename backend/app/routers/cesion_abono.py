from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.crud import cesion_abono as crud
from app.database import get_db

router = APIRouter(prefix="/cesiones", tags=["cesion_abono"])

@router.post("/")
def ceder_abono(dni_cedente: str, dni_beneficiario: str, id_abono: int, fecha_inicio: date, fecha_fin: date, db: Session = Depends(get_db)):
    crud.ceder_abono_temporal(db, dni_cedente, dni_beneficiario, id_abono, fecha_inicio, fecha_fin)
    return {"mensaje": "Cesión registrada correctamente"}

