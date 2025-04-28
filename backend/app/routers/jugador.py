from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.jugador import JugadorCreate, JugadorUpdate, JugadorResponse
from app.database import get_db
from app.crud import jugador as crud

router = APIRouter(prefix="/jugadores", tags=["Jugadores"])

@router.post("/", response_model=JugadorResponse)
def crear_jugador(jugador: JugadorCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_jugador(db, jugador)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[JugadorResponse])
def listar_jugador(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_jugadores(db, skip, limit)

@router.get("/{nombre}", response_model=JugadorResponse)
def obtener_jugador(nombre: str, db: Session = Depends(get_db)):
    jugador = crud.get_jugador(db, nombre)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@router.put("/{nombre}", response_model=JugadorResponse)
def actualizar_jugadorr(nombre: str, jugador_update: JugadorUpdate, db: Session = Depends(get_db)):
    jugador = crud.update_jugador(db, nombre, jugador_update)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@router.delete("/{nombre}")
def eliminar_jugador(nombre: str, db: Session = Depends(get_db)):
    ok = crud.delete_jugador(db, nombre)
    if not ok:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"ok": True, "mensaje": "Jugador eliminado correctamente"}


