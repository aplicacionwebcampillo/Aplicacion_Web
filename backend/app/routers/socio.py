from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.socio import SocioCreate
from app.crud import socio as crud
from app.database import get_db

router = APIRouter(prefix="/socios", tags=["socios"])

@router.post("/")
def registrar_socio(socio: SocioCreate, db: Session = Depends(get_db)):
    return crud.create_socio(db, socio)

@router.get("/{dni}")
def obtener_socio(dni: str, db: Session = Depends(get_db)):
    socio = crud.get_socio(db, dni)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return socio

