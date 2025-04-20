from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.jugador import Jugador
from app.schemas.jugador import JugadorCreate

def create_jugador(db: Session, jugador: JugadorCreate):
    db.execute(text("SELECT agregar_jugador(:id_equipo, :nombre, :posicion, :fecha_nacimiento, :foto, :biografia)"), jugador.dict())
    db.commit()

def delete_jugador(db: Session, id_jugador: int, id_equipo: int):
    db.execute(text("SELECT eliminar_jugador(:id_jugador, :id_equipo)"), {"id_jugador": id_jugador, "id_equipo": id_equipo})
    db.commit()

