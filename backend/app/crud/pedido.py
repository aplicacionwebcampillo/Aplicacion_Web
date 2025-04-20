from sqlalchemy.orm import Session
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate

def create_pedido(db: Session, pedido: PedidoCreate):
    db_pedido = Pedido(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def get_pedido(db: Session, id_pedido: int):
    return db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

