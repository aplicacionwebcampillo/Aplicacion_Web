from sqlalchemy import Column, Integer, String, Numeric
from app.database import Base

class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    imagen = Column(String(255), nullable=False)
