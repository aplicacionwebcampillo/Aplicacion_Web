from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from typing import List
from app.schemas.equipo import EquipoCreate, EquipoUpdate, EquipoResponse
from app.crud import equipo as equipo_crud

router = APIRouter(prefix="/equipos", tags=["Equipos"])

@router.post("/", response_model=EquipoResponse)
def crear_equipo(equipo: EquipoCreate, db: Session = Depends(get_db)):
    return equipo_crud.create_equipo(db, equipo)

@router.get("/", response_model=List[EquipoResponse])
def listar_equipos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.equipo.get_equipos(db, skip=skip, limit=limit)

@router.get("/{id_equipo}", response_model=EquipoResponse)
def obtener_equipo(id_equipo: int, db: Session = Depends(get_db)):
    equipo = crud.equipo.get_equipo(db, id_equipo)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@router.put("/{id_equipo}", response_model=EquipoResponse)
def actualizar_equipo(id_equipo: int, equipo_update: EquipoUpdate, db: Session = Depends(get_db)):
    equipo = crud.equipo.update_equipo(db, id_equipo, equipo_update)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@router.delete("/{id_equipo}")
def eliminar_equipo(id_equipo: int, db: Session = Depends(get_db)):
    equipo = crud.equipo.delete_equipo(db, id_equipo)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"mensaje": "Equipo eliminado correctamente"}

