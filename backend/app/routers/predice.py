from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.predice import PrediceCreate, PrediceUpdate, PrediceResponse
from app.crud import predice as predice_crud
from typing import List
from app.models import Usuario
from app.utils.emails_utils import enviar_correos
import asyncio

router = APIRouter(prefix="/predice", tags=["Predice"])


@router.post("/", response_model=PrediceResponse)
async def crear_prediccion(prediccion: PrediceCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.dni == prediccion.dni).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cliente_email = usuario.email
    
    await enviar_correos(
        cliente_email=cliente_email,
        asunto_cliente="Predicción completada",
        cuerpo_cliente=(
            f"Hola, gracias por intentar predicir un partido del Campillo del Río CF.\n"
            f"DNI:{prediccion.dni}, \nNombre Competicion: {prediccion.nombre_competicion}, \n"
            f"Temporada Competicion: {prediccion.temporada_competicion}, \nLocal: {prediccion.local}, \n"
            f"Visitante: {prediccion.visitante}, \nResultado Local: {prediccion.resultado_local}, \n"
            f"Resultado Visitante: {prediccion.resultado_visitante}, \nPagado: {prediccion.pagado}"
        ),
        asunto_admin="Nueva predicción registrada",
        cuerpo_admin=(
            f"Se ha registrado una nueva predicción: \nDNI:{prediccion.dni}, \n"
            f"Nombre Competicion: {prediccion.nombre_competicion}, \nTemporada Competicion: {prediccion.temporada_competicion}, \n"
            f"Local: {prediccion.local}, \nVisitante: {prediccion.visitante}, \n"
            f"Resultado Local: {prediccion.resultado_local}, \nResultado Visitante: {prediccion.resultado_visitante}, \n"
            f"Pagado: {prediccion.pagado}"
        )
    )
    
    db_prediccion = predice_crud.create_prediccion(db, prediccion)
    return PrediceResponse.from_orm(db_prediccion)


   

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
    resultado_local: str,
    resultado_visitante: str,
    db: Session = Depends(get_db)
):
    return predice_crud.validar_pago_predice(
        db,
        dni,
        nombre_competicion,
        temporada_competicion,
        local,
        visitante,
    	resultado_local,
    	resultado_visitante,
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

