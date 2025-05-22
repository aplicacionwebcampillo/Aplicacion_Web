from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.clasificacion import ClasificacionCreate, ClasificacionUpdate, ClasificacionResponse
from app.crud import clasificacion as clasificacion_crud

router = APIRouter(prefix="/clasificaciones", tags=["Clasificaciones"])

@router.post("/", response_model=ClasificacionResponse, status_code=status.HTTP_201_CREATED)
def crear_clasificacion(clasificacion: ClasificacionCreate, db: Session = Depends(get_db)):
    return clasificacion_crud.create_clasificacion(db, clasificacion)


@router.get("/", response_model=List[ClasificacionResponse])
def obtener_clasificaciones(nombre_competicion: str = None, temporada_competicion: str = None, db: Session = Depends(get_db)):
    return clasificacion_crud.get_clasificaciones(db, nombre_competicion, temporada_competicion)


@router.get("/{nombre_competicion}/{temporada_competicion}/{equipo}", response_model=ClasificacionResponse)
def obtener_clasificacion(nombre_competicion: str, temporada_competicion: str, equipo: str, db: Session = Depends(get_db)):
    clasificacion = clasificacion_crud.get_clasificacion(db, nombre_competicion, temporada_competicion, equipo)
    if not clasificacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clasificación no encontrada")
    return clasificacion


@router.put("/{nombre_competicion}/{temporada_competicion}/{equipo}", response_model=ClasificacionResponse)
def actualizar_clasificacion(
    nombre_competicion: str,
    temporada_competicion: str,
    equipo: str,
    clasificacion_update: ClasificacionUpdate,
    db: Session = Depends(get_db)
):
    return clasificacion_crud.update_clasificacion(db, nombre_competicion, temporada_competicion, equipo, clasificacion_update)


@router.delete("/{nombre_competicion}/{temporada_competicion}/{equipo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_clasificacion(nombre_competicion: str, temporada_competicion: str, equipo: str, db: Session = Depends(get_db)):
    eliminado = clasificacion_crud.delete_clasificacion(db, nombre_competicion, temporada_competicion, equipo)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clasificación no encontrada")
    return {"detail": "Clasificación eliminada correctamente"}

