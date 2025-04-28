from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.jugador import Jugador
from app.schemas.jugador import JugadorCreate, JugadorUpdate

def create_jugador(db: Session, jugador: JugadorCreate):
    db.execute(text("""
        SELECT agregar_jugador(
            :p_id_equipo,
            :p_nombre,
            :p_posicion,
            :p_fecha_nacimiento,
            :p_foto,
            :p_biografia,
            :p_dorsal
        )
    """), {
        "p_id_equipo": jugador.id_equipo,
        "p_nombre": jugador.nombre,
        "p_posicion": jugador.posicion,
        "p_fecha_nacimiento": jugador.fecha_nacimiento,
        "p_foto": jugador.foto,
	"p_biografia": jugador.biografia,
        "p_dorsal": jugador.dorsal
    })
    db.commit()
    return db.query(Jugador).filter(Jugador.nombre == jugador.nombre).first()

def get_jugador(db: Session, nombre: str):
    return db.query(Jugador).filter(Jugador.nombre == nombre).first()

def get_jugadores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Jugador).offset(skip).limit(limit).all()

def update_jugador(db: Session, nombre: str, jugador_update: JugadorUpdate):
    jugador = db.query(Jugador).filter(Jugador.nombre == nombre).first()
    if not jugador:
        return None
    for key, value in jugador_update.dict(exclude_unset=True).items():
        setattr(jugador, key, value)
    db.commit()
    db.refresh(jugador)
    return jugador

def delete_jugador(db: Session, nombre: str):
    jugador = db.query(Jugador).filter(Jugador.nombre == nombre).first()
    if jugador:
        db.delete(jugador)
    db.commit()
    return True


