from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import partido as partido_crud
from app.schemas.partido import PartidoCreate, PartidoUpdate, PartidoResponse
from app.database import get_db

router = APIRouter(prefix="/partidos", tags=["Partidos"])

@router.post("/", response_model=PartidoResponse, status_code=status.HTTP_201_CREATED)
def crear_partido(partido: PartidoCreate, db: Session = Depends(get_db)):
    return create_partido(db, partido)


@router.get("/{nombre_competicion}/{temporada_competicion}/{local}/{visitante}", response_model=PartidoResponse)
def obtener_partido(nombre_competicion: str, temporada_competicion: str, local: str, visitante: str, db: Session = Depends(get_db)):
    db_partido = get_partido(db, nombre_competicion, temporada_competicion, local, visitante)
    if db_partido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El partido no fue encontrado"
        )
    return db_partido


@router.get("/", response_model=List[PartidoResponse])
def obtener_partidos(nombre_competicion: str = None, temporada_competicion: str = None, db: Session = Depends(get_db)):
    return get_partidos_completos(db, nombre_competicion, temporada_competicion)


@router.put("/{nombre_competicion}/{temporada_competicion}/{local}/{visitante}", response_model=PartidoResponse)
def actualizar_partido(
    nombre_competicion: str,
    temporada_competicion: str,
    local: str,
    visitante: str,
    partido: PartidoUpdate,
    db: Session = Depends(get_db)
):
    return update_partido(db, nombre_competicion, temporada_competicion, local, visitante, partido)


@router.delete("/{nombre_competicion}/{temporada_competicion}/{local}/{visitante}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_partido(
    nombre_competicion: str,
    temporada_competicion: str,
    local: str,
    visitante: str,
    db: Session = Depends(get_db)
):
    delete_partido(db, nombre_competicion, temporada_competicion, local, visitante)
    return {"detail": "Partido eliminado correctamente"}

