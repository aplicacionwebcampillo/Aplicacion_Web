from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.predice import PrediceCreate
from app.crud import predice as crud
from app.database import get_db

router = APIRouter(prefix="/predicciones", tags=["predice"])

@router.post("/")
def hacer_prediccion(prediccion: PrediceCreate, db: Session = Depends(get_db)):
    return crud.create_prediccion(db, prediccion)

@router.get("/usuario/{dni}")
def obtener_predicciones(dni: str, db: Session = Depends(get_db)):
    return crud.get_predicciones_por_usuario(db, dni)

