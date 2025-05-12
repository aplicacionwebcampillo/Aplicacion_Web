from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.predice import PrediceCreate, PrediceUpdate, PrediceResponse
from app.crud import predice as predice_crud
from typing import List

router = APIRouter(prefix="/predice", tags=["Predice"])


@router.post("/", response_model=PrediceResponse)
def crear_prediccion(prediccion: PrediceCreate, db: Session = Depends(get_db)):
    return predice_crud.create_prediccion(db, prediccion)


@router.get("/", response_model=List[PrediceResponse])
def obtener_todas_predicciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return predice_crud.get_predicciones(db, skip=skip, limit=limit)

@router.put("/validar_pago/{dni}")
def validar_pago_predice(
    dni: str,
    nombre_competicion: str,
    temporada_competicion: str,
    local: str,
    visitante: str,
    resultado: str,
    db: Session = Depends(get_db)
):
    return predice_crud.validar_pago_predice(
        db,
        dni,
        nombre_competicion,
        temporada_competicion,
        local,
        visitante,
        resultado
    )

@router.get("/{dni}/{nombre_competicion}/{temporada_competicion}/{local}/{visitante}", response_model=PrediceResponse)
def obtener_prediccion_individual(
    dni: str,
    nombre_competicion: str,
    temporada_competicion: str,
    local: str,
    visitante: str,
    db: Session = Depends(get_db)
):
    prediccion = predice_crud.get_prediccion(db, dni, nombre_competicion, temporada_competicion, local, visitante)
    if not prediccion:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
    return prediccion


@router.put("/{dni}/{nombre_competicion}/{temporada_competicion}/{local}/{visitante}", response_model=PrediceResponse)
def actualizar_prediccion(
    dni: str,
    nombre_competicion: str,
    temporada_competicion: str,
    local: str,
    visitante: str,
    prediccion_update: PrediceUpdate,
    db: Session = Depends(get_db)
):
    try:
        return predice_crud.update_prediccion(db, dni, nombre_competicion, temporada_competicion, local, visitante, prediccion_update)
    except:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")


@router.delete("/{dni}/{nombre_competicion}/{temporada_competicion}/{local}/{visitante}")
def eliminar_prediccion(
    dni: str,
    nombre_competicion: str,
    temporada_competicion: str,
    local: str,
    visitante: str,
    db: Session = Depends(get_db)
):
    success = predice_crud.delete_prediccion(db, dni, nombre_competicion, temporada_competicion, local, visitante)
    if not success:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
    return {"ok": True, "mensaje": "Predicción eliminada correctamente"}

