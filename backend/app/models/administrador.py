from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Administrador(Base):
    __tablename__ = "administrador"

    dni = Column(String(9), ForeignKey("usuario.dni"), primary_key=True)
    cargo = Column(String(50), nullable=False)
    permisos = Column(String(50), nullable=False)
    foto_perfil = Column(String(255))
    estado = Column(String(15), default='activo')

    usuario = relationship("Usuario", back_populates="administrador")
