from sqlalchemy.orm import Session
from app.models.pedido import Pedido
from app.models.producto import Producto
from app.schemas.pedido import PedidoCreate, PedidoUpdate
from collections import Counter
from sqlalchemy import insert
from app.models.pedido_producto import pedido_producto

def create_pedido(db: Session, pedido: PedidoCreate):
    db_pedido = Pedido(
        descuento=pedido.descuento,
        precio_total=pedido.precio_total
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)

    productos_contados = Counter(pedido.productos_ids)

    for producto_id, cantidad in productos_contados.items():
        stmt = insert(pedido_producto).values(
            pedido_id=db_pedido.id_pedido,
            producto_id=producto_id,
            cantidad=cantidad
        )
        db.execute(stmt)

    db.commit()
    return db_pedido

def get_pedido(db: Session, id_pedido: int):
    return db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

def get_pedidos(db: Session):
    return db.query(Pedido).all()

from sqlalchemy import delete, insert
from collections import Counter
from app.models.pedido_producto import pedido_producto

def update_pedido(db: Session, id_pedido: int, pedido_update: PedidoUpdate):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido:
        return None

    # Actualiza campos del pedido
    pedido.descuento = pedido_update.descuento
    pedido.precio_total = pedido_update.precio_total
    db.commit()

    # Elimina productos anteriores del pedido
    db.execute(delete(pedido_producto).where(pedido_producto.c.pedido_id == id_pedido))

    # Añade los nuevos productos con sus cantidades
    productos_contados = Counter(pedido_update.productos_ids)
    for producto_id, cantidad in productos_contados.items():
        stmt = insert(pedido_producto).values(
            pedido_id=id_pedido,
            producto_id=producto_id,
            cantidad=cantidad
        )
        db.execute(stmt)

    db.commit()
    return pedido




def delete_pedido(db: Session, id_pedido: int):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if pedido:
        db.delete(pedido)
        db.commit()
    return pedido

