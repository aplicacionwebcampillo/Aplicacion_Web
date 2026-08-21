from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.exc import IntegrityError
from app.models.jugador import Jugador
from app.schemas.jugador import JugadorCreate, JugadorUpdate


def _mensaje_integridad(error: IntegrityError) -> str:
    # Los triggers de la BD (p.ej. validar_dorsal_unico) lanzan un mensaje
    # legible en la primera línea de la excepción original; el resto es
    # contexto interno de PL/pgSQL que no aporta nada al usuario.
    return str(error.orig).splitlines()[0] if error.orig else str(error)


def create_jugador(db: Session, jugador: JugadorCreate):
    db_jugador = Jugador(**jugador.dict())
    try:
        db.add(db_jugador)
        db.commit()
        db.refresh(db_jugador)
        return db_jugador
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail=_mensaje_integridad(e))

def get_jugador(db: Session, jugador_nombre: str):
    return db.query(Jugador).filter(Jugador.nombre == jugador_nombre).first()

def get_jugadores(db: Session, skip: int = 0, limit: int = 200):
    # Obtener los jugadores con paginación (skip, limit)
    return db.query(Jugador).offset(skip).limit(limit).all()

def update_jugador(db: Session, jugador_nombre: str, jugador_update: JugadorUpdate):
    db_jugador = db.query(Jugador).filter(Jugador.nombre == jugador_nombre).first()
    if db_jugador is None:
        return None

    # exclude_unset (no "campo con valor verdadero") para que se puedan
    # guardar valores como 0 goles/tarjetas o cadenas vacías sin que la
    # comprobación los descarte por ser "falsy".
    for campo, valor in jugador_update.dict(exclude_unset=True).items():
        setattr(db_jugador, campo, valor)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail=_mensaje_integridad(e))
    db.refresh(db_jugador)
    return db_jugador


def delete_jugador(db: Session, jugador_nombre: str):
    db_jugador = db.query(Jugador).filter(Jugador.nombre == jugador_nombre).first()
    if db_jugador is None:
        return None 

    db.delete(db_jugador)
    db.commit()
    return db_jugador

