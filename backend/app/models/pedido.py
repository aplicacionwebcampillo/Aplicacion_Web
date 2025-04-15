from sqlalchemy import Column, Integer, Numeric
from sqlalchemy.orm import relationship
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True)
    descuento = Column(Numeric(10, 2), default=0.00)
    precio_total = Column(Numeric(10, 2), nullable=False)
    cantidad = Column(Integer)

    compras = relationship("Compra", back_populates="pedido")
