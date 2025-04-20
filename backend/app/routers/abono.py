from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import abono as crud
from app.database import get_db

router = APIRouter(prefix="/abonos", tags=["abonos"])

@router.post("/comprar")
def comprar_abono(dni: str, id_abono: int, db: Session = Depends(get_db)):
    crud.comprar_abono(db, dni, id_abono)
    return {"mensaje": "Abono comprado correctamente"}

@router.post("/renovar")
def renovar_abono(dni: str, id_abono: int, db: Session = Depends(get_db)):
    crud.renovar_abono(db, dni, id_abono)
    return {"mensaje": "Abono renovado correctamente"}

@router.post("/cancelar")
def cancelar_abono(dni: str, id_abono: int, db: Session = Depends(get_db)):
    crud.cancelar_abono(db, dni, id_abono)
    return {"mensaje": "Abono cancelado correctamente"}

