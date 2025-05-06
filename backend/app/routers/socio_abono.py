from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.socio_abono import SocioAbonoCreate, SocioAbonoResponse, SocioAbonoUpdate
import app.crud.socio_abono as crud
from typing import List

router = APIRouter(prefix="/socio_abonos", tags=["Socios Abonos"])

@router.post("/", response_model=SocioAbonoResponse)
def crear_socio_abono(socio_abono: SocioAbonoCreate, db: Session = Depends(get_db)):
    return crud.create_socio_abono(db, socio_abono)

@router.get("/{dni}/{id_abono}", response_model=SocioAbonoResponse)
def obtener_socio_abono(dni: str, id_abono: int, db: Session = Depends(get_db)):
    socio_abono = crud.get_socio_abono(db, dni, id_abono)
    if not socio_abono:
        raise HTTPException(status_code=404, detail="SocioAbono no encontrado")
    return socio_abono

@router.get("/", response_model=List[SocioAbonoResponse])
def listar_socio_abonos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_socio_abonos(db, skip, limit)

@router.put("/{dni}/{id_abono}", response_model=SocioAbonoResponse)
def actualizar_socio_abono(dni: str, id_abono: int, socio_abono_update: SocioAbonoUpdate, db: Session = Depends(get_db)):
    socio_abono_actualizado = crud.update_socio_abono(db, dni, id_abono, socio_abono_update)
    if not socio_abono_actualizado:
        raise HTTPException(status_code=404, detail="SocioAbono no encontrado")
    return socio_abono_actualizado

@router.delete("/{dni}/{id_abono}", response_model=dict)
def eliminar_socio_abono(dni: str, id_abono: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_socio_abono(db, dni, id_abono)
    if not eliminado:
        raise HTTPException(status_code=404, detail="SocioAbono no encontrado")
    return {"mensaje": "SocioAbono eliminado correctamente"}

