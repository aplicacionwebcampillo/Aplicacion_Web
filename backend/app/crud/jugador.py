from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.exc import IntegrityError
from app.models.jugador import Jugador
from app.schemas.jugador import JugadorCreate, JugadorUpdate

def create_jugador(db: Session, jugador: JugadorCreate):
    db_jugador = Jugador(
        id_equipo=jugador.id_equipo,
        nombre=jugador.nombre,
        posicion=jugador.posicion,
        fecha_nacimiento=jugador.fecha_nacimiento,
        foto=jugador.foto,
        biografia=jugador.biografia,
        dorsal=jugador.dorsal,
    )
    try:
        db.add(db_jugador)
        db.commit()
        db.refresh(db_jugador) 
        return db_jugador
    except IntegrityError:
        db.rollback()  
        raise Exception("Error al crear el jugador, es posible que el equipo no exista.")

def get_jugador(db: Session, jugador_nombre: str):
    return db.query(Jugador).filter(Jugador.nombre == jugador_nombre).first()

def get_jugadores(db: Session, skip: int = 0, limit: int = 100):
    # Obtener los jugadores con paginación (skip, limit)
    return db.query(Jugador).offset(skip).limit(limit).all()

def update_jugador(db: Session, jugador_nombre: str, jugador_update: JugadorUpdate):
    db_jugador = db.query(Jugador).filter(Jugador.nombre == jugador_nombre).first()
    if db_jugador is None:
        return None

    if jugador_update.nombre:
        db_jugador.nombre = jugador_update.nombre
    if jugador_update.posicion:
        db_jugador.posicion = jugador_update.posicion
    if jugador_update.fecha_nacimiento:
        db_jugador.fecha_nacimiento = jugador_update.fecha_nacimiento
    if jugador_update.foto:
        db_jugador.foto = jugador_update.foto
    if jugador_update.biografia:
        db_jugador.biografia = jugador_update.biografia
    if jugador_update.dorsal:
        db_jugador.dorsal = jugador_update.dorsal

    db.commit()
    db.refresh(db_jugador)
    return db_jugador


def delete_jugador(db: Session, jugador_nombre: str):
    db_jugador = db.query(Jugador).filter(Jugador.nombre == jugador_nombre).first()
    if db_jugador is None:
        return None 

    db.delete(db_jugador)
    db.commit()
    return db_jugador

