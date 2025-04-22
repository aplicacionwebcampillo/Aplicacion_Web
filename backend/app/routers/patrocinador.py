from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.patrocinador import PatrocinadorCreate, PatrocinadorUpdate, PatrocinadorResponse
from app.database import get_db
from app.crud import patrocinador as crud

router = APIRouter(prefix="/patrocinadores", tags=["Patrocinadores"])

@router.post("/", response_model=PatrocinadorResponse)
def crear_patrocinador(patrocinador: PatrocinadorCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_patrocinador(db, patrocinador)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PatrocinadorResponse])
def listar_patrocinadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_patrocinadores(db, skip, limit)

@router.get("/{nombre}", response_model=PatrocinadorResponse)
def obtener_patrocinador(nombre: str, db: Session = Depends(get_db)):
    patrocinador = crud.get_patrocinador(db, nombre)
    if not patrocinador:
        raise HTTPException(status_code=404, detail="Patrocinador no encontrado")
    return patrocinador

@router.put("/{nombre}", response_model=PatrocinadorResponse)
def actualizar_patrocinador(nombre: str, patrocinador_update: PatrocinadorUpdate, db: Session = Depends(get_db)):
    patrocinador = crud.update_patrocinador(db, nombre, patrocinador_update)
    if not patrocinador:
        raise HTTPException(status_code=404, detail="Patrocinador no encontrado")
    return patrocinador

@router.delete("/{nombre}")
def eliminar_patrocinador(nombre: str, db: Session = Depends(get_db)):
    ok = crud.delete_patrocinador(db, nombre)
    if not ok:
        raise HTTPException(status_code=404, detail="Patrocinador no encontrado")
    return {"ok": True, "mensaje": "Patrocinador eliminado correctamente"}

