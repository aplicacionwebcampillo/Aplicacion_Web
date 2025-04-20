from sqlalchemy.orm import Session
from app.models.compra import Compra
from app.schemas.compra import CompraCreate

def create_compra(db: Session, compra: CompraCreate):
    db_compra = Compra(**compra.dict())
    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    return db_compra

def get_compra(db: Session, dni: str, id_pedido: int):
    return db.query(Compra).filter(Compra.dni == dni, Compra.id_pedido == id_pedido).first()

