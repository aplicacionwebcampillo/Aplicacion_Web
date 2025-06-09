from sqlalchemy import Column, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.pedido_producto import pedido_producto

class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True, index=True)
    descuento = Column(Float)
    precio_total = Column(Float)

    productos = relationship('Producto', secondary='pedido_producto', back_populates='pedidos')
    compras = relationship("Compra", back_populates="pedido")
    pedido_productos = relationship("PedidoProducto", back_populates="pedido", cascade="all, delete-orphan")
