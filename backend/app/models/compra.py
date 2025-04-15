from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Compra(Base):
    __tablename__ = "compra"

    dni = Column(String(9), ForeignKey("usuario.dni"), primary_key=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido", ondelete="RESTRICT"), primary_key=True)
    fecha_compra = Column(Date, nullable=False)
    pagado = Column(Boolean, default=False)

    usuario = relationship("Usuario", back_populates="compras")
    pedido = relationship("Pedido", back_populates="compras")
