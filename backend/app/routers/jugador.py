from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.database import get_db
from app.schemas.jugador import JugadorCreate, JugadorUpdate, JugadorResponse
from app.crud import jugador as jugador_crud

router = APIRouter()

@router.post("/", response_model=JugadorResponse)
def crear_jugador(jugador: JugadorCreate, db: Session = Depends(get_db)):
    db_jugador = crud.jugador.create_jugador(db=db, jugador=jugador)
    
    if db_jugador:
        equipo = crud.equipo.get_equipo(db, db_jugador.id_equipo)
        if equipo:
            equipo.num_jugadores += 1
            db.commit()
            db.refresh(equipo)
    
    return db_jugador


@router.get("/{jugador_id}", response_model=JugadorResponse)
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = crud.jugador.get_jugador(db=db, jugador_id=jugador_id)
    if db_jugador is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    return db_jugador


@router.get("/", response_model=List[JugadorResponse])
def obtener_jugadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_jugadores = crud.jugador.get_jugadores(db=db, skip=skip, limit=limit)
    return db_jugadores


@router.put("/{jugador_id}", response_model=JugadorResponse)
def actualizar_jugador(jugador_id: int, jugador_update: JugadorUpdate, db: Session = Depends(get_db)):
    db_jugador = crud.jugador.update_jugador(db=db, jugador_id=jugador_id, jugador_update=jugador_update)
    if db_jugador is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    return db_jugador


@router.delete("/{jugador_id}", response_model=JugadorResponse)
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = crud.jugador.delete_jugador(db=db, jugador_id=jugador_id)
    if db_jugador is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    
    # Actualizar el campo num_jugadores del equipo correspondiente
    equipo = crud.equipo.get_equipo(db, db_jugador.id_equipo)
    if equipo:
        equipo.num_jugadores -= 1
        db.commit()
        db.refresh(equipo)
    
    return db_jugador
    
