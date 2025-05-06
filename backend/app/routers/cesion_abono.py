from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.cesion_abono import (
    CesionAbonoCreate,
    CesionAbonoUpdate,
    CesionAbonoResponse
)
import app.crud.cesion_abono as crud

router = APIRouter(prefix="/cesiones", tags=["Cesiones de abono"])

@router.post("/", response_model=CesionAbonoResponse)
def crear_cesion_abono(cesion: CesionAbonoCreate, db: Session = Depends(get_db)):
    return crud.create_cesion_abono(db, cesion)

@router.get("/{id_cesion}", response_model=CesionAbonoResponse)
def obtener_cesion_abono(id_cesion: int, db: Session = Depends(get_db)):
    cesion = crud.get_cesion_abono(db, id_cesion)
    if not cesion:
        raise HTTPException(status_code=404, detail="Cesión no encontrada")
    return cesion

@router.get("/", response_model=List[CesionAbonoResponse])
def listar_cesiones_abono(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cesiones_abono(db, skip, limit)

@router.put("/{id_cesion}", response_model=CesionAbonoResponse)
def actualizar_cesion_abono(id_cesion: int, cesion_update: CesionAbonoUpdate, db: Session = Depends(get_db)):
    cesion_actualizada = crud.update_cesion_abono(db, id_cesion, cesion_update)
    if not cesion_actualizada:
        raise HTTPException(status_code=404, detail="Cesión no encontrada")
    return cesion_actualizada

@router.delete("/{id_cesion}", response_model=dict)
def eliminar_cesion_abono(id_cesion: int, db: Session = Depends(get_db)):
    cesion = crud.delete_cesion_abono(db, id_cesion)
    if not cesion:
        raise HTTPException(status_code=404, detail="Cesión no encontrada")
    return {"mensaje": "Cesión eliminada correctamente"}

