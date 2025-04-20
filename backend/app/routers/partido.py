from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import partido as crud
from app.database import get_db

router = APIRouter(prefix="/partidos", tags=["partidos"])

@router.put("/actualizar_resultado/")
def actualizar_resultado(nombre_competicion: str, temporada: str, local: str, visitante: str, resultado: str, db: Session = Depends(get_db)):
    crud.actualizar_resultado(db, nombre_competicion, temporada, local, visitante, resultado)
    return {"mensaje": "Resultado actualizado correctamente"}

