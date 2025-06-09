from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class PedidoProducto(Base):
    __tablename__ = "pedido_producto"

    id = Column(Integer, primary_key=True, index=True)  # O podrías usar llave compuesta pedido_id+producto_id
    pedido_id = Column(Integer, ForeignKey("pedido.id_pedido"))
    producto_id = Column(Integer, ForeignKey("producto.id_producto"))
    cantidad = Column(Integer, nullable=False)

    pedido = relationship("Pedido", back_populates="pedido_productos")
    producto = relationship("Producto")

