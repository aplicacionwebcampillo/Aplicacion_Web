from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    dni = Column(String(9), primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=True)
    fecha_nacimiento = Column(Date, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    tipo_usuario = Column(String(20), nullable=False)  # socio, no_socio, administrador

    # Relaciones con otras tablas (importadas en otros archivos)
    socio = relationship("Socio", back_populates="usuario", uselist=False)
    no_socio = relationship("NoSocio", back_populates="usuario", uselist=False)
    administrador = relationship("Administrador", back_populates="usuario", uselist=False)
    compras = relationship("Compra", back_populates="usuario")

