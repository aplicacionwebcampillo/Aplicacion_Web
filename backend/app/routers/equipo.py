from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.equipo import EquipoCreate
from app.crud import equipo as crud
from app.database import get_db

router = APIRouter(prefix="/equipos", tags=["equipos"])

@router.post("/")
def crear_equipo(equipo: EquipoCreate, db: Session = Depends(get_db)):
    return crud.create_equipo(db, equipo)

