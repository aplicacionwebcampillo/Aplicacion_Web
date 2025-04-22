from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.socio import SocioCreate, SocioResponse, SocioUpdate
import app.crud.socio as crud
from typing import List

router = APIRouter(prefix="/socios", tags=["Socios"])

@router.post("/", response_model=SocioResponse)
def crear_socio(socio: SocioCreate, db: Session = Depends(get_db)):
    db_socio = crud.get_socio(db, socio.dni)
    if db_socio:
        raise HTTPException(status_code=400, detail="Socio ya registrado")
    return crud.create_socio(db, socio)

@router.get("/{dni}", response_model=SocioResponse)
def obtener_socio(dni: str, db: Session = Depends(get_db)):
    socio = crud.get_socio(db, dni)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return socio

@router.get("/", response_model=List[SocioResponse])
def listar_socios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_socios(db, skip, limit)
    
@router.put("/{dni}", response_model=SocioResponse)
def actualizar_socio(dni: str, socio: SocioUpdate, db: Session = Depends(get_db)):
    socio_actualizado = crud.update_socio(db, dni, socio)
    if not socio_actualizado:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return socio_actualizado

@router.delete("/{dni}", response_model=dict)
def eliminar_socio(dni: str, db: Session = Depends(get_db)):
    socio_eliminado = crud.delete_socio(db, dni)
    if not socio_eliminado:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return {"mensaje": "Socio eliminado correctamente"}

