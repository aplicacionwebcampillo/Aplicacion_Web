from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.abono import AbonoCreate, AbonoResponse, AbonoUpdate
import app.crud.abono as crud
from typing import List

router = APIRouter(prefix="/abonos", tags=["Abonos"])

@router.post("/", response_model=AbonoResponse)
def crear_abono(abono: AbonoCreate, db: Session = Depends(get_db)):
    return crud.create_abono(db, abono)

@router.get("/{id_abono}", response_model=AbonoResponse)
def obtener_abono(id_abono: int, db: Session = Depends(get_db)):
    abono = crud.get_abono(db, id_abono)
    if not abono:
        raise HTTPException(status_code=404, detail="Abono no encontrado")
    return abono

@router.get("/", response_model=List[AbonoResponse])
def listar_abonos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_abonos(db, skip, limit)

@router.put("/{id_abono}", response_model=AbonoResponse)
def actualizar_abono(id_abono: int, abono_update: AbonoUpdate, db: Session = Depends(get_db)):
    abono_actualizado = crud.update_abono(db, id_abono, abono_update)
    if not abono_actualizado:
        raise HTTPException(status_code=404, detail="Abono no encontrado")
    return abono_actualizado

@router.delete("/{id_abono}", response_model=dict)
def eliminar_abono(id_abono: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_abono(db, id_abono)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Abono no encontrado")
    return {"mensaje": "Abono eliminado correctamente"}

