from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.socio_abono import SocioAbonoCreate, SocioAbonoResponse, SocioAbonoUpdate
import app.crud.socio_abono as crud
from typing import List
from app import crud
from app.models.socio import Socio
from app.models.socio_abono import SocioAbono
from app.models.abono import Abono
from sqlalchemy.orm import joinedload
from app.crud.abono import get_abono
import app.crud.socio_abono as crud


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


@router.post("/renovar/{dni}/{id_abono_nuevo}")
def renovar_abono(dni: str, id_abono_nuevo: int, db: Session = Depends(get_db)):
    socio_abono_actual = db.query(SocioAbono, Abono).join(
        Abono, SocioAbono.id_abono == Abono.id_abono
    ).filter(
        SocioAbono.dni == dni
    ).order_by(Abono.fecha_inicio.desc()).first()

    if not socio_abono_actual:
        raise HTTPException(status_code=404, detail="Abono actual no encontrado")

    socio_abono_actual, abono_actual = socio_abono_actual

    abono_nuevo = get_abono(db, id_abono_nuevo)
    if not abono_nuevo:
        raise HTTPException(status_code=404, detail="Nuevo abono no encontrado")

    socio_abono_existente = crud.get_socio_abono(db, dni, id_abono_nuevo)
    if socio_abono_existente:
        raise HTTPException(status_code=400, detail="El socio ya tiene el nuevo abono")

    try:
        crud.renovar_socio_abono(db, dni, abono_actual.id_abono, id_abono_nuevo)
        return {"message": "Abono renovado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al renovar el abono: {e}")


@router.get("/socio/{dni}/abono_digital")
def abono_digital(dni: str, db: Session = Depends(get_db)):
    abono = crud.get_abono_digital(db, dni)
    if not abono:
        raise HTTPException(status_code=404, detail="No se encontró abono digital válido para este socio")
    return abono



