from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CesionAbono(Base):
    __tablename__ = "cesion_abono"

    id_cesion = Column(Integer, primary_key=True, index=True)
    dni_cedente = Column(String, ForeignKey("socio.dni", ondelete="CASCADE"), nullable=False)
    dni_beneficiario = Column(String(9), ForeignKey("usuario.dni"), nullable=False)
    id_abono = Column(Integer, ForeignKey("abono.id_abono", ondelete="CASCADE"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    fecha_cesion = Column(Date, nullable=False)

    socio_cedente = relationship("Socio", back_populates="cesiones_realizadas")
    usuario_beneficiario = relationship("Usuario", back_populates="cesiones_recibidas")
    abono = relationship("Abono", back_populates="cesiones")


