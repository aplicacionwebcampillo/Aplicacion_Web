from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud import partido as partido_crud
from app.schemas.partido import PartidoCreate, PartidoUpdate, PartidoResponse
from app.database import get_db
from fastapi import status

router = APIRouter(prefix="/partidos", tags=["Partidos"])

@router.post("/", response_model=PartidoResponse, status_code=status.HTTP_201_CREATED)
def crear_partido(partido: PartidoCreate, db: Session = Depends(get_db)):
    return partido_crud.create_partido(db, partido)


@router.get("/{nombre_competicion}/{temporada_competicion}/{local}/{visitante}", response_model=PartidoResponse)
def obtener_partido(nombre_competicion: str, temporada_competicion: str, local: str, visitante: str, db: Session = Depends(get_db)):
    db_partido = partido_crud.get_partido(db, nombre_competicion, temporada_competicion, local, visitante)
    if db_partido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El partido no fue encontrado"
        )
    return db_partido


@router.get("/", response_model=List[PartidoResponse])
def obtener_partidos(nombre_competicion: str = None, temporada_competicion: str = None, db: Session = Depends(get_db)):
    return partido_crud.get_partidos_completos(db, nombre_competicion, temporada_competicion)


@router.put("/{nombre_competicion}/{temporada_competicion}/{local}/{visitante}", response_model=PartidoResponse)
def actualizar_partido(
    nombre_competicion: str,
    temporada_competicion: str,
    local: str,
    visitante: str,
    partido: PartidoUpdate,
    db: Session = Depends(get_db)
):
    return partido_crud.update_partido(db, nombre_competicion, temporada_competicion, local, visitante, partido)


@router.delete("/{nombre_competicion}/{temporada_competicion}/{local}/{visitante}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_partido(
    nombre_competicion: str,
    temporada_competicion: str,
    local: str,
    visitante: str,
    db: Session = Depends(get_db)
):
    partido_crud.delete_partido(db, nombre_competicion, temporada_competicion, local, visitante)
    return {"detail": "Partido eliminado correctamente"}


@router.get("/calendario", response_model=List[PartidoResponse])
def calendario_partidos(
    nombre_competicion: Optional[str] = None,
    temporada_competicion: Optional[str] = None,
    categoria: Optional[str] = None,
    jugado: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    return partido_crud.get_calendario_partidos(
        db,
        nombre_competicion=nombre_competicion,
        temporada_competicion=temporada_competicion,
        categoria=categoria,
        jugado=jugado,
    )











