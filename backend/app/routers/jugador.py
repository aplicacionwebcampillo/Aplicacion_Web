from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.jugador import JugadorCreate
from app.crud import jugador as crud
from app.database import get_db

router = APIRouter(prefix="/jugadores", tags=["jugadores"])

@router.post("/")
def agregar_jugador(jugador: JugadorCreate, db: Session = Depends(get_db)):
    return crud.create_jugador(db, jugador)

