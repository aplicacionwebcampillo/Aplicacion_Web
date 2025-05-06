from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    dni = Column(String(9), primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(15))
    fecha_nacimiento = Column(Date, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)

    socio = relationship("Socio", back_populates="usuario", uselist=False)
    administrador = relationship("Administrador", back_populates="usuario", uselist=False)
    compras = relationship("Compra", back_populates="usuario")
    posts_foro = relationship("PostForo", back_populates="usuario")
    cesiones_recibidas = relationship("CesionAbono", back_populates="usuario_beneficiario")



