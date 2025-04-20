from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.abono import Abono
from app.schemas.abono import AbonoCreate

def comprar_abono(db: Session, dni: str, id_abono: int):
    db.execute(text("SELECT comprar_abono(:dni, :id_abono)"), {"dni": dni, "id_abono": id_abono})
    db.commit()

def renovar_abono(db: Session, dni: str, id_abono: int):
    db.execute(text("SELECT renovar_abono(:dni, :id_abono)"), {"dni": dni, "id_abono": id_abono})
    db.commit()

def cancelar_abono(db: Session, dni: str, id_abono: int):
    db.execute(text("SELECT cancelar_abono(:dni, :id_abono)"), {"dni": dni, "id_abono": id_abono})
    db.commit()

