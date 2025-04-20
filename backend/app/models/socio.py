from sqlalchemy import Column, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.cesion_abono import CesionAbono

class Socio(Base):
    __tablename__ = "socio"

    dni = Column(String(9), ForeignKey("usuario.dni"), primary_key=True)
    num_socio = Column(String(20), unique=True, nullable=False)
    foto_perfil = Column(String(255))
    tipo_membresia = Column(String(30), nullable=False)
    estado = Column(String(15), default='activo')
    
    __table_args__ = (
        CheckConstraint("estado IN ('activo', 'inactivo', 'suspendido')", name="socio_estado_check"),
    )

    usuario = relationship("Usuario", back_populates="socio")
    predicciones = relationship("Predice", back_populates="socio")
    socio_abonos = relationship("SocioAbono", back_populates="socio")
    
    cesiones_realizadas = relationship(
        "CesionAbono",
        foreign_keys=[CesionAbono.dni_cedente],
        back_populates="cedente"
    )

    cesiones_recibidas = relationship(
        "CesionAbono",
        foreign_keys=[CesionAbono.dni_beneficiario],
        back_populates="beneficiario"
    )



