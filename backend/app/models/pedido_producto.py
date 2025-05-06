from sqlalchemy import Column, Integer, Float, Table, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

pedido_producto = Table(
    'pedido_producto',
    Base.metadata,
    Column("pedido_id", Integer, ForeignKey("pedido.id_pedido")),
    Column("producto_id", Integer, ForeignKey("producto.id_producto")),
    Column("id", Integer, primary_key=True),
    Column("cantidad", Integer)
)
