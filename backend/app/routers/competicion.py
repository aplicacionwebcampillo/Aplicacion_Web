from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import competicion as competicion_crud
from app.schemas.competicion import CompeticionCreate, CompeticionUpdate, CompeticionResponse
from app.database import get_db

router = APIRouter(prefix="/competiciones", tags=["competiciones"])


@router.get("/", response_model=List[CompeticionResponse])
def listar_competiciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    competiciones = competicion_crud.get_competiciones(db=db, skip=skip, limit=limit)
    return competiciones


@router.get("/{nombre}/{temporada}", response_model=CompeticionResponse)
def obtener_competicion(nombre: str, temporada: str, db: Session = Depends(get_db)):
    competicion = competicion_crud.get_competicion(db=db, nombre=nombre, temporada=temporada)
    if competicion is None:
        raise HTTPException(status_code=404, detail="Competición no encontrada")
    return competicion


@router.post("/", response_model=CompeticionResponse)
def crear_competicion(competicion: CompeticionCreate, db: Session = Depends(get_db)):
    db_competicion = competicion_crud.create_competicion(db=db, competicion=competicion)
    
    if db_competicion is None:
        raise HTTPException(status_code=404, detail="Competición no encontrada o no creada")
    
    return db_competicion


@router.put("/{nombre}/{temporada}", response_model=CompeticionResponse)
def actualizar_competicion(
    nombre: str,
    temporada: str,
    competicion_update: CompeticionUpdate,
    db: Session = Depends(get_db)
):
    db_competicion = competicion_crud.update_competicion(db=db, nombre=nombre, temporada=temporada, competicion_update=competicion_update)
    if db_competicion is None:
        raise HTTPException(status_code=404, detail="Competición no encontrada")
    return db_competicion


@router.delete("/{nombre}/{temporada}", response_model=CompeticionResponse)
def eliminar_competicion(nombre: str, temporada: str, db: Session = Depends(get_db)):
    db_competicion = competicion_crud.delete_competicion(db=db, nombre=nombre, temporada=temporada)
    if db_competicion is None:
        raise HTTPException(status_code=404, detail="Competición no encontrada")
    return db_competicion

